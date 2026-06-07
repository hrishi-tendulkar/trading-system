from __future__ import annotations

import pandas as pd

from scripts.mlp.run_watchlist_analysis import (
    refined_breakout_confirmation_triggered,
    refined_breakout_confirmation_watch,
    strategy_payload,
)


def _breakout_row(**overrides: object) -> pd.Series:
    row = {
        "ticker": "ABC",
        "close": 105.0,
        "ma_20": 100.0,
        "ma_50": 95.0,
        "atr_14": 4.0,
        "atr_pct": 0.038,
        "extension_vs_ma20": 0.05,
        "rs_10d": 0.02,
        "rs_20d": 0.04,
        "rs_60d": 0.03,
        "stock_vs_sector_20d": 0.01,
        "stock_vs_sector_60d": 0.0,
        "distance_from_52w_high": 0.05,
        "ret_20d": 0.08,
        "ret_5d": 0.03,
        "low_10": 98.0,
        "high_10": 103.0,
        "high_20": 104.0,
        "prior_high_20": 104.0,
        "days_to_earnings": 30.0,
        "event_risk": "Low",
        "is_benchmark": False,
        "sector": "Information Technology",
        "spy_above_ma20": 1,
        "spy_above_ma50": 1,
        "qqq_above_ma20": 1,
        "qqq_above_ma50": 1,
        "qqq_ma20_slope_5d": 0.01,
        "sector_above_ma20": 1,
        "sector_above_ma50": 1,
    }
    row.update(overrides)
    return pd.Series(row)


def test_refined_breakout_triggered_becomes_buy_now() -> None:
    row = _breakout_row()

    payload = strategy_payload(row, include_event_overlay=True)

    assert refined_breakout_confirmation_triggered(row) is True
    assert payload["strategy_id"] == "breakout-confirmation-triggered"
    assert payload["strategy_name"] == "Breakout Confirmation"
    assert payload["action_label"] == "Buy now"


def test_broad_breakout_without_sector_confirmation_is_not_promoted() -> None:
    row = _breakout_row(sector_above_ma20=0, sector_above_ma50=0)

    payload = strategy_payload(row, include_event_overlay=True)

    assert refined_breakout_confirmation_triggered(row) is False
    assert payload["strategy_id"] != "breakout-confirmation-triggered"
    assert payload["action_label"] != "Buy now"


def test_near_breakout_waits_for_confirmation_until_triggered() -> None:
    row = _breakout_row(close=102.0, prior_high_20=104.0)

    payload = strategy_payload(row, include_event_overlay=True)

    assert refined_breakout_confirmation_watch(row) is True
    assert payload["strategy_id"] == "wait-for-confirmation"
    assert payload["action_label"] == "Wait for confirmation"
