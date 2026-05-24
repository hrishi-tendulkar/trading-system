# Weekly Equity Intelligence Analysis Framework

## Purpose

Define the full analysis framework for the Weekly Equity Intelligence system. This document specifies:

- what quantitative analysis will be performed,
- how that quantitative analysis will be validated and backtested before production use,
- what qualitative analysis will be performed,
- and how the qualitative layer should support, refine, or challenge the quantitative layer.

This framework is intended to sit underneath the strategy and product documents and act as the canonical research-method reference for future implementation.

Related documents:

- [Weekly Equity Intelligence Strategy Blueprint](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/weekly-equity-intelligence-strategy-blueprint.md)
- [Weekly Equity Intelligence PRD](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/weekly-equity-intelligence-prd.md)

## Objective

Build a repeatable weekly stock-selection process for:

- long-only equity entries,
- holding and trimming decisions,
- cash-secured put candidates,
- and covered-call candidates.

The analysis framework should be:

- quantitative-first,
- explainable,
- testable,
- and supported by qualitative evidence rather than dominated by it.

## Core design principles

- Use quantitative analysis as the primary engine for ranking and decision support.
- Use qualitative analysis to validate, refine, or disqualify quantitative candidates.
- Keep short-term timing analysis separate from longer-term business-quality analysis.
- Keep stock-selection logic separate from options-overlay logic.
- Require every recurring signal to be measurable, storable, and backtestable where possible.
- Preserve enough historical context to understand why a recommendation was made at a point in time.

## First-principles foundation

This framework should be grounded in a small set of first principles rather than in a long list of market jargon.

### First principle 1: Price is the market's current clearing mechanism

What matters:

- Price reflects the balance between buyers and sellers.
- Persistent outperformance often signals real demand before the full narrative is obvious.

What does not automatically follow:

- Price strength alone does not prove business strength.

### First principle 2: Trends persist more often than random intuition suggests, but not forever

What matters:

- Stocks that are already acting well often continue to act well.
- Entries still matter because even strong stocks can be poor buys when extended.

What does not automatically follow:

- Every breakout or green candle is meaningful.

### First principle 3: Expectations move stocks more than absolute results

What matters:

- Revisions, guidance changes, and post-event reactions often matter more than static valuation or trailing metrics.

What does not automatically follow:

- Positive news is not enough if price rejects it.

### First principle 4: Business quality affects how long a position deserves our capital

What matters:

- Stronger businesses generally deserve more patience and larger tolerance for noise.

What does not automatically follow:

- A great business is always a good trade today.

### First principle 5: Risk control is part of edge, not a separate topic

What matters:

- Position sizing, stop logic, event awareness, and reward-to-risk determine whether an edge survives real-world trading.

What does not automatically follow:

- A high hit rate guarantees a good strategy.

## Reviewer lens: burden of proof for every analysis type

Every signal or analysis category must answer five questions before it earns a place in production:

1. What causal or behavioral logic explains why this signal might work?
2. Can it be measured consistently with available data?
3. Can it be known at decision time without look-ahead bias?
4. Does it add information beyond simpler signals already in the model?
5. Can it change a real portfolio decision, not just describe the chart nicely?

If a signal fails these tests, it should either be removed, downgraded to research-only status, or treated as an explanatory aid rather than a production input.

## Analysis stack overview

The system should analyze each stock through four layers:

### 1. Market regime analysis

Question:

- Is this a favorable environment to deploy capital aggressively, selectively, or defensively?

### 2. Quantitative stock analysis

Question:

- Does the stock show measurable evidence of attractive short-term tradeability and/or longer-term conviction?

### 3. Qualitative company and event analysis

Question:

- Does the narrative, management commentary, filing language, and event context support or weaken the quantitative case?

### 4. Recommendation synthesis

Question:

- Given the combined evidence, should the system recommend buying now, waiting, holding, trimming, or using an options overlay?

## Core analytical spine

If the framework becomes too complicated, fall back to this backbone:

1. `Regime`
- Should we be aggressive, selective, or defensive with new risk?

2. `Price and relative strength`
- Is the stock acting better than the market and its peer group?

3. `Setup and risk geometry`
- Is there a clean entry, invalidation, and favorable reward-to-risk?

4. `Event and fundamental filter`
- Is there supportive earnings, revision, or business context, and are there any major disqualifiers?

5. `Qualitative red-team`
- Is there anything in filings, transcripts, or disclosures that should confirm, refine, or kill the idea?

6. `Execution choice`
- Should this be expressed as stock, cash-secured put, covered call, or no action?

This should be the default decision path. Any additional layer must prove that it improves this core spine rather than merely describing it in more words.

## Part 1: Quantitative analysis framework

The quantitative layer is the core engine of the system.

It should produce:

- ranked stock candidates,
- explicit setup classifications,
- entry and exit levels,
- risk filters,
- and separate stock and options-overlay recommendations.

## Quantitative analysis categories

### 1. Market regime analysis

Purpose:

- Determine whether the system should be aggressive, selective, or defensive.

Metrics:

- `SPY` trend structure
- `QQQ` trend structure
- Sector ETF leadership and breadth
- Percentage of stocks above key moving averages in the active universe
- Breakout success rate in recent weeks
- Post-earnings continuation success rate in recent weeks
- Volatility regime proxies

Outputs:

- `Risk-on`
- `Selective risk-on`
- `Neutral`
- `Defensive`

Why it matters:

- The same setup performs differently in different market conditions.
- Regime should affect position sizing, number of new entries, and willingness to sell puts or write calls.

### 2. Trend and structure analysis

Purpose:

- Determine whether price structure is supportive of a near-term long trade.

Metrics:

- Price vs `10DMA`, `20DMA`, `50DMA`, and `200DMA`
- Slope of key moving averages
- Higher highs / higher lows structure
- Distance from recent breakout point
- Distance from key support and resistance zones
- Multi-week base formation
- Trend-channel integrity

Outputs:

- Trend strength score
- Structure quality score
- Support and resistance map
- Entry-zone candidates

### 3. Relative strength analysis

Purpose:

- Identify whether a stock is outperforming the market and its peer group.

Metrics:

- Relative performance vs `SPY`
- Relative performance vs sector ETF
- Relative performance over `1`, `4`, `8`, and `12` weeks
- Rate of change in relative strength
- Leadership persistence

Outputs:

- Relative strength score
- Leader / neutral / laggard classification

Why it matters:

- Strong short-term opportunities tend to occur in stocks already outperforming.

### 4. Volume and participation analysis

Purpose:

- Confirm whether price action is being supported by meaningful participation.

Metrics:

- Volume ratio vs trailing average
- Up-volume vs down-volume behavior
- Volume on breakout days
- Volume on pullbacks
- Accumulation/distribution proxies

Outputs:

- Participation score
- Accumulation / neutral / weak participation label

### 5. Volatility, compression, and expansion analysis

Purpose:

- Identify clean setup structures before or during expansion moves.

Metrics:

- ATR and ATR trend
- True-range contraction
- Range-tightening over multi-week periods
- Bollinger bandwidth or similar compression proxy
- Expansion confirmation after breakout or gap

Outputs:

- Compression score
- Expansion confirmation score
- Extended vs constructive state

### 6. Support, resistance, and risk geometry

Purpose:

- Convert chart structure into actionable trade levels.

Metrics:

- Prior breakout zones
- Recent swing highs and lows
- Pivot levels
- Moving-average support zones
- Gap-support zones
- ATR-based stop distance
- Reward-to-risk ratio to first and second targets

Outputs:

- Preferred entry zone
- Stop / invalidation level
- Target 1
- Target 2
- Reward-to-risk estimate

Why it matters:

- Recommendations should be actionable, not just directional opinions.

### 7. Event and catalyst analysis

Purpose:

- Incorporate measurable event-driven behavior into stock ranking.

Metrics:

- Earnings date proximity
- Post-earnings gap direction and hold rate
- Post-earnings drift over `1`, `5`, `10`, and `20` days
- Guidance raise / maintain / cut flag
- Analyst estimate revision count and direction
- Target-price change cluster count
- Major filing-event frequency

Outputs:

- Catalyst score
- Event-risk flag
- Post-earnings continuation candidate label
- Revision-momentum label

### 8. Fundamental trend analysis

Purpose:

- Separate technically strong but fragile stocks from those with stronger business support.

Metrics:

- Revenue growth trend
- Gross margin trend
- Operating margin trend
- EPS trend
- Free-cash-flow trend
- Guidance trend
- Estimate revision trend
- Balance-sheet sanity checks

Outputs:

- Fundamental quality score
- Improving / stable / weakening label

### 9. Options overlay analysis

Purpose:

- Decide whether stock, covered call, or cash-secured put is the best expression after the stock thesis is already approved.

Metrics:

- Option-chain liquidity
- Bid/ask spread quality
- Open interest
- Days to expiration
- Moneyness
- Implied volatility
- Premium yield
- Annualized premium yield
- Distance from preferred assignment or call-away price
- Event proximity, especially earnings

Outputs:

- Covered-call suitability score
- Cash-secured-put suitability score
- Overlay disqualification flags

Important rule:

- Options analysis is subordinate to stock analysis.
- Attractive premium alone is never enough.

## Quantitative composite outputs

The system should generate separate scores rather than one opaque number.

### A. Tradeability score

Built from:

- trend and structure,
- relative strength,
- participation,
- compression/expansion,
- catalyst path,
- and risk geometry.

### B. Conviction score

Built from:

- fundamental quality,
- estimate revisions,
- guidance trajectory,
- and business stability proxies.

### C. Overlay suitability score

Built from:

- option liquidity,
- premium attractiveness,
- strike suitability,
- and event-risk filters.

### D. Risk penalty

Built from:

- event risk,
- technical extension,
- poor reward-to-risk,
- liquidity issues,
- and regime mismatch.

## Setup classification

Each candidate should be mapped to one of a small set of explicit decision bases.

Use these terms:

- `Trade setup`: a repeatable tactical pattern with entry rules, invalidation, and an expected holding period
- `Risk rule`: a rule that suppresses or modifies action even when a chart looks acceptable
- `Context lens`: a market or benchmark interpretation aid that informs the call but is not itself a stock-picking edge

Current examples:

- `Constructive pullback continuation` as a `trade setup`
- `Breakout confirmation` as a `trade setup`
- `Post-earnings continuation` as a `trade setup`
- `Revision momentum` as a `trade setup`
- `Index trend follow-through` as a `trade setup`
- `Event freeze before earnings` as a `risk rule`
- `Benchmark trend reference` as a `context lens`
- `Cash-secured put entry` as an options expression
- `Covered-call income overlay` as an options expression

This is important because true trade setups can be backtested separately, while risk rules and context lenses should be evaluated based on whether they improve decision quality and reduce obvious mistakes.

## Adversarial review of the framework

This section intentionally argues against the framework's own components so that only the highest-value analysis survives.

### 1. Market regime analysis

Argument against:

- Regime labels can become hand-wavy excuses for changing behavior after the fact.
- If the definition is loose, the system may simply become a market-timing machine with weak discipline.

Argument for:

- Many setups behave very differently in strong tapes versus weak tapes.
- Regime does not need to predict the market perfectly; it only needs to improve aggression, selectivity, and risk sizing.

First-principles conclusion:

- Keep regime analysis, but keep it simple and rule-based.
- Use it to scale risk and selectivity, not to replace stock selection.

### 2. Trend and structure analysis

Argument against:

- Chart patterns are often described after the move and can become subjective.
- Too many pattern labels create inconsistency and overfitting.

Argument for:

- Short-term trading depends on whether other market participants are already supporting price.
- A stock above key moving averages with intact higher highs and higher lows is objectively in better shape than one below them.

First-principles conclusion:

- Keep trend and structure analysis as a core input.
- Prefer simple, measurable definitions over discretionary chart storytelling.

### 3. Relative strength analysis

Argument against:

- Relative strength can crowd the system into already-extended names.
- In sudden rotations, yesterday's leaders can fail quickly.

Argument for:

- Money tends to concentrate in leaders.
- For short-term longs, buying laggards usually requires stronger evidence than buying leaders.

First-principles conclusion:

- Keep relative strength as a core filter.
- Pair it with entry discipline so the system does not blindly chase.

### 4. Volume and participation analysis

Argument against:

- Volume is noisy, distorted by events, and easy to over-interpret.
- Many successful trends continue even without beautiful volume signatures.

Argument for:

- Clean breakouts and healthy pullbacks are more trustworthy when participation supports them.
- Volume is not a thesis, but it is useful confirmation.

First-principles conclusion:

- Keep volume analysis as a confirming signal, not a dominant one.
- Do not reject otherwise strong setups solely because volume patterns are imperfect.

### 5. Volatility, compression, and expansion analysis

Argument against:

- Compression metrics can be parameter-sensitive and may create false precision.
- Many strong moves begin without textbook volatility contraction.

Argument for:

- Range tightening often reflects supply-demand balance before resolution.
- Compression is useful for identifying better reward-to-risk entries.

First-principles conclusion:

- Keep compression analysis, but mainly for setup identification and entry quality.
- Do not require it for every valid trade.

### 6. Support, resistance, and risk geometry

Argument against:

- Support and resistance can become arbitrary lines drawn after the fact.
- False precision in stops and targets can imply more certainty than exists.

Argument for:

- A trade without invalidation and reward-to-risk framing is not operationally useful.
- Even imperfect support zones are better than undefined risk.

First-principles conclusion:

- Keep support, resistance, stops, and targets as mandatory outputs.
- Use zones and scenario ranges rather than pretending to know exact levels.

### 7. Event and catalyst analysis

Argument against:

- Event-driven trading can collapse into headline chasing.
- Analysts often react after the move rather than before it.

Argument for:

- Expectations and changes in expectations are among the strongest real drivers of short-term price movement.
- Post-earnings and revision behavior often create measurable continuation patterns.

First-principles conclusion:

- Keep event and revision analysis as a core input.
- Emphasize market reaction and revision clusters more than isolated headlines or rating changes.

### 8. Fundamental trend analysis

Argument against:

- Short-term trades can work even when fundamentals are mixed.
- Fundamental datasets are slower, sometimes revised, and can add noise if overused.

Argument for:

- Fundamental improvement helps separate fragile momentum from stronger candidates worth holding longer.
- Business quality affects conviction, sizing, and willingness to stay with a winner.

First-principles conclusion:

- Keep fundamentals as a conviction layer, not the primary short-term timing engine.
- Use a smaller set of robust metrics instead of building a mini equity-research department into every trade.

### 9. Options overlay analysis

Argument against:

- Options can distract from the core equity edge and create complexity that the data stack may not support.
- Premium can look attractive while hiding poor underlying trades.

Argument for:

- Covered calls and cash-secured puts are valid expressions for a stock-first process when timing and pricing align.
- They can improve entry discipline and income generation if kept simple.

First-principles conclusion:

- Keep options as overlays only.
- If data quality is weak, degrade gracefully to stock-only recommendations.

### 10. Qualitative analysis

Argument against:

- Qualitative analysis can easily become polished storytelling with hindsight bias.
- LLM summaries may sound persuasive even when they add little signal.

Argument for:

- Filings, transcripts, and management language changes can reveal risk or strengthening trends not yet obvious in the numbers.
- Qualitative context is especially useful for disqualifying bad candidates and extending good ones.

First-principles conclusion:

- Keep qualitative analysis tightly scoped.
- Use it to confirm, refine, disqualify, or extend a quantitative case, never to substitute for one.

## Minimum viable production core

The original framework is intentionally broad. The minimum viable production system should be narrower.

### Must-have in v1

- market regime analysis
- trend and structure analysis
- relative strength analysis
- support, resistance, and risk geometry
- event and revision analysis
- basic fundamental trend scoring
- simple qualitative review for top-ranked names only

### Useful but secondary in v1

- volume and participation confirmation
- compression and expansion analysis
- deeper filing-delta analysis
- options overlays

### Research-only until proven

- any signal that cannot be timestamped reliably
- any feature that requires brittle vendor coverage
- any heavily parameterized pattern logic that lacks clear incremental value
- any scoring input that mostly duplicates price, relative strength, or event reaction without adding a distinct decision benefit

## Simplification rule

If two signals tell nearly the same story, prefer the simpler and more robust one.

Examples:

- Prefer relative strength over a large family of overlapping momentum indicators.
- Prefer simple trend structure over an elaborate library of named candlestick patterns.
- Prefer revision direction and post-earnings reaction over analyst recommendation labels.

The framework should aim to be strong because it is selective, not because it is exhaustive.

## What this framework is not allowed to become

To stay sharp, the framework must not drift into:

- a chart-annotation system that sounds insightful but does not change decisions
- a narrative engine that overrides price and risk discipline
- a factor zoo made of correlated indicators with different names
- a backtest-optimization exercise that keeps tuning until the past looks good
- an options-income layer that distracts from solving stock selection first

## Part 2: Backtesting and validation framework

The system should not go into production based on intuition alone.

Before live use, quantitative logic should be validated in stages.

## Stage 1: Signal-level validation

Goal:

- Test whether individual signals have predictive value.

Examples:

- Do stocks with strong relative strength outperform over the next `1`, `2`, `4`, and `8` weeks?
- Do tight-range breakouts outperform random entries?
- Do estimate-revision clusters improve follow-through probability?
- Does light-volume pullback behavior predict better continuation?

Method:

- Define signal buckets
- Measure forward returns by bucket
- Compare hit rates, median returns, drawdowns, and dispersion
- Segment by market regime

## Stage 2: Trade-setup validation

Goal:

- Test whether the main trade setups work as tradable strategies.

Initial trade setups to test:

### 1. Constructive pullback continuation

Example ingredients:

- strong relative strength,
- intact uptrend,
- pullback into support,
- muted pullback volume,
- favorable reward-to-risk.

### 2. Post-earnings continuation

Example ingredients:

- positive earnings and/or guidance reaction,
- price holds the post-earnings move,
- revisions continue to improve,
- sector trend remains supportive.

### 3. Breakout confirmation / breakout + compression + leadership

Example ingredients:

- multi-week compression,
- clean breakout,
- volume confirmation,
- sector leadership,
- no immediate binary event risk.

Method:

- Define explicit entry rules
- Define stop rules
- Define profit-taking rules
- Define maximum holding periods
- Evaluate across multiple market regimes

## Stage 3: Portfolio simulation

Goal:

- Test the realistic weekly decision process rather than isolated signal behavior.

Portfolio assumptions to test:

- Top `3`, `5`, or `7` weekly ideas
- Position sizing rules
- Maximum sector concentration
- Cash allocation rules
- Limit on number of new positions per week
- Stop-loss behavior
- Partial-profit rules
- Hold-beyond-target rules for high-conviction names

Costs and frictions to include:

- Commissions if relevant
- Slippage
- Spread assumptions
- Delayed signal availability

Outputs:

- CAGR or annualized return proxy
- Maximum drawdown
- Win rate
- Average gain / average loss
- Expectancy
- Exposure levels
- Regime sensitivity

## Stage 4: Forward testing before production reliance

Goal:

- Validate that the strategy still behaves sensibly in live weekly conditions.

Process:

- Run the weekly report without committing full production capital
- Record recommended entries, stops, and targets
- Track results after `1`, `2`, `4`, and `8` weeks
- Review false positives and missed winners
- Tune signals only after enough sample size exists

## Backtesting guardrails

- Avoid look-ahead bias
- Avoid survivorship bias
- Use as-of dates for fundamentals and estimates
- Distinguish announcement date from data availability date
- Segment results by market regime
- Track whether a signal works only in bull phases
- Do not overfit by adding too many thresholds too early
- Separate stock-only backtests from options-overlay backtests

## Options backtesting rule

If reliable historical option-chain snapshots are not available:

- do not claim robust historical backtests for covered-call or cash-secured-put overlays,
- limit options work to forward-screening and operational guardrails,
- and keep the stock engine production-capable on its own.

## Part 3: Qualitative analysis framework

The qualitative layer should support the quantitative layer by adding context, detecting narrative shifts, and identifying risks that are not obvious from price and financial metrics alone.

It should not replace the quantitative engine.

## Qualitative data sources

- `10-K`
- `10-Q`
- `8-K`
- Earnings call transcripts
- Investor presentations
- Management prepared remarks
- Analyst notes or revisions where available
- Material company-specific news

## Qualitative analysis categories

### 1. Guidance and management tone analysis

Questions:

- Is management more confident, more cautious, or inconsistent?
- Are they acknowledging weakness directly or avoiding it?
- Is guidance language improving or deteriorating across quarters?

Use:

- Supports interpretation of earnings reactions and revision momentum.

### 2. Narrative change analysis

Questions:

- What themes are becoming more prominent or less prominent?
- Is the company talking more about demand strength, margin pressure, competitive intensity, or customer concentration?
- Are prior growth drivers still being emphasized?

Use:

- Helps determine whether a strong chart is backed by a strengthening business narrative or just short-term enthusiasm.

### 3. Risk-factor and disclosure-change analysis

Questions:

- Did the company add or materially alter risk factors?
- Did filing language around customers, supply chain, pricing, regulation, or capital allocation change?
- Is there a new financing, restructuring, legal issue, or executive change?

Use:

- Can disqualify otherwise attractive setups if hidden risk has materially increased.

### 4. Capital allocation and execution analysis

Questions:

- Is management allocating capital sensibly?
- Are buybacks, issuance, acquisitions, or spending decisions supportive or concerning?
- Is execution consistent with the long-term thesis?

Use:

- Supports longer-term conviction scoring.

### 5. Competitive positioning analysis

Questions:

- Is there evidence of pricing power, share gains, customer stickiness, or product-cycle strength?
- Is there evidence of erosion, commoditization, or rising competition?

Use:

- Adds context to margin trends and guidance quality.

### 6. Event-context analysis

Questions:

- Was a price move driven by a real fundamental event or a weaker headline?
- Is a catalyst likely to matter for days, weeks, or longer?
- Does the market reaction make sense relative to the event?

Use:

- Helps distinguish durable setups from noise.

## Qualitative output standard

Every qualitative insight should be tagged as one of:

- `Fact`
- `Inference`
- `Unknown`

Examples:

- `Fact`: Company raised full-year revenue guidance by `4%`.
- `Inference`: Management appears more confident in enterprise demand than last quarter.
- `Unknown`: It is unclear whether margin gains are durable or temporary.

This standard prevents AI-generated commentary from being treated as hard evidence.

## Part 4: How qualitative analysis supports quantitative analysis

Qualitative work should serve one of four jobs.

### 1. Confirm

Example:

- A stock shows strong relative strength and upward estimate revisions.
- Transcript analysis confirms management confidence and broad-based demand.

Result:

- Quantitative signal is reinforced.

### 2. Refine

Example:

- A technically attractive stock has solid momentum.
- Qualitative review shows the real driver is one narrow contract announcement rather than broad business improvement.

Result:

- Keep the trade, but lower conviction and tighten risk assumptions.

### 3. Disqualify

Example:

- A stock screens well on price and revisions.
- A recent `8-K` reveals a material legal issue or financing problem.

Result:

- Remove or downgrade the candidate despite good quantitative ranking.

### 4. Extend

Example:

- A stock enters as a short-term swing candidate.
- Ongoing filings and transcript analysis show a broader, durable business acceleration.

Result:

- Candidate may graduate from tactical trade to longer-hold idea.

## Qualitative constraints

- Qualitative findings should not create recommendations without a quantitative base case.
- The system should avoid unsupported judgments about management quality or moat unless tied to evidence.
- AI-generated summaries should cite sources or source classes where possible.
- The qualitative layer should be used more heavily on top-ranked names rather than the full universe.

## Part 5: End-to-end decision flow

The weekly process should work like this:

1. Determine market regime.
2. Run quantitative analysis across the watchlist.
3. Rank names by tradeability and conviction.
4. Classify each top candidate into a decision basis.
5. Generate entry, stop, and target levels from chart structure.
6. Run qualitative analysis on the top candidates and current holdings.
7. Confirm, refine, or disqualify candidates based on qualitative evidence.
8. Evaluate whether stock, cash-secured put, or covered call is the best expression.
9. Generate the final weekly action list.
10. Store the recommendation and supporting evidence for later review.

## Part 6: Production-readiness checklist

Before the strategy is trusted in production, confirm:

- quantitative signals are defined and stored consistently,
- at least `2` to `3` strategy families have been backtested,
- results have been segmented by regime,
- stop and target logic has been tested with realistic costs,
- historical recommendation logging is working,
- qualitative outputs are clearly separated into facts, inferences, and unknowns,
- and options logic is gated by actual data availability.

## Recommended implementation sequence

### Phase 1

- Market regime analysis
- Technical and relative-strength signals
- Entry, stop, and target generation
- Weekly stock ranking

### Phase 2

- Event and revision analysis
- Fundamental trend scoring
- Setup-family backtests

### Phase 3

- Qualitative transcript and filing analysis
- Qualitative confirmation and disqualification layer
- Historical recommendation review tooling

### Phase 4

- Options overlay screening
- Forward testing of covered-call and cash-secured-put logic
- Historical options research only if chain snapshots are available

## Summary

This framework is designed so that:

- quantitative analysis drives the initial opportunity set,
- backtesting determines which quantitative signals deserve trust,
- qualitative analysis improves interpretation and risk control,
- and final recommendations remain explainable, testable, and actionable in a weekly workflow.
