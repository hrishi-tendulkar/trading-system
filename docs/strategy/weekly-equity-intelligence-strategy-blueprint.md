# Weekly Equity Intelligence Strategy Blueprint

## Purpose

Define the investment-research and decision framework for a weekly public-equity intelligence system designed for a single user managing approximately `$200,000` of short-term capital. The system is intended to support long-only equity trades, cash-secured puts, and covered calls with mixed holding periods, while keeping the weekly workflow simple enough for an operator with limited time during the workweek.

This document defines the strategy logic. Product and engineering requirements derived from it belong in the companion PRD.

## Strategy objective

Build a disciplined weekly decision system that answers:

1. Which stocks are the best candidates to buy this week?
2. Which stocks should only be bought on pullback or confirmation?
3. Which existing positions should be held, trimmed, or exited?
4. Where should covered calls or cash-secured puts be used instead of common stock?
5. Which names have the strongest potential to remain owned beyond the original swing horizon?

The system should optimize for repeatable decision quality, not for predicting every short-term move.

## User and operating assumptions

- One user only
- U.S. listed equities
- Long-only directionality in v1
- Options limited to covered calls and cash-secured puts
- Weekly decision cadence, with daily data refreshes and event updates
- No intraday execution or minute-by-minute monitoring in v1
- No automated execution in v1
- Mixed holding periods: from several trading days to multiple months

## Strategy philosophy

The system should separate two ideas that often get blurred together:

1. Short-term tradeability
- Is this stock attractive over the next `1` to `20` trading days?

2. Longer-term conviction
- If the trade works, is this also a business we may want to keep owning longer?

This separation matters because:

- Great businesses can still have poor short-term entry timing
- Strong tactical setups can still lack durable business support
- Options overlays depend on both timing and conviction

The system should therefore generate separate scores and recommendations for:

- Near-term tradeability
- Longer-term conviction
- Options overlay suitability

## Decision precedence

The system should follow these precedence rules:

1. Equity thesis comes before options overlay.
- Covered calls and cash-secured puts are expressions of an underlying equity view, not independent alpha engines.

2. Weak business quality cannot be rescued by attractive option premium.
- If conviction is weak, the system should suppress aggressive options recommendations.

3. Weak timing can still coexist with strong conviction.
- A stock may remain a valid longer-term hold while being a poor weekly entry.

4. Options overlays should only appear after stock eligibility is established.
- Covered calls only on stocks the user is comfortable continuing to own or sell at the strike.
- Cash-secured puts only on stocks the user genuinely wants to own if assigned.

## Weekly decision outputs

Each weekly run should produce a compact action list grouped into:

### 1. Buy now

High-priority long entries for the coming week.

Required fields:

- Ticker
- Setup type
- Entry zone
- Initial stop or invalidation
- Target 1
- Target 2
- Expected holding period
- Key catalyst
- Confidence band
- Recommended expression: stock, cash-secured put, or wait

### 2. Buy on pullback

Names with good underlying quality but unattractive immediate entry.

Required fields:

- Ticker
- Preferred buy zone
- Support level
- What must remain true for entry
- Trigger expiry if applicable

### 3. Hold or add

Existing positions that remain valid.

Required fields:

- Ticker
- Keep / add / reduce label
- Updated stop
- Updated targets
- What improved or deteriorated this week

### 4. Trim or exit

Names where either the setup has failed, the target was reached, or the thesis materially weakened.

Required fields:

- Ticker
- Exit reason
- Immediate action
- Whether a re-entry setup should be watched

### 5. Options overlay

Stocks where covered calls or cash-secured puts improve the risk-reward tradeoff relative to buying or holding common stock alone.

Required fields:

- Ticker
- Overlay type
- Target expiry window
- Preferred strike logic
- Why overlay is preferred
- Key risks

## Strategy universe design

The strategy should operate on a curated universe rather than the full market.

### Core universe

- Roughly `50` to `70` primary watchlist names in v1, with room to expand later
- Average daily dollar volume above a minimum threshold
- Sector representation broad enough to avoid concentration in one theme
- Includes current holdings, high-conviction watchlist names, and tactical momentum candidates

### Optional outer universe

- `SPY`, `QQQ`, and sector ETFs for regime and relative-strength context
- Benchmark leaders and laggards for comparison

### Exclusions for v1

- Microcaps
- Illiquid small caps
- Highly event-driven biotech binary setups
- Complex options structures beyond covered calls and cash-secured puts

## Decision bases to support

The first version should focus on a small set of explicit decision bases that are understandable, testable, and consistent with weekly review.

Important terminology:

- `Trade setup`: a repeatable tactical pattern with entry rules, invalidation logic, expected holding period, and a path to historical replay
- `Risk rule`: a rule that suppresses or modifies action even when a chart looks acceptable
- `Context lens`: a market or benchmark interpretation aid that informs decisions but is not itself a stock-picking edge

This matters because not every named row on the page should be called a `strategy`. Some are true trade setups, some are risk controls, and some are context.

### 1. Constructive pullback continuation

Type:

- `Trade setup`

Characteristics:

- Strong relative strength versus benchmark and sector
- Uptrend remains intact
- Pullback into support or moving-average confluence
- Pullback is not too extended above the `20-day` average
- No major thesis damage

### 2. Breakout confirmation

Type:

- `Trade setup`

Characteristics:

- Trend is still intact
- Price is close enough to resistance that a defined trigger level exists
- Relative strength is acceptable but not strong enough yet for an immediate buy
- The system prefers proof through resistance over a blind early entry

### 3. Index trend follow-through

Type:

- `Trade setup`

Characteristics:

- Broad market ETF remains above key moving averages
- Volatility is controlled
- User wants broad market exposure rather than single-name idiosyncratic risk

### 4. Event freeze before earnings

Type:

- `Risk rule`

Characteristics:

- Earnings are close enough that the next move is likely to be event-dominated
- Fresh swing entries are suppressed by default
- Existing positions may still be held or reassessed rather than forced into a new buy/sell call

### 5. Benchmark trend reference

Type:

- `Context lens`

Characteristics:

- `SPY` or equivalent benchmark is used to anchor market posture
- Relative strength comparisons are defined against the benchmark
- The benchmark row informs selectivity and aggression but is not itself the central stock-picking edge

### 6. Cash-secured put entry

Characteristics:

- Desired stock is attractive, but current chase risk is high
- There is a clear preferred ownership price below spot
- Premium is adequate relative to the risk of assignment
- Liquidity and spreads are acceptable
- No disqualifying binary event is immediately ahead by default

### 7. Covered call income overlay

Characteristics:

- Stock is already owned
- Near-term upside is likely more moderate than explosive
- Investor is willing to trim or exit near the strike
- Implied premium is attractive relative to capped upside
- No disqualifying binary event is immediately ahead by default

## Signal framework

The system should organize signals into five families and avoid compressing everything into one opaque score.

### 1. Market regime and context

Purpose:

- Determine whether the environment supports aggressive deployment, selective deployment, or defense

Core signals:

- Benchmark trend structure
- Breadth proxies
- Sector leadership concentration
- Volatility regime
- Recent performance of breakout and post-earnings setups

Example output:

- `Risk-on`
- `Neutral/selective`
- `Defensive`

### 2. Short-term tradeability signals

Purpose:

- Evaluate whether a stock is actionable over the next several days to weeks

Core signals:

- Relative strength vs `SPY`
- Relative strength vs sector ETF or peer group
- Moving-average structure
- Distance from support or breakout
- Pullback quality
- Volume confirmation
- Volatility compression and expansion
- Post-earnings reaction quality
- Upcoming catalyst within `1` to `4` weeks
- Estimate revision direction

### 3. Longer-term conviction signals

Purpose:

- Evaluate whether a stock deserves longer holding tolerance if the trade works

Core signals:

- Revenue growth durability
- Margin trend
- Guidance trajectory
- Free-cash-flow quality
- Balance-sheet sanity
- Management execution consistency
- Business durability and category position
- Valuation sanity relative to growth and margins

### 4. Options overlay signals

Purpose:

- Decide whether stock ownership, covered calls, or cash-secured puts best express the idea

Core signals:

- Conviction in owning the stock
- Preferred entry or exit zone
- Time decay capture opportunity
- Implied volatility context
- Option chain liquidity and spreads
- Probability of willing assignment or called-away shares

### 5. Risk and crowding signals

Purpose:

- Avoid setups that look attractive but are poorly timed or overly fragile

Core signals:

- Extended distance from support
- Binary event exposure
- Crowded one-way move
- Recent failed breakouts in the same group
- Weak market-regime fit
- Liquidity risk

## Score design

The system should use component scores and a recommendation layer rather than a single black-box ranking.

### Proposed scorecard

#### A. Tradeability score

Range: `1` to `5`

Inputs:

- Trend structure
- Relative strength
- Participation
- Compression/expansion quality
- Catalyst path
- Timing and risk

#### B. Conviction score

Range: `1` to `5`

Inputs:

- Growth quality
- Profitability quality
- Guidance and revisions
- Business durability
- Management execution
- Valuation context

#### C. Overlay suitability score

Range: `1` to `5`

Inputs:

- Covered call suitability
- Cash-secured put suitability
- Common-stock preference strength

#### D. Risk penalty

Range: `0` to `3`

Inputs:

- Event risk
- Technical extension
- Liquidity concerns
- Regime mismatch

### Recommendation logic

The final recommendation should be rules-based and explainable. Example logic:

- High tradeability + high conviction + low risk penalty -> `Buy now`
- High conviction + moderate tradeability + poor entry -> `Buy on pullback`
- High conviction + stretched entry + attractive premium -> `Cash-secured put`
- Existing position + moderate upside + attractive premium -> `Covered call`
- Low tradeability or broken structure -> `Avoid / exit / do not add`

### Standard action taxonomy

Use a fixed action set:

- `Accumulate now`
- `Wait for better entry`
- `Sell cash-secured put`
- `Hold existing long`
- `Write covered call`
- `Do nothing / monitor`
- `Reduce / exit on thesis deterioration`
- `Avoid due to event or risk`

## Position and risk framework

The system should support a disciplined portfolio framework rather than generate isolated ideas without sizing context.

### Initial portfolio guardrails

- Target `5` to `10` active positions
- Position sizes generally in the `8%` to `15%` range, subject to liquidity and conviction
- Allow meaningful cash when opportunity quality is weak
- Cap exposure to one sector or theme
- Do not force new positions when the regime is unfavorable

### Trade-level rules to support

- Initial stop or invalidation
- Profit target zones
- Rules for moving stops
- Rules for holding beyond Target 1 when conviction remains strong
- Rules for trimming before major binary events

### Options-specific guardrails

- Covered calls only on stocks the user is comfortable selling at the strike
- Cash-secured puts only on stocks the user genuinely wants to own if assigned
- Avoid illiquid chains or excessively wide spreads
- Avoid overusing options to compensate for weak underlying setups
- Block options overlays around earnings or major binary events by default

## Qualitative research framework

The system should incorporate qualitative research, but only in structured ways that can later be compared and tested.

### Primary source types

- `10-K`
- `10-Q`
- `8-K`
- Earnings call transcripts
- Investor presentations
- Analyst revisions and rating changes
- Company-specific news

### What qualitative work should detect

- Guidance tone shifts
- Repeated themes becoming stronger or weaker
- Evidence of execution strength or slippage
- Capital-allocation changes
- Pricing-power commentary
- Demand durability commentary
- Risk-factor changes
- Language that suggests business deterioration before the numbers fully show it

### Evidence standards

Each qualitative conclusion should be logged as:

- Fact
- Inference
- Unknown

The system should not elevate AI-generated narrative summaries to the same status as hard data without clear labeling.

## Weekly operating cadence

### Daily background processing

- Refresh end-of-day market data
- Update earnings calendar and major event data
- Capture analyst estimate and target changes
- Ingest new filings, transcript availability, and material news
- Recompute stock-level features

### Weekly decision run

Recommended timing:

- Friday after close or over the weekend

Weekly workflow:

1. Classify overall market regime.
2. Re-rank the stock universe on tradeability and conviction.
3. Review new post-earnings and revision-based opportunities.
4. Identify current holdings that changed status.
5. Generate recommended entries, stops, targets, and overlay candidates.
6. Produce a compact weekly action report.

### Event-triggered updates

Outside the weekly run, the system should flag:

- Earnings reactions
- Major guidance changes
- Material `8-K` events
- Significant analyst revision clusters

These should update the research context, but v1 does not need to force immediate intraday decisions.

## Data requirements

The strategy requires the following data categories.

### Market data

- Daily OHLCV
- Corporate actions
- Benchmark and sector ETF history
- Sector and industry classification

### Fundamental data

- Quarterly income-statement items
- Cash-flow items
- Balance-sheet basics
- Guidance history where available

### Estimate and analyst data

- Consensus EPS and revenue estimates
- Historical estimate revisions
- Target price changes
- Recommendation changes
- Coverage breadth

### Event data

- Earnings dates
- Earnings results
- Filing timestamps and metadata
- Company news with timestamp and category

### Text sources

- Filing text
- Earnings call transcripts
- Investor presentations where available

### Options data

- Option chains
- Implied volatility
- Open interest
- Bid/ask spreads
- Delta and time to expiry

If historical option-chain snapshots are unavailable, the system should still support live weekly filtering for overlay candidates, but should not claim robust historical backtesting for options overlays.

## Research and backtesting plan

The strategy should not be trusted without explicit validation.

### Stage 1. Signal validation

Test each signal or signal family independently:

- Does it improve forward returns over `1`, `2`, `4`, and `8` weeks?
- Does it reduce drawdowns?
- Does it add value only in certain regimes?

### Stage 2. Trade-setup validation

Test each trade setup:

- Constructive pullback continuation
- Post-earnings continuation
- Revision momentum
- Breakout confirmation / breakout from compression
- Cash-secured put entry
- Covered call overlay

Questions:

- What is the hit rate?
- What is the average gain versus loss?
- How quickly does edge decay?
- Does the setup need a regime filter?

### Stage 3. Portfolio simulation

Run weekly portfolio simulations with:

- Ranking cutoffs
- Position-size assumptions
- Maximum names held
- Stop logic
- Profit-taking logic
- Cash rules
- Transaction cost and slippage assumptions

### Stage 4. Forward testing

Before meaningful capital reliance:

- Record weekly recommendations
- Track realized outcomes
- Tag each idea by setup type, catalyst type, and regime
- Review false positives and missed winners

## Decision-review and learning loop

Each idea should be stored with:

- Recommendation date
- Setup family
- Entry and exit plan
- Scores at decision time
- Evidence summary
- Event context
- Realized outcome after `1`, `2`, `4`, and `8` weeks

This history is critical because the real edge will come from learning:

- which setups work best,
- which signals are redundant,
- when options overlays help,
- and when the system should hold more cash.

## V1 scope recommendation

### In scope

- Weekly ranking and action generation
- Daily end-of-day refresh
- Long-only stock recommendations
- Covered-call and cash-secured-put candidate identification as overlays on approved equity ideas
- Separate tradeability and conviction scoring
- Basic regime classification
- Historical logging of recommendations and scores

### Out of scope

- Intraday execution logic
- Short selling
- Leverage and margin optimization
- Complex multi-leg options strategies
- Standalone options alpha engines
- Fully autonomous order placement
- Highly customized factor research across the entire market

## Key design principles

- Keep the weekly output actionable and compact
- Separate timing from business quality
- Separate stock selection from options expression
- Prefer measurable signals to abstract narratives
- Preserve historical recommendations for learning
- Avoid forcing activity in weak regimes
- Treat data lineage and explainability as core requirements

## Companion deliverable

The product and engineering implications of this strategy are captured in:

- [Weekly Equity Intelligence PRD](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/weekly-equity-intelligence-prd.md)
