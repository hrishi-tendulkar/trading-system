#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch daily price history for the MLP watchlist.")
    parser.add_argument(
        "--watchlist",
        default="data/reference/mlp_watchlist.csv",
        help="CSV with at least a ticker column.",
    )
    parser.add_argument("--start", default="2025-05-22", help="Inclusive YYYY-MM-DD start date.")
    parser.add_argument("--end", default="2026-05-23", help="Exclusive YYYY-MM-DD end date.")
    parser.add_argument(
        "--outdir",
        default="data/raw/mlp",
        help="Directory for exported CSV files.",
    )
    return parser.parse_args()


def fetch_earnings_snapshot(tickers: list[str]) -> pd.DataFrame:
    rows = []
    for ticker in tickers:
        cal = yf.Ticker(ticker).calendar
        earnings_date = None
        if isinstance(cal, dict):
            raw_dates = cal.get("Earnings Date") or []
            if raw_dates:
                earnings_date = str(raw_dates[0])
        rows.append({"ticker": ticker, "next_earnings_date": earnings_date})
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    watchlist = pd.read_csv(args.watchlist)
    tickers = watchlist.loc[watchlist["is_active"].fillna(True), "ticker"].tolist()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    raw = yf.download(
        tickers,
        start=args.start,
        end=args.end,
        auto_adjust=False,
        progress=False,
        group_by="ticker",
        threads=True,
    )

    rows = []
    missing = []
    for ticker in tickers:
        if ticker not in raw.columns.get_level_values(0):
            missing.append(ticker)
            continue
        frame = raw[ticker].reset_index()
        frame.columns = [col.lower().replace(" ", "_") for col in frame.columns]
        if frame.empty or frame["close"].dropna().empty:
            missing.append(ticker)
            continue
        frame["ticker"] = ticker
        rows.append(frame)

    for ticker in missing:
        try:
            single = yf.download(
                ticker,
                start=args.start,
                end=args.end,
                auto_adjust=False,
                progress=False,
                threads=False,
            ).reset_index()
            if single.empty:
                continue
            single.columns = [col.lower().replace(" ", "_") for col in single.columns]
            if "close" not in single or single["close"].dropna().empty:
                continue
            single["ticker"] = ticker
            rows.append(single)
        except Exception:
            continue

    prices = pd.concat(rows, ignore_index=True)
    prices["date"] = pd.to_datetime(prices["date"]).dt.date.astype(str)
    prices = prices[
        ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    ].sort_values(["ticker", "date"])

    earnings = fetch_earnings_snapshot(tickers)

    prices.to_csv(outdir / "mlp_prices.csv", index=False)
    earnings.to_csv(outdir / "mlp_earnings_snapshot.csv", index=False)

    print(f"Wrote {len(prices)} price rows to {outdir / 'mlp_prices.csv'}")
    print(f"Wrote {len(earnings)} earnings rows to {outdir / 'mlp_earnings_snapshot.csv'}")


if __name__ == "__main__":
    main()
