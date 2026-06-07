from __future__ import annotations

import csv
from datetime import date
from functools import lru_cache
from pathlib import Path

from packages.core.strategy_registry import get_strategy_record
from packages.core.ui_data import _load_recommendation_records
from packages.schemas.strategy_engine import (
    StrategyCandidateRow,
    StrategyIndexCard,
    StrategyMetricCard,
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
    "Index trend follow-through": "etf-trend-rotation",
    "Selective Mean Reversion": "selective-mean-reversion",
}

STRATEGY_ID_TO_CODE = {
    "breakout-confirmation-triggered": "breakout-confirmation",
    "wait-for-confirmation": "breakout-confirmation",
    "strong-stock-constructive-pullback": "sector-confirmed-pullback-continuation",
    "broad-market-trend-hold": "etf-trend-rotation",
    "extended-strength-wait": "sector-confirmed-pullback-continuation",
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


def _map_strategy_code(strategy_name: str, strategy_id: str | None = None) -> str | None:
    if strategy_id and strategy_id in STRATEGY_ID_TO_CODE:
        return STRATEGY_ID_TO_CODE[strategy_id]
    return STRATEGY_NAME_TO_CODE.get(strategy_name)


def _candidate_quality(record) -> str:
    if record.refined_score >= 7:
        return "A"
    if record.refined_score >= 5:
        return "B"
    return "C"


def _evidence_tier(basis_code: str) -> str:
    mapping = {
        "breakout-confirmation": "Strong but narrowed",
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


def _plain_language_copy(basis_code: str) -> dict[str, object]:
    copy = {
        "breakout-confirmation": {
            "strategy_definition": (
                "This strategy looks for strong stocks that are already acting well, "
                "but only buys them once price proves the breakout is real."
            ),
            "trust_summary": (
                "This is the strongest currently promoted strategy only in its narrowed "
                "form. It deserves attention when the market is supportive, the sector "
                "confirms, and price has actually triggered."
            ),
            "this_week_call": (
                "Use this as a live action strategy, not just a watchlist lens."
            ),
            "this_week_use": (
                "If this page shows board-promoted names, those are the continuation setups "
                "the current mainline is most willing to act on right now."
            ),
            "best_used_for": (
                "Leadership names that are proving strength through a real trigger."
            ),
            "avoid_when": (
                "A stock only looks interesting on paper but has not actually "
                "broken out yet."
            ),
            "works_best_when": [
                "The market is supportive rather than defensive.",
                "The sector confirms rather than fights the move.",
                "The stock is already a relative-strength leader.",
                "The breakout trigger is fresh and not overly extended.",
            ],
            "breaks_down_when": [
                "The stock is late, crowded, or already overextended.",
                "The breakout never really confirms through price.",
                "Sector confirmation is weak or unavailable.",
                "The broader market loses risk appetite.",
            ],
        },
        "sector-confirmed-pullback-continuation": {
            "strategy_definition": (
                "This strategy looks for strong stocks pulling back in a healthy way, "
                "then tries to buy the reset instead of chasing strength."
            ),
            "trust_summary": (
                "This strategy is usable, but narrower than the raw label suggests. "
                "The broad version is not strong enough on its own, so only tighter "
                "pullback cases deserve trust."
            ),
            "this_week_call": (
                "Treat this as a selective secondary strategy, not the first place "
                "to force capital."
            ),
            "this_week_use": (
                "Use this page to find controlled pullbacks in strong names, but "
                "only when the setup still offers "
                "a defined risk point and supportive context."
            ),
            "best_used_for": (
                "Strong stocks that cooled off without breaking their bigger uptrend."
            ),
            "avoid_when": (
                "A stock is falling too deeply, too messily, or without "
                "supportive sector context."
            ),
            "works_best_when": [
                "The market is constructive, not chaotic.",
                "The stock remains in an uptrend even after the pullback.",
                "The pullback is controlled rather than a deep breakdown.",
            ],
            "breaks_down_when": [
                "The pullback gets too deep or too loose.",
                "Sector support is weak or missing.",
                "The setup is really just broad dip-buying, not continuation.",
            ],
        },
        "etf-trend-rotation": {
            "strategy_definition": (
                "This strategy is meant to give cleaner exposure through ETFs when "
                "single-name timing is less attractive."
            ),
            "trust_summary": (
                "The idea makes sense, but the current tested rule is not strong enough yet. "
                "Treat it as research, not a live action source."
            ),
            "this_week_call": (
                "Use for context only until a stronger weekly rotation version "
                "is built."
            ),
            "this_week_use": (
                "If this page shows names, read them as research candidates "
                "rather than immediate action ideas."
            ),
            "best_used_for": "Simpler market or sector exposure when the trend is clean.",
            "avoid_when": "You need a proven live edge from the current tested entry rule.",
            "works_best_when": [
                "The market is clearly supportive.",
                "The ETF is trending cleanly above key moving averages.",
                "Relative strength versus the benchmark is improving.",
            ],
            "breaks_down_when": [
                "Trend signals are flat and undifferentiated.",
                "The rule is acting like broad beta rather than rotation.",
                "The best edge only exists in a small pocket of the regime map.",
            ],
        },
        "selective-mean-reversion": {
            "strategy_definition": (
                "This strategy tests whether very selective oversold rebounds add "
                "value without pretending that every dip is buyable."
            ),
            "trust_summary": (
                "This is research only. It is not a current action-board strategy "
                "and should not drive fresh capital decisions yet."
            ),
            "this_week_call": "Read this as a sandbox, not as a live production strategy.",
            "this_week_use": (
                "If this page shows anything useful, it should mainly sharpen "
                "research and edge validation rather than trigger action."
            ),
            "best_used_for": "Studying narrow defensive or stress-regime rebounds.",
            "avoid_when": "You want a current mainline strategy with live trust.",
            "works_best_when": [
                "The setup is explicitly narrow rather than broad dip-buying.",
                "The regime is defensive or stressed enough for snap-back behavior to matter.",
                "The stock is not structurally broken.",
            ],
            "breaks_down_when": [
                "Every weak chart is treated as a rebound candidate.",
                "The market is healthy enough that continuation is the better lens.",
                "The signal depends on unstable, regime-specific behavior.",
            ],
        },
    }
    return copy[basis_code]


def _backtest_label(basis_code: str) -> str:
    return {
        "breakout-confirmation": "Strong historical support when narrowed",
        "sector-confirmed-pullback-continuation": "Mixed overall, usable only in narrower cases",
        "etf-trend-rotation": "Not strong enough yet",
        "selective-mean-reversion": "Research-only evidence",
    }[basis_code]


def _backtest_takeaway(basis_code: str, replay: StrategyReplaySummary | None) -> str:
    if replay is None:
        return "Backtest evidence is not loaded yet, so use doctrine rather than metrics."
    if basis_code == "breakout-confirmation":
        return (
            "This is the cleanest replay-backed strategy in the current set only after "
            "the supportive-regime and sector-confirmation gates are preserved. "
            "The main thing to remember is that its edge comes from waiting for proof, "
            "not predicting breakouts early."
        )
    if basis_code == "sector-confirmed-pullback-continuation":
        return (
            "The headline numbers are only mediocre, which is exactly why this "
            "strategy must stay narrow. "
            "Use it only when the pullback is controlled and the surrounding context is supportive."
        )
    if basis_code == "etf-trend-rotation":
        return (
            "The current tested rule is too flat versus the benchmark to earn live trust. "
            "This page is mainly telling you the concept still needs a better entry design."
        )
    return (
        "The evidence is too regime-specific and unstable to trust for routine weekly action. "
        "Treat this strategy as research unless later testing becomes much clearer."
    )


def _metric_cards(replay: StrategyReplaySummary | None) -> list[StrategyMetricCard]:
    if replay is None:
        return []
    return [
        StrategyMetricCard(
            label="How many examples were tested",
            value=f"{replay.sample_size}",
            meaning="More examples make the read more trustworthy than a tiny sample would.",
        ),
        StrategyMetricCard(
            label="Average 5-day move after a signal",
            value=f"{replay.avg_5d * 100:.2f}%",
            meaning=(
                "This is the average short-term move after the setup appears. "
                "Positive is better, but it matters more when it is consistent."
            ),
        ),
        StrategyMetricCard(
            label="Average 10-day result versus SPY",
            value=f"{replay.avg_excess_10d * 100:.2f}%",
            meaning=(
                "This asks whether the setup beat simply owning the benchmark. "
                "Positive means the strategy added value beyond market direction."
            ),
        ),
        StrategyMetricCard(
            label="Share of signals that were up after 10 days",
            value=f"{replay.win_rate_10d * 100:.1f}%",
            meaning=(
                "This is the percentage of winning signals. Around 50% is "
                "coin-flip territory unless the payoff profile is clearly better."
            ),
        ),
    ]


def _status_summary(
    basis_code: str,
    live_matches: int,
    board_promoted: int,
) -> str:
    if basis_code == "breakout-confirmation":
        return (
            f"{board_promoted} live action names are currently promoted, with "
            f"{live_matches} total live matches under the breakout lens."
        )
    if basis_code == "sector-confirmed-pullback-continuation":
        return (
            f"{board_promoted} names are currently strong enough for the main board, "
            f"with {live_matches} total pullback matches still worth tracking."
        )
    if basis_code == "etf-trend-rotation":
        return (
            f"{live_matches} ETF context matches are visible, but none should be "
            "treated as main-board actions yet."
        )
    return f"{live_matches} research matches are visible, but none belong on the main board."


def _best_use_now(basis_code: str) -> str:
    mapping = {
        "breakout-confirmation": (
            "Use when you want the clearest currently promoted continuation setups."
        ),
        "sector-confirmed-pullback-continuation": (
            "Use as a selective secondary sleeve for controlled pullbacks in strong names."
        ),
        "etf-trend-rotation": "Use for context only while the live rule is being redesigned.",
        "selective-mean-reversion": "Use only as research into niche rebound behavior.",
    }
    return mapping[basis_code]


def _as_of_date() -> date | None:
    records = _load_recommendation_records()
    if not records:
        return None
    return date.fromisoformat(records[0].as_of_date)


def get_strategy_page_view(basis_code: str) -> StrategyPageView | None:
    strategy = get_strategy_record(basis_code)
    if strategy is None:
        return None
    copy = _plain_language_copy(basis_code)

    rows: list[StrategyCandidateRow] = []
    for record in _load_recommendation_records():
        mapped_code = _map_strategy_code(record.strategy_name, record.strategy_id)
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
        strategy_definition=copy["strategy_definition"],
        trust_summary=copy["trust_summary"],
        this_week_call=copy["this_week_call"],
        this_week_use=copy["this_week_use"],
        best_used_for=copy["best_used_for"],
        avoid_when=copy["avoid_when"],
        rule_spine=strategy.rule_spine,
        works_best_when=copy["works_best_when"],
        breaks_down_when=copy["breaks_down_when"],
        as_of_date=_as_of_date(),
        stats={
            "live_matches": len(rows),
            "board_promoted": board_count,
            "strategy_only": strategy_only_count,
            "suppressed": suppressed_count,
        },
        headline_note=_headline_note(basis_code, board_count, suppressed_count),
        backtest_label=_backtest_label(basis_code),
        backtest_takeaway=_backtest_takeaway(basis_code, replay),
        metric_cards=_metric_cards(replay),
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


def get_strategy_index_cards() -> list[StrategyIndexCard]:
    cards: list[StrategyIndexCard] = []
    for basis_code in (
        "breakout-confirmation",
        "sector-confirmed-pullback-continuation",
        "etf-trend-rotation",
        "selective-mean-reversion",
    ):
        strategy = get_strategy_page_view(basis_code)
        if strategy is None:
            continue
        cards.append(
            StrategyIndexCard(
                basis_code=basis_code,
                display_name=strategy.strategy_name,
                trust_level=strategy.trust_level,
                promotion_status=strategy.promotion_status,
                live_matches=strategy.stats["live_matches"],
                board_promoted=strategy.stats["board_promoted"],
                status_summary=_status_summary(
                    basis_code,
                    strategy.stats["live_matches"],
                    strategy.stats["board_promoted"],
                ),
                best_use_now=_best_use_now(basis_code),
            )
        )
    return cards
