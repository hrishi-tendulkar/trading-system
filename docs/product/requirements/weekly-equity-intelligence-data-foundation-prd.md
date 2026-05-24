# Weekly Equity Intelligence Data Foundation PRD

## Status

- Owner: Product
- Status: Draft
- Last updated: 2026-05-22

## Purpose

Define the product requirements for the data foundation needed to power the Weekly Equity Intelligence system.

This PRD translates the strategy and analysis framework into a buildable, prioritized data scope. Its goal is to answer:

- what data the product must have to deliver a credible weekly decision workflow,
- what historical depth is required for research and backtesting,
- what ongoing feeds are required for daily and weekly operations,
- and what can be deferred without breaking the core user outcome.

This is a data-product PRD, not a vendor-selection memo. It should help Finance, Product, and Engineering evaluate providers and sequence implementation.

## Related Documents

- [PRODUCT](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/PRODUCT.md)
- [Weekly Equity Intelligence PRD](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/weekly-equity-intelligence-prd.md)
- [Trading System High-Level Design](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/high-level-design.md)
- [Weekly Equity Intelligence Strategy Blueprint](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/weekly-equity-intelligence-strategy-blueprint.md)
- [Weekly Equity Intelligence Analysis Framework](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/finance/frameworks/weekly-equity-intelligence-analysis-framework.md)

## Product Problem

The Weekly Equity Intelligence product depends on a broad but carefully prioritized data stack. Without a disciplined data foundation, the system risks becoming:

- technically expensive but strategically weak,
- explainable in theory but not backtestable in practice,
- or rich in research content but poor at generating actionable weekly decisions.

The product therefore needs a clear answer to:

1. Which data is absolutely required to produce a strong weekly stock-ranking and decision workflow?
2. Which data materially improves confidence, explainability, and backtesting quality?
3. Which data is helpful but should not block v1?

## User Job

The user wants a weekly system that tells them:

- what to buy now,
- what to buy on pullback,
- what to hold,
- what to trim or sell,
- and when covered calls or cash-secured puts are the preferred expression.

The data foundation succeeds only if it materially improves that weekly decision loop.

## Product Principles

- Weekly decision quality is the center of gravity.
- Stock selection comes before options overlays.
- Data requirements should be driven by the product workflow, not by vendor feature lists.
- Historical point-in-time correctness matters wherever backtesting depends on it.
- Raw captures and source lineage are product requirements, not engineering niceties.
- Missing optional data should degrade gracefully rather than break the weekly workflow.

## Core User Outcomes Supported by This PRD

This data foundation must enable the product to:

- rank a curated stock universe weekly,
- generate explainable entry, stop, and target guidance,
- flag important changes since the previous review,
- support short-term tradeability and longer-term conviction scores separately,
- support basic covered-call and cash-secured-put overlays,
- and create a historical record suitable for forward testing and backtesting.

## Scope Model

This PRD uses three priority levels:

### `P0`

Data required to ship a credible v1 weekly stock-intelligence product.

If a `P0` dataset is missing, the weekly core workflow is materially weakened or not trustworthy.

### `P1`

Data that materially improves ranking quality, explainability, qualitative review, or overlays, but is not required to make the stock engine viable.

### `P2`

Data that is useful for later sophistication, deeper research, or improved overlays, but should not block the initial product.

## P0 Requirements

These are the minimum datasets required for a strong v1 product.

## 1. Security Master and Universe Metadata

### Why this is `P0`

The entire system depends on stable identity, clean joins, and survivorship-safe universe management.

### Historical requirements

- ticker history
- stable security identifier such as FIGI, CUSIP, or vendor-specific permanent ID
- company name history
- exchange history
- delisting history
- symbol change history
- sector and industry classification
- ETF mappings for benchmark and sector comparisons

### Ongoing requirements

- new symbol additions and removals
- identifier updates
- delisting and suspension updates
- sector and industry classification updates

### Product dependencies

- watchlist management
- universe eligibility
- benchmark and sector mapping
- backtesting without symbol-survivorship distortion

## 2. Daily Price, Volume, and Corporate Actions

### Why this is `P0`

This is the core quantitative substrate. Without it, there is no meaningful trend, structure, or relative-strength engine.

### Historical requirements

- daily `open`, `high`, `low`, `close`
- daily `adjusted_close`
- daily `volume`
- split factors
- dividend adjustments
- unadjusted and adjusted price history
- daily dollar volume

### Ongoing requirements

- daily end-of-day OHLCV refresh
- late corrections when vendors revise EOD bars
- ongoing split and dividend updates

### Recommended historical depth

- target: `10+ years`
- minimum acceptable for v1: `5 years`

### Product dependencies

- trend and structure analysis
- moving averages
- ATR and volatility
- support/resistance mapping
- relative strength
- breakout and pullback detection
- weekly ranking
- backtesting

## 3. Benchmark and Sector Market Data

### Why this is `P0`

The strategy explicitly depends on regime and relative-strength logic. That requires benchmark and sector context.

### Historical requirements

- daily OHLCV for `SPY`, `QQQ`, `IWM`
- daily OHLCV for major sector ETFs
- optional volatility benchmark such as `VIX`

### Ongoing requirements

- daily EOD refresh for benchmark and sector ETFs
- benchmark corrections or corporate-action changes if applicable

### Product dependencies

- market regime analysis
- relative strength vs market
- relative strength vs sector
- sector leadership context

## 4. Earnings Calendar and Earnings Results

### Why this is `P0`

Earnings are one of the most important catalysts in the strategy. The product cannot responsibly rank or filter ideas without upcoming-event awareness and post-event result context.

### Historical requirements

- scheduled earnings date
- actual earnings announcement date
- announcement time if available
- actual EPS
- consensus EPS at time of report if available
- EPS surprise
- actual revenue
- consensus revenue at time of report if available
- revenue surprise
- guidance raise / maintain / cut flag if available

### Ongoing requirements

- upcoming earnings calendar refresh
- confirmed date changes
- actual results ingestion on report day
- structured guidance updates if available

### Recommended historical depth

- target: `5-10 years`
- minimum acceptable for v1: `3 years`

### Product dependencies

- event-risk filtering
- post-earnings continuation setup detection
- catalyst labeling
- weekly watchlist review
- daily change digest

## 5. Analyst Estimates and Revision History

### Why this is `P0`

The strategy relies on expectations and expectation changes, not just trailing fundamentals. Estimate revisions are one of the highest-value differentiators for weekly tactical stock selection.

### Historical requirements

- consensus EPS estimates by period and date
- consensus revenue estimates by period and date
- number of analysts in the consensus
- revision history with timestamps
- direction and magnitude of estimate changes
- forward fiscal year estimates where available
- target price history where available
- coverage count history

### Ongoing requirements

- daily estimate revision updates
- new target price changes
- coverage additions and removals

### Recommended historical depth

- target: `5-10 years`
- minimum acceptable for v1: `3 years`

### Product dependencies

- revision momentum setup detection
- conviction support
- earnings follow-through analysis
- weekly “what changed” explanations
- explainable catalyst scoring

### Important note

Raw recommendation labels such as `buy`, `hold`, or `sell` are less important than revision direction, estimate deltas, and coverage breadth.

## 6. Core Fundamental Statements

### Why this is `P0`

The strategy keeps short-term timing and longer-term conviction separate. Fundamental data is not the timing engine, but it is a required filter and conviction layer.

### Historical requirements

- quarterly income statement
- quarterly balance sheet
- quarterly cash flow statement
- annual statement history
- revenue
- gross profit and gross margin
- operating income and operating margin
- diluted EPS
- free cash flow or derivable cash flow components
- capex
- cash and equivalents
- total debt
- diluted share count

### Ongoing requirements

- quarterly and annual updates
- restatements or corrections
- statement availability dates if possible

### Recommended historical depth

- target: `10 years`
- minimum acceptable for v1: `5 years`

### Product dependencies

- conviction score
- fragile-business avoidance
- longer-hold candidate identification
- contextual support for weekly recommendations

## 7. SEC Filing Metadata and Filing Text

### Why this is `P0`

The product’s qualitative red-team layer depends on source-of-truth filings, especially for risk-factor changes, material events, and factual evidence.

### Historical requirements

- `10-K`, `10-Q`, `8-K` metadata
- filing type
- filing date and time
- accession number or permanent source URL
- raw filing text or extracted text
- amendment flags

### Ongoing requirements

- new filing detection
- filing metadata ingestion
- filing text capture
- amendment detection

### Recommended historical depth

- target: `3-5+ years`
- minimum acceptable for v1: `2 years`

### Product dependencies

- qualitative risk review
- material event context
- fact extraction
- evidence traceability

## 8. Company News Feed

### Why this is `P0`

The product needs basic awareness of material company-specific developments outside earnings and filings.

### Historical requirements

- timestamped news items
- headline
- source
- URL
- ticker mapping
- article published time

### Ongoing requirements

- daily news refresh
- reliable timestamping
- duplicate handling across sources if needed

### Recommended historical depth

- target: `3+ years`
- minimum acceptable for v1: `1 year`

### Product dependencies

- daily change digest
- event context
- disqualification of otherwise attractive setups
- evidence summary

## 9. Recommendation and Outcome History

### Why this is `P0`

This is internal product data, but it is essential. Without it, the product cannot learn, forward-test, or evaluate itself.

### Historical and ongoing requirements

- recommendation timestamp
- ticker
- setup family
- tradeability score
- conviction score
- risk penalty
- final action label
- entry zone
- stop / invalidation
- targets
- catalyst label
- evidence summary
- regime label
- realized forward returns over `1w`, `2w`, `4w`, `8w`

### Product dependencies

- forward testing
- backtest comparison
- weekly review history
- “what worked vs what failed” learning loop

## P1 Requirements

These datasets materially improve the product but should not block the first credible release.

## 10. Earnings Call Transcripts

### Why this is `P1`

Transcripts are valuable for management tone, narrative shifts, and qualitative confirmation. But the stock engine can function without them if filings and structured event data are present.

### Historical requirements

- transcript text
- transcript date/time
- speaker attribution if available
- prepared remarks / Q&A split if available

### Ongoing requirements

- transcript ingestion after earnings
- corrected transcript replacement if vendor revises

### Product dependencies

- qualitative confirmation
- narrative change analysis
- management tone review

## 11. Options Chain Snapshots

### Why this is `P1`

Options overlays are part of the product, but they are secondary to stock selection. The product should launch its stock engine first if options data quality is weak.

### Historical requirements

- option chain snapshots by date
- expiration
- strike
- call/put flag
- bid
- ask
- last
- volume
- open interest
- implied volatility
- days to expiration
- contract multiplier
- adjusted contract metadata after splits or actions

### Ongoing requirements

- daily end-of-day chain snapshots for supported names
- daily open interest and implied volatility refresh
- expiration calendar updates

### Recommended historical depth

- target: `2-5+ years`
- minimum acceptable for live screening: no backfill required if only forward use is planned

### Product dependencies

- covered-call candidate ranking
- cash-secured-put candidate ranking
- overlay liquidity and spread filters
- premium yield calculations

### Important note

If historical chain snapshots are unavailable, the product may still support live weekly overlay screening, but historical options backtests should be out of scope.

## 12. Advanced Corporate Event Structuring

### Why this is `P1`

Structured event flags beyond basic earnings and filings improve interpretation and disqualification logic, but are not required for the initial weekly stock engine.

### Historical requirements

- major corporate event labels where available
- merger or financing event flags
- executive change events
- guidance-event tagging

### Ongoing requirements

- ongoing event classification updates

### Product dependencies

- cleaner event context
- better qualitative red-team triage

## 13. Breadth and Market Internal Health Metrics

### Why this is `P1`

These improve regime detection, but a simpler regime model can launch first using benchmarks and sector behavior alone.

### Historical requirements

- percent of stocks above key moving averages
- new highs / new lows
- advancers / decliners
- equal-weight benchmark behavior if available

### Ongoing requirements

- daily breadth refresh

### Product dependencies

- improved regime classification
- risk scaling and selectivity adjustments

## 14. Richer News Classification

### Why this is `P1`

Better categorization helps compression of information into decisions, but raw timestamped news is enough to begin.

### Historical requirements

- category labels such as company, sector, macro, product, legal, financing
- relevance or confidence metadata if provided

### Ongoing requirements

- ongoing category and relevance updates

### Product dependencies

- cleaner daily digest
- better event triage

## P2 Requirements

These are useful later but should not block the product.

## 15. Investor Presentations and Event Decks

### Why this is `P2`

Helpful for deeper research, but lower-value than filings and transcripts for the weekly operating loop.

### Historical requirements

- investor decks
- earnings decks
- event presentations
- publication date

### Ongoing requirements

- new deck detection and storage

## 16. Deeper Options Analytics

### Why this is `P2`

Not required for covered calls and cash-secured puts in a stock-first product.

### Historical and ongoing examples

- full Greeks beyond delta
- IV percentile history
- skew analytics
- theoretical pricing models
- option-surface analytics

## 17. Macro and Alternative Data Expansion

### Why this is `P2`

Can enrich later research, but not required for the core weekly workflow.

### Examples

- detailed macro calendars
- rates curves beyond simple benchmark context
- fund flows
- ownership datasets
- social sentiment
- alternative data feeds

## Cross-Cutting Data Requirements

These apply to all datasets.

## 18. Point-in-Time Correctness

### Requirement

Where backtesting depends on timing, the system should store what was knowable at decision time, not merely the latest revised value.

### Highest-priority datasets for point-in-time integrity

- analyst estimates and revisions
- earnings calendar and actual results
- fundamentals with availability dates
- filing timestamps
- options snapshots

### Why it matters

- prevents look-ahead bias
- makes backtesting credible
- allows recommendation replay

## 19. Raw Capture, Normalization, and Lineage

### Requirement

Every provider integration should support:

- raw payload storage where feasible
- normalized tables
- derived feature tables
- fetch timestamp
- effective date
- source identifier
- source record ID if available

### Why it matters

- debugging
- vendor comparison
- reproducibility
- auditability of recommendations

## 20. Historical Backfill Requirements by Priority

### `P0` historical backfill targets

- `10+ years` of daily price and corporate-action history
- `5-10 years` of earnings calendar and earnings results
- `5-10 years` of analyst estimate and revision history if possible
- `5-10 years` of core quarterly and annual fundamentals
- `3-5+ years` of filing metadata and text
- internal recommendation history from day one of system operation

### `P1` historical backfill targets

- `3-5+ years` of transcripts if affordable
- `2-5+ years` of options chain snapshots if options backtesting is a goal
- `3+ years` of breadth data if externally sourced

## 21. Ongoing Refresh Cadence Requirements

### Daily after market close

- EOD price and volume refresh
- benchmark and sector refresh
- technical feature recompute
- analyst revision updates
- earnings calendar refresh
- new news ingestion
- new filing detection
- options chain snapshot if supported

### Weekly

- full-universe rerank
- entry / stop / target recomputation
- weekly action report generation
- holdings review generation
- overlay candidate refresh

### Event-driven

- earnings result ingestion
- guidance changes
- material `8-K` updates
- transcript arrival
- major estimate revision clusters

### Quarterly

- new fundamental statements
- conviction-layer refresh
- filing-delta review

## 22. Product Degradation Rules

The product should fail gracefully when non-core data is missing.

### Required degradation behavior

- If transcript data is unavailable, keep the stock engine active and reduce qualitative depth.
- If options data is unavailable, keep the long-only engine active and suppress overlay recommendations.
- If analyst ratings are unavailable but revision history exists, proceed.
- If richer news classification is unavailable, fall back to timestamped raw news with basic relevance rules.

### Non-acceptable degradation

- The product must not generate confident weekly recommendations if EOD price history or earnings calendar integrity is broken.
- The product must not present options backtests if historical chain snapshots are missing.

## 23. Provider Evaluation Criteria

When evaluating vendors, score them on:

- coverage of U.S. equities in the target universe
- historical depth
- point-in-time integrity
- revision-history availability
- filings coverage
- transcript coverage
- options chain history quality
- update latency
- API stability and rate limits
- cost
- raw payload completeness

This PRD does not choose providers, but it defines the criteria they must be judged against.

## Non-Goals

- Intraday bars in v1
- Level 2 or order-book data
- real-time streaming market data
- execution and broker integration
- multi-user permissions
- complex options analytics platform behavior
- alternative-data experimentation before the core weekly loop is working

## Success Criteria

This data foundation succeeds when:

- the product can generate a credible weekly stock-ranking and recommendation workflow from `P0` data alone,
- `P1` data cleanly improves explanation and overlays without destabilizing the core workflow,
- historical datasets are sufficient to test the first `2-3` strategy families,
- and missing `P1/P2` feeds do not break the core user experience.

## Open Questions

- Which provider best covers analyst revision history at acceptable cost?
- Can one provider cover both stock data and options snapshots well enough, or will options require a second vendor?
- How much historical transcript coverage is affordable and truly valuable in v1?
- Do we need third-party breadth data, or can internal breadth be derived from an expanded reference universe?
- What minimum historical depth should be considered a hard block for go-live?

## Implementation Recommendation

Sequence the product in this order:

1. `P0` security master, daily prices, corporate actions, benchmark data, earnings data, revisions, fundamentals, filings, and internal recommendation history
2. `P1` transcripts and options chain support
3. `P1` richer event and breadth improvements
4. `P2` research expansion and advanced overlays

This sequence preserves the stock-first product promise and avoids delaying the weekly decision workflow for secondary data ambitions.
