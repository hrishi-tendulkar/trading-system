# Internal Terminology

## Purpose

Define a small shared vocabulary for Trading System so product, finance, engineering, and research work from the same terms.

## Core terms

### Data layer

Raw and lightly normalized inputs:

- watchlists
- daily prices
- earnings snapshots
- future event and fundamentals feeds

### Feature engine

The computation layer that turns raw data into measurable fields such as:

- moving averages
- relative strength
- volatility
- regime flags
- sector confirmation fields

### Strategy engine

The rules layer that converts features into:

- setup classification
- action labels
- entry zones
- invalidations
- targets

Current main implementation:

- `scripts/mlp/run_watchlist_analysis.py`

### Replay engine

The historical evaluation layer that tests how strategy logic would have behaved using past data.

This includes:

- backtests
- forward-return evaluation
- strategy variant comparison

Current main experiment harness:

- `scripts/mlp/run_strategy_iterations.py`

### Weekly board

The final weekly action output the user reads.

This should answer:

- what deserves action now
- what deserves patience
- what should be avoided

### Mainline

The current preferred strategy logic in the primary pipeline.

This is the closest thing to the “current default engine,” even if it is not yet production-grade.

### Canonical strategy set

The official list of active and research trading strategies the system is allowed to reason from.

Current reference:

- `docs/strategy/canonical-trading-strategies.md`

### Experiment variant

A deliberately testable alternative rule set used in the replay engine.

Examples:

- `regime_gated`
- `sector_filtered_pullback`
- `etf_rotation_top`

## Decision-basis terminology

### Setup family

A repeatable tradable pattern with:

- entry logic
- invalidation logic
- expected holding style
- replay path

Examples:

- `Constructive pullback continuation`
- `Breakout confirmation`
- `ETF rotation`

### Risk rule

A rule that suppresses or modifies action even if the chart otherwise looks acceptable.

Example:

- `Event freeze before earnings`

### Context lens

A framing aid that helps interpret other signals but is not itself the primary stock-picking edge.

Example:

- `Benchmark trend reference`

## Action terminology

### Buy now

A name or ETF that is currently actionable without waiting for a better entry.

### Buy on pullback

A continuation candidate where the thesis is attractive, but the preferred action is to wait for a controlled reset closer to support.

### Wait for confirmation

A candidate with a potentially valid continuation path, but one that still needs proof through price behavior.

### Do not chase

A setup the system still wants the user aware of, but not at the current price because extension or freshness is no longer good enough for a disciplined entry.

### Hold

A name that still has enough structure to keep on the board, but does not justify a fresh entry.

### No action

A valid output meaning the setup does not currently deserve capital.

### Suppressed

A name that might otherwise qualify, but is blocked from fresh-cash promotion by a risk rule such as near-term event exposure.

## Exposure terminology

### ETF sleeve

The part of the engine focused on:

- broad market exposure
- sector rotation
- cleaner group-level expressions

### Single-name sleeve

The part of the engine focused on individual stock entries after:

- regime checks
- leadership checks
- sector confirmation
- entry-quality tests

## Quality terminology

### Tradeable

A setup with enough alignment between regime, leadership, entry quality, and risk geometry to deserve real attention.

### Trust-calibrated

A recommendation whose wording reflects both:

- the live setup quality
- and the historical evidence quality

### Research mode

The system is still learning and refining logic; it should not be treated as strongly live-ready yet.

### Live-ready

Not a synonym for perfect.

It means the weekly board is strong enough, selective enough, and explainable enough to be used in real decision-making with controlled trust.
