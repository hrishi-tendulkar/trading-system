#!/usr/bin/env python3

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import requests


WIKI_URL = "https://en.wikipedia.org/wiki/S%26P_100"
OUT_PATH = Path("data/reference/sp100_watchlist.csv")

EXTRA_ROWS = [
    {"ticker": "SPY", "display_name": "SPDR S&P 500 ETF", "sector": "Benchmark", "is_benchmark": True, "is_active": True},
    {"ticker": "QQQ", "display_name": "Invesco QQQ Trust", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLK", "display_name": "Technology Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLF", "display_name": "Financial Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLV", "display_name": "Health Care Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLE", "display_name": "Energy Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLI", "display_name": "Industrial Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
    {"ticker": "XLY", "display_name": "Consumer Discretionary Select Sector SPDR Fund", "sector": "ETF", "is_benchmark": False, "is_active": True},
]


def main() -> None:
    response = requests.get(WIKI_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    constituents = tables[2].rename(columns={"Symbol": "ticker", "Name": "display_name", "Sector": "sector"})
    constituents = constituents[["ticker", "display_name", "sector"]].copy()
    constituents["ticker"] = constituents["ticker"].str.replace(".", "-", regex=False)
    constituents["is_benchmark"] = False
    constituents["is_active"] = True

    extras = pd.DataFrame(EXTRA_ROWS)
    watchlist = pd.concat([constituents, extras], ignore_index=True)
    watchlist = watchlist.drop_duplicates(subset=["ticker"], keep="first")
    watchlist = watchlist.sort_values(["is_benchmark", "ticker"], ascending=[True, True]).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    watchlist.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(watchlist)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
