# MLP Weekly Report

Generated from CSV-based analysis for `2026-05-22`.

## Current Weekly Calls

| Ticker | Strategy | Action | Horizon | Entry | Stop | Target |
|---|---|---|---|---|---|---|
| TSLA | Constructive pullback continuation | Buy now | 1-3 weeks | $417-$426 | $388 | $458 |
| VOO | Index trend follow-through | Buy now | 2-4 weeks | $683-$686 | $666 | $694 |
| NVDA | Breakout confirmation | Wait for confirmation | Wait this week | $237 | $206 | $246 |
| CRM | Event freeze before earnings | Hold / reassess after earnings | This week only | Until earnings on 2026-05-27 | Close < $175 | Re-rank after report |
| SPY | Benchmark trend reference | Benchmark reference | Reference only | Benchmark | Context | Primary trade |

## Why These Calls Are More Trustworthy

- Recommendations now come from explicit strategy families instead of one generic score, so `buy now` and `wait for confirmation` are no longer the same idea with different adjectives.
- The model now penalizes names that are too extended above the 20-day average instead of automatically pushing the strongest recent movers to the top.
- Entry zone, invalidation, target, and explanation all come from the same setup family instead of being stitched together after the fact.

## Simple Backtest Readout

- Average 1-week return from holding the top 2 eligible ideas each Friday: `0.08%`
- Average excess return vs `SPY`: `-0.22%`
- Weekly win rate of the top-2 portfolio: `46.4%`

## Backtest by Action Label

| Action | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Hold | 13 | 0.96% | 61.5% |
| No action | 39 | 0.89% | 64.1% |
| Wait for confirmation | 15 | 0.55% | 53.3% |
| Buy now | 37 | -0.18% | 51.4% |
| Buy on pullback | 8 | -1.70% | 25.0% |

## Backtest by Strategy Family

| Strategy | Observations | Avg 1W Return | Win Rate |
|---|---:|---:|---:|
| Trend hold / monitor | 13 | 0.96% | 61.5% |
| No actionable setup | 39 | 0.89% | 64.1% |
| Breakout confirmation | 15 | 0.55% | 53.3% |
| Index trend follow-through | 26 | 0.19% | 61.5% |
| Constructive pullback continuation | 11 | -1.06% | 27.3% |
| Extended strength, wait for pullback | 8 | -1.70% | 25.0% |

## Important Limitation

- Historical backtests in this MLP are still mostly technical because we do not yet have point-in-time historical earnings calendars, transcript changes, or revision history. That means the strategy family replay is useful for direction, but not yet a production-grade validation of event-aware logic.