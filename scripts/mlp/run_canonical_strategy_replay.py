#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from packages.core.canonical_strategy_replay import (
    build_strategy_replay_artifacts,
    prepare_replay_features,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run canonical strategy-separated replay across the S&P 100 plus ETF universe."
    )
    parser.add_argument("--watchlist", default="data/reference/sp100_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/sp100_5y/mlp_prices.csv")
    parser.add_argument("--outdir", default="data/processed")
    parser.add_argument("--version-label", default=f"{date.today().isoformat()}_v1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prices = pd.read_csv(args.prices)
    watchlist = pd.read_csv(args.watchlist)

    features = prepare_replay_features(prices, watchlist)
    artifacts = build_strategy_replay_artifacts(features)

    outdir = Path(args.outdir) / f"canonical_strategy_replay_{args.version_label}"
    outdir.mkdir(parents=True, exist_ok=True)

    output_map = {
        "canonical_strategy_signals.csv": artifacts["signals"],
        "canonical_strategy_summary.csv": artifacts["strategy_summary"],
        "canonical_strategy_regime_summary.csv": artifacts["regime_summary"],
        "canonical_strategy_sector_summary.csv": artifacts["sector_summary"],
        "canonical_etf_rotation_summary.csv": artifacts["etf_rotation_summary"],
        "canonical_pullback_band_summary.csv": artifacts["pullback_band_summary"],
        "canonical_pullback_sector_summary.csv": artifacts["pullback_sector_summary"],
        "canonical_breakout_context_summary.csv": artifacts["breakout_context_summary"],
        "canonical_mean_reversion_regime_summary.csv": artifacts["mean_reversion_regime_summary"],
        "canonical_strategy_comparison.csv": artifacts["comparison"],
    }
    for name, frame in output_map.items():
        frame.to_csv(outdir / name, index=False)

    manifest = {
        "version_label": args.version_label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "universe": "S&P 100 + ETFs",
        "source_watchlist": args.watchlist,
        "source_prices": args.prices,
        "signal_rules": {
            "etf_trend_rotation": {
                "instrument_scope": "SPY, QQQ, XLK, XLF, XLV, XLE, XLI, XLY",
                "trigger": "first day a trend-qualified ETF becomes newly eligible",
                "filters": ["close > 20DMA > 50DMA", "20DMA slope positive", "RS 20D > 1%", "RS 60D > 0"],
            },
            "sector_confirmed_pullback_continuation": {
                "instrument_scope": "single names only",
                "trigger": "first day a controlled pullback becomes newly eligible",
                "filters": [
                    "close > 50DMA",
                    "20DMA > 50DMA",
                    "RS 20D > 2%",
                    "pullback from prior 20D high between 2% and 15%",
                    "extension vs 20DMA between -3% and +6%",
                ],
            },
            "breakout_confirmation": {
                "instrument_scope": "single names only",
                "trigger": "first confirmed close above the prior 20-day high",
                "filters": ["close > 20DMA > 50DMA", "RS 20D > 0", "RS 60D > 0"],
            },
            "selective_mean_reversion": {
                "instrument_scope": "single names only",
                "trigger": "first oversold rebound day after a sharp 5D setback",
                "filters": [
                    "current close > prior close",
                    "5D return <= -6%",
                    "extension vs 20DMA between -10% and -2%",
                    "close >= 97% of 50DMA",
                ],
            },
        },
    }
    (outdir / "replay_manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"Wrote canonical strategy replay outputs to {outdir}")


if __name__ == "__main__":
    main()
