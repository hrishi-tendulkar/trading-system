# MLP Weekly Report

Generated from CSV-based analysis for `2026-05-22`.

## Current Weekly Calls

| Ticker | Strategy | Action | Horizon | Entry | Stop | Target |
|---|---|---|---|---|---|---|
| GS | Constructive pullback continuation | Buy now | 1-3 weeks | $984-$997 | $896 | $1041 |
| QQQ | Constructive pullback continuation | Buy now | 1-3 weeks | $712-$718 | $642 | $738 |
| XLK | Constructive pullback continuation | Buy now | 1-3 weeks | $178-$180 | $154 | $188 |
| TSLA | Constructive pullback continuation | Buy now | 1-3 weeks | $417-$426 | $388 | $458 |
| VOO | Index trend follow-through | Buy now | 2-4 weeks | $683-$686 | $666 | $694 |
| AAPL | Extended strength, wait for pullback | Buy on pullback | Wait this week | $289 | $284 | $315 |
| LLY | Extended strength, wait for pullback | Buy on pullback | Wait this week | $974 | $945 | $1094 |
| PANW | Extended strength, wait for pullback | Buy on pullback | Wait this week | $212 | $201 | $272 |
| AMD | Extended strength, wait for pullback | Buy on pullback | Wait this week | $406 | $375 | $499 |
| XLE | Breakout confirmation | Wait for confirmation | Wait this week | $62 | $57 | $63 |
| V | Breakout confirmation | Wait for confirmation | Wait this week | $335 | $319 | $342 |
| XLF | Breakout confirmation | Wait for confirmation | Wait this week | $52 | $51 | $53 |
| JPM | Breakout confirmation | Wait for confirmation | Wait this week | $307 | $299 | $315 |
| NVDA | Breakout confirmation | Wait for confirmation | Wait this week | $237 | $206 | $246 |
| MSFT | Breakout confirmation | Wait for confirmation | Wait this week | $433 | $406 | $446 |
| ABBV | Trend hold / monitor | Hold | 1-2 weeks | $205 | Yet | Cleaner catalyst |
| GE | Trend hold / monitor | Hold | 1-2 weeks | $288 | Yet | Cleaner catalyst |
| NOW | Trend hold / monitor | Hold | 1-2 weeks | $91 | Yet | Cleaner catalyst |
| XLV | Trend hold / monitor | Hold | 1-2 weeks | $144 | Yet | Cleaner catalyst |
| XOM | Trend hold / monitor | Hold | 1-2 weeks | $151 | Yet | Cleaner catalyst |
| COST | Event freeze before earnings | Hold / reassess after earnings | This week only | Until earnings on 2026-05-28 | Close < $1015 | Re-rank after report |
| CRM | Event freeze before earnings | Hold / reassess after earnings | This week only | Until earnings on 2026-05-27 | Close < $175 | Re-rank after report |
| GOOGL | No actionable setup | No action | Wait this week | No fresh entry | $341 | Cleaner setup |
| AMZN | No actionable setup | No action | Wait this week | No fresh entry | $242 | Cleaner setup |
| CAT | No actionable setup | No action | Wait this week | No fresh entry | $799 | Cleaner setup |
| AVGO | No actionable setup | No action | Wait this week | No fresh entry | $377 | Cleaner setup |
| MA | No actionable setup | No action | Wait this week | No fresh entry | $491 | Cleaner setup |
| META | No actionable setup | No action | Wait this week | No fresh entry | $600 | Cleaner setup |
| NFLX | No actionable setup | No action | Wait this week | No fresh entry | $87 | Cleaner setup |
| PLTR | No actionable setup | No action | Wait this week | No fresh entry | $133 | Cleaner setup |
| UBER | No actionable setup | No action | Wait this week | No fresh entry | $70 | Cleaner setup |
| WMT | No actionable setup | No action | Wait this week | No fresh entry | $118 | Cleaner setup |
| SPY | Benchmark trend reference | Benchmark reference | Reference only | Benchmark | Context | Primary trade |

## Why These Calls Are More Trustworthy

- Recommendations now come from explicit strategy families instead of one generic score, so `buy now` and `wait for confirmation` are no longer the same idea with different adjectives.
- The model now penalizes names that are too extended above the 20-day average instead of automatically pushing the strongest recent movers to the top.
- Entry zone, invalidation, target, and explanation all come from the same setup family instead of being stitched together after the fact.

## Simple Backtest Readout

- Average 1-week return from holding the top 2 eligible ideas each Friday: `0.29%`
- Average excess return vs `SPY`: `0.00%`
- Weekly win rate of the top-2 portfolio: `55.6%`

## Backtest by Action Label

| Action | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Buy on pullback | 427 | 0.78% | 55.0% |
| No action | 2049 | 0.54% | 56.0% |
| Wait for confirmation | 740 | 0.51% | 56.5% |
| Buy now | 825 | 0.33% | 56.5% |
| Hold | 503 | 0.27% | 56.9% |

## Backtest by Strategy Family

| Strategy | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Extended strength, wait for pullback | 427 | 0.78% | 55.0% |
| No actionable setup | 2049 | 0.54% | 56.0% |
| Breakout confirmation | 740 | 0.51% | 56.5% |
| Constructive pullback continuation | 574 | 0.38% | 55.4% |
| Trend hold / monitor | 503 | 0.27% | 56.9% |
| Index trend follow-through | 251 | 0.21% | 59.0% |

## Important Limitation

- Historical backtests in this MLP are still mostly technical because we do not yet have point-in-time historical earnings calendars, transcript changes, or revision history. That means the strategy family replay is useful for direction, but not yet a production-grade validation of event-aware logic.