#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from run_watchlist_analysis import add_features, strategy_payload

SECTOR_ETF_MAP = {
    "Information Technology": "XLK",
    "Financials": "XLF",
    "Health Care": "XLV",
    "Energy": "XLE",
    "Industrials": "XLI",
    "Consumer Discretionary": "XLY",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run higher-leverage strategy iterations on a broader universe.")
    parser.add_argument("--watchlist", default="data/reference/sp100_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/sp100_5y/mlp_prices.csv")
    parser.add_argument("--outdir", default="data/processed/strategy_iterations")
    return parser.parse_args()


def prepare_features(prices: pd.DataFrame, watchlist: pd.DataFrame) -> pd.DataFrame:
    prices = prices.merge(watchlist[["ticker", "sector", "is_benchmark"]], on="ticker", how="left")
    features = add_features(prices)
    features = features.sort_values(["ticker", "date"]).copy()
    for horizon, days in [("1w", 5), ("2w", 10), ("3w", 15)]:
        features[f"fwd_{horizon}_return"] = features.groupby("ticker")["close"].shift(-days) / features["close"] - 1
    return features


def regime_ok(row: pd.Series) -> bool:
    return bool(
        row.get("spy_above_ma20", 0) == 1
        and row.get("spy_above_ma50", 0) == 1
        and row.get("qqq_above_ma20", 0) == 1
        and row.get("qqq_above_ma50", 0) == 1
        and row.get("qqq_ma20_slope_5d", -1) > 0
    )


def classify_variant(row: pd.Series, variant: str) -> dict[str, object]:
    if variant == "baseline":
        payload = strategy_payload(row, include_event_overlay=False)
        rank_score = float(row.get("refined_score", 0))
        return {
            "variant": variant,
            "strategy_name": payload["strategy_name"],
            "action_label": payload["action_label"],
            "rank_score": rank_score,
        }

    close = float(row["close"])
    ma20 = float(row["ma_20"])
    ma50 = float(row["ma_50"])
    atr = float(row["atr_14"])
    extension = float(row["extension_vs_ma20"])
    dist_high = float(row["distance_from_52w_high"])
    rs_10d = float(row.get("rs_10d", np.nan))
    rs_20d = float(row.get("rs_20d", np.nan))
    rs_60d = float(row.get("rs_60d", np.nan))
    svs_20d = float(row.get("stock_vs_sector_20d", np.nan))
    svs_60d = float(row.get("stock_vs_sector_60d", np.nan))
    ret_5d = float(row.get("ret_5d", np.nan))
    atr_pct = float(row.get("atr_pct", np.nan))
    days_to_earnings = row.get("days_to_earnings")
    sector = str(row.get("sector", ""))
    sector_ok = bool(row.get("sector_above_ma20", 0) == 1 and row.get("sector_above_ma50", 0) == 1)

    support = max(float(row["low_10"]), ma20)
    stop = min(ma50, support - 0.5 * atr, close - 0.75 * atr)
    stop = max(stop, 0.0)
    target = close + 1.75 * atr
    rr_1 = (target - close) / max(close - stop, 0.01)
    base_score = (
        2.0 * (rs_20d if pd.notna(rs_20d) else -1)
        + 1.25 * (rs_10d if pd.notna(rs_10d) else -1)
        + 0.75 * (rs_60d if pd.notna(rs_60d) else -1)
        - 1.5 * max(extension - 0.04, 0)
        - 2.0 * max(atr_pct - 0.05, 0)
    )

    if pd.notna(days_to_earnings) and 0 <= float(days_to_earnings) <= 7:
        return {
            "variant": variant,
            "strategy_name": "Event freeze before earnings",
            "action_label": "No action",
            "rank_score": -99.0,
        }

    if variant == "strict_rs_entry":
        if close > ma20 > ma50 and rs_20d > 0.05 and rs_10d > 0.02 and rs_60d > 0 and ret_5d > 0 and 0.01 <= extension <= 0.05 and dist_high <= 0.15 and atr_pct <= 0.055:
            return {"variant": variant, "strategy_name": "Constructive pullback continuation", "action_label": "Buy now", "rank_score": base_score}
        if close > ma20 > ma50 and rs_20d > 0.05 and extension > 0.05 and extension <= 0.10:
            return {"variant": variant, "strategy_name": "Extended strength, wait for pullback", "action_label": "Buy on pullback", "rank_score": base_score - 0.5}
        if close > ma20 > ma50 and rs_20d > 0 and dist_high <= 0.12:
            return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 1.0}
        if close > ma20 and rs_20d > -0.01:
            return {"variant": variant, "strategy_name": "Trend hold / monitor", "action_label": "Hold", "rank_score": base_score - 2.0}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -5.0}

    if variant == "regime_gated":
        if not regime_ok(row):
            if close > ma20 > ma50 and rs_20d > 0.03:
                return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 2.0}
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

        return classify_variant(row, "strict_rs_entry") | {"variant": variant}

    if variant == "rr_selective":
        if not regime_ok(row):
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if close > ma20 > ma50 and rs_20d > 0.05 and rs_10d > 0.02 and rs_60d > 0 and ret_5d > 0 and 0.01 <= extension <= 0.045 and dist_high <= 0.12 and atr_pct <= 0.05 and rr_1 >= 1.5:
            return {"variant": variant, "strategy_name": "Constructive pullback continuation", "action_label": "Buy now", "rank_score": base_score + rr_1}
        if close > ma20 > ma50 and rs_20d > 0.06 and extension > 0.045 and extension <= 0.08:
            return {"variant": variant, "strategy_name": "Extended strength, wait for pullback", "action_label": "Buy on pullback", "rank_score": base_score}
        if close > ma20 > ma50 and rs_20d > 0.02 and rs_60d > 0:
            return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 1.0}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

    if variant == "pullback_only":
        if not regime_ok(row):
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if close > ma20 > ma50 and rs_20d > 0.04 and rs_60d > 0 and 0.03 <= extension <= 0.08 and atr_pct <= 0.05 and rr_1 >= 1.2:
            return {"variant": variant, "strategy_name": "Constructive pullback continuation", "action_label": "Buy on pullback", "rank_score": base_score + 0.5 * rr_1}
        if close > ma20 > ma50 and rs_20d > 0.02 and rs_60d > 0:
            return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 1.0}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

    if variant == "sector_filtered_pullback":
        if not regime_ok(row):
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if sector == "ETF":
            if close > ma20 > ma50 and rs_20d > 0.03 and rs_60d > 0:
                return {"variant": variant, "strategy_name": "Index trend follow-through", "action_label": "Buy now", "rank_score": base_score}
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if sector_ok and close > ma20 > ma50 and rs_20d > 0.04 and rs_60d > 0 and svs_20d > 0 and svs_60d >= 0 and 0.03 <= extension <= 0.10 and atr_pct <= 0.055:
            return {"variant": variant, "strategy_name": "Constructive pullback continuation", "action_label": "Buy on pullback", "rank_score": base_score + 0.5 * svs_20d}
        if sector_ok and close > ma20 > ma50 and rs_20d > 0.02 and svs_20d >= 0:
            return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 0.75}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

    if variant == "near_high_continuation":
        if not regime_ok(row):
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        near_high = dist_high <= 0.08
        if sector == "ETF":
            if close > ma20 > ma50 and rs_20d > 0.03 and near_high:
                return {"variant": variant, "strategy_name": "Index trend follow-through", "action_label": "Buy now", "rank_score": base_score + 0.5}
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if sector_ok and close > ma20 > ma50 and near_high and rs_20d > 0.05 and rs_60d > 0 and svs_20d > 0 and atr_pct <= 0.05 and extension <= 0.05:
            return {"variant": variant, "strategy_name": "Near-high continuation", "action_label": "Buy now", "rank_score": base_score + 1.0}
        if sector_ok and close > ma20 > ma50 and near_high and rs_20d > 0.02:
            return {"variant": variant, "strategy_name": "Breakout confirmation", "action_label": "Wait for confirmation", "rank_score": base_score - 0.5}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

    if variant == "etf_rotation_top":
        if sector != "ETF":
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if not regime_ok(row):
            return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}
        if close > ma20 > ma50 and rs_20d > 0.02 and rs_60d > 0:
            return {"variant": variant, "strategy_name": "ETF rotation", "action_label": "Buy now", "rank_score": base_score + max(rs_20d, 0)}
        if close > ma20 > ma50:
            return {"variant": variant, "strategy_name": "ETF rotation", "action_label": "Wait for confirmation", "rank_score": base_score - 1.0}
        return {"variant": variant, "strategy_name": "No actionable setup", "action_label": "No action", "rank_score": -10.0}

    raise ValueError(f"Unknown variant: {variant}")


def evaluate_variant(features: pd.DataFrame, variant: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    eligible = features[~features["is_benchmark"].fillna(False)].copy()
    rows = []
    portfolio_rows = []
    latest_rows = []
    trading_dates = sorted(eligible["date"].drop_duplicates())
    fridays = [d for d in trading_dates if d.weekday() == 4]
    latest_date = max(trading_dates)

    for dt in fridays:
        day = eligible[eligible["date"] == dt].copy()
        if day.empty:
            continue
        classified = pd.DataFrame([classify_variant(row, variant) for _, row in day.iterrows()])
        scored = pd.concat([day.reset_index(drop=True), classified], axis=1)
        rows.append(scored)
        if dt == latest_date:
            latest_rows.append(scored.copy())

        actionable = scored[scored["action_label"].isin(["Buy now", "Buy on pullback"])]
        actionable = actionable.sort_values(["action_label", "rank_score"], ascending=[True, False])
        top2 = actionable.head(2)
        top5 = actionable.head(5)
        for label, bucket in [("top2", top2), ("top5", top5)]:
            if bucket.empty:
                continue
            portfolio_rows.append(
                {
                    "variant": variant,
                    "date": dt.date().isoformat(),
                    "portfolio_label": label,
                    "count": len(bucket),
                    "avg_fwd_1w_return": bucket["fwd_1w_return"].mean(),
                    "avg_fwd_2w_return": bucket["fwd_2w_return"].mean(),
                    "avg_fwd_3w_return": bucket["fwd_3w_return"].mean(),
                }
            )

    all_rows = pd.concat(rows, ignore_index=True)
    latest = pd.concat(latest_rows, ignore_index=True) if latest_rows else pd.DataFrame()
    portfolios = pd.DataFrame(portfolio_rows)

    summary = (
        all_rows.groupby("action_label")
        .agg(
            observations=("ticker", "count"),
            avg_fwd_1w_return=("fwd_1w_return", "mean"),
            avg_fwd_2w_return=("fwd_2w_return", "mean"),
            avg_fwd_3w_return=("fwd_3w_return", "mean"),
            win_rate_1w=("fwd_1w_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
    )
    summary["variant"] = variant
    return latest, portfolios, summary


def main() -> None:
    args = parse_args()
    prices = pd.read_csv(args.prices)
    watchlist = pd.read_csv(args.watchlist)
    features = prepare_features(prices, watchlist)

    variants = [
        "baseline",
        "strict_rs_entry",
        "regime_gated",
        "rr_selective",
        "pullback_only",
        "sector_filtered_pullback",
        "near_high_continuation",
        "etf_rotation_top",
    ]
    latest_frames = []
    portfolio_frames = []
    summary_frames = []

    for variant in variants:
        latest, portfolios, summary = evaluate_variant(features, variant)
        latest_frames.append(latest)
        portfolio_frames.append(portfolios)
        summary_frames.append(summary)

    latest_all = pd.concat(latest_frames, ignore_index=True)
    portfolios_all = pd.concat(portfolio_frames, ignore_index=True)
    summaries_all = pd.concat(summary_frames, ignore_index=True)

    variant_scorecard = (
        portfolios_all.groupby(["variant", "portfolio_label"])
        .agg(
            observations=("date", "count"),
            avg_fwd_1w_return=("avg_fwd_1w_return", "mean"),
            avg_fwd_2w_return=("avg_fwd_2w_return", "mean"),
            avg_fwd_3w_return=("avg_fwd_3w_return", "mean"),
        )
        .reset_index()
        .sort_values(["portfolio_label", "avg_fwd_1w_return"], ascending=[True, False])
    )

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    latest_all.to_csv(outdir / "iteration_latest.csv", index=False)
    portfolios_all.to_csv(outdir / "iteration_portfolios.csv", index=False)
    summaries_all.to_csv(outdir / "iteration_action_summaries.csv", index=False)
    variant_scorecard.to_csv(outdir / "iteration_variant_scorecard.csv", index=False)
    print(f"Wrote iteration outputs to {outdir}")


if __name__ == "__main__":
    main()
