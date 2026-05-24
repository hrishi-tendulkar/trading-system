# Weekly Equity Intelligence PRD

## Purpose

Define the product requirements for a weekly equity-intelligence system that converts market, company, event, and options data into a practical weekly decision workflow for a single user.

This PRD is derived from the strategy logic defined in:

- [Weekly Equity Intelligence Strategy Blueprint](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/weekly-equity-intelligence-strategy-blueprint.md)

## Product summary

The product should help the user decide, each week:

- what to buy now,
- what to buy only on pullback,
- what to hold, trim, or sell,
- and where covered calls or cash-secured puts are the preferred expression.

The product is a decision-support system. It is not an order execution engine and should not require intraday attention to be useful.

## User and context

### Primary user

- One technically capable investor managing approximately `$200,000` of short-term capital
- Prefers long-only equities plus covered calls and cash-secured puts
- Has limited weekday time and wants a weekly action-oriented output

### Primary job to be done

- Give me a concise weekly report telling me what to buy, what to watch, what to sell, and how to express the idea.

### Secondary jobs

- Track whether a trade should evolve into a longer-term hold
- Keep a historical record of recommendations and outcomes
- Reduce emotionally reactive or inconsistent decision-making

## Product goals

- Produce a high-quality weekly action list from a curated universe
- Surface the most actionable opportunities without requiring intraday monitoring
- Keep long-term conviction logic separate from short-term timing logic
- Support options overlays where they improve risk-reward
- Preserve historical evidence, scores, and outcomes for later refinement

## Non-goals

- Automated order execution
- Intraday trading or minute-by-minute alerts
- Multi-user collaboration in v1
- Complex options strategies beyond covered calls and cash-secured puts
- A black-box system that generates unexplained buy or sell calls

## Product principles

- Actionability over volume
- Explainability over opaque scoring
- Weekly consistency over constant activity
- Traceability over unsupported AI commentary
- Feasible v1 scope over overbuilt infrastructure
- Stock-first decisions, options-second overlays

## Core user outcomes

The product succeeds if the user can, once a week, quickly understand:

- which names deserve capital now,
- which names deserve patience,
- which names are breaking down,
- and when options overlays are smarter than stock alone.

## Key user workflows

### 1. Weekly review workflow

Frequency:

- Once per week, ideally over the weekend

Steps:

1. Open weekly market-regime summary.
2. Review `Buy now` list.
3. Review `Buy on pullback` watchlist.
4. Review existing holdings and recommended actions.
5. Review options overlay candidates.
6. Decide which trades to place for the week.

### 2. Daily monitoring workflow

Frequency:

- Brief check after market close on weekdays

Steps:

1. Review meaningful changes since yesterday.
2. Check earnings reactions, estimate revision clusters, and broken setups.
3. Update awareness, but avoid requiring constant intervention.

### 3. Position review workflow

Steps:

1. Open a holding detail view.
2. See original entry thesis, current scores, and updated risk levels.
3. Decide whether to keep, add, trim, or exit.

## Core outputs

### 1. Weekly action report

Must include:

- Market regime classification
- `Buy now` list
- `Buy on pullback` list
- `Hold / add` list
- `Trim / exit` list
- Options overlay candidates
- Key changes since last week

### 2. Stock recommendation card

Each recommendation should include:

- Ticker
- Company name
- Decision basis type: `trade setup`, `risk rule`, or `context lens`
- Decision basis name
- Tradeability score
- Conviction score
- Risk penalty
- Entry zone
- Stop or invalidation
- Target 1
- Target 2
- Expected holding period
- Key catalyst
- Evidence summary
- Recommended expression: stock, covered call, cash-secured put, or wait

### Standard action taxonomy

The product should use a fixed action vocabulary:

- `Accumulate now`
- `Wait for better entry`
- `Sell cash-secured put`
- `Hold existing long`
- `Write covered call`
- `Do nothing / monitor`
- `Reduce / exit on thesis deterioration`
- `Avoid due to event or risk`

### 3. Stock detail page

Must show:

- Current scores and recommendation
- Why this week
- Why not stronger
- Recent price and relative-strength context
- Upcoming events
- Fundamental trend summary
- Relevant filings and transcripts
- Analyst revision summary
- Analysis modules with findings first, then insight
- Cross-signal synthesis
- Recommendation logic tying the action, entry, stop, and target together
- Historical recommendations and outcomes
- Single-stock replay where enough history exists

### 3a. Decision-basis detail page

Must show:

- Whether the basis is a `trade setup`, `risk rule`, or `context lens`
- What the basis is trying to do
- Explicit rule spine
- Historical replay or backtest summary where available
- Current live matches
- Known failure modes or confidence limits

### 4. Daily change digest

Must highlight:

- New post-earnings candidates
- Major estimate revision changes
- Broken technical setups
- New filing or news events with likely relevance

## Functional requirements

### 1. Universe and watchlist management

The product must:

- Maintain a canonical stock universe and active watchlist
- Tag holdings, tactical candidates, and long-term candidates
- Preserve history of watchlist changes

### 2. Data ingestion

The product must ingest on scheduled cadences:

- Daily OHLCV price data
- Sector and benchmark data
- Corporate actions
- Earnings calendar and earnings results
- Fundamental statement data
- Filing metadata and selected filing text
- Earnings call transcripts
- Analyst estimate and target changes where available
- Relevant company and market news
- Options chain data for supported tickers

### 3. Feature computation

The product must compute:

- Trend and moving-average structure
- Relative strength versus benchmark and sector
- Volume and participation signals
- Volatility compression and expansion measures
- Post-earnings reaction features
- Estimate revision features
- Fundamental trend features
- Options overlay features such as premium context and liquidity checks

### 4. Scoring and recommendation engine

The product must:

- Generate a `tradeability score`
- Generate a `conviction score`
- Generate an `overlay suitability score`
- Apply risk penalties
- Produce an explainable final recommendation
- Preserve both component scores and final action labels

The product must keep these outputs distinct:

- `long_only_buy_rank`
- `covered_call_candidate_rank`
- `cash_secured_put_candidate_rank`

The product must not collapse stock quality, tactical setup quality, and option-premium attractiveness into one opaque composite.

### 5. AI-assisted qualitative analysis

The product must support:

- Summarization of filings and transcripts
- Detection of narrative changes across periods
- Extraction of structured evidence from text sources
- Labeling of outputs as facts, inferences, or unknowns where appropriate

The product must not:

- Present unsupported AI narrative as factual source data

### 6. Historical persistence and evaluation

The product must:

- Store every scored run with timestamps
- Store recommendation history by ticker
- Store realized outcome windows after recommendation
- Support later backtests of signals, trade setups, and ranking logic

### 7. Delivery and UX

The product must provide:

- A weekly summary view
- A ranked opportunities view
- A holdings review view
- A stock detail view
- A daily change summary

The product may initially deliver these through:

- a lightweight internal web app,
- a generated report,
- or both

## Data requirements

### Required for v1

#### Market data

- Daily OHLCV
- Splits and dividends
- Benchmark ETF history
- Sector ETF history
- Sector and industry classification

#### Company fundamentals

- Quarterly revenue
- EPS
- Gross margin
- Operating margin
- Free cash flow where available
- Balance-sheet basics
- Guidance data where available

#### Event data

- Earnings calendar
- Earnings result metadata
- Filing timestamps and types
- Company news timestamps and categories

#### Text data

- `10-K`, `10-Q`, and `8-K` text
- Earnings call transcripts

#### Analyst and estimate data

- Consensus estimates
- Historical estimate revisions
- Target price changes
- Recommendation changes

#### Options data

- Chain data by expiry and strike
- Implied volatility
- Delta
- Open interest
- Bid/ask spread

If historical option-chain snapshots are not available, options overlays may be supported for live weekly screening, but historical options backtesting should remain out of scope.

### Strongly recommended but not mandatory for v1

- Historical IV percentile
- Ownership or sponsorship proxies
- Cleaner sector and industry peer mappings
- Richer news classification metadata

## Source and provider strategy

The product should be provider-agnostic at the schema and service layers.

### Recommended v1 sourcing direction

- Primary bundled provider for broad market, fundamentals, calendar, analyst, and possibly transcript coverage
- Direct SEC EDGAR integration for filings and source-of-truth metadata
- OpenAI API for summarization, extraction, classification, and synthesis

### Provider design requirement

Every provider must be wrapped in an adapter layer so the system can swap vendors later without rewriting core business logic.

The stock engine must run independently of the options provider. If options data is unavailable or degraded, the weekly long-only workflow should still complete successfully.

## Intelligence cadence requirements

### Daily jobs

- Refresh market data
- Refresh event and earnings data
- Ingest new filings and transcripts
- Update analyst revision data
- Recompute features and scores for changed names

### Weekly jobs

- Recompute full-universe rankings
- Generate weekly action report
- Generate holdings review
- Generate options overlay candidates
- Persist weekly recommendations and rationale

### Event-driven jobs

- React to new earnings events
- React to material filing updates
- React to major analyst revision clusters

Event-driven processing in v1 may still remain batch-oriented rather than true real time.

## Recommendation output requirements

Each recommendation record must support:

- as-of date
- ticker
- recommendation category
- decision basis type
- decision basis name
- tradeability score
- conviction score
- overlay suitability score
- risk penalty
- entry zone
- invalidation
- target 1
- target 2
- expected holding period
- key catalyst
- evidence summary
- recommended expression

## Evaluation requirements

The product must support validation at three levels:

### 1. Signal-level evaluation

- Compare forward returns by signal strength
- Measure signal stability by market regime

### 2. Setup-family evaluation

- Compare performance across pullbacks, post-earnings continuation, revision momentum, and breakout setups
- Evaluate options overlays separately from stock-only entries

### 3. Portfolio-level evaluation

- Simulate weekly portfolios using ranked ideas
- Include slippage, trading costs, and position-sizing assumptions

## Non-functional requirements

- Reliability: scheduled jobs must be restartable and observable
- Traceability: every recommendation must tie back to source data and run time
- Modularity: providers, signals, and scoring modules must be swappable
- Cost control: the product must support a small-universe v1 without runaway API or model costs
- Reproducibility: reruns on the same data snapshot should be explainable

## V1 scope

### In scope

- Curated universe and watchlist management
- Daily batch ingestion
- Weekly recommendation generation
- Long-only recommendation logic
- Covered-call and cash-secured-put candidate logic as overlays on approved equity names
- Stock-level evidence summaries
- Historical storage of scores and recommendations
- Lightweight delivery surface

### Out of scope

- Brokerage integration
- Automated order execution
- Intraday signal generation
- Shorting workflows
- Multi-leg options strategy support
- Multi-user features
- Deep options analytics without reliable historical chain data

## Dependencies and open questions

### Dependencies

- Final provider selection and contracts
- Data model design
- Signal-definition specification
- Report and UI delivery choice

### Open questions

- What should the initial active universe size be beyond the likely `50` to `70` name v1 watchlist?
- Which data provider best balances analyst-revision depth with cost?
- Should the first output surface be a report, a dashboard, or both?
- How much recommendation logic should be deterministic rules versus model-assisted synthesis?
- What minimum options-liquidity thresholds should be enforced in v1?

## Suggested implementation phases

### Phase 1. Foundation

- Universe, watchlist, and source-adapter setup
- Market, event, and filing ingestion
- Historical storage and run tracking

### Phase 2. Core intelligence

- Feature computation
- Tradeability and conviction scorecards
- Weekly action report generation

### Phase 3. Qualitative and options overlays

- Transcript and filing analysis
- Structured evidence extraction
- Covered-call and cash-secured-put candidate generation

### Phase 4. Evaluation and refinement

- Backtesting
- Forward-testing logs
- Score and rule tuning

## Relationship to existing docs

This PRD extends and narrows the broader platform direction defined in:

- [Trading System High-Level Design](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/high-level-design.md)
- [High-Level Technical Requirements](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/engineering/requirements/high-level-technical-requirements.md)
