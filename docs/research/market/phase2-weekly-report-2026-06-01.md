# MLP Weekly Report

Generated from CSV-based analysis for `2026-05-29`.

## Current Weekly Calls

| Ticker | Strategy | Action | Horizon | Entry | Stop | Target |
|---|---|---|---|---|---|---|
| QQQ | ETF rotation | Buy now | 2-4 weeks | $734-$738 | $698 | $751 |
| XLK | ETF rotation | Buy now | 2-4 weeks | $189-$191 | $172 | $196 |
| GS | Extended strength, wait for pullback | Wait for pullback | Wait this week | $959 | $932 | $1053 |
| MSFT | Extended strength, wait for pullback | Wait for pullback | Wait this week | $418 | $406 | $462 |
| AAPL | Trend hold / monitor | Hold | 1-2 weeks | $295 | Yet | Cleaner catalyst |
| AMD | Trend hold / monitor | Hold | 1-2 weeks | $426 | Yet | Cleaner catalyst |
| GE | Trend hold / monitor | Hold | 1-2 weeks | $295 | Yet | Cleaner catalyst |
| LLY | Trend hold / monitor | Hold | 1-2 weeks | $1000 | Yet | Cleaner catalyst |
| PANW | Trend hold / monitor | Hold | 1-2 weeks | $222 | Yet | Cleaner catalyst |
| TSLA | Trend hold / monitor | Hold | 1-2 weeks | $413 | Yet | Cleaner catalyst |
| VOO | Trend hold / monitor | Hold | 1-2 weeks | $677 | Yet | Cleaner catalyst |
| NOW | Trend hold / monitor | Hold | 1-2 weeks | $94 | Yet | Cleaner catalyst |
| PLTR | Trend hold / monitor | Hold | 1-2 weeks | $135 | Yet | Cleaner catalyst |
| CRM | Trend hold / monitor | Hold | 1-2 weeks | $175 | Yet | Cleaner catalyst |
| META | Trend hold / monitor | Hold | 1-2 weeks | $607 | Yet | Cleaner catalyst |
| AVGO | Event freeze before earnings | Hold / reassess after earnings | This week only | Until earnings on 2026-06-03 | Close < $415 | Re-rank after report |
| AMZN | No actionable setup | No action | Wait this week | No fresh entry | $247 | Cleaner setup |
| XLV | No actionable setup | No action | Wait this week | No fresh entry | $145 | Cleaner setup |
| ABBV | No actionable setup | No action | Wait this week | No fresh entry | $207 | Cleaner setup |
| CAT | No actionable setup | No action | Wait this week | No fresh entry | $815 | Cleaner setup |
| NVDA | No actionable setup | No action | Wait this week | No fresh entry | $199 | Cleaner setup |
| XLF | No actionable setup | No action | Wait this week | No fresh entry | $51 | Cleaner setup |
| GOOGL | No actionable setup | No action | Wait this week | No fresh entry | $348 | Cleaner setup |
| V | No actionable setup | No action | Wait this week | No fresh entry | $315 | Cleaner setup |
| COST | No actionable setup | No action | Wait this week | No fresh entry | $937 | Cleaner setup |
| JPM | No actionable setup | No action | Wait this week | No fresh entry | $295 | Cleaner setup |
| UBER | No actionable setup | No action | Wait this week | No fresh entry | $69 | Cleaner setup |
| WMT | No actionable setup | No action | Wait this week | No fresh entry | $113 | Cleaner setup |
| MA | No actionable setup | No action | Wait this week | No fresh entry | $487 | Cleaner setup |
| NFLX | No actionable setup | No action | Wait this week | No fresh entry | $84 | Cleaner setup |
| XLE | No actionable setup | No action | Wait this week | No fresh entry | $55 | Cleaner setup |
| XOM | No actionable setup | No action | Wait this week | No fresh entry | $142 | Cleaner setup |
| SPY | Benchmark trend reference | Benchmark reference | Reference only | Benchmark | Context | Primary trade |

## Why These Calls Are More Trustworthy

- Recommendations now come from explicit strategy families instead of one generic score, so `buy now` and `wait for confirmation` are no longer the same idea with different adjectives.
- The model now penalizes names that are too extended above the 20-day average instead of automatically pushing the strongest recent movers to the top.
- Entry zone, invalidation, target, and explanation all come from the same setup family instead of being stitched together after the fact.

## Simple Backtest Readout

- Average 1-week return from holding the top 2 eligible ideas each Friday: `0.83%`
- Average excess return vs `SPY`: `0.46%`
- Weekly win rate of the top-2 portfolio: `73.1%`

## Backtest by Action Label

| Action | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Wait for pullback | 73 | 1.56% | 67.1% |
| No action | 297 | 0.68% | 59.3% |
| Buy on pullback | 39 | 0.67% | 71.8% |
| Hold | 409 | 0.29% | 52.3% |
| Wait for confirmation | 14 | -0.26% | 42.9% |

## Backtest by Strategy Family

| Strategy | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Extended strength, wait for pullback | 73 | 1.56% | 67.1% |
| No actionable setup | 297 | 0.68% | 59.3% |
| Constructive pullback continuation | 39 | 0.67% | 71.8% |
| Trend hold / monitor | 409 | 0.29% | 52.3% |
| Breakout confirmation | 14 | -0.26% | 42.9% |

## Important Limitation

- Historical backtests in this MLP are still mostly technical because we do not yet have point-in-time historical earnings calendars, transcript changes, or revision history. That means the strategy family replay is useful for direction, but not yet a production-grade validation of event-aware logic.