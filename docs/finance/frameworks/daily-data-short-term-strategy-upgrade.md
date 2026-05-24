# Daily-Data Short-Term Strategy Upgrade

## Purpose

Define how Trading System should improve short-term stock decisions when the practical data foundation is:

- daily OHLCV data,
- roughly `2` to `3` years of history,
- no real-time or intraday feed,
- and incomplete point-in-time event, transcript, and revision history.

This is a finance-framework refinement for the current product reality. It is not a claim that we already have a fully event-aware or institutionally complete signal stack.

## Scope

This document is specifically about:

- short-term long-only stock decisions over the next `1` to `15` trading days,
- weekly ranking and daily post-close refreshes,
- and how to get better results from the data we actually have now.

It does not redefine the longer-term conviction framework or the stock-first, options-second product posture.

## Evidence Ledger

### Facts

- The current product and MLP are built around a weekly decision cadence with daily data refreshes.
- The current MLP uses daily OHLCV, benchmark-relative metrics, ATR-style volatility, and a lightweight earnings snapshot.
- The system does not rely on intraday execution or real-time monitoring in v1.
- Historical replay is currently much stronger for technical and price-behavior signals than for event-aware signals that require point-in-time revisions, transcript deltas, or filing-language history.

### Inferences

- The near-term edge should come primarily from price structure, relative strength, risk geometry, and regime fit.
- Event-aware logic should mostly act as a guardrail or a conditional overlay unless and until richer point-in-time history is available.
- A better short-term system should behave more like a regime-filtered setup engine than a generic cross-sectional score sorter.

### Unknowns

- Which exact threshold combinations will produce the best expectancy by setup family across the target universe.
- How stable post-earnings and revision-based edges are without richer historical event datasets.
- How much setup performance changes by sector, volatility regime, and benchmark posture in the real production universe.

## Core Strategy Shift

The short-term engine should move from:

- a broad "good stock" ranking mentality

to:

- a constrained "good setup, good regime, good entry, acceptable risk" decision system.

That means the finance layer should stop rewarding raw strength too early and instead prioritize four questions in order:

1. Is the market environment supportive enough for this type of setup?
2. Is the stock behaving like a leader rather than just bouncing?
3. Is the entry still early enough to offer favorable risk geometry?
4. Does the historical behavior of similar setups justify action now?

## Operating Assumptions

The short-term strategy should assume:

- signals are evaluated after the close,
- decisions are placed for the next session or next few sessions,
- no intraday rescue is available,
- and any edge must survive overnight gaps and normal daily volatility.

This matters because many attractive-looking setups only work if they are babysat intraday. Those should be excluded by design.

## Short-Term Doctrine For Daily-Only Data

When the data is daily-only, the system should favor signals with these properties:

- visible at end of day,
- measurable without discretionary chart reading,
- robust enough to backtest over `2` to `3` years,
- and directly tied to entry quality or risk quality.

The core short-term decision stack should therefore be:

1. `Regime gate`
2. `Event freeze`
3. `Trend integrity`
4. `Relative-strength quality`
5. `Entry-quality test`
6. `Risk-geometry test`
7. `Setup-level historical expectancy`

If a candidate fails an early gate, the system should prefer `No action`, `Wait for confirmation`, or `Buy on pullback` over forcing a ranked buy.

## Signal Families To Prioritize

### 1. Regime and tape quality

Purpose:

- decide whether the system should act aggressively, selectively, or defensively.

Signals to keep:

- `SPY` and `QQQ` above or below `20DMA` and `50DMA`
- benchmark `20DMA` slope
- percentage of active universe above `20DMA` and `50DMA`
- recent success rate of the main long setups over the last `4` to `8` weeks
- simple realized-volatility regime proxy from benchmark ATR percent

Why this matters:

- the same single-name chart means different things in a healthy tape versus a sloppy tape.

### 2. Relative-strength quality

Purpose:

- separate true leaders from names that only look good in isolation.

Signals to keep:

- relative return vs `SPY` over `5`, `10`, `20`, and `60` trading days
- relative return vs sector ETF where available
- persistence of outperformance, not just one lookback
- distance from `52-week` high as a supporting context signal, not a primary edge

Preferred interpretation:

- one strong period is not enough
- multi-window strength consistency is better than a single momentum burst

### 3. Trend integrity and pullback behavior

Purpose:

- identify whether price is still in a healthy continuation structure.

Signals to keep:

- close vs `20DMA` and `50DMA`
- `20DMA` vs `50DMA`
- slope of `20DMA` and `50DMA`
- higher-low structure over the last `10` to `20` sessions
- depth of pullback from recent high
- number of recent closes above `20DMA`

Why this matters:

- short-term long setups work better when the stock is still being supported on pullbacks rather than merely recovering from damage.

### 4. Entry quality and overextension control

Purpose:

- stop the system from buying after the easiest part of the move already happened.

Signals to keep:

- extension above `20DMA`
- extension above `50DMA`
- ATR percent of price
- distance from nearest support
- reward-to-risk to first target

Preferred rules:

- strong stocks that are too extended should move to `Buy on pullback`, not `Buy now`
- a candidate should not earn a top action unless invalidation is close enough to define risk cleanly

### 5. Compression, expansion, and participation

Purpose:

- distinguish constructive energy build from noisy drift.

Signals to keep:

- `ATR` trend over `10` to `20` sessions
- range tightening over `5` to `10` sessions
- volume ratio vs `20-day` average
- breakout-day or gap-day volume confirmation

Interpretation rule:

- use these mainly as confirmation and entry-quality refiners, not as the primary ranking engine

### 6. Event awareness as a guardrail

Purpose:

- avoid converting a weekly process into event gambling.

Signals to keep:

- days to next earnings
- whether earnings occurred in the last `1` to `10` trading days
- whether there was a large recent gap move

Doctrine:

- before earnings, event logic is mostly a suppressor
- after earnings, event logic can become a setup input only if the post-event move holds over several sessions

## Priority Setup Families

The short-term system should prioritize a small set of explicit, daily-data-compatible setup families.

### 1. Constructive pullback continuation

Use when:

- trend is intact,
- relative strength is positive across multiple windows,
- pullback remains above or near `20DMA`,
- and extension has cooled enough to restore acceptable risk geometry.

Why it belongs:

- this is one of the cleanest daily-data continuation setups and is easy to explain and backtest.

### 2. Breakout confirmation

Use when:

- trend is intact,
- price is near a defined resistance or pivot zone,
- but immediate buy quality is not high enough without proof.

Why it belongs:

- it prevents premature entries and converts uncertainty into a clear trigger.

### 3. Relative-strength re-acceleration

Use when:

- the stock had prior leadership,
- momentum cooled without full technical damage,
- and relative strength turns back up before price becomes too extended.

Why it belongs:

- with daily data, this can capture second-leg opportunities that are often cleaner than first-chase breakouts.

Suggested measurable proxies:

- positive `20-day` and `60-day` relative return,
- flat to slightly positive `5-day` return,
- close reclaiming short-term support after a shallow pause,
- and no major breakdown below `50DMA`.

### 4. Post-earnings continuation

Use when:

- earnings already happened,
- the stock gapped or moved strongly,
- and that move holds through the next several sessions.

Why it belongs:

- post-event reaction is often more meaningful than the earnings headline itself.

Constraint:

- this setup should be treated as conditionally credible in live decisions, but only lightly trusted in historical validation until point-in-time earnings history is richer.

### 5. No-action / disqualification state

The system should explicitly classify names into `No action` when:

- regime is hostile,
- event risk dominates,
- relative strength is weak,
- the setup is too extended,
- or invalidation is too far away.

This is not a failure. It is part of the edge.

## Recommendation Architecture

The short-term engine should use gated decision logic instead of only sorting by one score.

### Stage 1: Hard disqualifiers

Suppress fresh `Buy now` calls when any of these are true:

- earnings within `7` calendar days
- close below `50DMA`
- negative `20-day` relative strength vs `SPY`
- ATR percent above the acceptable band for the setup
- reward-to-risk to first target below minimum threshold

### Stage 2: Setup classification

Classify only the remaining names into one setup family:

- `Constructive pullback continuation`
- `Breakout confirmation`
- `Relative-strength re-acceleration`
- `Post-earnings continuation`
- `Index trend follow-through`

### Stage 3: Entry-quality grading

Grade the setup as:

- `A`
- `B`
- `C`
- or `Fail`

Based on:

- extension,
- support proximity,
- ATR burden,
- relative-strength consistency,
- and regime fit.

### Stage 4: Historical expectancy overlay

For each setup family, attach a rolling evidence block using the last `2` to `3` years:

- sample count
- win rate
- median forward return
- average forward return
- median max drawdown before target or exit window
- regime-specific performance where sample size is sufficient

This should not be a black-box prediction. It should be a credibility check on whether the setup deserves action.

## Score Design Upgrade

The system should keep a compact scorecard, but the scorecard should support the gates rather than replace them.

### Keep

- `Tradeability score`
- `Risk penalty`
- `Setup family`
- `Entry quality grade`

### De-emphasize for short-term action

- a broad conviction-heavy composite for timing-sensitive entries
- any input that depends on revisions, transcripts, or filing deltas we do not yet store historically

### Proposed short-term component design

#### A. Regime support score

Measures:

- tape quality and whether this setup type is favored now

#### B. Leadership score

Measures:

- multi-window relative strength and trend persistence

#### C. Entry quality score

Measures:

- extension, support proximity, and breakout or pullback cleanliness

#### D. Risk geometry score

Measures:

- ATR burden, stop distance, and reward-to-risk

#### E. Event penalty

Measures:

- upcoming earnings and other obvious binary timing hazards

The final action should be rules-based, for example:

- strong regime support + strong leadership + strong entry quality + acceptable risk geometry + low event penalty -> `Buy now`
- strong leadership + good structure + poor immediate entry -> `Buy on pullback`
- intact structure but incomplete proof -> `Wait for confirmation`
- hostile event timing or weak risk geometry -> `No action`

## What Should Improve Results

With the current data foundation, the most likely path to better short-term results is not more indicator count. It is:

1. better regime filtering,
2. stricter overextension control,
3. stronger relative-strength consistency tests,
4. setup-specific rather than generic ranking logic,
5. and explicit historical expectancy by setup family.

This should improve results by reducing low-quality entries, not by claiming to predict more upside than the market offers.

## Backtesting Priorities

The next validation cycle should test:

1. each setup family separately
2. each setup with and without regime filters
3. each setup with and without overextension filters
4. expectancy by entry-quality grade
5. forward returns over `5`, `10`, and `15` trading days
6. failure rates around earnings proximity windows

Primary evaluation metrics should include:

- win rate
- median forward return
- average forward return
- downside capture or max adverse excursion proxy
- percentage of setups that become immediately extended failures

## Explicit Deferrals

The short-term engine should not pretend to have production-grade versions of these yet:

- analyst revision momentum as a historical ranking input
- transcript-tone change as a repeatable signal
- filing-language deltas as a live short-term factor
- intraday breakout quality
- same-day execution logic

Those belong later, after richer point-in-time datasets exist.

## Product and Engineering Implications

The product should surface, for every short-term candidate:

- setup family
- regime state
- entry quality grade
- key invalidation
- expected holding window
- historical expectancy block
- and the specific reason a name is `Buy now`, `Buy on pullback`, `Wait`, or `No action`

Engineering should treat these as first-class persisted fields rather than narrative-only output.

## Decision

For the current Trading System data reality, the short-term finance strategy should be:

- daily-data-first,
- regime-filtered,
- setup-family-based,
- entry-discipline-heavy,
- and explicit about where event-aware intelligence is still thin.

That is a more credible path to better decisions than broadening the model with weakly supported signals too early.
