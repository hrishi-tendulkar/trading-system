from __future__ import annotations

import pandas as pd

from packages.core.canonical_strategy_replay import (
    build_breakout_confirmation_signals,
    build_pullback_continuation_signals,
    sector_confirmation_labels,
    signal_starts,
)


def _base_row() -> dict[str, object]:
    return {
        "display_name": "Example",
        "sector": "Information Technology",
        "instrument_type": "Single name",
        "etf_subgroup": "Not applicable",
        "regime": "Risk-on",
        "regime_supportive": True,
        "sector_confirmation": "Confirmed",
        "close": 100.0,
        "ma_20": 95.0,
        "ma_50": 90.0,
        "atr_pct": 0.03,
        "ret_5d": -0.01,
        "ret_20d": 0.10,
        "rs_20d": 0.05,
        "rs_60d": 0.10,
        "distance_from_52w_high": 0.05,
        "pullback_from_high_20": 0.05,
        "pullback_depth_band": "3-6%",
        "extension_vs_ma20": 0.03,
        "extension_band": "2-4%",
        "prior_high_20": 102.0,
        "oversold_extension_band": "> -2%",
        "fwd_5d_return": 0.02,
        "fwd_10d_return": 0.03,
        "fwd_15d_return": 0.04,
        "spy_fwd_5d_return": 0.01,
        "spy_fwd_10d_return": 0.01,
        "spy_fwd_15d_return": 0.01,
        "excess_5d_return": 0.01,
        "excess_10d_return": 0.02,
        "excess_15d_return": 0.03,
        "signal_sample_ready": True,
    }


def test_breakout_confirmation_requires_true_triggered_entry() -> None:
    first_day = _base_row() | {"date": pd.Timestamp("2026-01-02"), "ticker": "ABC", "close": 99.0}
    second_day = _base_row() | {"date": pd.Timestamp("2026-01-03"), "ticker": "ABC", "close": 103.0}
    features = pd.DataFrame([first_day, second_day])

    signals = build_breakout_confirmation_signals(features)

    assert list(signals["date"]) == [pd.Timestamp("2026-01-03")]
    assert list(signals["ticker"]) == ["ABC"]
    assert list(signals["signal_style"]) == ["Triggered breakout entry"]


def test_pullback_signals_preserve_depth_and_extension_bands() -> None:
    signal_row = _base_row() | {
        "date": pd.Timestamp("2026-02-06"),
        "ticker": "PULL",
        "pullback_from_high_20": 0.07,
        "pullback_depth_band": "6-10%",
        "extension_vs_ma20": 0.02,
        "extension_band": "2-4%",
    }
    features = pd.DataFrame([signal_row])

    signals = build_pullback_continuation_signals(features)

    assert len(signals) == 1
    row = signals.iloc[0]
    assert row["strategy_name"] == "Sector-Confirmed Pullback Continuation"
    assert row["pullback_depth_band"] == "6-10%"
    assert row["extension_band"] == "2-4%"


def test_signal_starts_only_count_the_first_true_row_per_ticker() -> None:
    condition = pd.Series([False, True, True, False, True, True], dtype=bool)
    tickers = pd.Series(["AAA", "AAA", "AAA", "AAA", "BBB", "BBB"])

    starts = signal_starts(condition, tickers)

    assert starts.tolist() == [False, True, False, False, True, False]


def test_sector_confirmation_marks_missing_proxy_as_unavailable() -> None:
    features = pd.DataFrame(
        [
            {
                "instrument_type": "Single name",
                "sector_close": None,
                "sector_above_ma20": 0.0,
                "sector_above_ma50": 0.0,
            },
            {
                "instrument_type": "Single name",
                "sector_close": 50.0,
                "sector_above_ma20": 1.0,
                "sector_above_ma50": 1.0,
            },
            {
                "instrument_type": "Broad ETF",
                "sector_close": 500.0,
                "sector_above_ma20": 1.0,
                "sector_above_ma50": 1.0,
            },
        ]
    )

    labels = sector_confirmation_labels(features)

    assert labels.tolist() == ["Unavailable", "Confirmed", "Not applicable"]
