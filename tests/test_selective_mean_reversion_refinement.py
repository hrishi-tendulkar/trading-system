from __future__ import annotations

import pandas as pd

from scripts.mlp.run_selective_mean_reversion_refinement import (
    VARIANTS,
    build_variant_signals,
    classify_rebound_quality,
)


def _variant(variant_id: str):
    return next(variant for variant in VARIANTS if variant.variant_id == variant_id)


def _base_row() -> dict[str, object]:
    return {
        "date": pd.Timestamp("2026-02-06"),
        "ticker": "ABC",
        "close": 98.0,
        "prev_close": 96.0,
        "ma_20": 100.0,
        "ma_50": 99.0,
        "atr_pct": 0.04,
        "ret_5d": -0.07,
        "ret_20d": -0.04,
        "rs_20d": -0.01,
        "stock_vs_sector_20d": 0.01,
        "extension_vs_ma20": -0.03,
        "pullback_from_high_20": 0.08,
        "sector_confirmation": "Confirmed",
        "signal_sample_ready": True,
        "regime": "Defensive",
        "spy_above_ma50": 0,
        "fwd_5d_return": 0.01,
        "fwd_10d_return": 0.02,
        "fwd_15d_return": 0.03,
        "spy_fwd_5d_return": 0.0,
        "spy_fwd_10d_return": 0.0,
        "spy_fwd_15d_return": 0.0,
        "excess_5d_return": 0.01,
        "excess_10d_return": 0.02,
        "excess_15d_return": 0.03,
    }


def test_defensive_variant_excludes_risk_on_dip_buying() -> None:
    defensive_row = _base_row()
    risk_on_row = _base_row() | {
        "date": pd.Timestamp("2026-02-09"),
        "ticker": "XYZ",
        "regime": "Risk-on",
    }
    features = pd.DataFrame([defensive_row, risk_on_row])

    signals = build_variant_signals(features, _variant("defensive_v1"))

    assert signals["ticker"].tolist() == ["ABC"]


def test_rebound_quality_separates_intact_rebounds_from_damaged_trends() -> None:
    true_rebound = _base_row()
    damaged = _base_row() | {
        "ticker": "DAM",
        "close": 90.0,
        "ma_20": 92.0,
        "ma_50": 100.0,
        "ret_20d": -0.20,
        "pullback_from_high_20": 0.25,
    }
    features = pd.DataFrame([true_rebound, damaged])

    labels = classify_rebound_quality(features)

    assert labels.tolist() == ["true_rebound_candidate", "damaged_trend_or_broad_dip"]
