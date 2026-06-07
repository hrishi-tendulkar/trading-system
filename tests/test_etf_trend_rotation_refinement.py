from __future__ import annotations

import pandas as pd

from scripts.mlp.run_etf_trend_rotation_refinement import (
    EtfRotationVariant,
    build_variant_candidates,
    portfolio_period_returns,
    weekly_decision_rows,
    weekly_trades,
)


def _etf_row(
    *,
    date: str,
    ticker: str,
    close: float = 100.0,
    rs_20d: float = 0.03,
    rank_boost: float = 0.0,
) -> dict[str, object]:
    return {
        "date": pd.Timestamp(date),
        "ticker": ticker,
        "display_name": ticker,
        "sector": "ETF",
        "instrument_type": "Sector ETF",
        "etf_subgroup": "Sector ETF",
        "regime": "Risk-on",
        "regime_supportive": True,
        "close": close,
        "ma_20": 95.0,
        "ma_50": 90.0,
        "ma_20_slope_5d": 0.01,
        "atr_pct": 0.02,
        "ret_10d": 0.02 + rank_boost,
        "ret_20d": 0.05 + rank_boost,
        "rs_10d": 0.01 + rank_boost,
        "rs_20d": rs_20d + rank_boost,
        "rs_60d": 0.04 + rank_boost,
        "fwd_5d_return": 0.03 + rank_boost,
        "spy_fwd_5d_return": 0.01,
        "excess_5d_return": 0.02 + rank_boost,
        "signal_sample_ready": True,
    }


def test_weekly_decision_rows_use_last_available_day_per_week() -> None:
    features = pd.DataFrame(
        [
            _etf_row(date="2026-01-07", ticker="XLK", close=99.0),
            _etf_row(date="2026-01-09", ticker="XLK", close=101.0),
            _etf_row(date="2026-01-09", ticker="XLY", close=102.0),
        ]
    )

    rows = weekly_decision_rows(features)

    assert set(rows["date"]) == {pd.Timestamp("2026-01-09")}
    assert set(rows["ticker"]) == {"XLK", "XLY"}


def test_variant_candidates_apply_scope_and_strict_relative_strength_gate() -> None:
    variant = EtfRotationVariant(
        variant_id="test_sector",
        display_name="Test Sector",
        rule_summary=[],
        top_n=1,
        universe_scope="sector",
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
    )
    features = pd.DataFrame(
        [
            _etf_row(date="2026-01-09", ticker="XLK", rs_20d=0.02),
            _etf_row(date="2026-01-09", ticker="XLY", rs_20d=-0.01),
            _etf_row(date="2026-01-09", ticker="SPY", rs_20d=0.02),
        ]
    )

    candidates = build_variant_candidates(features, variant)

    assert candidates["ticker"].tolist() == ["XLK"]


def test_weekly_trades_select_top_n_and_apply_friction() -> None:
    variant = EtfRotationVariant(
        variant_id="test_top2",
        display_name="Test Top 2",
        rule_summary=[],
        top_n=2,
        universe_scope="sector",
    )
    features = pd.DataFrame(
        [
            _etf_row(date="2026-01-09", ticker="XLK", rank_boost=0.03),
            _etf_row(date="2026-01-09", ticker="XLY", rank_boost=0.02),
            _etf_row(date="2026-01-09", ticker="XLF", rank_boost=0.01),
        ]
    )
    candidates = build_variant_candidates(features, variant)

    trades = weekly_trades(candidates)
    periods = portfolio_period_returns(trades)

    assert set(trades["ticker"]) == {"XLK", "XLY"}
    assert trades["portfolio_weight"].tolist() == [0.5, 0.5]
    assert trades["trade_return_net"].round(3).tolist() == [0.048, 0.058]
    assert periods.loc[0, "trade_count"] == 2
