#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from packages.core.canonical_strategy_replay import (
    ETF_TICKERS,
    prepare_replay_features,
    signal_starts,
)

HOLDING_DAYS = 15
HOLDING_WEEKS = 3
FRICTION_BPS = 20
TOP_N = 5
MIN_SAMPLE_SIZE = 150
BENCHMARK_TICKER = "SPY"


@dataclass(frozen=True)
class PullbackVariant:
    variant_id: str
    display_name: str
    rule_summary: list[str]
    action_role: str = "live_buy_pullback"
    pullback_min: float = 0.02
    pullback_max: float = 0.15
    extension_min: float = -0.03
    extension_max: float = 0.06
    rs_10d_min: float | None = None
    rs_20d_min: float = 0.02
    rs_60d_min: float = 0.0
    stock_vs_sector_20d_min: float | None = None
    stock_vs_sector_60d_min: float | None = None
    atr_pct_max: float = 0.06
    distance_from_52w_high_max: float | None = None
    days_above_ma20_15_min: float | None = None
    close_vs_ma20_min: float | None = None
    require_supportive_regime: bool = False
    require_risk_on: bool = False
    require_sector_confirmed: bool = False


VARIANTS = [
    PullbackVariant(
        variant_id="baseline_current_v1",
        display_name="Current v1 Pullback",
        rule_summary=[
            "current canonical pullback rule",
            "pullback from prior 20D high between 2% and 15%",
            "extension vs 20DMA between -3% and +6%",
            "no explicit regime or sector-confirmation gate",
        ],
    ),
    PullbackVariant(
        variant_id="supportive_confirmed_controlled",
        display_name="Supportive + Confirmed Controlled Pullback",
        rule_summary=[
            "current trend and RS spine",
            "regime must be Risk-on or Selective risk-on",
            "sector must be confirmed",
            "pullback depth 3% to 10%",
            "extension vs 20DMA -2% to +4%",
            "stock must outperform sector over 20D",
            "ATR percent <= 5.5%",
        ],
        pullback_min=0.03,
        pullback_max=0.10,
        extension_min=-0.02,
        extension_max=0.04,
        stock_vs_sector_20d_min=0.0,
        atr_pct_max=0.055,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="risk_on_confirmed_controlled",
        display_name="Risk-On + Confirmed Controlled Pullback",
        rule_summary=[
            "controlled confirmed pullback",
            "regime must be Risk-on",
        ],
        pullback_min=0.03,
        pullback_max=0.10,
        extension_min=-0.02,
        extension_max=0.04,
        stock_vs_sector_20d_min=0.0,
        atr_pct_max=0.055,
        require_risk_on=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="shallow_confirmed_reset",
        display_name="Shallow Confirmed Reset",
        rule_summary=[
            "supportive sector-confirmed pullback",
            "pullback depth 0% to 6%",
            "extension vs 20DMA 0% to +6%",
            "keeps very shallow resets separate from true pullbacks",
        ],
        pullback_min=0.0,
        pullback_max=0.06,
        extension_min=0.0,
        extension_max=0.06,
        stock_vs_sector_20d_min=0.0,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="mid_depth_low_extension",
        display_name="Mid-Depth Low-Extension Pullback",
        rule_summary=[
            "supportive sector-confirmed pullback",
            "pullback depth 3% to 6%",
            "extension vs 20DMA 0% to +4%",
            "ATR percent <= 5.5%",
        ],
        pullback_min=0.03,
        pullback_max=0.06,
        extension_min=0.0,
        extension_max=0.04,
        stock_vs_sector_20d_min=0.0,
        atr_pct_max=0.055,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="deeper_controlled_confirmed",
        display_name="Deeper Controlled Confirmed Pullback",
        rule_summary=[
            "supportive sector-confirmed pullback",
            "pullback depth 6% to 10%",
            "extension vs 20DMA -2% to +4%",
            "tests whether non-deep but larger resets are useful",
        ],
        pullback_min=0.06,
        pullback_max=0.10,
        extension_min=-0.02,
        extension_max=0.04,
        stock_vs_sector_20d_min=0.0,
        atr_pct_max=0.055,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="strict_rs_support_proximity",
        display_name="Strict RS + Support-Proximity Pullback",
        rule_summary=[
            "supportive sector-confirmed controlled pullback",
            "RS 10D >= -1%, RS 20D >= 3%, RS 60D >= 2%",
            "stock outperformed sector over 20D and 60D",
            "close at least 99% of 20DMA",
            "ATR percent <= 5%",
            "within 12% of 52-week high",
        ],
        pullback_min=0.03,
        pullback_max=0.10,
        extension_min=-0.01,
        extension_max=0.03,
        rs_10d_min=-0.01,
        rs_20d_min=0.03,
        rs_60d_min=0.02,
        stock_vs_sector_20d_min=0.0,
        stock_vs_sector_60d_min=0.0,
        atr_pct_max=0.05,
        distance_from_52w_high_max=0.12,
        close_vs_ma20_min=0.99,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
    PullbackVariant(
        variant_id="watch_only_extended_strength",
        display_name="Watch-Only Extended Strength",
        action_role="watch_only",
        rule_summary=[
            "supportive sector-confirmed leadership",
            "extension vs 20DMA above +6% through +12%",
            "not a live pullback entry; should stay Wait for pullback",
        ],
        pullback_min=0.0,
        pullback_max=0.06,
        extension_min=0.06,
        extension_max=0.12,
        rs_20d_min=0.05,
        stock_vs_sector_20d_min=0.0,
        atr_pct_max=0.06,
        require_supportive_regime=True,
        require_sector_confirmed=True,
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refine and validate Strategy 2 / Sector-Confirmed Pullback Continuation variants."
    )
    parser.add_argument("--watchlist", default="data/reference/sp100_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/sp100_5y/mlp_prices.csv")
    parser.add_argument("--outdir", default="data/processed")
    parser.add_argument("--version-label", default=f"{date.today().isoformat()}_strategy2_v1")
    return parser.parse_args()


def build_variant_signals(features: pd.DataFrame, variant: PullbackVariant) -> pd.DataFrame:
    condition = (
        ~features["ticker"].isin(ETF_TICKERS)
        & (features["close"] > features["ma_50"])
        & (features["ma_20"] > features["ma_50"])
        & (features["rs_20d"] >= variant.rs_20d_min)
        & (features["rs_60d"] >= variant.rs_60d_min)
        & (features["ret_20d"] > 0.0)
        & features["pullback_from_high_20"].between(variant.pullback_min, variant.pullback_max)
        & features["extension_vs_ma20"].between(variant.extension_min, variant.extension_max)
        & (features["atr_pct"] <= variant.atr_pct_max)
        & features["signal_sample_ready"]
    )
    if variant.rs_10d_min is not None:
        condition &= features["rs_10d"] >= variant.rs_10d_min
    if variant.stock_vs_sector_20d_min is not None:
        condition &= features["stock_vs_sector_20d"] >= variant.stock_vs_sector_20d_min
    if variant.stock_vs_sector_60d_min is not None:
        condition &= features["stock_vs_sector_60d"] >= variant.stock_vs_sector_60d_min
    if variant.distance_from_52w_high_max is not None:
        condition &= features["distance_from_52w_high"] <= variant.distance_from_52w_high_max
    if variant.days_above_ma20_15_min is not None:
        condition &= features["days_above_ma20_15"] >= variant.days_above_ma20_15_min
    if variant.close_vs_ma20_min is not None:
        condition &= features["close"] >= variant.close_vs_ma20_min * features["ma_20"]
    if variant.require_supportive_regime:
        condition &= features["regime_supportive"]
    if variant.require_risk_on:
        condition &= features["regime"].eq("Risk-on")
    if variant.require_sector_confirmed:
        condition &= features["sector_confirmation"].eq("Confirmed")

    starts = signal_starts(condition, features["ticker"])
    rows = features.loc[starts].copy()
    rows["variant_id"] = variant.variant_id
    rows["variant_name"] = variant.display_name
    rows["action_role"] = variant.action_role
    support_distance = rows["extension_vs_ma20"].abs()
    rows["support_proximity_score"] = -support_distance.fillna(1)
    rows["score"] = (
        rows["rs_20d"].fillna(0) * 2.0
        + rows["rs_60d"].fillna(0)
        + rows["stock_vs_sector_20d"].fillna(0)
        - rows["atr_pct"].fillna(0)
        - support_distance.fillna(0) * 0.5
        - rows["pullback_from_high_20"].clip(lower=0).fillna(0) * 0.25
    )
    return rows


def summarize_signal_level(signals: pd.DataFrame) -> pd.DataFrame:
    grouped = signals.groupby(["variant_id", "variant_name", "action_role"], dropna=False)
    return (
        grouped.agg(
            sample_size=("ticker", "count"),
            avg_fwd_5d_return=("fwd_5d_return", "mean"),
            avg_fwd_10d_return=("fwd_10d_return", "mean"),
            avg_fwd_15d_return=("fwd_15d_return", "mean"),
            avg_excess_5d_return=("excess_5d_return", "mean"),
            avg_excess_10d_return=("excess_10d_return", "mean"),
            avg_excess_15d_return=("excess_15d_return", "mean"),
            win_rate_15d=("fwd_15d_return", lambda s: (s > 0).mean()),
            supportive_regime_share=("regime_supportive", "mean"),
            sector_confirmed_share=("sector_confirmation", lambda s: (s == "Confirmed").mean()),
            avg_pullback_from_high_20=("pullback_from_high_20", "mean"),
            avg_extension_vs_ma20=("extension_vs_ma20", "mean"),
            avg_atr_pct=("atr_pct", "mean"),
        )
        .reset_index()
        .sort_values(["avg_excess_15d_return", "sample_size"], ascending=[False, False])
    )


def weekly_portfolio_trades(signals: pd.DataFrame) -> pd.DataFrame:
    live = signals.loc[signals["action_role"] == "live_buy_pullback"].copy()
    if live.empty:
        return pd.DataFrame()
    live = live.sort_values(["date", "score"], ascending=[True, False]).copy()
    live["review_week"] = live["date"].dt.to_period("W-FRI").dt.end_time.dt.normalize()
    weekly = []
    for (variant_id, review_week), bucket in live.groupby(["variant_id", "review_week"]):
        picked = bucket.sort_values("score", ascending=False).head(TOP_N).copy()
        picked["review_week"] = review_week
        picked["portfolio_weight"] = 1.0 / len(picked)
        weekly.append(picked)
    trades = pd.concat(weekly, ignore_index=True)
    friction = FRICTION_BPS / 10_000
    trades["trade_return_net"] = trades[f"fwd_{HOLDING_DAYS}d_return"] - friction
    trades["spy_trade_return_net"] = trades[f"spy_fwd_{HOLDING_DAYS}d_return"] - friction
    trades["trade_excess_net"] = trades["trade_return_net"] - trades["spy_trade_return_net"]
    return trades


def portfolio_period_returns(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    periods = (
        trades.groupby(["variant_id", "variant_name", "review_week"], dropna=False)
        .agg(
            gross_return=("fwd_15d_return", "mean"),
            trade_return_net=("trade_return_net", "mean"),
            spy_trade_return_net=("spy_trade_return_net", "mean"),
            trade_count=("ticker", "count"),
        )
        .reset_index()
        .sort_values(["variant_id", "review_week"])
    )
    periods["strategy_return_net"] = periods["trade_return_net"] / HOLDING_WEEKS
    periods["spy_exposure_return_net"] = periods["spy_trade_return_net"] / HOLDING_WEEKS
    return periods


def equity_curve(periods: pd.DataFrame, return_col: str) -> pd.DataFrame:
    curve = periods[["variant_id", "variant_name", "review_week", return_col]].copy()
    curve = curve.rename(columns={return_col: "period_return"})
    curve["equity"] = (1 + curve["period_return"]).groupby(curve["variant_id"]).cumprod()
    curve["peak"] = curve.groupby("variant_id")["equity"].cummax()
    curve["drawdown"] = curve["equity"] / curve["peak"] - 1
    return curve


def annualized_return(period_returns: pd.Series, weeks_in_replay: int) -> float:
    if period_returns.empty or weeks_in_replay <= 0:
        return np.nan
    terminal = float((1 + period_returns).prod())
    return terminal ** (52 / weeks_in_replay) - 1


def summarize_portfolio(periods: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    if periods.empty:
        return pd.DataFrame()
    all_weeks = pd.Series(features["date"].drop_duplicates().sort_values())
    all_fridays = [dt for dt in all_weeks if dt.weekday() == 4]
    weeks_in_replay = len(all_fridays)

    strategy_curve = equity_curve(periods, "strategy_return_net")
    spy_exposure_curve = equity_curve(periods, "spy_exposure_return_net")
    spy_prices = (
        features.loc[features["ticker"] == BENCHMARK_TICKER, ["date", "close"]]
        .dropna()
        .sort_values("date")
    )
    spy_buy_hold_return = spy_prices["close"].iloc[-1] / spy_prices["close"].iloc[0] - 1
    spy_buy_hold_ann = (1 + spy_buy_hold_return) ** (252 / len(spy_prices)) - 1
    spy_drawdown = (spy_prices["close"] / spy_prices["close"].cummax() - 1).min()

    rows = []
    for (variant_id, variant_name), bucket in periods.groupby(["variant_id", "variant_name"]):
        strat_returns = bucket["strategy_return_net"]
        spy_returns = bucket["spy_exposure_return_net"]
        active_weeks = len(bucket)
        strat_ann = annualized_return(strat_returns, weeks_in_replay)
        spy_exp_ann = annualized_return(spy_returns, weeks_in_replay)
        strat_curve = strategy_curve.loc[strategy_curve["variant_id"] == variant_id]
        spy_exp_curve = spy_exposure_curve.loc[spy_exposure_curve["variant_id"] == variant_id]
        excess = strat_returns - spy_returns
        rows.append(
            {
                "variant_id": variant_id,
                "variant_name": variant_name,
                "active_weeks": active_weeks,
                "active_share": active_weeks / weeks_in_replay,
                "total_trades": int(bucket["trade_count"].sum()),
                "avg_trades_per_active_week": bucket["trade_count"].mean(),
                "strategy_ann_return_net": strat_ann,
                "spy_exposure_ann_return_net": spy_exp_ann,
                "ann_excess_vs_spy_exposure_net": strat_ann - spy_exp_ann,
                "spy_buy_hold_ann_return": spy_buy_hold_ann,
                "ann_excess_vs_spy_buy_hold": strat_ann - spy_buy_hold_ann,
                "strategy_max_drawdown": strat_curve["drawdown"].min(),
                "spy_exposure_max_drawdown": spy_exp_curve["drawdown"].min(),
                "spy_buy_hold_max_drawdown": spy_drawdown,
                "avg_week_return_net": strat_returns.mean(),
                "avg_week_exposure_spy_net": spy_returns.mean(),
                "avg_week_excess_net": excess.mean(),
                "win_rate_week": (strat_returns > 0).mean(),
                "exposure_spy_win_rate_week": (spy_returns > 0).mean(),
                "excess_win_rate_week": (excess > 0).mean(),
                "return_vol_week": strat_returns.std(ddof=0),
                "excess_vol_week": excess.std(ddof=0),
                "sharpe_like_week": strat_returns.mean() / strat_returns.std(ddof=0)
                if strat_returns.std(ddof=0) > 0
                else np.nan,
                "information_like_week": excess.mean() / excess.std(ddof=0)
                if excess.std(ddof=0) > 0
                else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["ann_excess_vs_spy_exposure_net", "strategy_ann_return_net"],
        ascending=[False, False],
    )


def summarize_by_dimension(signals: pd.DataFrame, dimension: str) -> pd.DataFrame:
    return (
        signals.groupby(["variant_id", "variant_name", "action_role", dimension], dropna=False)
        .agg(
            sample_size=("ticker", "count"),
            avg_fwd_15d_return=("fwd_15d_return", "mean"),
            avg_excess_15d_return=("excess_15d_return", "mean"),
            win_rate_15d=("fwd_15d_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values(["variant_id", "sample_size"], ascending=[True, False])
    )


def promotion_decisions(
    signal_summary: pd.DataFrame,
    portfolio_summary: pd.DataFrame,
    regime_summary: pd.DataFrame,
    sector_summary: pd.DataFrame,
    ticker_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    signal_by_variant = signal_summary.set_index("variant_id")
    portfolio_by_variant = portfolio_summary.set_index("variant_id")
    baseline_info = portfolio_by_variant.loc["baseline_current_v1", "information_like_week"]
    for variant in VARIANTS:
        if variant.action_role != "live_buy_pullback":
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "variant_name": variant.display_name,
                    "decision": "watch_only",
                    "rule_summary": " | ".join(variant.rule_summary),
                }
            )
            continue
        if variant.variant_id not in signal_by_variant.index or variant.variant_id not in portfolio_by_variant.index:
            continue
        sig = signal_by_variant.loc[variant.variant_id]
        port = portfolio_by_variant.loc[variant.variant_id]
        variant_regimes = regime_summary.loc[regime_summary["variant_id"] == variant.variant_id]
        variant_sectors = sector_summary.loc[sector_summary["variant_id"] == variant.variant_id]
        variant_tickers = ticker_summary.loc[ticker_summary["variant_id"] == variant.variant_id]
        largest_regime_share = variant_regimes["sample_size"].max() / sig["sample_size"]
        largest_sector_share = variant_sectors["sample_size"].max() / sig["sample_size"]
        largest_ticker_share = variant_tickers["sample_size"].max() / sig["sample_size"]
        clears_promotion_bar = bool(
            sig["sample_size"] >= MIN_SAMPLE_SIZE
            and port["ann_excess_vs_spy_buy_hold"] >= 0.03
            and port["ann_excess_vs_spy_exposure_net"] > 0
            and port["strategy_max_drawdown"] >= port["spy_buy_hold_max_drawdown"] - 0.02
            and port["information_like_week"] > baseline_info
            and port["information_like_week"] > 0
            and largest_regime_share < 0.85
            and largest_sector_share < 0.45
            and largest_ticker_share < 0.08
        )
        decision = "active_current" if variant.variant_id == "baseline_current_v1" else (
            "promotable" if clears_promotion_bar else "research_only"
        )
        rows.append(
            {
                "variant_id": variant.variant_id,
                "variant_name": variant.display_name,
                "decision": decision,
                "sample_size": int(sig["sample_size"]),
                "ann_excess_vs_spy_buy_hold": port["ann_excess_vs_spy_buy_hold"],
                "ann_excess_vs_spy_exposure_net": port["ann_excess_vs_spy_exposure_net"],
                "strategy_ann_return_net": port["strategy_ann_return_net"],
                "strategy_max_drawdown": port["strategy_max_drawdown"],
                "spy_buy_hold_max_drawdown": port["spy_buy_hold_max_drawdown"],
                "information_like_week": port["information_like_week"],
                "baseline_current_v1_information_like_week": baseline_info,
                "largest_regime_share": largest_regime_share,
                "largest_sector_share": largest_sector_share,
                "largest_ticker_share": largest_ticker_share,
                "rule_summary": " | ".join(variant.rule_summary),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["decision", "ann_excess_vs_spy_exposure_net"], ascending=[True, False], na_position="last"
    )


def main() -> None:
    args = parse_args()
    prices = pd.read_csv(args.prices)
    watchlist = pd.read_csv(args.watchlist)
    features = prepare_replay_features(prices, watchlist)

    signals = pd.concat(
        [build_variant_signals(features, variant) for variant in VARIANTS],
        ignore_index=True,
    )
    signal_summary = summarize_signal_level(signals)
    trades = weekly_portfolio_trades(signals)
    periods = portfolio_period_returns(trades)
    portfolio_summary = summarize_portfolio(periods, features)
    regime_summary = summarize_by_dimension(signals, "regime")
    sector_summary = summarize_by_dimension(signals, "sector")
    ticker_summary = summarize_by_dimension(signals, "ticker")
    depth_extension_summary = summarize_by_dimension(signals, "pullback_depth_band")
    extension_summary = summarize_by_dimension(signals, "extension_band")
    decisions = promotion_decisions(
        signal_summary,
        portfolio_summary,
        regime_summary,
        sector_summary,
        ticker_summary,
    )

    outdir = Path(args.outdir) / f"strategy2_pullback_refinement_{args.version_label}"
    outdir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "strategy2_variant_signals.csv": signals,
        "strategy2_signal_summary.csv": signal_summary,
        "strategy2_weekly_trades.csv": trades,
        "strategy2_weekly_period_returns.csv": periods,
        "strategy2_portfolio_summary.csv": portfolio_summary,
        "strategy2_regime_summary.csv": regime_summary,
        "strategy2_sector_summary.csv": sector_summary,
        "strategy2_ticker_summary.csv": ticker_summary,
        "strategy2_pullback_depth_summary.csv": depth_extension_summary,
        "strategy2_extension_summary.csv": extension_summary,
        "strategy2_promotion_decisions.csv": decisions,
    }
    for filename, frame in outputs.items():
        frame.to_csv(outdir / filename, index=False)

    manifest = {
        "version_label": args.version_label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "universe": "S&P 100 + ETFs",
        "source_watchlist": args.watchlist,
        "source_prices": args.prices,
        "strategy": "Strategy 2 / Sector-Confirmed Pullback Continuation",
        "holding_days": HOLDING_DAYS,
        "weekly_top_n": TOP_N,
        "round_trip_friction_bps": FRICTION_BPS,
        "minimum_sample_size": MIN_SAMPLE_SIZE,
        "variants": [
            {
                "variant_id": variant.variant_id,
                "display_name": variant.display_name,
                "action_role": variant.action_role,
                "rule_summary": variant.rule_summary,
            }
            for variant in VARIANTS
        ],
    }
    (outdir / "strategy2_refinement_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote Strategy 2 refinement outputs to {outdir}")


if __name__ == "__main__":
    main()
