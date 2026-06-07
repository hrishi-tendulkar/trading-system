#!/usr/bin/env python3
# ruff: noqa: E402, I001, UP017

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
    BROAD_ETF_TICKERS,
    ETF_TICKERS,
    SECTOR_ETF_TICKERS,
    prepare_replay_features,
)


BENCHMARK_TICKER = "SPY"
HOLDING_DAYS = 5
FRICTION_BPS = 20
FRICTION_SENSITIVITY_BPS = (10, 20, 40)
MIN_ACTIVE_WEEKS = 80


@dataclass(frozen=True)
class EtfRotationVariant:
    variant_id: str
    display_name: str
    rule_summary: list[str]
    top_n: int
    universe_scope: str
    require_supportive_regime: bool = True
    require_risk_on: bool = False
    require_positive_rs_20d: bool = False
    require_positive_rs_60d: bool = False
    rs_20d_min: float = 0.0
    rs_60d_min: float = 0.0
    atr_pct_max: float = 0.04
    rank_rs_10d_weight: float = 0.5
    rank_rs_20d_weight: float = 1.0
    rank_rs_60d_weight: float = 0.75
    rank_ret_20d_weight: float = 0.25
    rank_vol_penalty_weight: float = 0.5


VARIANTS = [
    EtfRotationVariant(
        variant_id="top1_all_supportive_balanced",
        display_name="Top 1 All ETFs / Supportive Balanced RS",
        top_n=1,
        universe_scope="all",
        require_positive_rs_20d=False,
        require_positive_rs_60d=False,
        rule_summary=[
            "weekly Friday selection from SPY, QQQ, and sector ETFs",
            "regime must be Risk-on or Selective risk-on",
            "close > 20DMA > 50DMA with positive 20DMA slope",
            "rank by 10D/20D/60D relative strength plus 20D return, penalize volatility",
            "hold one week; pick top 1",
        ],
    ),
    EtfRotationVariant(
        variant_id="top2_all_supportive_balanced",
        display_name="Top 2 All ETFs / Supportive Balanced RS",
        top_n=2,
        universe_scope="all",
        require_positive_rs_20d=False,
        require_positive_rs_60d=False,
        rule_summary=[
            "weekly Friday selection from SPY, QQQ, and sector ETFs",
            "same balanced RS rule as top 1",
            "hold one week; equal-weight top 2",
        ],
    ),
    EtfRotationVariant(
        variant_id="top1_all_supportive_strict_rs",
        display_name="Top 1 All ETFs / Supportive Strict RS",
        top_n=1,
        universe_scope="all",
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
        rs_60d_min=0.0,
        rule_summary=[
            "weekly Friday selection from SPY, QQQ, and sector ETFs",
            "supportive regime and trend gate",
            "RS 20D must exceed SPY by at least 1%; RS 60D must be positive",
            "hold one week; pick top 1",
        ],
    ),
    EtfRotationVariant(
        variant_id="top2_all_supportive_strict_rs",
        display_name="Top 2 All ETFs / Supportive Strict RS",
        top_n=2,
        universe_scope="all",
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
        rs_60d_min=0.0,
        rule_summary=[
            "weekly Friday selection from SPY, QQQ, and sector ETFs",
            "same strict RS rule as top 1",
            "hold one week; equal-weight top 2",
        ],
    ),
    EtfRotationVariant(
        variant_id="top1_sector_supportive_strict_rs",
        display_name="Top 1 Sector ETFs / Supportive Strict RS",
        top_n=1,
        universe_scope="sector",
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
        rs_60d_min=0.0,
        rule_summary=[
            "weekly Friday selection from sector ETFs only",
            "supportive regime and trend gate",
            "RS 20D must exceed SPY by at least 1%; RS 60D must be positive",
            "hold one week; pick top 1",
        ],
    ),
    EtfRotationVariant(
        variant_id="top2_sector_supportive_strict_rs",
        display_name="Top 2 Sector ETFs / Supportive Strict RS",
        top_n=2,
        universe_scope="sector",
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
        rs_60d_min=0.0,
        rule_summary=[
            "weekly Friday selection from sector ETFs only",
            "same strict RS rule as sector top 1",
            "hold one week; equal-weight top 2",
        ],
    ),
    EtfRotationVariant(
        variant_id="top1_broad_supportive_trend",
        display_name="Top 1 Broad ETFs / Supportive Trend",
        top_n=1,
        universe_scope="broad",
        require_positive_rs_20d=False,
        require_positive_rs_60d=False,
        rule_summary=[
            "weekly Friday selection from SPY and QQQ only",
            "supportive regime and trend gate",
            "rank by balanced RS and momentum",
            "hold one week; pick top 1",
        ],
    ),
    EtfRotationVariant(
        variant_id="top1_all_risk_on_strict_rs",
        display_name="Top 1 All ETFs / Risk-on Strict RS",
        top_n=1,
        universe_scope="all",
        require_risk_on=True,
        require_positive_rs_20d=True,
        require_positive_rs_60d=True,
        rs_20d_min=0.01,
        rs_60d_min=0.0,
        rule_summary=[
            "weekly Friday selection from SPY, QQQ, and sector ETFs",
            "regime must be Risk-on, not merely Selective risk-on",
            "strict RS and trend gates",
            "hold one week; pick top 1",
        ],
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refine and validate ranked weekly ETF Trend / Rotation variants."
    )
    parser.add_argument("--watchlist", default="data/reference/sp100_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/sp100_5y/mlp_prices.csv")
    parser.add_argument("--outdir", default="data/processed")
    parser.add_argument("--version-label", default=f"{date.today().isoformat()}_etf_v2_research")
    return parser.parse_args()


def etf_universe_for_variant(variant: EtfRotationVariant) -> tuple[str, ...]:
    if variant.universe_scope == "all":
        return ETF_TICKERS
    if variant.universe_scope == "sector":
        return SECTOR_ETF_TICKERS
    if variant.universe_scope == "broad":
        return BROAD_ETF_TICKERS
    raise ValueError(f"Unknown ETF universe scope: {variant.universe_scope}")


def weekly_decision_rows(features: pd.DataFrame) -> pd.DataFrame:
    etfs = features.loc[
        features["ticker"].isin(ETF_TICKERS) & features["signal_sample_ready"]
    ].copy()
    etfs["review_week"] = etfs["date"].dt.to_period("W-FRI").dt.end_time.dt.normalize()
    last_dates = etfs.groupby("review_week")["date"].transform("max")
    return etfs.loc[etfs["date"].eq(last_dates)].copy()


def build_variant_candidates(features: pd.DataFrame, variant: EtfRotationVariant) -> pd.DataFrame:
    universe = etf_universe_for_variant(variant)
    rows = weekly_decision_rows(features)
    condition = (
        rows["ticker"].isin(universe)
        & (rows["close"] > rows["ma_20"])
        & (rows["ma_20"] > rows["ma_50"])
        & (rows["ma_20_slope_5d"] > 0)
        & (rows["atr_pct"] <= variant.atr_pct_max)
    )
    if variant.require_supportive_regime:
        condition &= rows["regime_supportive"]
    if variant.require_risk_on:
        condition &= rows["regime"].eq("Risk-on")
    if variant.require_positive_rs_20d:
        condition &= rows["rs_20d"] >= variant.rs_20d_min
    if variant.require_positive_rs_60d:
        condition &= rows["rs_60d"] >= variant.rs_60d_min

    candidates = rows.loc[condition].copy()
    candidates["variant_id"] = variant.variant_id
    candidates["variant_name"] = variant.display_name
    candidates["top_n"] = variant.top_n
    candidates["rank_score"] = (
        candidates["rs_10d"].fillna(0) * variant.rank_rs_10d_weight
        + candidates["rs_20d"].fillna(0) * variant.rank_rs_20d_weight
        + candidates["rs_60d"].fillna(0) * variant.rank_rs_60d_weight
        + candidates["ret_20d"].fillna(0) * variant.rank_ret_20d_weight
        - candidates["atr_pct"].fillna(0) * variant.rank_vol_penalty_weight
    )
    return candidates


def weekly_trades(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    picks = []
    for (variant_id, review_week), bucket in candidates.groupby(["variant_id", "review_week"]):
        top_n = int(bucket["top_n"].iloc[0])
        picked = bucket.sort_values(["rank_score", "rs_20d", "rs_60d"], ascending=False).head(top_n)
        picked = picked.copy()
        picked["portfolio_weight"] = 1.0 / len(picked)
        picks.append(picked)
    trades = pd.concat(picks, ignore_index=True).sort_values(
        ["variant_id", "review_week", "rank_score"]
    )
    return apply_friction(trades, FRICTION_BPS)


def apply_friction(trades: pd.DataFrame, friction_bps: int) -> pd.DataFrame:
    trades = trades.copy()
    friction = friction_bps / 10_000
    trades["friction_bps"] = friction_bps
    trades["trade_return_net"] = trades[f"fwd_{HOLDING_DAYS}d_return"] - friction
    trades["spy_trade_return_net"] = trades[f"spy_fwd_{HOLDING_DAYS}d_return"] - friction
    trades["trade_excess_net"] = trades["trade_return_net"] - trades["spy_trade_return_net"]
    return trades


def portfolio_period_returns(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    return (
        trades.groupby(["variant_id", "variant_name", "review_week"], dropna=False)
        .agg(
            gross_return=(f"fwd_{HOLDING_DAYS}d_return", "mean"),
            strategy_return_net=("trade_return_net", "mean"),
            spy_exposure_return_net=("spy_trade_return_net", "mean"),
            trade_count=("ticker", "count"),
        )
        .reset_index()
        .sort_values(["variant_id", "review_week"])
    )


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


def spy_buy_hold_stats(features: pd.DataFrame) -> tuple[float, float]:
    spy_prices = (
        features.loc[features["ticker"] == BENCHMARK_TICKER, ["date", "close"]]
        .dropna()
        .sort_values("date")
    )
    spy_buy_hold_return = spy_prices["close"].iloc[-1] / spy_prices["close"].iloc[0] - 1
    spy_buy_hold_ann = (1 + spy_buy_hold_return) ** (252 / len(spy_prices)) - 1
    spy_drawdown = (spy_prices["close"] / spy_prices["close"].cummax() - 1).min()
    return spy_buy_hold_ann, spy_drawdown


def summarize_portfolio(
    periods: pd.DataFrame, trades: pd.DataFrame, features: pd.DataFrame
) -> pd.DataFrame:
    if periods.empty:
        return pd.DataFrame()
    all_weeks = pd.Series(features["date"].drop_duplicates().sort_values())
    all_fridays = [dt for dt in all_weeks if dt.weekday() == 4]
    weeks_in_replay = len(all_fridays)
    spy_buy_hold_ann, spy_drawdown = spy_buy_hold_stats(features)
    strategy_curve = equity_curve(periods, "strategy_return_net")
    spy_exposure_curve = equity_curve(periods, "spy_exposure_return_net")
    rows = []
    for (variant_id, variant_name), bucket in periods.groupby(["variant_id", "variant_name"]):
        variant_trades = trades.loc[trades["variant_id"] == variant_id]
        strat_returns = bucket["strategy_return_net"]
        spy_returns = bucket["spy_exposure_return_net"]
        excess = strat_returns - spy_returns
        active_weeks = len(bucket)
        ticker_counts = variant_trades["ticker"].value_counts(normalize=True)
        regime_counts = variant_trades["regime"].value_counts(normalize=True)
        etf_subgroup_counts = variant_trades["etf_subgroup"].value_counts(normalize=True)
        rows.append(
            {
                "variant_id": variant_id,
                "variant_name": variant_name,
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
                "strategy_max_drawdown": strategy_curve.loc[
                    strategy_curve["variant_id"] == variant_id, "drawdown"
                ].min(),
                "spy_exposure_max_drawdown": spy_exposure_curve.loc[
                    spy_exposure_curve["variant_id"] == variant_id, "drawdown"
                ].min(),
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
                "largest_ticker_share": ticker_counts.iloc[0]
                if not ticker_counts.empty
                else np.nan,
                "largest_regime_share": regime_counts.iloc[0]
                if not regime_counts.empty
                else np.nan,
                "largest_etf_subgroup_share": etf_subgroup_counts.iloc[0]
                if not etf_subgroup_counts.empty
                else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["ann_excess_vs_spy_buy_hold", "ann_excess_vs_spy_exposure_net"],
        ascending=[False, False],
    )


def summarize_signal_level(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    return (
        candidates.groupby(["variant_id", "variant_name"], dropna=False)
        .agg(
            candidate_count=("ticker", "count"),
            candidate_weeks=("review_week", "nunique"),
            avg_candidate_rank_score=("rank_score", "mean"),
            avg_candidate_5d_return=(f"fwd_{HOLDING_DAYS}d_return", "mean"),
            avg_candidate_5d_excess=("excess_5d_return", "mean"),
            candidate_win_rate_5d=(f"fwd_{HOLDING_DAYS}d_return", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values(["avg_candidate_5d_excess", "candidate_count"], ascending=[False, False])
    )


def summarize_by_dimension(trades: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    return (
        trades.groupby(["variant_id", "variant_name", dimension], dropna=False)
        .agg(
            trade_count=("ticker", "count"),
            avg_5d_return_net=("trade_return_net", "mean"),
            avg_5d_excess_net=("trade_excess_net", "mean"),
            win_rate_5d=("trade_return_net", lambda s: (s > 0).mean()),
        )
        .reset_index()
        .sort_values(["variant_id", "trade_count"], ascending=[True, False])
    )


def friction_sensitivity(trades: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for friction_bps in FRICTION_SENSITIVITY_BPS:
        friction_trades = apply_friction(
            trades.drop(
                columns=[
                    "friction_bps",
                    "trade_return_net",
                    "spy_trade_return_net",
                    "trade_excess_net",
                ],
                errors="ignore",
            ),
            friction_bps,
        )
        periods = portfolio_period_returns(friction_trades)
        summary = summarize_portfolio(periods, friction_trades, features)
        summary["friction_bps"] = friction_bps
        rows.append(summary)
    return pd.concat(rows, ignore_index=True).sort_values(
        ["variant_id", "friction_bps"]
    )


def promotion_decisions(portfolio_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    variants_by_id = {variant.variant_id: variant for variant in VARIANTS}
    for _, port in portfolio_summary.iterrows():
        variant = variants_by_id[port["variant_id"]]
        clears_bar = bool(
            port["active_weeks"] >= MIN_ACTIVE_WEEKS
            and port["ann_excess_vs_spy_buy_hold"] >= 0.03
            and port["ann_excess_vs_spy_exposure_net"] > 0
            and port["strategy_max_drawdown"] >= port["spy_buy_hold_max_drawdown"] - 0.02
            and port["information_like_week"] > 0
            and port["largest_ticker_share"] < 0.45
            and port["largest_regime_share"] < 0.90
        )
        rows.append(
            {
                "variant_id": variant.variant_id,
                "variant_name": variant.display_name,
                "decision": "promotable" if clears_bar else "research_only",
                "active_weeks": int(port["active_weeks"]),
                "strategy_ann_return_net": port["strategy_ann_return_net"],
                "ann_excess_vs_spy_buy_hold": port["ann_excess_vs_spy_buy_hold"],
                "ann_excess_vs_spy_exposure_net": port["ann_excess_vs_spy_exposure_net"],
                "strategy_max_drawdown": port["strategy_max_drawdown"],
                "spy_buy_hold_max_drawdown": port["spy_buy_hold_max_drawdown"],
                "largest_ticker_share": port["largest_ticker_share"],
                "largest_regime_share": port["largest_regime_share"],
                "information_like_week": port["information_like_week"],
                "rule_summary": " | ".join(variant.rule_summary),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["decision", "ann_excess_vs_spy_buy_hold"], ascending=[True, False]
    )


def main() -> None:
    args = parse_args()
    prices = pd.read_csv(args.prices)
    watchlist = pd.read_csv(args.watchlist)
    features = prepare_replay_features(prices, watchlist)

    candidates = pd.concat(
        [build_variant_candidates(features, variant) for variant in VARIANTS],
        ignore_index=True,
    )
    trades = weekly_trades(candidates)
    periods = portfolio_period_returns(trades)
    signal_summary = summarize_signal_level(candidates)
    portfolio_summary = summarize_portfolio(periods, trades, features)
    regime_summary = summarize_by_dimension(trades, "regime")
    ticker_summary = summarize_by_dimension(trades, "ticker")
    subgroup_summary = summarize_by_dimension(trades, "etf_subgroup")
    sensitivity = friction_sensitivity(trades, features)
    decisions = promotion_decisions(portfolio_summary)

    outdir = Path(args.outdir) / f"etf_trend_rotation_refinement_{args.version_label}"
    outdir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "etf_variant_candidates.csv": candidates,
        "etf_weekly_trades.csv": trades,
        "etf_weekly_period_returns.csv": periods,
        "etf_signal_summary.csv": signal_summary,
        "etf_portfolio_summary.csv": portfolio_summary,
        "etf_regime_summary.csv": regime_summary,
        "etf_ticker_summary.csv": ticker_summary,
        "etf_subgroup_summary.csv": subgroup_summary,
        "etf_friction_sensitivity.csv": sensitivity,
        "etf_promotion_decisions.csv": decisions,
    }
    for filename, frame in outputs.items():
        frame.to_csv(outdir / filename, index=False)

    manifest = {
        "version_label": args.version_label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "universe": "S&P 100 + ETFs",
        "source_watchlist": args.watchlist,
        "source_prices": args.prices,
        "strategy": "ETF Trend / Rotation",
        "holding_days": HOLDING_DAYS,
        "base_round_trip_friction_bps": FRICTION_BPS,
        "friction_sensitivity_bps": list(FRICTION_SENSITIVITY_BPS),
        "minimum_active_weeks": MIN_ACTIVE_WEEKS,
        "variants": [
            {
                "variant_id": variant.variant_id,
                "display_name": variant.display_name,
                "top_n": variant.top_n,
                "universe_scope": variant.universe_scope,
                "rule_summary": variant.rule_summary,
            }
            for variant in VARIANTS
        ],
    }
    (outdir / "etf_refinement_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote ETF Trend / Rotation refinement outputs to {outdir}")


if __name__ == "__main__":
    main()
