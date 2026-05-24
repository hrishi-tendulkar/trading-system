# Weekly Equity Intelligence MLP Plan

## Purpose

Define the fastest believable way to test the Weekly Equity Intelligence strategy without committing early to deep API integration, broad universe coverage, or full product infrastructure.

`MLP` here means:

- the smallest version that can teach us whether the strategy is directionally useful,
- whether the weekly workflow is actually usable,
- and whether the ranking logic feels better than ad hoc discretionary review.

This is intentionally not the same as the full `v1` product.

## Core Question

Before we build a proper platform, we should answer:

- if we look at a tiny watchlist of real stocks weekly,
- and compute a simple set of technical and event-driven signals,
- does the output actually help us decide what to buy, hold, or avoid?

If the answer is no, deeper integrations are premature.

## Recommended MLP Principle

Do not start by building infrastructure.

Start by proving:

1. the weekly review workflow is useful,
2. the ranking logic is directionally helpful,
3. the evidence summaries are interpretable,
4. and the manual effort is low enough to sustain.

## Recommended Starter Universe

Use a tiny, intentionally mixed set:

- `NVDA`
- `TSLA`
- `CRM`
- `VOO`
- `SPY`

Optional sixth and seventh names:

- `META`
- `AVGO`

Why this mix:

- gives us one benchmark (`SPY`)
- gives us one passive broad-market reference (`VOO`)
- includes both high-beta growth names and a large-cap enterprise software name
- keeps the analysis small enough that we can deeply inspect each weekly output

## What We Actually Need to Test First

For the MLP, we do **not** need:

- broad market coverage
- options chains
- transcripts
- rich news infrastructure
- a full UI
- or even automated daily ingestion

We only need enough data and tooling to answer:

- does the weekly scorecard make sense?
- does it identify stronger vs weaker names?
- does it catch deterioration early enough to matter?

## Four Credible MLP Paths

## Option A: CSV Lab, No Real Integration

### What it is

- manually download `1 year` or `2026 YTD` daily OHLCV CSVs for `5-7` stocks and `SPY`
- load them into a local notebook or DuckDB
- compute weekly features and rankings
- manually add earnings dates and a few event notes in a side table

### Data sources

- Yahoo Finance CSV export or equivalent manual source
- SEC EDGAR manually for recent filings
- manual earnings dates from company IR pages or public finance pages

### Storage

- local CSV files
- DuckDB or Pandas

### Pros

- fastest possible start
- almost zero cost
- zero vendor lock-in
- enough to validate ranking logic quickly

### Cons

- not operationally scalable
- weak auditability
- manual data refreshes

### Best use

- first `3-7 day` proof of concept

## Option B: Supabase-Light Import

### What it is

- same small-stock universe
- manually gather `1 year` or `2026 YTD` daily OHLCV
- import into a few Supabase tables
- run feature computation and weekly scoring from scripts

### Minimal tables

- `securities`
- `daily_prices`
- `earnings_events`
- `manual_notes`
- `weekly_runs`
- `recommendations`

### Pros

- starts building the real backbone
- easy to query and compare weekly outputs
- creates a clean upgrade path toward the proper product

### Cons

- still requires manual or semi-manual loading
- slightly slower than a notebook-only start

### Best use

- best balance between speed and future reuse

## Option C: FMP-Only Tiny Universe Pilot

### What it is

- use `FMP Starter`
- ingest only `5-10` names plus `SPY` and maybe a few sector ETFs
- skip broad normalization complexity
- run a simplified weekly pipeline directly into Supabase

### Pros

- proves the real data source early
- low recurring cost
- still lightweight enough to move fast

### Cons

- introduces API integration work earlier
- can distract from validating the strategy logic itself

### Best use

- good second step after we like the notebook/CSV results

## Option D: Google Sheets / Spreadsheet First

### What it is

- maintain a watchlist and daily price history in a spreadsheet
- compute basic moving averages, relative strength, and weekly ranking in formulas
- keep manual event notes in adjacent tabs

### Pros

- very visible and easy to inspect
- collaborative with yourself
- lowest engineering friction

### Cons

- weak reproducibility
- harder to backtest properly
- formulas become messy quickly

### Best use

- useful if the main goal is quickly seeing the workflow before coding

## Recommended Path

My recommendation is a staged approach:

### Stage 1: `CSV + Supabase-Light`

This is the best MLP.

Why:

- faster than real API integration
- more durable than spreadsheet-only
- close enough to the eventual architecture that the work is reusable

### Stage 2: `FMP Tiny-Universe Pilot`

Once we like the scoring and workflow:

- replace manual CSV refreshes with `FMP Starter`
- keep the same schema and scoring logic

This lets us validate product value before deeper infrastructure.

## What the MLP Should Include

### Data scope

For `5-7` stocks plus `SPY`:

- daily OHLCV
- adjusted close if available
- earnings dates
- 1-2 recent filing references per company
- simple manual event notes

### Time range

Choose one:

- `2026 YTD` for fastest start
- last `1 year` for more realistic signal behavior

Recommended:

- use `1 year` if manual extraction is not painful
- otherwise start with `2026 YTD`

## Minimal Analysis to Run

The MLP should keep the signal set small.

### Technical / quantitative

- price vs `20DMA`
- price vs `50DMA`
- `4-week` return
- `4-week` relative return vs `SPY`
- ATR or simple realized volatility
- distance from recent high
- volume ratio vs trailing average

### Event context

- days to next earnings
- did earnings occur in the past `10` trading days
- manual flag for recent major filing or event

### Fundamental context

For the MLP, keep this manual or lightweight:

- revenue growth direction
- margin direction if easy to obtain
- one simple “fundamental improving / stable / weakening” note

### Output

For each stock, once per week:

- score summary
- trend status
- relative strength status
- event risk flag
- action label
- short explanation

## Suggested Weekly Output Format

Each Friday or weekend, produce a table like:

| Ticker | Trend | RS vs SPY | Event Risk | Fundamental Support | Action | Notes |
|---|---|---|---|---|---|---|
| NVDA | Strong | Strong | Low | Improving | Buy candidate | Pullback held, leading tape |
| CRM | Neutral | Neutral | Low | Stable | Watch for entry | Needs stronger momentum |
| TSLA | Weak | Weak | Medium | Mixed | Avoid / no action | Poor structure, noisy catalyst path |

This is enough to evaluate whether the workflow is useful.

## Minimal Database Design for Supabase-Light

If we choose the recommended path, keep the schema tiny.

### Table 1: `securities`

- `ticker`
- `company_name`
- `sector`
- `is_benchmark`

### Table 2: `daily_prices`

- `ticker`
- `date`
- `open`
- `high`
- `low`
- `close`
- `adj_close`
- `volume`

### Table 3: `earnings_events`

- `ticker`
- `earnings_date`
- `notes`

### Table 4: `manual_notes`

- `ticker`
- `note_date`
- `note_type`
- `summary`

### Table 5: `weekly_runs`

- `run_date`
- `market_note`

### Table 6: `recommendations`

- `run_date`
- `ticker`
- `trend_score`
- `rs_score`
- `event_risk_flag`
- `fundamental_flag`
- `action_label`
- `summary`

## Minimal Implementation Plan

### Week 1

- choose `5-7` names
- gather `2026 YTD` or `1 year` of CSV price history
- load into Supabase or DuckDB
- compute a first pass of weekly signals

### Week 2

- generate `8-12` historical weekly reviews by replaying prior Fridays
- see if the rankings feel sensible
- refine signal thresholds

### Week 3

- add manual earnings dates and filing notes
- compare whether event context materially improves recommendations

### Week 4

- decide whether the workflow is valuable enough to automate with `FMP Starter`

## Creative Variants

If we want to move even faster:

### Variant 1: Replay Fridays only

Instead of daily processing, only ingest Friday closes and weekly highs/lows.

Why:

- dramatically smaller dataset
- enough to test the weekly workflow

Tradeoff:

- weaker ATR and volume logic

### Variant 2: Benchmark-first regime journal

Keep a manual weekly note on `SPY` and `VOO` first, then rank the other names relative to that.

Why:

- lets us test whether regime framing improves decisions

### Variant 3: Human-in-the-loop qualitative overlay

Do not automate qualitative analysis at all initially.

Instead:

- once a week, read the latest earnings note or filing headline for only the top `2-3` candidates
- add one manual note

Why:

- far faster than building transcript or filing pipelines
- still tests whether qualitative context changes decisions

## Recommended Final Answer

The quickest believable MLP is:

1. start with `5-7` stocks and `SPY`
2. use `2026 YTD` or `1 year` of daily OHLCV
3. import into `Supabase-Light` or `DuckDB`
4. compute a very small weekly scorecard
5. add earnings dates and a few manual notes by hand
6. run weekly replay analysis before automating anything

If that works, then upgrade to:

- `FMP Starter`
- same schema
- same weekly scoring logic

That path teaches us whether the strategy and workflow are useful before we spend time on broader integrations.
