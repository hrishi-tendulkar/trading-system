from __future__ import annotations

import csv
from datetime import date
from functools import lru_cache
from pathlib import Path

from packages.core.strategy_registry import get_strategy_record
from packages.core.ui_data import _load_recommendation_records
from packages.schemas.strategy_engine import (
    StrategyCandidateRow,
    StrategyPageView,
    StrategyReplaySummary,
)

STRATEGY_NAME_TO_CODE = {
    "Breakout confirmation": "breakout-confirmation",
    "Breakout Confirmation": "breakout-confirmation",
    "Constructive pullback continuation": "sector-confirmed-pullback-continuation",
    "Sector-Confirmed Pullback Continuation": "sector-confirmed-pullback-continuation",
    "ETF rotation": "etf-trend-rotation",
    "ETF Trend / Rotation": "etf-trend-rotation",
    "Selective Mean Reversion": "selective-mean-reversion",
}

ACTION_CODE_MAP = {
    "Buy now": "BUY_NOW",
    "Buy on pullback": "BUY_PULLBACK",
    "Wait for confirmation": "WAIT_CONFIRMATION",
    "Wait for pullback": "DO_NOT_CHASE",
    "Hold": "NO_ACTION",
    "Hold / reassess after earnings": "SUPPRESSED",
    "No action": "NO_ACTION",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _replay_dir() -> Path:
    return _repo_root() / "data" / "processed" / "canonical_strategy_replay_2026-05-25_v1"


@lru_cache(maxsize=1)
def _load_replay_summary_by_code() -> dict[str, StrategyReplaySummary]:
    path = _replay_dir() / "canonical_strategy_comparison.csv"
    summaries: dict[str, StrategyReplaySummary] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            summary = StrategyReplaySummary(
                strategy_code=row["strategy_id"],
                strategy_name=row["strategy_name"],
                sample_size=int(row["sample_size"]),
                avg_5d=float(row["avg_fwd_5d_return"]),
                avg_10d=float(row["avg_fwd_10d_return"]),
                avg_15d=float(row["avg_fwd_15d_return"]),
                avg_excess_5d=float(row["avg_excess_5d_return"]),
                avg_excess_10d=float(row["avg_excess_10d_return"]),
                avg_excess_15d=float(row["avg_excess_15d_return"]),
                win_rate_5d=float(row["win_rate_5d"]),
                win_rate_10d=float(row["win_rate_10d"]),
                win_rate_15d=float(row["win_rate_15d"]),
            )
            summaries[summary.strategy_code] = summary
    return summaries


def _map_strategy_code(strategy_name: str) -> str | None:
    return STRATEGY_NAME_TO_CODE.get(strategy_name)


def _candidate_quality(record) -> str:
    if record.refined_score >= 7:
        return "A"
    if record.refined_score >= 5:
        return "B"
    return "C"


def _evidence_tier(basis_code: str) -> str:
    mapping = {
        "breakout-confirmation": "Strong",
        "sector-confirmed-pullback-continuation": "Moderate",
        "etf-trend-rotation": "Exploratory",
        "selective-mean-reversion": "Exploratory",
    }
    return mapping.get(basis_code, "Exploratory")


def _is_suppressed(record) -> tuple[bool, str | None]:
    if record.action_label == "Hold / reassess after earnings":
        return True, "Event freeze before earnings"
    if record.days_to_earnings is not None and 0 <= record.days_to_earnings <= 7:
        return True, "Near-term event risk"
    return False, None


def _is_board_promoted(basis_code: str, action_label: str, suppressed: bool) -> bool:
    if suppressed:
        return False
    if basis_code == "breakout-confirmation":
        return action_label in {"Buy now", "Wait for confirmation"}
    if basis_code == "sector-confirmed-pullback-continuation":
        return action_label == "Buy on pullback"
    return False


def _normalize_action(basis_code: str, action_label: str) -> tuple[str, str]:
    if basis_code == "sector-confirmed-pullback-continuation":
        if action_label == "Buy now":
            return "BUY_PULLBACK", "Buy on pullback"
        if action_label == "Wait for pullback":
            return "BUY_PULLBACK", "Buy on pullback"
    return ACTION_CODE_MAP.get(action_label, "NO_ACTION"), action_label


def _headline_note(basis_code: str, board_count: int, suppressed_count: int) -> str:
    if basis_code == "breakout-confirmation":
        return (
            f"{board_count} live breakout names are current board candidates. "
            "This sleeve is the strongest promoted continuation engine right now."
        )
    if basis_code == "sector-confirmed-pullback-continuation":
        return (
            f"{board_count} pullback candidates are live, but this sleeve is intentionally "
            "narrower than the broad aggregate replay because only selected confirmed "
            "sub-buckets earned trust."
        )
    if basis_code == "etf-trend-rotation":
        return (
            "ETF trend ideas are visible for context, but this sleeve is not currently "
            "trusted to feed the main board until a ranked rotation variant is tested."
        )
    return (
        f"{suppressed_count} names are blocked or deprioritized, and this sleeve remains "
        "a research view rather than an action-board source."
    )


def _as_of_date() -> date | None:
    records = _load_recommendation_records()
    if not records:
        return None
    return date.fromisoformat(records[0].as_of_date)


def get_strategy_page_view(basis_code: str) -> StrategyPageView | None:
    strategy = get_strategy_record(basis_code)
    if strategy is None:
        return None

    rows: list[StrategyCandidateRow] = []
    for record in _load_recommendation_records():
        mapped_code = _map_strategy_code(record.strategy_name)
        if mapped_code != basis_code:
            continue
        suppressed, suppression_reason = _is_suppressed(record)
        board_promoted = _is_board_promoted(basis_code, record.action_label, suppressed)
        live_state = "Strategy-only"
        if suppressed:
            live_state = "Suppressed"
        elif board_promoted:
            live_state = "Board-promoted"
        action_code, action_label = _normalize_action(basis_code, record.action_label)

        rows.append(
            StrategyCandidateRow(
                ticker=record.ticker,
                company=record.company,
                strategy_code=basis_code,
                strategy_name=strategy.display_name,
                current_action_code=action_code,
                current_action_label=action_label,
                setup_quality_band=_candidate_quality(record),
                historical_evidence_tier=_evidence_tier(basis_code),
                live_state=live_state,
                why_now=record.observed_reason,
                why_not_stronger=record.strategy_rationale,
                entry_value=f"{record.entry_label} {record.entry_value}".strip(),
                invalidation_value=f"{record.stop_label} {record.stop_value}".strip(),
                next_catalyst=record.next_earnings_date or "No near-term event loaded",
                confidence=record.confidence,
                board_promoted=board_promoted,
                suppressed=suppressed,
                suppression_reason=suppression_reason,
            )
        )

    rows.sort(
        key=lambda row: (
            0
            if row.live_state == "Board-promoted"
            else 1
            if row.live_state == "Strategy-only"
            else 2,
            row.ticker,
        )
    )

    board_count = sum(1 for row in rows if row.board_promoted)
    suppressed_count = sum(1 for row in rows if row.suppressed)
    strategy_only_count = sum(1 for row in rows if row.live_state == "Strategy-only")
    replay = _load_replay_summary_by_code().get(basis_code)

    return StrategyPageView(
        basis_code=basis_code,
        strategy_name=strategy.display_name,
        trust_level=strategy.trust_level,
        promotion_status=strategy.promotion_status,
        board_enabled=strategy.board_enabled,
        page_summary=strategy.page_summary,
        rule_spine=strategy.rule_spine,
        as_of_date=_as_of_date(),
        stats={
            "live_matches": len(rows),
            "board_promoted": board_count,
            "strategy_only": strategy_only_count,
            "suppressed": suppressed_count,
        },
        headline_note=_headline_note(basis_code, board_count, suppressed_count),
        replay_summary=replay,
        current_rows=rows,
    )


def list_strategy_pages() -> list[dict[str, str]]:
    pages = []
    for basis_code in (
        "breakout-confirmation",
        "sector-confirmed-pullback-continuation",
        "etf-trend-rotation",
        "selective-mean-reversion",
    ):
        record = get_strategy_record(basis_code)
        if record is None:
            continue
        pages.append(
            {
                "basis_code": record.basis_code,
                "display_name": record.display_name,
                "trust_level": record.trust_level,
                "promotion_status": record.promotion_status,
            }
        )
    return pages
