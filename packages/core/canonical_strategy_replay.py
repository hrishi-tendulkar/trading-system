from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from scripts.mlp.run_watchlist_analysis import add_features, market_regime

BENCHMARK_TICKER = "SPY"
BROAD_ETF_TICKERS = ("SPY", "QQQ")
SECTOR_ETF_TICKERS = ("XLK", "XLF", "XLV", "XLE", "XLI", "XLY")
ETF_TICKERS = BROAD_ETF_TICKERS + SECTOR_ETF_TICKERS
SUPPORTIVE_REGIMES = ("Risk-on", "Selective risk-on")
FORWARD_HORIZONS = (5, 10, 15)

CORE_SIGNAL_COLUMNS = [
    "strategy_id",
    "strategy_name",
    "signal_style",
    "date",
    "ticker",
    "display_name",
    "sector",
    "instrument_type",
    "etf_subgroup",
    "regime",
    "regime_supportive",
    "sector_confirmation",
    "close",
    "ma_20",
    "ma_50",
    "atr_pct",
    "ret_5d",
    "ret_20d",
    "rs_20d",
    "rs_60d",
    "distance_from_52w_high",
    "pullback_from_high_20",
    "pullback_depth_band",
    "extension_vs_ma20",
    "extension_band",
    "prior_high_20",
    "oversold_extension_band",
    "fwd_5d_return",
    "fwd_10d_return",
    "fwd_15d_return",
    "spy_fwd_5d_return",
    "spy_fwd_10d_return",
    "spy_fwd_15d_return",
    "excess_5d_return",
    "excess_10d_return",
    "excess_15d_return",
]


def prepare_replay_features(prices: pd.DataFrame, watchlist: pd.DataFrame) -> pd.DataFrame:
    metadata = watchlist[
        ["ticker", "display_name", "sector", "is_benchmark", "is_active"]
    ].drop_duplicates("ticker")
    base_prices = prices.drop(
        columns=[col for col in ["display_name", "sector", "is_benchmark", "is_active"] if col in prices.columns]
    )
    features = add_features(base_prices.merge(metadata, on="ticker", how="left"))
    features = features.sort_values(["ticker", "date"]).copy()
    features["date"] = pd.to_datetime(features["date"])
    features["regime"] = features.apply(market_regime, axis=1)
    features["regime_supportive"] = features["regime"].isin(SUPPORTIVE_REGIMES)

    grouped = features.groupby("ticker", sort=False)
    for horizon in FORWARD_HORIZONS:
        features[f"fwd_{horizon}d_return"] = grouped["close"].shift(-horizon) / features["close"] - 1

    benchmark = features.loc[
        features["ticker"] == BENCHMARK_TICKER,
        ["date"] + [f"fwd_{horizon}d_return" for horizon in FORWARD_HORIZONS],
    ].rename(
        columns={
            f"fwd_{horizon}d_return": f"spy_fwd_{horizon}d_return"
            for horizon in FORWARD_HORIZONS
        }
    )
    features = features.merge(benchmark, on="date", how="left")
    for horizon in FORWARD_HORIZONS:
        features[f"excess_{horizon}d_return"] = (
            features[f"fwd_{horizon}d_return"] - features[f"spy_fwd_{horizon}d_return"]
        )

    features["instrument_type"] = np.select(
        [
            features["ticker"].isin(BROAD_ETF_TICKERS),
            features["ticker"].isin(SECTOR_ETF_TICKERS),
        ],
        ["Broad ETF", "Sector ETF"],
        default="Single name",
    )
    features["etf_subgroup"] = np.where(
        features["instrument_type"] == "Single name", "Not applicable", features["instrument_type"]
    )
    features["sector_confirmation"] = sector_confirmation_labels(features)

    features["prev_close"] = grouped["close"].shift(1)
    features["prior_high_20"] = grouped["high"].transform(lambda s: s.rolling(20).max().shift(1))
    features["pullback_from_high_20"] = (features["prior_high_20"] - features["close"]) / features[
        "prior_high_20"
    ]
    features["pullback_depth_band"] = bucketize(
        features["pullback_from_high_20"],
        bins=[0.0, 0.03, 0.06, 0.10, 0.15, np.inf],
        labels=["0-3%", "3-6%", "6-10%", "10-15%", "15%+"],
        default_label="Outside tracked band",
    )
    features["extension_band"] = bucketize(
        features["extension_vs_ma20"],
        bins=[-np.inf, -0.02, 0.0, 0.02, 0.04, 0.06, np.inf],
        labels=["<-2%", "-2% to 0%", "0-2%", "2-4%", "4-6%", "6%+"],
        default_label="Unavailable",
    )
    features["oversold_extension_band"] = bucketize(
        features["extension_vs_ma20"],
        bins=[-np.inf, -0.08, -0.05, -0.02, np.inf],
        labels=["<= -8%", "-8% to -5%", "-5% to -2%", "> -2%"],
        default_label="Unavailable",
    )
    features["signal_sample_ready"] = features[
        [f"fwd_{horizon}d_return" for horizon in FORWARD_HORIZONS]
        + [f"excess_{horizon}d_return" for horizon in FORWARD_HORIZONS]
    ].notna().all(axis=1)
    return features


def bucketize(
    series: pd.Series,
    *,
    bins: list[float],
    labels: list[str],
    default_label: str,
) -> pd.Series:
    bucketed = pd.cut(series, bins=bins, labels=labels, include_lowest=True, right=False)
    return bucketed.astype(object).where(bucketed.notna(), default_label)


def sector_confirmation_labels(features: pd.DataFrame) -> pd.Series:
    has_proxy = features["sector_close"].notna() if "sector_close" in features.columns else pd.Series(
        False, index=features.index
    )
    confirmed = features["sector_above_ma20"].eq(1) & features["sector_above_ma50"].eq(1)
    labels = np.select(
        [
            features["instrument_type"] != "Single name",
            ~has_proxy,
            confirmed,
            has_proxy,
        ],
        ["Not applicable", "Unavailable", "Confirmed", "Unconfirmed"],
        default="Unavailable",
    )
    return pd.Series(labels, index=features.index)


def build_strategy_replay_artifacts(features: pd.DataFrame) -> dict[str, pd.DataFrame]:
    signals = pd.concat(
        [
            build_etf_trend_rotation_signals(features),
            build_pullback_continuation_signals(features),
            build_breakout_confirmation_signals(features),
            build_selective_mean_reversion_signals(features),
        ],
        ignore_index=True,
    ).sort_values(["strategy_name", "date", "ticker"])

    strategy_summary = summarize_signals(signals, ["strategy_id", "strategy_name", "signal_style"])
    strategy_summary["supportive_regime_share"] = (
        signals.groupby(["strategy_id", "strategy_name", "signal_style"])["regime_supportive"]
        .mean()
        .to_numpy()
    )
    strategy_summary = strategy_summary.sort_values(
        ["avg_excess_10d_return", "avg_excess_15d_return", "sample_size"],
        ascending=[False, False, False],
    )

    regime_summary = summarize_signals(
        signals,
        ["strategy_id", "strategy_name", "signal_style", "regime"],
    ).sort_values(["strategy_name", "regime"])

    sector_summary = summarize_signals(
        signals,
        ["strategy_id", "strategy_name", "signal_style", "sector"],
    ).sort_values(["strategy_name", "sample_size"], ascending=[True, False])

    etf_summary = summarize_signals(
        signals.loc[signals["strategy_id"] == "etf-trend-rotation"],
        ["strategy_id", "strategy_name", "regime", "etf_subgroup"],
    ).sort_values(["regime", "etf_subgroup"])

    pullback_signals = signals.loc[signals["strategy_id"] == "sector-confirmed-pullback-continuation"]
    pullback_band_summary = summarize_signals(
        pullback_signals,
        ["strategy_id", "strategy_name", "sector_confirmation", "pullback_depth_band", "extension_band"],
    ).sort_values(["sector_confirmation", "pullback_depth_band", "extension_band"])
    pullback_sector_summary = summarize_signals(
        pullback_signals,
        ["strategy_id", "strategy_name", "regime", "sector_confirmation"],
    ).sort_values(["regime", "sector_confirmation"])

    breakout_signals = signals.loc[signals["strategy_id"] == "breakout-confirmation"]
    breakout_context_summary = summarize_signals(
        breakout_signals,
        ["strategy_id", "strategy_name", "regime", "sector_confirmation"],
    ).sort_values(["regime", "sector_confirmation"])

    mean_reversion_signals = signals.loc[signals["strategy_id"] == "selective-mean-reversion"]
    mean_reversion_regime_summary = summarize_signals(
        mean_reversion_signals,
        ["strategy_id", "strategy_name", "regime", "oversold_extension_band"],
    ).sort_values(["regime", "oversold_extension_band"])

    comparison = strategy_summary[
        [
            "strategy_id",
            "strategy_name",
            "signal_style",
            "sample_size",
            "avg_fwd_5d_return",
            "avg_fwd_10d_return",
            "avg_fwd_15d_return",
            "avg_excess_5d_return",
            "avg_excess_10d_return",
            "avg_excess_15d_return",
            "win_rate_5d",
            "win_rate_10d",
            "win_rate_15d",
            "supportive_regime_share",
        ]
    ].copy()

    return {
        "signals": signals,
        "strategy_summary": strategy_summary,
        "regime_summary": regime_summary,
        "sector_summary": sector_summary,
        "etf_rotation_summary": etf_summary,
        "pullback_band_summary": pullback_band_summary,
        "pullback_sector_summary": pullback_sector_summary,
        "breakout_context_summary": breakout_context_summary,
        "mean_reversion_regime_summary": mean_reversion_regime_summary,
        "comparison": comparison,
    }


def build_etf_trend_rotation_signals(features: pd.DataFrame) -> pd.DataFrame:
    condition = (
        features["ticker"].isin(ETF_TICKERS)
        & (features["close"] > features["ma_20"])
        & (features["ma_20"] > features["ma_50"])
        & (features["ma_20_slope_5d"] > 0)
        & (features["rs_20d"] > 0.01)
        & (features["rs_60d"] > 0.0)
        & (features["atr_pct"] <= 0.04)
    )
    return signal_rows(
        features,
        condition,
        strategy_id="etf-trend-rotation",
        strategy_name="ETF Trend / Rotation",
        signal_style="Daily trend entry",
    )


def build_pullback_continuation_signals(features: pd.DataFrame) -> pd.DataFrame:
    condition = (
        ~features["ticker"].isin(ETF_TICKERS)
        & (features["close"] > features["ma_50"])
        & (features["ma_20"] > features["ma_50"])
        & (features["rs_20d"] > 0.02)
        & (features["rs_60d"] > 0.0)
        & (features["ret_20d"] > 0.0)
        & features["pullback_from_high_20"].between(0.02, 0.15)
        & features["extension_vs_ma20"].between(-0.03, 0.06)
        & (features["atr_pct"] <= 0.06)
    )
    return signal_rows(
        features,
        condition,
        strategy_id="sector-confirmed-pullback-continuation",
        strategy_name="Sector-Confirmed Pullback Continuation",
        signal_style="Daily pullback entry",
    )


def build_breakout_confirmation_signals(features: pd.DataFrame) -> pd.DataFrame:
    breakout_trigger = features["close"] > features["prior_high_20"]
    condition = (
        ~features["ticker"].isin(ETF_TICKERS)
        & (features["close"] > features["ma_20"])
        & (features["ma_20"] > features["ma_50"])
        & breakout_trigger
        & (features["rs_20d"] > 0.0)
        & (features["rs_60d"] > 0.0)
        & (features["atr_pct"] <= 0.06)
        & (features["distance_from_52w_high"] <= 0.15)
    )
    return signal_rows(
        features,
        condition,
        strategy_id="breakout-confirmation",
        strategy_name="Breakout Confirmation",
        signal_style="Triggered breakout entry",
    )


def build_selective_mean_reversion_signals(features: pd.DataFrame) -> pd.DataFrame:
    condition = (
        ~features["ticker"].isin(ETF_TICKERS)
        & features["prev_close"].notna()
        & (features["close"] > features["prev_close"])
        & (features["ret_5d"] <= -0.06)
        & features["extension_vs_ma20"].between(-0.10, -0.02)
        & (features["close"] >= 0.97 * features["ma_50"])
        & (features["atr_pct"] <= 0.07)
    )
    return signal_rows(
        features,
        condition,
        strategy_id="selective-mean-reversion",
        strategy_name="Selective Mean Reversion",
        signal_style="Oversold rebound trigger",
    )


def signal_rows(
    features: pd.DataFrame,
    condition: pd.Series,
    *,
    strategy_id: str,
    strategy_name: str,
    signal_style: str,
) -> pd.DataFrame:
    starts = signal_starts(condition, features["ticker"])
    rows = features.loc[starts & features["signal_sample_ready"]].copy()
    rows["strategy_id"] = strategy_id
    rows["strategy_name"] = strategy_name
    rows["signal_style"] = signal_style
    return rows[CORE_SIGNAL_COLUMNS]


def signal_starts(condition: pd.Series, tickers: pd.Series) -> pd.Series:
    normalized = condition.fillna(False).astype(bool)
    prior = normalized.groupby(tickers).shift(1)
    prior = prior.where(prior.notna(), False).astype(bool)
    return normalized & ~prior


def summarize_signals(signals: pd.DataFrame, group_cols: Iterable[str]) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame(columns=list(group_cols) + summary_metric_columns())
    grouped = signals.groupby(list(group_cols), dropna=False)
    summary = grouped.agg(
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
    )
    return summary.reset_index()


def summary_metric_columns() -> list[str]:
    return [
        "sample_size",
        "avg_fwd_5d_return",
        "avg_fwd_10d_return",
        "avg_fwd_15d_return",
        "avg_excess_5d_return",
        "avg_excess_10d_return",
        "avg_excess_15d_return",
        "win_rate_5d",
        "win_rate_10d",
        "win_rate_15d",
    ]
