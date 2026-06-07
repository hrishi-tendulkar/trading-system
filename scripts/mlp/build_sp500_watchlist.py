#!/usr/bin/env python3

from __future__ import annotations

from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
OUT_PATH = Path("data/reference/sp500_watchlist.csv")

EXTRA_ROWS = [
    {
        "ticker": "SPY",
        "display_name": "SPDR S&P 500 ETF",
        "sector": "Benchmark",
        "is_benchmark": True,
        "is_active": True,
    },
    {
        "ticker": "QQQ",
        "display_name": "Invesco QQQ Trust",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLK",
        "display_name": "Technology Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLF",
        "display_name": "Financial Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLV",
        "display_name": "Health Care Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLE",
        "display_name": "Energy Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLI",
        "display_name": "Industrial Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLY",
        "display_name": "Consumer Discretionary Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLP",
        "display_name": "Consumer Staples Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLC",
        "display_name": "Communication Services Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLU",
        "display_name": "Utilities Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
    {
        "ticker": "XLRE",
        "display_name": "Real Estate Select Sector SPDR Fund",
        "sector": "ETF",
        "is_benchmark": False,
        "is_active": True,
    },
]


def _fetch_html() -> str:
    request = Request(WIKI_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:  # noqa: S310
        return response.read().decode("utf-8")


def main() -> None:
    tables = pd.read_html(StringIO(_fetch_html()))
    constituents = tables[0].rename(
        columns={
            "Symbol": "ticker",
            "Security": "display_name",
            "GICS Sector": "sector",
        }
    )
    constituents = constituents[["ticker", "display_name", "sector"]].copy()
    constituents["ticker"] = constituents["ticker"].str.replace(".", "-", regex=False)
    constituents["is_benchmark"] = False
    constituents["is_active"] = True

    extras = pd.DataFrame(EXTRA_ROWS)
    watchlist = pd.concat([constituents, extras], ignore_index=True)
    watchlist = watchlist.drop_duplicates(subset=["ticker"], keep="first")
    watchlist = watchlist.sort_values(
        ["is_benchmark", "sector", "ticker"],
        ascending=[True, True, True],
    ).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    watchlist.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(watchlist)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
