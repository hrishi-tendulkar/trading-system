#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SECTOR_ETF_MAP = {
    "Information Technology": "XLK",
    "Financials": "XLF",
    "Health Care": "XLV",
    "Energy": "XLE",
    "Industrials": "XLI",
    "Consumer Discretionary": "XLY",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run MLP watchlist analysis with explicit strategy families and simple backtests."
    )
    parser.add_argument("--watchlist", default="data/reference/mlp_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/mlp/mlp_prices.csv")
    parser.add_argument("--earnings", default="data/raw/mlp/mlp_earnings_snapshot.csv")
    parser.add_argument("--outdir", default="data/processed/mlp")
    parser.add_argument("--report", default="docs/research/market/mlp-weekly-report-2026-05-22.md")
    return parser.parse_args()


def add_features(prices: pd.DataFrame, benchmark: str = "SPY") -> pd.DataFrame:
    frames = []
    prices = prices.sort_values(["ticker", "date"]).copy()
    prices["date"] = pd.to_datetime(prices["date"])
    bench = prices.loc[prices["ticker"] == benchmark, ["date", "close"]].rename(columns={"close": "benchmark_close"})
    bench["benchmark_ma_20"] = bench["benchmark_close"].rolling(20).mean()
    bench["benchmark_ma_50"] = bench["benchmark_close"].rolling(50).mean()
    bench["benchmark_ret_5d"] = bench["benchmark_close"].pct_change(5, fill_method=None)
    bench["benchmark_ret_10d"] = bench["benchmark_close"].pct_change(10, fill_method=None)
    bench["benchmark_ret_20d"] = bench["benchmark_close"].pct_change(20)
    bench["benchmark_ret_60d"] = bench["benchmark_close"].pct_change(60, fill_method=None)
    qqq = prices.loc[prices["ticker"] == "QQQ", ["date", "close"]].rename(columns={"close": "qqq_close"})
    qqq["qqq_ma_20"] = qqq["qqq_close"].rolling(20).mean()
    qqq["qqq_ma_50"] = qqq["qqq_close"].rolling(50).mean()
    qqq["qqq_ma_20_prev"] = qqq["qqq_ma_20"].shift(5)
    sector_frames = []
    for sector, etf in SECTOR_ETF_MAP.items():
        sector_frame = prices.loc[prices["ticker"] == etf, ["date", "close"]].rename(columns={"close": "sector_close"})
        if sector_frame.empty:
            continue
        sector_frame["sector"] = sector
        sector_frame["sector_ret_10d"] = sector_frame["sector_close"].pct_change(10, fill_method=None)
        sector_frame["sector_ret_20d"] = sector_frame["sector_close"].pct_change(20, fill_method=None)
        sector_frame["sector_ret_60d"] = sector_frame["sector_close"].pct_change(60, fill_method=None)
        sector_frame["sector_ma_20"] = sector_frame["sector_close"].rolling(20).mean()
        sector_frame["sector_ma_50"] = sector_frame["sector_close"].rolling(50).mean()
        sector_frames.append(sector_frame)
    sector_df = pd.concat(sector_frames, ignore_index=True) if sector_frames else pd.DataFrame()

    for ticker, frame in prices.groupby("ticker", sort=False):
        f = frame.copy()
        f["ret_5d"] = f["close"].pct_change(5, fill_method=None)
        f["ret_10d"] = f["close"].pct_change(10, fill_method=None)
        f["ret_20d"] = f["close"].pct_change(20, fill_method=None)
        f["ret_60d"] = f["close"].pct_change(60, fill_method=None)
        f["ma_20"] = f["close"].rolling(20).mean()
        f["ma_50"] = f["close"].rolling(50).mean()
        f["ma_20_prev"] = f["ma_20"].shift(5)
        f["ma_50_prev"] = f["ma_50"].shift(5)
        f["low_10"] = f["low"].rolling(10).min()
        f["high_10"] = f["high"].rolling(10).max()
        f["high_20"] = f["high"].rolling(20).max()
        f["prior_high_20"] = f["high"].rolling(20).max().shift(1)
        tr = pd.concat(
            [
                f["high"] - f["low"],
                (f["high"] - f["close"].shift(1)).abs(),
                (f["low"] - f["close"].shift(1)).abs(),
            ],
            axis=1,
        ).max(axis=1)
        f["atr_14"] = tr.rolling(14).mean()
        f["atr_pct"] = f["atr_14"] / f["close"]
        f["high_252"] = f["close"].rolling(252, min_periods=20).max()
        f["distance_from_52w_high"] = (f["high_252"] - f["close"]) / f["high_252"]
        f["volume_ratio_20d"] = f["volume"] / f["volume"].rolling(20).mean()
        f["extension_vs_ma20"] = (f["close"] - f["ma_20"]) / f["ma_20"]
        f["extension_vs_ma50"] = (f["close"] - f["ma_50"]) / f["ma_50"]
        f["close_above_ma20"] = (f["close"] > f["ma_20"]).astype(int)
        f["days_above_ma20_15"] = f["close_above_ma20"].rolling(15).sum()
        f = f.merge(
            bench[
                [
                    "date",
                    "benchmark_close",
                    "benchmark_ma_20",
                    "benchmark_ma_50",
                    "benchmark_ret_5d",
                    "benchmark_ret_10d",
                    "benchmark_ret_20d",
                    "benchmark_ret_60d",
                ]
            ],
            on="date",
            how="left",
        )
        f = f.merge(qqq[["date", "qqq_close", "qqq_ma_20", "qqq_ma_50", "qqq_ma_20_prev"]], on="date", how="left")
        f["rs_5d"] = f["ret_5d"] - f["benchmark_ret_5d"]
        f["rs_10d"] = f["ret_10d"] - f["benchmark_ret_10d"]
        f["rs_20d"] = f["ret_20d"] - f["benchmark_ret_20d"]
        f["rs_60d"] = f["ret_60d"] - f["benchmark_ret_60d"]
        f["ma_20_slope_5d"] = (f["ma_20"] / f["ma_20_prev"]) - 1
        f["ma_50_slope_5d"] = (f["ma_50"] / f["ma_50_prev"]) - 1
        f["spy_above_ma20"] = (f["benchmark_close"] > f["benchmark_ma_20"]).astype(int)
        f["spy_above_ma50"] = (f["benchmark_close"] > f["benchmark_ma_50"]).astype(int)
        f["qqq_above_ma20"] = (f["qqq_close"] > f["qqq_ma_20"]).astype(int)
        f["qqq_above_ma50"] = (f["qqq_close"] > f["qqq_ma_50"]).astype(int)
        f["qqq_ma20_slope_5d"] = (f["qqq_ma_20"] / f["qqq_ma_20_prev"]) - 1
        if "sector" in f.columns and not sector_df.empty:
            f = f.merge(
                sector_df[
                    [
                        "date",
                        "sector",
                        "sector_close",
                        "sector_ret_10d",
                        "sector_ret_20d",
                        "sector_ret_60d",
                        "sector_ma_20",
                        "sector_ma_50",
                    ]
                ],
                on=["date", "sector"],
                how="left",
            )
            f["stock_vs_sector_20d"] = f["ret_20d"] - f["sector_ret_20d"]
            f["stock_vs_sector_60d"] = f["ret_60d"] - f["sector_ret_60d"]
            f["sector_above_ma20"] = (f["sector_close"] > f["sector_ma_20"]).astype(float)
            f["sector_above_ma50"] = (f["sector_close"] > f["sector_ma_50"]).astype(float)
        f["trend_score"] = (
            (f["close"] > f["ma_20"]).astype(int)
            + (f["close"] > f["ma_50"]).astype(int)
            + (f["ma_20"] > f["ma_50"]).astype(int)
        )
        f["momentum_score"] = ((f["ret_5d"] > 0).astype(int) + (f["ret_20d"] > 0).astype(int))
        f["rs_score"] = ((f["rs_20d"] > 0).astype(int) + (f["rs_20d"] > 0.03).astype(int))
        f["proximity_score"] = (f["distance_from_52w_high"] <= 0.10).astype(int)
        f["risk_penalty"] = (f["atr_pct"] > 0.06).astype(int)
        f["extension_penalty"] = (f["extension_vs_ma20"] > 0.06).astype(int)
        f["refined_score"] = (
            f["trend_score"]
            + f["momentum_score"]
            + f["rs_score"]
            + f["proximity_score"]
            - f["risk_penalty"]
            - f["extension_penalty"]
        )
        frames.append(f)
    return pd.concat(frames, ignore_index=True)


def with_earnings_flags(latest: pd.DataFrame, earnings: pd.DataFrame) -> pd.DataFrame:
    merged = latest.merge(earnings, on="ticker", how="left")
    merged["next_earnings_date"] = pd.to_datetime(merged["next_earnings_date"], errors="coerce")
    merged["days_to_earnings"] = (merged["next_earnings_date"] - merged["date"]).dt.days
    merged["event_risk"] = np.select(
        [
            merged["days_to_earnings"].between(0, 7, inclusive="both"),
            merged["days_to_earnings"].between(8, 15, inclusive="both"),
        ],
        ["High", "Medium"],
        default="Low",
    )
    return merged


def market_regime(row: pd.Series) -> str:
    if (
        row.get("spy_above_ma20", 0) == 1
        and row.get("spy_above_ma50", 0) == 1
        and row.get("qqq_above_ma20", 0) == 1
        and row.get("qqq_above_ma50", 0) == 1
        and row.get("qqq_ma20_slope_5d", -1) > 0
    ):
        return "Risk-on"
    if (
        row.get("spy_above_ma20", 0) == 1
        and row.get("spy_above_ma50", 0) == 1
    ):
        return "Selective risk-on"
    if row.get("spy_above_ma20", 0) == 1 or row.get("qqq_above_ma20", 0) == 1:
        return "Neutral"
    return "Defensive"


def sector_confirmed(row: pd.Series) -> bool:
    return bool(row.get("sector_above_ma20", 0) == 1 and row.get("sector_above_ma50", 0) == 1)


def refined_breakout_confirmation_triggered(row: pd.Series) -> bool:
    prior_high_20 = row.get("prior_high_20", np.nan)
    return bool(
        pd.notna(prior_high_20)
        and market_regime(row) in {"Risk-on", "Selective risk-on"}
        and sector_confirmed(row)
        and float(row["close"]) > float(row["ma_20"]) > float(row["ma_50"])
        and float(row["close"]) > float(prior_high_20)
        and float(row.get("rs_20d", np.nan)) > 0
        and float(row.get("rs_60d", np.nan)) > 0
        and float(row.get("atr_pct", np.nan)) <= 0.06
        and float(row.get("distance_from_52w_high", np.nan)) <= 0.15
    )


def refined_breakout_confirmation_watch(row: pd.Series) -> bool:
    prior_high_20 = row.get("prior_high_20", np.nan)
    close = float(row["close"])
    trigger = float(prior_high_20) if pd.notna(prior_high_20) else float(row.get("high_20", np.nan))
    if pd.isna(trigger) or trigger <= 0:
        return False
    return bool(
        market_regime(row) in {"Risk-on", "Selective risk-on"}
        and sector_confirmed(row)
        and close > float(row["ma_20"]) > float(row["ma_50"])
        and close <= trigger
        and close >= 0.97 * trigger
        and float(row.get("rs_20d", np.nan)) > 0
        and float(row.get("rs_60d", np.nan)) > 0
        and float(row.get("atr_pct", np.nan)) <= 0.06
        and float(row.get("distance_from_52w_high", np.nan)) <= 0.15
    )


def strategy_payload(
    row: pd.Series,
    *,
    include_event_overlay: bool,
) -> dict[str, object]:
    ticker = row["ticker"]
    close = float(row["close"])
    ma20 = float(row["ma_20"])
    ma50 = float(row["ma_50"])
    atr = float(row["atr_14"])
    extension = float(row["extension_vs_ma20"])
    rs_20d = float(row["rs_20d"])
    rs_10d = float(row.get("rs_10d", np.nan))
    rs_60d = float(row.get("rs_60d", np.nan))
    svs_20d = float(row.get("stock_vs_sector_20d", np.nan))
    svs_60d = float(row.get("stock_vs_sector_60d", np.nan))
    dist_high = float(row["distance_from_52w_high"])
    support = max(float(row["low_10"]), ma20)
    breakout_level = float(row["high_10"])
    stop = min(ma50, support - 0.5 * atr)
    stop = min(stop, close - 0.75 * atr)
    stop = max(stop, 0.0)
    target = close + 1.75 * atr
    days_to_earnings = row.get("days_to_earnings")
    is_benchmark = bool(row.get("is_benchmark", False))
    sector = str(row.get("sector", ""))
    regime = market_regime(row)
    sector_ok = sector_confirmed(row)
    prior_high_20 = row.get("prior_high_20", np.nan)
    breakout_trigger = float(prior_high_20) if pd.notna(prior_high_20) else breakout_level

    payload = {
        "strategy_id": "no-action",
        "strategy_name": "No actionable setup",
        "basis_type": "Decision basis",
        "sleeve": "Single-name sleeve",
        "action_label": "No action",
        "horizon": "Wait this week",
        "entry_label": "Stand aside",
        "entry_value": "No fresh entry",
        "stop_label": "Reassess if close <",
        "stop_value": f"${stop:.0f}",
        "target_label": "Need first",
        "target_value": "Cleaner setup",
        "strategy_rationale": "The chart is missing either strong relative strength, clean support, or acceptable timing.",
        "observed_reason": "Setup quality is not yet strong enough to justify fresh capital.",
    }

    if is_benchmark and ticker == "SPY":
        payload.update(
            {
                "strategy_id": "benchmark-reference",
                "strategy_name": "Benchmark trend reference",
                "basis_type": "Context lens",
                "sleeve": "Context",
                "action_label": "Benchmark reference",
                "horizon": "Reference only",
                "entry_label": "Role",
                "entry_value": "Benchmark",
                "stop_label": "Use for",
                "stop_value": "Context",
                "target_label": "Not a",
                "target_value": "Primary trade",
                "strategy_rationale": "SPY sets the tape. It should anchor relative-strength and market-posture judgments rather than compete for capital in this tiny prototype.",
                "observed_reason": "Benchmark trend is still constructive and useful for context.",
            }
        )
        return payload

    if (
        sector == "ETF"
        and ticker in {"VOO", "QQQ", "XLK", "XLF", "XLV", "XLE", "XLI", "XLY"}
        and close > ma20 > ma50
        and row["atr_pct"] < 0.03
        and regime in {"Risk-on", "Selective risk-on"}
        and rs_20d > 0.02
        and rs_60d > 0
        and (ticker in {"VOO", "QQQ"} or rs_10d >= 0)
    ):
        payload.update(
            {
                "strategy_id": "etf-rotation",
                "strategy_name": "ETF rotation",
                "basis_type": "Setup family",
                "sleeve": "ETF sleeve",
                "action_label": "Buy now",
                "horizon": "2-4 weeks",
                "entry_label": "Buy this week",
                "entry_value": f"${max(ma20, close - 0.4 * atr):.0f}-${close:.0f}",
                "stop_label": "Exit if close <",
                "stop_value": f"${(ma20 - 1.0 * atr):.0f}",
                "target_label": "First target",
                "target_value": f"${(close + 1.2 * atr):.0f}",
                "strategy_rationale": "Use the strongest broad or sector ETF when the tape is constructive and group-level momentum offers a cleaner expression than single-name risk.",
                "observed_reason": "Trend is intact, the regime is supportive, and ETF-level strength is strong enough to justify direct exposure.",
            }
        )
        return payload

    if include_event_overlay and pd.notna(days_to_earnings) and 0 <= float(days_to_earnings) <= 7:
        payload.update(
            {
                "strategy_id": "event-risk-hold",
                "strategy_name": "Event freeze before earnings",
                "basis_type": "Risk guardrail",
                "sleeve": "Single-name sleeve",
                "action_label": "Hold / reassess after earnings",
                "horizon": "This week only",
                "entry_label": "Do not add",
                "entry_value": f"Until earnings on {row['next_earnings_date'].date().isoformat()}",
                "stop_label": "If already held",
                "stop_value": f"Close < ${max(ma20 - 0.5 * atr, 0):.0f}",
                "target_label": "Next action",
                "target_value": "Re-rank after report",
                "strategy_rationale": "Even if the stock is stabilizing, the earnings event dominates the next move and makes fresh weekly entries more binary than this system should prefer.",
                "observed_reason": "Earnings are close enough that event risk matters more than the current chart.",
            }
        )
        return payload

    if regime == "Defensive":
        payload.update(
            {
                "strategy_id": "regime-filtered-out",
                "strategy_name": "No actionable setup",
                "basis_type": "Decision basis",
                "sleeve": "Single-name sleeve",
                "action_label": "No action",
                "horizon": "Wait this week",
                "entry_label": "Stand aside",
                "entry_value": "Regime filter",
                "stop_label": "Reassess if",
                "stop_value": "Tape improves",
                "target_label": "Need first",
                "target_value": "Stronger market",
                "strategy_rationale": "The stock may be acceptable on its own, but the broader tape is not supportive enough for fresh long entries.",
                "observed_reason": "Market regime is too weak to justify a fresh long setup.",
            }
        )
        return payload

    if refined_breakout_confirmation_triggered(row):
        payload.update(
            {
                "strategy_id": "breakout-confirmation-triggered",
                "strategy_name": "Breakout Confirmation",
                "basis_type": "Setup family",
                "sleeve": "Single-name sleeve",
                "action_label": "Buy now",
                "horizon": "1-3 weeks",
                "entry_label": "Buy while above",
                "entry_value": f"${breakout_trigger:.0f}",
                "stop_label": "Exit if close <",
                "stop_value": f"${max(ma20 - atr, 0):.0f}",
                "target_label": "First target",
                "target_value": f"${(close + 1.5 * atr):.0f}",
                "strategy_rationale": "Strategy 1 v2 only promotes triggered breakouts when the market is supportive and the sector confirms. This keeps broad or unsupported breakouts in research/watch mode instead of treating them as live buys.",
                "observed_reason": "Price closed above the prior 20-day high with supportive market regime, confirmed sector context, intact trend, positive relative strength, and acceptable ATR risk.",
            }
        )
        return payload

    if (
        regime in {"Risk-on", "Selective risk-on"}
        and sector_ok
        and close > ma20 > ma50
        and rs_20d > 0.04
        and rs_60d > 0
        and svs_20d > 0
        and svs_60d >= 0
        and dist_high <= 0.12
        and 0.02 <= extension <= 0.06
        and row["atr_pct"] <= 0.05
    ):
        payload.update(
            {
                "strategy_id": "strong-stock-constructive-pullback",
                "strategy_name": "Constructive pullback continuation",
                "basis_type": "Setup family",
                "sleeve": "Single-name sleeve",
                "action_label": "Buy on pullback",
                "horizon": "1-3 weeks",
                "entry_label": "Only buy near",
                "entry_value": f"${max(ma20, close - 0.5 * atr):.0f}",
                "stop_label": "Exit if close <",
                "stop_value": f"${stop:.0f}",
                "target_label": "Take profit near",
                "target_value": f"${target:.0f}",
                "strategy_rationale": "Treat pullback as an entry method for continuation, not a standalone edge. Buy only when the stock is strong, the sector is also leading, and the reset is controlled rather than damaged.",
                "observed_reason": "Trend is intact, the sector is supportive, and the stock remains stronger than both the market and its group while pulling back in a controlled way.",
            }
        )
        return payload

    if (
        regime in {"Risk-on", "Selective risk-on"}
        and close > ma20 > ma50
        and rs_20d > 0.05
        and rs_60d > 0
        and extension > 0.06
        and extension <= 0.12
    ):
        payload.update(
            {
                "strategy_id": "extended-strength-wait",
                "strategy_name": "Extended strength, wait for pullback",
                "basis_type": "Setup family",
                "sleeve": "Single-name sleeve",
                "action_label": "Wait for pullback",
                "horizon": "Wait this week",
                "entry_label": "Only buy near",
                "entry_value": f"${ma20:.0f}",
                "stop_label": "Cancel if close <",
                "stop_value": f"${(ma20 - atr):.0f}",
                "target_label": "If trend resets",
                "target_value": f"${(close + atr):.0f}",
                "strategy_rationale": "A strong stock can still be a bad immediate buy if the entry is too extended above support, even in a supportive tape.",
                "observed_reason": "The stock is acting well, but it has already run far enough above the 20-day average that patience matters more than enthusiasm.",
            }
        )
        return payload

    if (
        refined_breakout_confirmation_watch(row)
    ):
        payload.update(
            {
                "strategy_id": "wait-for-confirmation",
                "strategy_name": "Breakout Confirmation",
                "basis_type": "Setup family",
                "sleeve": "Single-name sleeve",
                "action_label": "Wait for confirmation",
                "horizon": "Wait this week",
                "entry_label": "Only buy above",
                "entry_value": f"${breakout_trigger:.0f}",
                "stop_label": "Cancel if close <",
                "stop_value": f"${(ma20 - atr):.0f}",
                "target_label": "If breakout sticks",
                "target_value": f"${(breakout_trigger + 1.2 * atr):.0f}",
                "strategy_rationale": "Breakouts should be treated as continuation with proof. Strategy 1 v2 is not live until price closes above the prior 20-day high in a supportive, sector-confirmed context.",
                "observed_reason": "Trend, market regime, sector context, relative strength, and risk are acceptable, but price has not yet triggered the breakout entry.",
            }
        )
        return payload

    if close > ma20 and rs_20d > -0.02:
        payload.update(
            {
                "strategy_id": "trend-hold",
                "strategy_name": "Trend hold / monitor",
                "basis_type": "Decision basis",
                "sleeve": "Single-name sleeve",
                "action_label": "Hold",
                "horizon": "1-2 weeks",
                "entry_label": "Keep only if close >",
                "entry_value": f"${max(ma20 - 0.5 * atr, 0):.0f}",
                "stop_label": "Do not add",
                "stop_value": "Yet",
                "target_label": "Need first",
                "target_value": "Cleaner catalyst",
                "strategy_rationale": "The stock is still functioning, but the timing case for fresh money is not strong enough yet.",
                "observed_reason": "Price is above near-term support, though the edge for a new position remains modest.",
            }
        )
        return payload

    return payload


def apply_current_strategy(latest: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in latest.iterrows():
        payload = strategy_payload(row, include_event_overlay=True)
        merged = {**row.to_dict(), **payload}
        rows.append(merged)
    df = pd.DataFrame(rows)
    df["action_rank"] = df["action_label"].map(
        {
            "Buy now": 0,
            "Buy on pullback": 1,
            "Wait for pullback": 2,
            "Wait for confirmation": 3,
            "Hold": 4,
            "Hold / reassess after earnings": 5,
            "No action": 6,
            "Benchmark reference": 7,
        }
    )
    return df


def run_backtest(features: pd.DataFrame, watchlist: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    eligible = features.merge(watchlist[["ticker", "sector", "is_benchmark"]], on="ticker", how="left")
    eligible = eligible[eligible["ticker"] != "SPY"].copy()
    trading_dates = sorted(eligible["date"].drop_duplicates())
    fridays = [d for d in trading_dates if d.weekday() == 4]
    rows = []
    stock_weeks = []
    for dt in fridays:
        day = eligible[eligible["date"] == dt].copy()
        if day.empty:
            continue
        idx = trading_dates.index(dt)
        future_dt = trading_dates[idx + 5] if idx + 5 < len(trading_dates) else None
        if future_dt is None:
            continue
        future = eligible[eligible["date"] == future_dt][["ticker", "close"]].rename(columns={"close": "future_close"})
        day = day.merge(future, on="ticker", how="inner")
        day["fwd_1w_return"] = day["future_close"] / day["close"] - 1
        strategy_rows = []
        for _, row in day.iterrows():
            payload = strategy_payload(row, include_event_overlay=False)
            merged = {**row.to_dict(), **payload}
            strategy_rows.append(merged)
        scored = pd.DataFrame(strategy_rows)
        scored["action_rank"] = scored["action_label"].map(
            {
                "Buy now": 0,
                "Buy on pullback": 1,
                "Wait for pullback": 2,
                "Wait for confirmation": 3,
                "Hold": 4,
                "No action": 5,
            }
        ).fillna(5)
        top = (
            scored[scored["action_label"].isin(["Buy now", "Buy on pullback"])]
            .sort_values(["action_rank", "refined_score", "rs_20d"], ascending=[True, False, False])
            .head(2)
        )
        if top.empty:
            continue
        spy_now = features[(features["ticker"] == "SPY") & (features["date"] == dt)]["close"].iloc[0]
        spy_future = features[(features["ticker"] == "SPY") & (features["date"] == future_dt)]["close"].iloc[0]
        spy_ret = spy_future / spy_now - 1
        rows.append(
            {
                "signal_date": dt.date().isoformat(),
                "holding_end_date": future_dt.date().isoformat(),
                "selected_tickers": ",".join(top["ticker"].tolist()),
                "selected_strategies": ",".join(top["strategy_id"].tolist()),
                "portfolio_return_1w": top["fwd_1w_return"].mean(),
                "spy_return_1w": spy_ret,
                "excess_return_1w": top["fwd_1w_return"].mean() - spy_ret,
            }
        )
        stock_weeks.append(
            scored[
                [
                    "ticker",
                    "date",
                    "strategy_id",
                    "strategy_name",
                    "action_label",
                    "refined_score",
                    "fwd_1w_return",
                ]
            ].copy()
        )

    portfolio = pd.DataFrame(rows)
    stock_week = pd.concat(stock_weeks, ignore_index=True) if stock_weeks else pd.DataFrame()
    bucket_summary = (
        stock_week.groupby("action_label")
        .agg(
            observations=("fwd_1w_return", "count"),
            avg_fwd_1w_return=("fwd_1w_return", "mean"),
            win_rate=("fwd_1w_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values("avg_fwd_1w_return", ascending=False)
    )
    strategy_summary = (
        stock_week.groupby(["strategy_id", "strategy_name"])
        .agg(
            observations=("fwd_1w_return", "count"),
            avg_fwd_1w_return=("fwd_1w_return", "mean"),
            win_rate=("fwd_1w_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values("avg_fwd_1w_return", ascending=False)
    )
    return portfolio, bucket_summary, strategy_summary, stock_week


def write_markdown_report(
    report_path: Path,
    latest: pd.DataFrame,
    portfolio: pd.DataFrame,
    action_buckets: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> None:
    latest = latest.sort_values(["action_rank", "refined_score"], ascending=[True, False])
    top_portfolio_avg = portfolio["portfolio_return_1w"].mean() if not portfolio.empty else np.nan
    top_excess_avg = portfolio["excess_return_1w"].mean() if not portfolio.empty else np.nan
    win_rate = (portfolio["portfolio_return_1w"] > 0).mean() if not portfolio.empty else np.nan

    lines = [
        "# MLP Weekly Report",
        "",
        f"Generated from CSV-based analysis for `{latest['date'].max().date().isoformat()}`.",
        "",
        "## Current Weekly Calls",
        "",
        "| Ticker | Strategy | Action | Horizon | Entry | Stop | Target |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, row in latest.iterrows():
        lines.append(
            f"| {row['ticker']} | {row['strategy_name']} | {row['action_label']} | {row['horizon']} | {row['entry_value']} | {row['stop_value']} | {row['target_value']} |"
        )

    lines += [
        "",
        "## Why These Calls Are More Trustworthy",
        "",
        "- Recommendations now come from explicit strategy families instead of one generic score, so `buy now` and `wait for confirmation` are no longer the same idea with different adjectives.",
        "- The model now penalizes names that are too extended above the 20-day average instead of automatically pushing the strongest recent movers to the top.",
        "- Entry zone, invalidation, target, and explanation all come from the same setup family instead of being stitched together after the fact.",
        "",
        "## Simple Backtest Readout",
        "",
        f"- Average 1-week return from holding the top 2 eligible ideas each Friday: `{top_portfolio_avg:.2%}`",
        f"- Average excess return vs `SPY`: `{top_excess_avg:.2%}`",
        f"- Weekly win rate of the top-2 portfolio: `{win_rate:.1%}`",
        "",
        "## Backtest by Action Label",
        "",
        "| Action | Observations | Avg 1W Return | Win Rate |",
        "|---|---:|---:|---:|",
    ]
    for _, row in action_buckets.iterrows():
        lines.append(
            f"| {row['action_label']} | {int(row['observations'])} | {row['avg_fwd_1w_return']:.2%} | {row['win_rate']:.1%} |"
        )

    lines += [
        "",
        "## Backtest by Strategy Family",
        "",
        "| Strategy | Observations | Avg 1W Return | Win Rate |",
        "|---|---:|---:|---:|",
    ]
    for _, row in strategy_summary.iterrows():
        lines.append(
            f"| {row['strategy_name']} | {int(row['observations'])} | {row['avg_fwd_1w_return']:.2%} | {row['win_rate']:.1%} |"
        )

    lines += [
        "",
        "## Important Limitation",
        "",
        "- Historical backtests in this MLP are still mostly technical because we do not yet have point-in-time historical earnings calendars, transcript changes, or revision history. That means the strategy family replay is useful for direction, but not yet a production-grade validation of event-aware logic.",
    ]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    prices = pd.read_csv(args.prices)
    earnings = pd.read_csv(args.earnings)
    watchlist = pd.read_csv(args.watchlist)
    prices = prices.merge(watchlist[["ticker", "sector", "is_benchmark"]], on="ticker", how="left")

    features = add_features(prices)
    latest_date = features["date"].max()
    latest = features[features["date"] == latest_date].copy()
    latest = with_earnings_flags(latest, earnings)
    latest = apply_current_strategy(latest)

    portfolio, action_buckets, strategy_summary, stock_week = run_backtest(features, watchlist)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    latest.to_csv(outdir / "mlp_current_recommendations.csv", index=False)
    portfolio.to_csv(outdir / "mlp_backtest_portfolio.csv", index=False)
    action_buckets.to_csv(outdir / "mlp_backtest_actions.csv", index=False)
    strategy_summary.to_csv(outdir / "mlp_backtest_strategies.csv", index=False)
    stock_week.to_csv(outdir / "mlp_backtest_stock_signals.csv", index=False)

    write_markdown_report(Path(args.report), latest, portfolio, action_buckets, strategy_summary)

    print(f"Wrote current recommendations to {outdir / 'mlp_current_recommendations.csv'}")
    print(f"Wrote backtest portfolio summary to {outdir / 'mlp_backtest_portfolio.csv'}")
    print(f"Wrote strategy summary to {outdir / 'mlp_backtest_strategies.csv'}")


if __name__ == "__main__":
    main()
