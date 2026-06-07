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

BENCHMARK_TICKER = "SPY"
FRICTION_BPS = 20
TOP_N = 5
MIN_SAMPLE_SIZE = 100
HOLDING_WINDOWS = (5, 10, 15)
SUPPORTIVE_REGIMES = ("Risk-on", "Selective risk-on")
STRESS_REGIMES = ("Defensive", "Neutral")


@dataclass(frozen=True)
class MeanReversionVariant:
    variant_id: str
    display_name: str
    rule_summary: list[str]
    regime_scope: str
    ret_5d_max: float = -0.06
    extension_min: float = -0.10
    extension_max: float = -0.02
    ma50_proximity_min: float = 0.97
    atr_pct_max: float = 0.07
    require_up_close: bool = True
    require_ma50_reclaim: bool = False
    require_ma20_reclaim: bool = False
    require_sector_confirmed: bool = False
    require_spy_below_ma50: bool = False
    require_ma_stack_not_broken: bool = False
    max_20d_drawdown: float | None = None


VARIANTS = [
    MeanReversionVariant(
        variant_id="v1_baseline_current",
        display_name="Current v1 Oversold Rebound",
        regime_scope="all",
        rule_summary=[
            "current v1 rule",
            "first up-close after 5D return <= -6%",
            "extension vs 20DMA between -10% and -2%",
            "close >= 97% of 50DMA",
            "ATR percent <= 7%",
        ],
    ),
    MeanReversionVariant(
        variant_id="defensive_v1",
        display_name="Defensive v1 Oversold Rebound",
        regime_scope="defensive",
        rule_summary=[
            "current v1 rule",
            "regime must be Defensive",
        ],
    ),
    MeanReversionVariant(
        variant_id="stress_v1",
        display_name="Stress-Regime v1 Oversold Rebound",
        regime_scope="stress",
        rule_summary=[
            "current v1 rule",
            "regime must be Defensive or Neutral",
        ],
    ),
    MeanReversionVariant(
        variant_id="defensive_moderate_band_near_50dma",
        display_name="Defensive Moderate Oversold Near 50DMA",
        regime_scope="defensive",
        extension_min=-0.05,
        extension_max=-0.02,
        ma50_proximity_min=0.99,
        atr_pct_max=0.055,
        require_ma_stack_not_broken=True,
        max_20d_drawdown=0.12,
        rule_summary=[
            "Defensive regime only",
            "5D return <= -6%",
            "extension vs 20DMA between -5% and -2%",
            "close >= 99% of 50DMA",
            "20DMA not materially below 50DMA",
            "ATR percent <= 5.5%",
            "20D drawdown capped at 12%",
        ],
    ),
    MeanReversionVariant(
        variant_id="defensive_deep_band_near_50dma",
        display_name="Defensive Deep Oversold Near 50DMA",
        regime_scope="defensive",
        extension_min=-0.08,
        extension_max=-0.05,
        ma50_proximity_min=0.97,
        atr_pct_max=0.06,
        require_ma_stack_not_broken=True,
        max_20d_drawdown=0.15,
        rule_summary=[
            "Defensive regime only",
            "5D return <= -6%",
            "extension vs 20DMA between -8% and -5%",
            "close >= 97% of 50DMA",
            "20DMA not materially below 50DMA",
            "ATR percent <= 6%",
            "20D drawdown capped at 15%",
        ],
    ),
    MeanReversionVariant(
        variant_id="stress_moderate_reclaim_50dma",
        display_name="Stress Moderate Band + 50DMA Reclaim",
        regime_scope="stress",
        extension_min=-0.05,
        extension_max=-0.02,
        ma50_proximity_min=0.97,
        atr_pct_max=0.055,
        require_ma50_reclaim=True,
        require_ma_stack_not_broken=True,
        max_20d_drawdown=0.12,
        rule_summary=[
            "Defensive or Neutral regime",
            "5D return <= -6%",
            "extension vs 20DMA between -5% and -2%",
            "close reclaims 50DMA after prior close below it",
            "20DMA not materially below 50DMA",
            "ATR percent <= 5.5%",
        ],
    ),
    MeanReversionVariant(
        variant_id="stress_moderate_sector_confirmed",
        display_name="Stress Moderate Band + Sector Confirmed",
        regime_scope="stress",
        extension_min=-0.05,
        extension_max=-0.02,
        ma50_proximity_min=0.99,
        atr_pct_max=0.055,
        require_sector_confirmed=True,
        require_ma_stack_not_broken=True,
        max_20d_drawdown=0.12,
        rule_summary=[
            "Defensive or Neutral regime",
            "5D return <= -6%",
            "extension vs 20DMA between -5% and -2%",
            "close >= 99% of 50DMA",
            "sector ETF must be above 20DMA and 50DMA",
            "ATR percent <= 5.5%",
        ],
    ),
    MeanReversionVariant(
        variant_id="defensive_spy_below_ma50_reclaim_20dma",
        display_name="Defensive SPY Stress + 20DMA Reclaim",
        regime_scope="defensive",
        extension_min=-0.08,
        extension_max=0.01,
        ma50_proximity_min=0.97,
        atr_pct_max=0.06,
        require_spy_below_ma50=True,
        require_ma20_reclaim=True,
        require_ma_stack_not_broken=True,
        max_20d_drawdown=0.15,
        rule_summary=[
            "Defensive regime with SPY below 50DMA",
            "5D return <= -6%",
            "prior close below 20DMA and current close reclaims 20DMA",
            "close >= 97% of 50DMA",
            "ATR percent <= 6%",
        ],
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refine and validate Selective Mean Reversion variants."
    )
    parser.add_argument("--watchlist", default="data/reference/sp100_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/sp100_5y/mlp_prices.csv")
    parser.add_argument("--outdir", default="data/processed")
    parser.add_argument(
        "--version-label",
        default=f"{date.today().isoformat()}_selective_mean_reversion_v1_refinement",
    )
    return parser.parse_args()


def classify_rebound_quality(features: pd.DataFrame) -> pd.Series:
    close_near_50dma = features["close"] >= 0.97 * features["ma_50"]
    ma_stack_intact = features["ma_20"] >= 0.98 * features["ma_50"]
    controlled_damage = features["pullback_from_high_20"].le(0.15) & features["ret_20d"].ge(-0.12)
    sector_or_relative_support = (
        features["sector_confirmation"].eq("Confirmed") | features["rs_20d"].ge(-0.03)
    )
    damaged = (
        (features["close"] < 0.95 * features["ma_50"])
        | (features["ma_20"] < 0.95 * features["ma_50"])
        | (features["pullback_from_high_20"] > 0.20)
        | (features["ret_20d"] < -0.18)
    )
    labels = np.select(
        [
            close_near_50dma & ma_stack_intact & controlled_damage & sector_or_relative_support,
            damaged,
        ],
        ["true_rebound_candidate", "damaged_trend_or_broad_dip"],
        default="ambiguous_rebound",
    )
    return pd.Series(labels, index=features.index)


def build_variant_signals(features: pd.DataFrame, variant: MeanReversionVariant) -> pd.DataFrame:
    condition = (
        ~features["ticker"].isin(ETF_TICKERS)
        & features["prev_close"].notna()
        & (features["ret_5d"] <= variant.ret_5d_max)
        & features["extension_vs_ma20"].between(variant.extension_min, variant.extension_max)
        & (features["close"] >= variant.ma50_proximity_min * features["ma_50"])
        & (features["atr_pct"] <= variant.atr_pct_max)
        & features["signal_sample_ready"]
    )
    if variant.require_up_close:
        condition &= features["close"] > features["prev_close"]
    if variant.regime_scope == "defensive":
        condition &= features["regime"].eq("Defensive")
    elif variant.regime_scope == "stress":
        condition &= features["regime"].isin(STRESS_REGIMES)
    elif variant.regime_scope == "supportive":
        condition &= features["regime"].isin(SUPPORTIVE_REGIMES)
    elif variant.regime_scope != "all":
        raise ValueError(f"Unsupported regime scope: {variant.regime_scope}")
    if variant.require_ma50_reclaim:
        condition &= (features["prev_close"] < features["ma_50"]) & (features["close"] >= features["ma_50"])
    if variant.require_ma20_reclaim:
        condition &= (features["prev_close"] < features["ma_20"]) & (features["close"] >= features["ma_20"])
    if variant.require_sector_confirmed:
        condition &= features["sector_confirmation"].eq("Confirmed")
    if variant.require_spy_below_ma50:
        condition &= features["spy_above_ma50"].eq(0)
    if variant.require_ma_stack_not_broken:
        condition &= features["ma_20"] >= 0.98 * features["ma_50"]
    if variant.max_20d_drawdown is not None:
        condition &= features["pullback_from_high_20"] <= variant.max_20d_drawdown

    starts = signal_starts(condition, features["ticker"])
    rows = features.loc[starts].copy()
    rows["variant_id"] = variant.variant_id
    rows["variant_name"] = variant.display_name
    rows["rebound_quality"] = classify_rebound_quality(rows)
    rows["score"] = (
        -rows["extension_vs_ma20"].fillna(0)
        - rows["atr_pct"].fillna(0)
        + rows["stock_vs_sector_20d"].fillna(0)
        + rows["rs_20d"].fillna(0) * 0.5
        - rows["pullback_from_high_20"].fillna(0) * 0.25
    )
    return rows


def summarize_signal_level(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame()
    grouped = signals.groupby(["variant_id", "variant_name"], dropna=False)
    return (
        grouped.agg(
            sample_size=("ticker", "count"),
            avg_fwd_5d_return=("fwd_5d_return", "mean"),
            avg_fwd_10d_return=("fwd_10d_return", "mean"),
            avg_fwd_15d_return=("fwd_15d_return", "mean"),
            avg_excess_5d_return=("excess_5d_return", "mean"),
            avg_excess_10d_return=("excess_10d_return", "mean"),
            avg_excess_15d_return=("excess_15d_return", "mean"),
            win_rate_5d=("fwd_5d_return", lambda s: (s > 0).mean()),
            win_rate_10d=("fwd_10d_return", lambda s: (s > 0).mean()),
            win_rate_15d=("fwd_15d_return", lambda s: (s > 0).mean()),
            true_rebound_share=("rebound_quality", lambda s: (s == "true_rebound_candidate").mean()),
            damaged_or_broad_dip_share=(
                "rebound_quality",
                lambda s: (s == "damaged_trend_or_broad_dip").mean(),
            ),
            defensive_share=("regime", lambda s: (s == "Defensive").mean()),
            stress_share=("regime", lambda s: s.isin(STRESS_REGIMES).mean()),
            sector_confirmed_share=("sector_confirmation", lambda s: (s == "Confirmed").mean()),
        )
        .reset_index()
        .sort_values(["avg_excess_10d_return", "avg_excess_15d_return"], ascending=[False, False])
    )


def weekly_portfolio_trades(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame()
    signals = signals.sort_values(["date", "score"], ascending=[True, False]).copy()
    signals["review_week"] = signals["date"].dt.to_period("W-FRI").dt.end_time.dt.normalize()
    weekly = []
    for (variant_id, review_week), bucket in signals.groupby(["variant_id", "review_week"]):
        picked = bucket.sort_values("score", ascending=False).head(TOP_N).copy()
        picked["review_week"] = review_week
        picked["portfolio_weight"] = 1.0 / len(picked)
        weekly.append(picked)
    trades = pd.concat(weekly, ignore_index=True)
    friction = FRICTION_BPS / 10_000
    for holding_days in HOLDING_WINDOWS:
        trades[f"trade_return_{holding_days}d_net"] = trades[f"fwd_{holding_days}d_return"] - friction
        trades[f"spy_trade_return_{holding_days}d_net"] = (
            trades[f"spy_fwd_{holding_days}d_return"] - friction
        )
        trades[f"trade_excess_{holding_days}d_net"] = (
            trades[f"trade_return_{holding_days}d_net"] - trades[f"spy_trade_return_{holding_days}d_net"]
        )
    return trades


def portfolio_period_returns(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    rows = []
    for holding_days in HOLDING_WINDOWS:
        holding_weeks = max(holding_days / 5, 1)
        periods = (
            trades.groupby(["variant_id", "variant_name", "review_week"], dropna=False)
            .agg(
                trade_return_net=(f"trade_return_{holding_days}d_net", "mean"),
                spy_trade_return_net=(f"spy_trade_return_{holding_days}d_net", "mean"),
                trade_count=("ticker", "count"),
            )
            .reset_index()
            .sort_values(["variant_id", "review_week"])
        )
        periods["holding_days"] = holding_days
        periods["strategy_return_net"] = periods["trade_return_net"] / holding_weeks
        periods["spy_exposure_return_net"] = periods["spy_trade_return_net"] / holding_weeks
        rows.append(periods)
    return pd.concat(rows, ignore_index=True)


def equity_curve(periods: pd.DataFrame, return_col: str) -> pd.DataFrame:
    curve = periods[["variant_id", "variant_name", "holding_days", "review_week", return_col]].copy()
    curve = curve.rename(columns={return_col: "period_return"})
    group_cols = [curve["variant_id"], curve["holding_days"]]
    curve["equity"] = (1 + curve["period_return"]).groupby(group_cols).cumprod()
    curve["peak"] = curve.groupby(["variant_id", "holding_days"])["equity"].cummax()
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
    trading_dates = pd.Series(features["date"].drop_duplicates().sort_values())
    weeks_in_replay = sum(dt.weekday() == 4 for dt in trading_dates)
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
    for (variant_id, variant_name, holding_days), bucket in periods.groupby(
        ["variant_id", "variant_name", "holding_days"]
    ):
        strat_returns = bucket["strategy_return_net"]
        spy_returns = bucket["spy_exposure_return_net"]
        active_weeks = len(bucket)
        strat_curve = strategy_curve.loc[
            (strategy_curve["variant_id"] == variant_id)
            & (strategy_curve["holding_days"] == holding_days)
        ]
        spy_exp_curve = spy_exposure_curve.loc[
            (spy_exposure_curve["variant_id"] == variant_id)
            & (spy_exposure_curve["holding_days"] == holding_days)
        ]
        excess = strat_returns - spy_returns
        rows.append(
            {
                "variant_id": variant_id,
                "variant_name": variant_name,
                "holding_days": holding_days,
                "active_weeks": active_weeks,
                "active_share": active_weeks / weeks_in_replay,
                "total_trades": int(bucket["trade_count"].sum()),
                "avg_trades_per_active_week": bucket["trade_count"].mean(),
                "strategy_ann_return_net": annualized_return(strat_returns, weeks_in_replay),
                "spy_exposure_ann_return_net": annualized_return(spy_returns, weeks_in_replay),
                "ann_excess_vs_spy_exposure_net": annualized_return(strat_returns, weeks_in_replay)
                - annualized_return(spy_returns, weeks_in_replay),
                "spy_buy_hold_ann_return": spy_buy_hold_ann,
                "ann_excess_vs_spy_buy_hold": annualized_return(strat_returns, weeks_in_replay)
                - spy_buy_hold_ann,
                "strategy_max_drawdown": strat_curve["drawdown"].min(),
                "spy_exposure_max_drawdown": spy_exp_curve["drawdown"].min(),
                "spy_buy_hold_max_drawdown": spy_drawdown,
                "avg_week_return_net": strat_returns.mean(),
                "avg_week_exposure_spy_net": spy_returns.mean(),
                "avg_week_excess_net": excess.mean(),
                "win_rate_week": (strat_returns > 0).mean(),
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
        ["ann_excess_vs_spy_buy_hold", "ann_excess_vs_spy_exposure_net"],
        ascending=[False, False],
    )


def summarize_by_dimension(signals: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame()
    return (
        signals.groupby(["variant_id", "variant_name", dimension], dropna=False)
        .agg(
            sample_size=("ticker", "count"),
            avg_fwd_5d_return=("fwd_5d_return", "mean"),
            avg_fwd_10d_return=("fwd_10d_return", "mean"),
            avg_fwd_15d_return=("fwd_15d_return", "mean"),
            avg_excess_5d_return=("excess_5d_return", "mean"),
            avg_excess_10d_return=("excess_10d_return", "mean"),
            avg_excess_15d_return=("excess_15d_return", "mean"),
            win_rate_10d=("fwd_10d_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values(["variant_id", "sample_size"], ascending=[True, False])
    )


def summarize_by_year(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame()
    dated = signals.copy()
    dated["year"] = dated["date"].dt.year
    return summarize_by_dimension(dated, "year")


def promotion_decisions(
    signal_summary: pd.DataFrame,
    portfolio_summary: pd.DataFrame,
    regime_summary: pd.DataFrame,
    sector_summary: pd.DataFrame,
    ticker_summary: pd.DataFrame,
    year_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    signal_by_variant = signal_summary.set_index("variant_id") if not signal_summary.empty else pd.DataFrame()
    variant_lookup = {variant.variant_id: variant for variant in VARIANTS}
    for _, port in portfolio_summary.iterrows():
        variant_id = port["variant_id"]
        if variant_id not in signal_by_variant.index:
            continue
        sig = signal_by_variant.loc[variant_id]
        variant_regimes = regime_summary.loc[regime_summary["variant_id"] == variant_id]
        variant_sectors = sector_summary.loc[sector_summary["variant_id"] == variant_id]
        variant_tickers = ticker_summary.loc[ticker_summary["variant_id"] == variant_id]
        variant_years = year_summary.loc[year_summary["variant_id"] == variant_id]
        largest_regime_share = variant_regimes["sample_size"].max() / sig["sample_size"]
        largest_sector_share = variant_sectors["sample_size"].max() / sig["sample_size"]
        largest_ticker_share = variant_tickers["sample_size"].max() / sig["sample_size"]
        largest_year_share = variant_years["sample_size"].max() / sig["sample_size"]
        clears_main_bar = bool(
            sig["sample_size"] >= MIN_SAMPLE_SIZE
            and port["holding_days"] in (10, 15)
            and port["ann_excess_vs_spy_buy_hold"] >= 0.03
            and port["ann_excess_vs_spy_exposure_net"] > 0
            and port["strategy_max_drawdown"] >= port["spy_buy_hold_max_drawdown"] - 0.02
            and port["information_like_week"] > 0
            and sig["damaged_or_broad_dip_share"] <= 0.10
            and largest_sector_share < 0.45
            and largest_ticker_share < 0.10
            and largest_year_share < 0.40
        )
        narrow_but_trackable = bool(
            not clears_main_bar
            and sig["sample_size"] >= 50
            and port["ann_excess_vs_spy_buy_hold"] >= -0.03
            and port["ann_excess_vs_spy_exposure_net"] > 0
            and port["information_like_week"] > 0
            and sig["damaged_or_broad_dip_share"] <= 0.15
            and largest_ticker_share < 0.15
            and largest_year_share < 0.40
        )
        if clears_main_bar:
            decision = "promotable_main_board"
        elif narrow_but_trackable:
            decision = "paper_live_candidate"
        else:
            decision = "research_only"
        rows.append(
            {
                "variant_id": variant_id,
                "variant_name": port["variant_name"],
                "holding_days": int(port["holding_days"]),
                "decision": decision,
                "sample_size": int(sig["sample_size"]),
                "active_weeks": int(port["active_weeks"]),
                "ann_excess_vs_spy_buy_hold": port["ann_excess_vs_spy_buy_hold"],
                "ann_excess_vs_spy_exposure_net": port["ann_excess_vs_spy_exposure_net"],
                "strategy_ann_return_net": port["strategy_ann_return_net"],
                "spy_buy_hold_ann_return": port["spy_buy_hold_ann_return"],
                "strategy_max_drawdown": port["strategy_max_drawdown"],
                "spy_buy_hold_max_drawdown": port["spy_buy_hold_max_drawdown"],
                "information_like_week": port["information_like_week"],
                "true_rebound_share": sig["true_rebound_share"],
                "damaged_or_broad_dip_share": sig["damaged_or_broad_dip_share"],
                "largest_regime_share": largest_regime_share,
                "largest_sector_share": largest_sector_share,
                "largest_ticker_share": largest_ticker_share,
                "largest_year_share": largest_year_share,
                "rule_summary": " | ".join(variant_lookup[variant_id].rule_summary),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["decision", "ann_excess_vs_spy_buy_hold", "ann_excess_vs_spy_exposure_net"],
        ascending=[True, False, False],
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
    year_summary = summarize_by_year(signals)
    quality_summary = summarize_by_dimension(signals, "rebound_quality")
    oversold_band_summary = summarize_by_dimension(signals, "oversold_extension_band")
    decisions = promotion_decisions(
        signal_summary,
        portfolio_summary,
        regime_summary,
        sector_summary,
        ticker_summary,
        year_summary,
    )

    outdir = Path(args.outdir) / f"selective_mean_reversion_refinement_{args.version_label}"
    outdir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "mean_reversion_variant_signals.csv": signals,
        "mean_reversion_signal_summary.csv": signal_summary,
        "mean_reversion_weekly_trades.csv": trades,
        "mean_reversion_weekly_period_returns.csv": periods,
        "mean_reversion_portfolio_summary.csv": portfolio_summary,
        "mean_reversion_regime_summary.csv": regime_summary,
        "mean_reversion_sector_summary.csv": sector_summary,
        "mean_reversion_ticker_summary.csv": ticker_summary,
        "mean_reversion_year_summary.csv": year_summary,
        "mean_reversion_quality_summary.csv": quality_summary,
        "mean_reversion_oversold_band_summary.csv": oversold_band_summary,
        "mean_reversion_promotion_decisions.csv": decisions,
    }
    for filename, frame in outputs.items():
        frame.to_csv(outdir / filename, index=False)

    manifest = {
        "version_label": args.version_label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "universe": "S&P 100 + ETFs",
        "source_watchlist": args.watchlist,
        "source_prices": args.prices,
        "strategy": "Selective Mean Reversion",
        "holding_windows": list(HOLDING_WINDOWS),
        "weekly_top_n": TOP_N,
        "round_trip_friction_bps": FRICTION_BPS,
        "minimum_sample_size": MIN_SAMPLE_SIZE,
        "daily_ohlcv_only": True,
        "variants": [
            {
                "variant_id": variant.variant_id,
                "display_name": variant.display_name,
                "rule_summary": variant.rule_summary,
            }
            for variant in VARIANTS
        ],
    }
    (outdir / "mean_reversion_refinement_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote Selective Mean Reversion refinement outputs to {outdir}")


if __name__ == "__main__":
    main()
