# Broader Universe Phase 2 Plan

## Status

- Owner: Finance + Product + Engineering
- Status: Active
- Date: 2026-05-23

## Why this exists

The original `5`-name MLP was good enough to validate the product shape:

- weekly overview,
- stock detail,
- strategy detail,
- and decision-basis language.

It was **not** good enough to validate real trading usefulness.

That means Step 1 validated the workflow shell, not the strategy edge.

This document defines Step 2.

## What we did today

We expanded the historical pilot from the original `5` names to a broader `33`-ticker pilot universe with roughly `3` years of daily price history using the existing repo pipeline.

Pilot universe includes:

- large-cap leaders,
- sector and industry variety,
- current single-name candidates,
- and benchmark / sector ETFs.

Artifacts created:

- `data/reference/phase2_watchlist.csv`
- `data/raw/phase2/mlp_prices.csv`
- `data/raw/phase2/mlp_earnings_snapshot.csv`
- `data/processed/phase2/mlp_current_recommendations.csv`
- `data/processed/phase2/mlp_backtest_portfolio.csv`
- `data/processed/phase2/mlp_backtest_actions.csv`
- `data/processed/phase2/mlp_backtest_strategies.csv`
- `docs/research/market/phase2-weekly-report-2026-05-23.md`

## What the broader pilot tells us

### Observed

- The current pipeline can pull and process roughly `3` years of daily data for a materially broader pilot universe.
- The current top-2 portfolio replay over the broader pilot produced about `0.29%` average `1`-week return and about `0.00%` average excess return versus `SPY`.
- In the current replay, `Buy now` did **not** materially outperform weaker buckets.
- `Buy on pullback`, `Wait for confirmation`, and even `No action` all showed similar or better average forward `1`-week returns than `Buy now`.
- `Constructive pullback continuation` was directionally positive, but it was not clearly strong enough yet to justify high trust.

### Derived

- The current workflow is usable.
- The current strategy logic is not yet strong enough to support confident live trading next week without further tightening.
- The main problem is not lack of UI structure anymore.
- The main problem is lack of signal discrimination: the model is not yet proving that its strongest labels are truly the strongest opportunities.

### Unknown

- Whether better setup gating will produce a meaningful improvement in short-term edge.
- Whether regime segmentation or sector segmentation will reveal stronger sub-patterns hidden inside the aggregate averages.
- Whether the most useful near-term version is a `top 5` stock workflow, a `50-70` name full watchlist workflow, or a staged hybrid of both.

## Plain-English conclusion

We should **not** call the strategy validated for live use yet.

We **should** say this:

- the product shell is validated,
- the data path is now proven beyond the tiny `5`-stock toy example,
- and the next phase is to improve the strategy with broader replay evidence rather than continuing to polish presentation first.

## What good looks like now

For the next phase, "good" should mean all of these:

1. `Buy now` clearly beats `No action` and `Hold` in forward returns.
2. The top-2 or top-5 weekly portfolio shows persistent positive excess return versus `SPY`.
3. Setup families are selective enough that they fire less often but with better expectancy.
4. The weekly board can be generated across a broader curated watchlist without manual heroics.
5. The user can open next week's review and see a believable top `3-5` names rather than a decorative ranking.

If those conditions are not met, we are still in research mode, not trading mode.

## Phase 2 goal

Build a broader, evidence-driven weekly stock engine that is strong enough to support a real short-term trading workflow for the next week’s review.

## Phase 2 workstreams

### Workstream 1: Broader curated universe

Goal:

- move from a tiny demonstration universe toward the product's real operating shape.

Next step:

- expand from the `33`-ticker pilot to a curated `50-70` name active watchlist.

Requirements:

- high liquidity
- broad sector coverage
- includes current holdings, high-conviction names, and tactical momentum names
- benchmark and sector ETFs included for regime and relative-strength context

### Workstream 2: Better backtest instrumentation

Goal:

- stop relying on one weak summary metric.

Next step:

- extend the replay beyond average `1`-week return.

Metrics to add:

- forward return over `5`, `10`, and `15` trading days
- max adverse excursion proxy
- max favorable excursion proxy
- return by setup family
- return by regime bucket
- return by sector bucket
- return by entry-quality grade
- hit rate of invalidation breach before target window

Why:

- a swing setup can be directionally right but still too volatile or too fragile to trade well

### Workstream 3: Strategy tightening

Goal:

- improve discrimination so the best labels actually earn their rank.

Immediate priorities:

- stricter regime gate
- multi-window relative-strength requirement instead of only `20-day` relative strength
- better overextension filter
- clearer reward-to-risk minimum
- explicit `No action` preference when edge is mediocre
- separate `live setup looks good` from `historically proven setup`

Likely near-term rule changes to test:

- require positive relative strength across `10`, `20`, and `60` days for top long entries
- downgrade setup quality when ATR burden is too high
- downgrade continuation setups that are too close to prior highs without enough reset
- split `Constructive pullback continuation` into higher-quality and lower-quality sub-variants

### Workstream 4: Next-week usable output

Goal:

- make the system useful for the upcoming weekly review even if it is not fully production-grade.

Next step:

- generate a top `5` candidate board from the broader pilot
- produce stock-detail style reasoning for those top names
- label each one explicitly as:
  - `tradeable now`
  - `watch only`
  - `do not touch yet`

Why:

- this gives the user something concrete to pressure-test in real time next week without pretending the engine is already done

## Recommended execution sequence

### Phase 2A: This weekend

1. Keep the broadened `33`-ticker pilot as the working research base.
2. Extend backtest outputs so we can see more than average `1`-week return.
3. Identify which current setup families are clearly weak or noisy.

### Phase 2B: Early next week

1. Expand to a `50-70` name watchlist.
2. Re-run the daily-data replay on the larger universe.
3. Tighten setup rules and compare before/after results.

### Phase 2C: Before the next weekly review

1. Produce a real top `5` candidate board.
2. Generate detail views for those names.
3. Use the system as a decision-support tool for live review with explicit confidence limits.

## Product stance

The product should now treat the original `5`-name MLP as:

- design validation,
- language validation,
- and process validation.

It should **not** treat that first pass as strategy validation.

## Finance stance

The finance system should treat the broader `33`-name replay as the first serious evidence checkpoint.

Current takeaway:

- promising workflow,
- insufficient edge proof,
- proceed by tightening strategy logic and expanding replay depth.

## Engineering stance

Engineering should prioritize:

- reliable broader-universe ingestion,
- richer replay metrics,
- and persistent run outputs that make before/after rule comparisons easy.

This is a better use of time now than additional manual HTML refinement.

## Final call

This project has now moved from:

- "can we mock a weekly review?"

to:

- "can we make the weekly engine selective enough to deserve trust?"

That is the correct frontier.
