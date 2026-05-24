#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a tradeable next-week board from current recommendations.")
    parser.add_argument("--recommendations", default="data/processed/sp100_5y_research_aligned_main/mlp_current_recommendations.csv")
    parser.add_argument("--out", default="docs/research/market/tradeable-board-2026-05-24.md")
    return parser.parse_args()


def rank_stock_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["stock_rank_score"] = (
        1.5 * df["rs_20d"].fillna(-999)
        + 0.75 * df["rs_60d"].fillna(-999)
        + 1.0 * df["stock_vs_sector_20d"].fillna(-999)
        + 0.5 * df["stock_vs_sector_60d"].fillna(-999)
        - 0.75 * df["extension_vs_ma20"].fillna(0)
        - 1.0 * df["atr_pct"].fillna(0)
    )
    return df


def main() -> None:
    args = parse_args()
    recs = pd.read_csv(args.recommendations)

    etfs = recs[recs["sleeve"] == "ETF sleeve"].copy()
    etfs = etfs[etfs["action_label"] == "Buy now"].sort_values(["rs_20d", "rs_60d"], ascending=False)

    stocks = recs[recs["sleeve"] == "Single-name sleeve"].copy()
    buy_pullback = rank_stock_rows(stocks[stocks["action_label"] == "Buy on pullback"])
    buy_pullback = buy_pullback.sort_values("stock_rank_score", ascending=False)

    wait_pullback = rank_stock_rows(stocks[stocks["action_label"] == "Wait for pullback"])
    wait_pullback = wait_pullback.sort_values("stock_rank_score", ascending=False)

    waits = rank_stock_rows(stocks[stocks["action_label"] == "Wait for confirmation"])
    waits = waits.sort_values("stock_rank_score", ascending=False)

    top_etfs = etfs.head(2)
    top_pullbacks = buy_pullback.head(3)
    top_wait_pullbacks = wait_pullback.head(3)
    top_waits = waits.head(3)
    attention_frames = [
        top_etfs.assign(attention_rank=10 + top_etfs["rs_20d"].fillna(0)),
        top_pullbacks.assign(attention_rank=8 + top_pullbacks["stock_rank_score"].fillna(-999)),
        top_wait_pullbacks.assign(attention_rank=5 + top_wait_pullbacks["stock_rank_score"].fillna(-999)),
        top_waits.assign(attention_rank=3 + top_waits["stock_rank_score"].fillna(-999)),
    ]
    attention = pd.concat([frame for frame in attention_frames if not frame.empty], ignore_index=True)
    attention = attention.sort_values("attention_rank", ascending=False).head(5)

    lines = [
        "# Tradeable Board",
        "",
        "## Date",
        "",
        str(recs["date"].max())[:10],
        "",
        "## Universe",
        "",
        "`S&P 100 + ETF sleeve`",
        "",
        "## Objective",
        "",
        "Produce a small next-week board that is actually usable in the real market.",
        "",
        "This board separates:",
        "",
        "- `ETF sleeve`: cleaner market or sector exposure",
        "- `Single-name sleeve`: more selective stock entries",
        "",
        "## ETF Sleeve",
        "",
        "| Ticker | Strategy | Action | Entry | Stop | Target | Why it matters |",
        "|---|---|---|---|---|---|---|",
    ]

    for _, row in top_etfs.iterrows():
        lines.append(
            f"| {row['ticker']} | {row['strategy_name']} | {row['action_label']} | {row['entry_value']} | {row['stop_value']} | {row['target_value']} | Stronger group-level trend expression with lower single-name event risk |"
        )

    lines += [
        "",
        "## Single-Name Sleeve: Buy On Pullback",
        "",
        "| Ticker | Strategy | Action | Entry | Stop | Target | Why it matters |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, row in top_pullbacks.iterrows():
        lines.append(
            f"| {row['ticker']} | {row['strategy_name']} | {row['action_label']} | {row['entry_value']} | {row['stop_value']} | {row['target_value']} | Stock remains stronger than market and/or sector while offering a cleaner reset than chase entries |"
        )

    lines += [
        "",
        "## Single-Name Sleeve: Wait For Pullback",
        "",
        "| Ticker | Strategy | Action | Pullback Zone | Cancel Level | Why it matters |",
        "|---|---|---|---|---|---|",
    ]
    for _, row in top_wait_pullbacks.iterrows():
        lines.append(
            f"| {row['ticker']} | {row['strategy_name']} | {row['action_label']} | {row['entry_value']} | {row['stop_value']} | Strong stock, but the current entry is too stretched to justify fresh buying today |"
        )

    lines += [
        "",
        "## Single-Name Sleeve: Wait For Confirmation",
        "",
        "| Ticker | Strategy | Action | Entry Trigger | Stop | Target | Why it matters |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, row in top_waits.iterrows():
        lines.append(
            f"| {row['ticker']} | {row['strategy_name']} | {row['action_label']} | {row['entry_value']} | {row['stop_value']} | {row['target_value']} | Strong candidate, but should prove itself through price before capital is deployed |"
        )

    lines += [
        "",
        "## Practical Read",
        "",
        "- `Buy now` is mostly an ETF decision right now.",
        "- `Buy on pullback` is the main single-name entry style currently supported by the research and replay.",
        "- `Wait for pullback` means the stock is strong, but the current price is too stretched to chase.",
        "- `Wait for confirmation` is not a junk bucket. It is a live watchlist for names that could become actionable soon.",
        "",
        "## Current Top 5 Attention List",
        "",
    ]
    for idx, (_, row) in enumerate(attention.iterrows(), start=1):
        lines.append(f"{idx}. `{row['ticker']}`")

    lines += [
        "",
        "## Operating View",
        "",
        "- The engine is saying `use ETFs for immediate exposure` and `be patient with most single names`.",
        "- A small board is a feature, not a bug. The system should earn selectivity before it earns trust.",
        "",
        "## Important Limits",
        "",
        "- This is still based mostly on daily-price-only research logic.",
        "- The engine is more selective than before, but it is still in `research mode`, not full `live-ready` confidence mode.",
        "- Single-name `Buy now` is still not strong enough to be handed out casually.",
    ]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"Wrote tradeable board to {out}")


if __name__ == "__main__":
    main()
