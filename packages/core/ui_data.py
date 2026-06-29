from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

from packages.core.universes import (
    UniverseMember,
    active_universe_source,
    load_active_universe_members,
)
from packages.core.weekly_runs import (
    current_recommendations_path,
    current_week_start,
    default_publish_week_start,
    legacy_recommendations_path,
    list_manifests,
    load_current_manifest,
    load_current_recommendation_rows,
    load_manifest,
    load_recommendation_rows,
    prior_market_close_for_week,
)


@dataclass(frozen=True)
class RecommendationRecord:
    as_of_date: str
    ticker: str
    company: str
    sector: str
    is_benchmark: bool
    close: float
    ret_20d: float
    rs_20d: float
    distance_from_52w_high: float
    days_to_earnings: float | None
    next_earnings_date: str | None
    event_risk: str
    strategy_id: str
    strategy_name: str
    basis_type: str
    action_label: str
    horizon: str
    entry_label: str
    entry_value: str
    stop_label: str
    stop_value: str
    target_label: str
    target_value: str
    strategy_rationale: str
    observed_reason: str
    action_rank: int
    refined_score: float
    trend_score: int
    momentum_score: int
    rs_score: int
    proximity_score: int
    risk_penalty: int
    extension_penalty: int

    @property
    def action_bucket(self) -> str:
        mapping = {
            "Buy now": "Buy now",
            "Buy on pullback": "Buy on pullback",
            "Wait for confirmation": "Wait for confirmation",
            "No action": "Do not chase",
            "Hold": "Do not chase",
            "Hold / reassess after earnings": "Do not chase",
            "Benchmark reference": "Reference only",
        }
        return mapping.get(self.action_label, "Monitor")

    @property
    def holder_bucket(self) -> str | None:
        mapping = {
            "Buy now": "Hold / add on strength",
            "Buy on pullback": "Hold but wait for better entry",
            "Wait for confirmation": "Hold but do not add",
            "Hold": "Hold",
            "Hold / reassess after earnings": "Hold but event-sensitive",
            "No action": "Reassess",
        }
        return mapping.get(self.action_label)

    @property
    def badge_class(self) -> str:
        mapping = {
            "Buy now": "buy",
            "Buy on pullback": "wait",
            "Wait for confirmation": "focus",
            "Hold": "hold",
            "Hold / reassess after earnings": "risk",
            "No action": "avoid",
            "Benchmark reference": "neutral",
        }
        return mapping.get(self.action_label, "neutral")

    @property
    def confidence(self) -> str:
        if self.refined_score >= 7:
            return "High"
        if self.refined_score >= 5:
            return "Medium"
        return "Low"

    @property
    def role_label(self) -> str:
        if self.is_benchmark:
            return "Benchmark context"
        if self.sector == "ETF":
            return "ETF context"
        if self.action_label == "Buy now":
            return "Tradeable now"
        if self.action_label == "Buy on pullback":
            return "Core watch"
        if self.action_label == "Wait for confirmation":
            return "Tactical watch"
        if self.action_label == "Hold / reassess after earnings":
            return "Event-sensitive hold"
        if self.action_label == "Hold":
            return "Hold / review"
        return "Monitor"

    @property
    def why_now(self) -> str:
        return self.observed_reason

    @property
    def why_not_stronger(self) -> str:
        return self.strategy_rationale


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _first_existing(candidates: list[str]) -> Path:
    root = _repo_root()
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    raise FileNotFoundError(f"No supported data source found in: {candidates}")


def _to_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def _to_float(value: str) -> float:
    return float(value) if value else 0.0


def _to_optional_float(value: str) -> float | None:
    return float(value) if value else None


def _to_int(value: str) -> int:
    return int(float(value)) if value else 0


def _format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def _format_distance(value: float) -> str:
    return f"{value * 100:.1f}% below 52-week high"


def _format_currency(value: float) -> str:
    return f"${value:,.2f}"


def _format_days_to_earnings(days: float | None) -> str:
    if days is None:
        return "No date loaded"
    rounded = int(days)
    if rounded < 0:
        return f"{abs(rounded)} days since earnings"
    if rounded == 0:
        return "Earnings today"
    return f"{rounded} days to earnings"


def _format_timestamp_label(value: str) -> str:
    try:
        parsed = value.replace("+00:00", "")
        date_part, time_part = parsed.split("T", 1)
        return f"{date_part} {time_part[:5]} UTC"
    except ValueError:
        return value


def _canonical_strategy(record: RecommendationRecord) -> tuple[str | None, str | None]:
    by_id = {
        "breakout-confirmation-triggered": (
            "breakout-confirmation",
            "Breakout Confirmation",
        ),
        "wait-for-confirmation": (
            "breakout-confirmation",
            "Breakout Confirmation",
        ),
        "strong-stock-constructive-pullback": (
            "sector-confirmed-pullback-continuation",
            "Sector-Confirmed Pullback Continuation",
        ),
        "extended-strength-wait": (
            "sector-confirmed-pullback-continuation",
            "Sector-Confirmed Pullback Continuation",
        ),
        "broad-market-trend-hold": (
            "etf-trend-rotation",
            "ETF Trend / Rotation",
        ),
        "etf-rotation": (
            "etf-trend-rotation",
            "ETF Trend / Rotation",
        ),
    }
    return by_id.get(record.strategy_id, (None, None))


def _fresh_cash_action_label(record: RecommendationRecord) -> str:
    mapping = {
        "Hold": "No fresh buy",
        "Hold / reassess after earnings": "Wait through earnings",
        "No action": "No fresh buy",
    }
    return mapping.get(record.action_label, record.action_label)


def _fresh_cash_entry(record: RecommendationRecord) -> str:
    if record.action_label == "Hold / reassess after earnings":
        return f"Wait until after earnings on {record.next_earnings_date or 'the next event'}"
    if record.action_label in {"Hold", "No action"}:
        return "Stand aside this week"
    return f"{record.entry_label} {record.entry_value}".strip()


def _fresh_cash_invalidation(record: RecommendationRecord) -> str:
    if record.action_label in {"Hold", "Hold / reassess after earnings", "No action"}:
        return f"Reassess if {record.stop_value or 'the setup changes'}"
    return f"{record.stop_label} {record.stop_value}".strip()


@lru_cache(maxsize=1)
def _load_watchlist_members() -> dict[str, UniverseMember]:
    return load_active_universe_members()


@lru_cache(maxsize=1)
def _load_recommendation_records() -> list[RecommendationRecord]:
    rows = load_current_recommendation_rows()
    if rows:
        return _recommendation_records_from_rows(rows)
    return _load_recommendation_records_from_path(str(current_recommendations_path()))


@lru_cache(maxsize=16)
def _load_recommendation_records_from_path(path_value: str) -> list[RecommendationRecord]:
    path = Path(path_value)
    return _recommendation_records_from_rows(_csv_rows(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _recommendation_records_from_rows(rows: list[dict[str, str]]) -> list[RecommendationRecord]:
    watchlist = _load_watchlist_members()
    records: list[RecommendationRecord] = []
    for row in rows:
        ticker = row["ticker"].upper()
        member = watchlist.get(ticker)
        company = member.display_name if member else ticker
        records.append(
            RecommendationRecord(
                as_of_date=row.get("date", row.get("as_of_date", "")),
                ticker=ticker,
                company=company,
                sector=row["sector"].strip(),
                is_benchmark=_to_bool(row["is_benchmark"]),
                close=_to_float(row["close"]),
                ret_20d=_to_float(row["ret_20d"]),
                rs_20d=_to_float(row["rs_20d"]),
                distance_from_52w_high=_to_float(row["distance_from_52w_high"]),
                days_to_earnings=_to_optional_float(row["days_to_earnings"]),
                next_earnings_date=row["next_earnings_date"].strip() or None,
                event_risk=row["event_risk"].strip() or "Unknown",
                strategy_id=row["strategy_id"].strip(),
                strategy_name=row["strategy_name"].strip(),
                basis_type=row["basis_type"].strip(),
                action_label=row["action_label"].strip(),
                horizon=row["horizon"].strip(),
                entry_label=row["entry_label"].strip(),
                entry_value=row["entry_value"].strip(),
                stop_label=row["stop_label"].strip(),
                stop_value=row["stop_value"].strip(),
                target_label=row["target_label"].strip(),
                target_value=row["target_value"].strip(),
                strategy_rationale=row["strategy_rationale"].strip(),
                observed_reason=row["observed_reason"].strip(),
                action_rank=_to_int(row["action_rank"]),
                refined_score=_to_float(row["refined_score"]),
                trend_score=_to_int(row["trend_score"]),
                momentum_score=_to_int(row["momentum_score"]),
                rs_score=_to_int(row["rs_score"]),
                proximity_score=_to_int(row["proximity_score"]),
                risk_penalty=_to_int(row["risk_penalty"]),
                extension_penalty=_to_int(row["extension_penalty"]),
            )
        )
    return sorted(records, key=lambda record: (record.action_rank, record.ticker))


def _published_dataset_name() -> str:
    manifest = load_current_manifest()
    if manifest:
        return manifest.run_id
    path = current_recommendations_path()
    return path.parent.name


def _non_benchmark_records() -> list[RecommendationRecord]:
    return [record for record in _load_recommendation_records() if not record.is_benchmark]


def _count_active_members() -> int:
    return sum(1 for member in _load_watchlist_members().values() if member.is_active)


def _active_universe_label() -> str:
    source = active_universe_source()
    return source.slug


def _active_universe_path_label() -> str:
    source = active_universe_source()
    try:
        return str(source.path.relative_to(_repo_root()))
    except ValueError:
        return str(source.path)


def _market_posture(
    records: list[RecommendationRecord],
    all_records: list[RecommendationRecord] | None = None,
) -> tuple[str, str, list[str]]:
    source_records = all_records or _load_recommendation_records()
    benchmark = next(
        (record for record in source_records if record.is_benchmark),
        None,
    )
    buy_count = sum(1 for record in records if record.action_label == "Buy now")
    event_sensitive_count = sum(
        1
        for record in records
        if record.event_risk == "High"
        or (record.days_to_earnings is not None and record.days_to_earnings <= 7)
    )
    if benchmark and benchmark.ret_20d > 0 and buy_count >= 2:
        title = "Selective risk-on"
        summary = (
            "Leadership is still present, but the product should keep capital "
            "concentrated in the strongest few candidates instead of buying broadly."
        )
    elif benchmark and benchmark.ret_20d > 0:
        title = "Neutral to constructive"
        summary = (
            "Market trend is supportive enough to keep reviewing candidates, "
            "but not strong enough to force new buys."
        )
    else:
        title = "Defensive"
        summary = (
            "Market trend is not giving enough support for aggressive fresh "
            "entries, so preserving cash matters more."
        )
    points = [
        f"{buy_count} names currently qualify as immediate action candidates.",
        (
            f"{event_sensitive_count} names have high event risk or earnings within "
            "7 days; check the event date before acting."
        ),
        "Open any candidate card below to see entry, risk, catalyst, and rationale.",
    ]
    return title, summary, points


def _top_actions(records: list[RecommendationRecord]) -> list[dict[str, str]]:
    actionable_labels = {"Buy now", "Buy on pullback", "Wait for confirmation"}
    candidates = [record for record in records if record.action_label in actionable_labels]
    return [
        {
            "ticker": record.ticker,
            "company": record.company,
            "action": record.action_label,
            "badge_class": record.badge_class,
            "reason": record.observed_reason,
            "why_not_stronger": record.strategy_rationale,
            "expression": record.horizon,
            "entry_label": record.entry_label,
            "entry_value": record.entry_value,
            "stop_label": record.stop_label,
            "stop_value": record.stop_value,
            "target_label": record.target_label,
            "target_value": record.target_value,
            "catalyst": record.next_earnings_date or "No near-term event loaded",
            "strategy_code": _canonical_strategy(record)[0],
            "strategy_name": _canonical_strategy(record)[1],
        }
        for record in candidates[:3]
    ]


def _fresh_cash_buckets(records: list[RecommendationRecord]) -> list[dict[str, object]]:
    ordered_buckets = ["Buy now", "Buy on pullback", "Wait for confirmation", "Do not chase"]
    groups: list[dict[str, object]] = []
    for bucket in ordered_buckets:
        bucket_records = [record for record in records if record.action_bucket == bucket]
        if not bucket_records:
            continue
        groups.append(
            {
                "title": bucket,
                "items": [
                    {
                        "ticker": record.ticker,
                        "company": record.company,
                        "action": _fresh_cash_action_label(record),
                        "badge_class": record.badge_class,
                        "why_now": record.why_now,
                        "why_not_stronger": record.why_not_stronger,
                        "entry": _fresh_cash_entry(record),
                        "invalidation": _fresh_cash_invalidation(record),
                        "catalyst": record.next_earnings_date or "No near-term event loaded",
                        "strategy_code": _canonical_strategy(record)[0],
                        "strategy_name": _canonical_strategy(record)[1],
                    }
                    for record in bucket_records
                ],
            }
        )
    return groups


def _holder_buckets(records: list[RecommendationRecord]) -> list[dict[str, object]]:
    ordered_buckets = [
        "Hold / add on strength",
        "Hold",
        "Hold but wait for better entry",
        "Hold but do not add",
        "Hold but event-sensitive",
        "Reassess",
    ]
    groups: list[dict[str, object]] = []
    for bucket in ordered_buckets:
        bucket_records = [record for record in records if record.holder_bucket == bucket][:5]
        if not bucket_records:
            continue
        groups.append(
            {
                "title": bucket,
                "items": [
                    {
                        "ticker": record.ticker,
                        "company": record.company,
                        "change": record.strategy_name,
                        "risk_type": record.event_risk,
                        "reassess": f"{record.stop_label} {record.stop_value}".strip(),
                    }
                    for record in bucket_records
                ],
            }
        )
    return groups


def _deep_dive_queue(records: list[RecommendationRecord]) -> list[dict[str, str]]:
    queue_labels = {
        "Buy now",
        "Buy on pullback",
        "Wait for confirmation",
        "Hold / reassess after earnings",
    }
    queue_records = [record for record in records if record.action_label in queue_labels]
    return [
        {
            "ticker": record.ticker,
            "company": record.company,
            "reason": record.strategy_name,
            "note": record.observed_reason,
            "strategy_code": _canonical_strategy(record)[0],
            "strategy_name": _canonical_strategy(record)[1],
        }
        for record in queue_records[:3]
    ]


def _run_metadata(records: list[RecommendationRecord], run_id: str | None = None) -> dict[str, str]:
    manifest = load_manifest(run_id) if run_id else load_current_manifest()
    as_of_date = records[0].as_of_date if records else "Unknown"
    if manifest:
        current_manifest = load_current_manifest()
        active_strategy_versions = ", ".join(
            f"{basis_code}: {version_label}"
            for basis_code, version_label in sorted(manifest.active_strategy_versions.items())
        )
        return {
            "recommendation_week": f"Week of {manifest.recommendation_week_start}",
            "published_at": _format_timestamp_label(manifest.published_at),
            "data_through": manifest.source_data_through,
            "last_checked": _format_timestamp_label(manifest.last_checked_at),
            "run_id": manifest.run_id,
            "status": "Current published plan"
            if current_manifest and current_manifest.run_id == manifest.run_id
            else "Archived immutable plan",
            "market_data_through": manifest.market_data_through,
            "timezone": manifest.timezone,
            "strategy_registry_version": manifest.strategy_registry_version,
            "active_strategy_versions": active_strategy_versions or "Unpinned legacy manifest",
        }
    return {
        "recommendation_week": f"Week of {as_of_date}",
        "published_at": f"{as_of_date} after market close",
        "data_through": as_of_date,
        "last_checked": as_of_date,
        "run_id": f"{_published_dataset_name()}-{as_of_date}",
        "status": "Published weekly plan",
        "strategy_registry_version": "Unpinned legacy dataset",
        "active_strategy_versions": "Unpinned legacy dataset",
    }


def _freshness_alerts(metadata: dict[str, str], today: date | None = None) -> list[dict[str, str]]:
    alerts: list[dict[str, str]] = []
    effective_today = today or date.today()
    try:
        active_week = current_week_start(effective_today)
        next_publish_week = default_publish_week_start(effective_today)
        expected_week = min(active_week, next_publish_week)
        recommendation_week = date.fromisoformat(
            metadata["recommendation_week"].replace("Week of ", "")
        )
        expected_source_through = prior_market_close_for_week(recommendation_week)
        source_through = date.fromisoformat(metadata["data_through"])
    except ValueError:
        return [
            {
                "title": "Weekly freshness unknown",
                "message": (
                    "The current run metadata could not be parsed. "
                    "Verify the weekly publish job."
                ),
            }
        ]

    if recommendation_week < expected_week:
        alerts.append(
            {
                "title": "Current-week report missing",
                "message": (
                    f"No weekly report has been published for Week of "
                    f"{expected_week.isoformat()}. Latest available report is "
                    f"{metadata['recommendation_week']}."
                ),
            }
        )
    if source_through < expected_source_through:
        alerts.append(
            {
                "title": "Source data is stale",
                "message": (
                    f"This report uses data through {source_through.isoformat()}, "
                    f"but the expected prior-week close is {expected_source_through.isoformat()}."
                ),
            }
        )
    return alerts


def _scheduled_addenda(records: list[RecommendationRecord]) -> list[dict[str, str]]:
    event_sensitive = [
        record
        for record in records
        if record.days_to_earnings is not None and 0 <= record.days_to_earnings <= 7
    ][:3]
    addenda = [
        {
            "date": records[0].as_of_date if records else "Unknown",
            "status": "Scheduled check complete",
            "summary": (
                "No full weekly rerun was performed. The weekday check protects "
                "the published plan by flagging material changes only."
            ),
        }
    ]
    for record in event_sensitive:
        addenda.append(
            {
                "date": records[0].as_of_date,
                "status": "Event risk watch",
                "summary": (
                    f"{record.ticker} remains tied to "
                    f"{record.next_earnings_date or 'an upcoming event'}; "
                    "do not silently rewrite the Sunday plan."
                ),
            }
        )
    return addenda


def get_weekly_review() -> dict[str, object]:
    records = _non_benchmark_records()
    posture_title, posture_summary, posture_points = _market_posture(records)
    metadata = _run_metadata(records)
    buy_now_count = sum(1 for record in records if record.action_label == "Buy now")
    pullback_count = sum(1 for record in records if record.action_label == "Buy on pullback")
    wait_count = sum(1 for record in records if record.action_label == "Wait for confirmation")
    return {
        "title": f"Weekly summary for {metadata['recommendation_week'].lower()}",
        "summary": (
            "This page converts the latest published run into this week's buy, "
            "wait, and avoid decisions. It does not know your current holdings yet."
        ),
        "coverage": {
            "analyzed_count": str(len(records)),
            "board_note": (
                f"{len(records)} non-benchmark names were analyzed in this run. "
                "Every analyzed name appears in the full candidate board below."
            ),
            "holdings_note": (
                "Holding guidance is disabled until you provide a current holdings list. "
                "For now, the page only gives fresh-cash and watchlist decisions."
            ),
        },
        "facts": [
            {"label": "Recommendation week", "value": metadata["recommendation_week"]},
            {"label": "Published", "value": metadata["published_at"]},
            {"label": "Data through", "value": metadata["data_through"]},
            {"label": "Last checked", "value": metadata["last_checked"]},
            {"label": "Market posture", "value": posture_title},
            {"label": "Universe", "value": str(_count_active_members())},
            {"label": "Published run", "value": metadata["run_id"]},
            {
                "label": "Strategy registry",
                "value": metadata["strategy_registry_version"],
            },
        ],
        "alerts": _freshness_alerts(metadata),
        "metadata": metadata,
        "posture": {
            "title": posture_title,
            "summary": posture_summary,
            "points": posture_points,
        },
        "start_here": _top_actions(records),
        "fresh_cash": _fresh_cash_buckets(records),
        "holders": _holder_buckets(records),
        "deep_dives": _deep_dive_queue(records),
        "selectivity_note": (
            f"{buy_now_count} names are buy-now candidates, {pullback_count} need a "
            f"better entry, and {wait_count} need confirmation first."
        ),
    }


def get_archive_index() -> dict[str, object]:
    manifests = list_manifests()
    if not manifests:
        records = _non_benchmark_records()
        metadata = _run_metadata(records)
        buy_now_count = sum(1 for record in records if record.action_label == "Buy now")
        watch_count = sum(
            1
            for record in records
            if record.action_label in {"Buy on pullback", "Wait for confirmation"}
        )
        weeks = [
            {
                "week_id": metadata["run_id"],
                "label": metadata["recommendation_week"],
                "published": metadata["published_at"],
                "data_through": metadata["data_through"],
                "status": metadata["status"],
                "buy_now_count": str(buy_now_count),
                "watch_count": str(watch_count),
                "deep_dive_count": str(len(_deep_dive_queue(records))),
            }
        ]
    else:
        weeks = []
        current = load_current_manifest()
        for manifest in manifests:
            weeks.append(
                {
                    "week_id": manifest.run_id,
                    "label": f"Week of {manifest.recommendation_week_start}",
                    "published": _format_timestamp_label(manifest.published_at),
                    "data_through": manifest.source_data_through,
                    "status": "Current published plan"
                    if current and current.run_id == manifest.run_id
                    else "Archived immutable plan",
                    "buy_now_count": "View",
                    "watch_count": "View",
                    "deep_dive_count": "View",
                }
            )
    return {
        "title": "Archive",
        "summary": (
            "Reopen prior weekly plans as they were published, with daily addenda "
            "and later outcomes layered on without rewriting the original call."
        ),
        "weeks": weeks,
        "research_reports": [
            {
                "label": "Canonical strategy replay",
                "date": "2026-05-25",
                "path": "docs/research/market/sp100-canonical-strategy-replay-2026-05-25.md",
            },
            {
                "label": "Tradeable board report",
                "date": "2026-05-24",
                "path": "docs/research/market/tradeable-board-2026-05-24.md",
            },
            {
                "label": "Phase 2 weekly report",
                "date": "2026-05-23",
                "path": "docs/research/market/phase2-weekly-report-2026-05-23.md",
            },
        ],
    }


def get_archive_week(week_id: str) -> dict[str, object] | None:
    manifest = load_manifest(week_id)
    if manifest:
        all_records = _recommendation_records_from_rows(load_recommendation_rows(manifest.run_id))
        records = [record for record in all_records if not record.is_benchmark]
        metadata = _run_metadata(records, manifest.run_id)
    else:
        all_records = _load_recommendation_records_from_path(str(legacy_recommendations_path()))
        records = [record for record in all_records if not record.is_benchmark]
        metadata = _run_metadata(records)
        if week_id != metadata["run_id"]:
            return None
    posture_title, posture_summary, posture_points = _market_posture(records, all_records)
    return {
        "week_id": week_id,
        "title": metadata["recommendation_week"],
        "metadata": metadata,
        "posture": {
            "title": posture_title,
            "summary": posture_summary,
            "points": posture_points,
        },
        "weekly_plan": {
            "start_here": _top_actions(records),
            "fresh_cash": _fresh_cash_buckets(records),
            "holders": _holder_buckets(records),
            "deep_dives": _deep_dive_queue(records),
        },
        "daily_addenda": _scheduled_addenda(records),
        "outcomes": [
            {
                "label": "1D / 5D / 10D outcomes",
                "status": "Pending historical outcome job",
                "detail": (
                    "Outcome layers should be appended after the fact and must not "
                    "modify what the weekly plan originally recommended."
                ),
            }
        ],
        "capture_scope": [
            "Weekly overview and market posture",
            "Recommendation board buckets and action ranks",
            "Deep-dive queue and stock-level evidence shown that week",
            "Strategy page outputs and candidate lineage",
            "Scheduled weekday addenda",
            "Run metadata, data-through timestamps, and source lineage",
            "Later outcome and postmortem layers",
        ],
    }


def get_daily_digest() -> dict[str, object]:
    records = _non_benchmark_records()
    event_risk = [
        record
        for record in records
        if record.days_to_earnings is not None and 0 <= record.days_to_earnings <= 7
    ][:2]
    actionable = [record for record in records if record.action_label == "Buy now"][:2]
    waiting = [record for record in records if record.action_label == "Wait for confirmation"][:2]

    items: list[dict[str, str]] = []
    for record in event_risk:
        items.append(
            {
                "category": "Holding risk increased",
                "headline": f"{record.ticker} enters an earnings-sensitive window",
                "detail": (
                    f"{record.company} reports on "
                    f"{record.next_earnings_date or 'an upcoming date'}, so the weekly plan "
                    f"should stay disciplined around event risk."
                ),
            }
        )
    for record in actionable:
        items.append(
            {
                "category": "Watchlist candidate became actionable",
                "headline": f"{record.ticker} remains a live fresh-cash candidate",
                "detail": f"{record.entry_label} {record.entry_value}. {record.observed_reason}",
            }
        )
    for record in waiting:
        items.append(
            {
                "category": "Wait for confirmation",
                "headline": f"{record.ticker} still needs proof before capital",
                "detail": (
                    f"{record.target_label} {record.target_value}. {record.strategy_rationale}"
                ),
            }
        )

    if not items:
        verdict = "No material change"
    elif event_risk:
        verdict = f"{len(event_risk)} event-risk names need review"
    else:
        verdict = f"{len(actionable)} names remain actionable"

    carry_forward = [
        {
            "ticker": record.ticker,
            "company": record.company,
            "trigger": f"{record.entry_label} {record.entry_value}".strip(),
            "next_step": record.action_label,
        }
        for record in (actionable + waiting)[:4]
    ]
    return {
        "title": "What Changed Since Yesterday",
        "summary": (
            "This latest-state digest is derived from the most recent published "
            "run. It stays small, explicit, and focused on changes that should "
            "matter before the next weekly session."
        ),
        "verdict": verdict,
        "items": items[:5],
        "carry_forward": carry_forward,
    }


def get_watchlist_view() -> dict[str, object]:
    watchlist = _load_watchlist_members()
    recommendations = {record.ticker: record for record in _load_recommendation_records()}
    active_tickers = {member.ticker for member in watchlist.values() if member.is_active}
    covered_active_tickers = active_tickers & set(recommendations)
    grouped: dict[str, list[dict[str, str]]] = {
        "Tradeable now": [],
        "Core watch": [],
        "Tactical watch": [],
        "Hold / review": [],
        "ETF context": [],
        "Benchmark context": [],
        "Monitor": [],
    }
    for member in sorted((m for m in watchlist.values() if m.is_active), key=lambda m: m.ticker):
        record = recommendations.get(member.ticker)
        role = (
            record.role_label
            if record
            else ("Benchmark context" if member.is_benchmark else "Monitor")
        )
        grouped.setdefault(role, []).append(
            {
                "ticker": member.ticker,
                "company": member.display_name,
                "sector": member.sector,
                "action": record.action_label if record else "No published recommendation",
                "badge_class": record.badge_class if record else "neutral",
                "note": record.observed_reason if record else "Awaiting recommendation projection.",
            }
        )

    sections = [{"title": title, "items": items} for title, items in grouped.items() if items]
    return {
        "title": "Active universe",
        "summary": (
            "This view keeps the watchlist scannable first. It shows how the "
            "current published recommendation set maps onto the active universe "
            "while separating current product capability from future editing tools."
        ),
        "facts": [
            {"label": "Active names", "value": str(_count_active_members())},
            {
                "label": "Recommendation coverage",
                "value": f"{len(covered_active_tickers)} / {len(active_tickers)}",
            },
            {"label": "Active universe", "value": _active_universe_label()},
            {"label": "Source file", "value": _active_universe_path_label()},
            {"label": "Published run", "value": _published_dataset_name()},
        ],
        "sections": sections,
    }


def get_stock_detail(ticker: str) -> dict[str, object] | None:
    normalized = ticker.upper()
    record = next(
        (item for item in _load_recommendation_records() if item.ticker == normalized),
        None,
    )
    if record is None:
        return None
    return {
        "ticker": record.ticker,
        "company": record.company,
        "as_of_date": record.as_of_date,
        "primary_thesis": record.strategy_rationale,
        "current_call": _fresh_cash_action_label(record),
        "portfolio_call": "Unavailable until current holdings are provided",
        "confidence": record.confidence,
        "badge_class": record.badge_class,
        "basis_type": record.basis_type,
        "strategy_name": record.strategy_name,
        "horizon": record.horizon,
        "event_risk": record.event_risk,
        "facts": [
            {"label": "Close", "value": _format_currency(record.close)},
            {"label": "20D return", "value": _format_percent(record.ret_20d)},
            {"label": "RS vs benchmark", "value": _format_percent(record.rs_20d)},
            {"label": "Earnings", "value": _format_days_to_earnings(record.days_to_earnings)},
        ],
        "setup_plan": [
            {"label": "Fresh-cash action", "value": _fresh_cash_entry(record)},
            {"label": "Reassess if", "value": _fresh_cash_invalidation(record)},
            {"label": record.target_label, "value": record.target_value},
        ],
        "score_breakdown": [
            {"label": "Refined score", "value": f"{record.refined_score:.0f}"},
            {"label": "Trend", "value": str(record.trend_score)},
            {"label": "Momentum", "value": str(record.momentum_score)},
            {"label": "Relative strength", "value": str(record.rs_score)},
            {"label": "Proximity", "value": str(record.proximity_score)},
        ],
        "observed": [
            f"Close: {_format_currency(record.close)}.",
            (
                f"20-day return: {_format_percent(record.ret_20d)} with "
                f"relative strength of {_format_percent(record.rs_20d)} "
                "versus the benchmark."
            ),
            (
                f"Event risk: {record.event_risk}. "
                f"{record.next_earnings_date or 'No upcoming earnings date loaded'} "
                f"({_format_days_to_earnings(record.days_to_earnings)})."
            ),
            f"{_format_distance(record.distance_from_52w_high)}.",
        ],
        "derived": [
            record.observed_reason,
            record.strategy_rationale,
            f"Current strategy family: {record.strategy_name} ({record.basis_type}).",
        ],
        "why_now": record.why_now,
        "why_not_stronger": record.why_not_stronger,
        "history_note": (
            "Recommendation history and prior weekly snapshots land in the next "
            "phase, but this page now uses a stable decision contract."
        ),
    }
