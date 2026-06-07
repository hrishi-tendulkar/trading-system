# Medium-Term Strategy Operating System Vision

## Purpose

Define the medium-term operating vision for Trading System.

The product should not remain only a weekly report generator. The weekly report is the primary user-facing output, but the system we are building toward is a single-operator strategy operating system: a disciplined loop for developing, improving, promoting, running, and reviewing short-term trading strategies at personal scale.

## Vision

Trading System should borrow the useful operating discipline of mature short-term trading firms without copying their full infrastructure, staffing model, intraday workflow, or execution stack.

At this scale, the goal is not to run dozens of strategies or trade in real time. The goal is to apply the same core discipline to the current four canonical strategies:

- define each strategy clearly,
- test and improve strategy versions,
- promote only validated versions into weekly production,
- generate the weekly report from the latest promoted strategy set,
- track what would have happened if the weekly strategy calls were followed,
- and use that evidence to refine, demote, or retire strategies over time.

## Operating Model

The medium-term system should support six linked loops.

### 1. Strategy Library

Maintain a small set of explicit strategy families rather than one blended ranking model.

The current starting library is:

- `ETF Trend / Rotation`
- `Sector-Confirmed Pullback Continuation`
- `Breakout Confirmation`
- `Selective Mean Reversion`

The system may later support more strategies, but the near-term priority is to run the current four with professional discipline.

### 2. Strategy Research And Refinement

Each strategy should be improvable over time through research variants, threshold changes, regime filters, entry rules, suppressors, and evidence review.

New ideas should move through a lifecycle:

- `idea`
- `research`
- `backtesting`
- `paper_live`
- `promoted`
- `retired`

Research variants should not automatically affect weekly recommendations.

### 3. Promotion Into Weekly Production

Only promoted strategy versions should feed the weekly action board.

The weekly report should use a pinned strategy registry version so it is always clear which strategy versions were active for that report. This protects the product from mixing research logic with fresh-capital decisions.

### 4. Weekly Report Generation

Each weekly run should evaluate the active promoted strategy versions, produce per-strategy candidates, apply risk suppressors, and then assemble the final board.

The board is not the source of truth. It is the production promotion layer after strategy evaluation.

### 5. Backtesting And Replay

Every meaningful strategy version should be replayable against historical data where the available data supports it.

Backtests should answer:

- how the strategy performed,
- which regimes helped or hurt it,
- whether it beat the relevant benchmark,
- whether drawdown and trade frequency were acceptable,
- and whether the evidence is strong enough for promotion.

### 6. Live Weekly Outcome Review

The system should also evaluate each published weekly run after the fact.

This review should answer:

- what happened to each weekly recommendation,
- whether entries, stops, targets, and invalidations behaved as expected,
- whether skipped or suppressed names would have helped or hurt,
- whether a strategy is improving, decaying, or regime-dependent,
- and what should be changed in the next strategy version.

This live review is different from historical backtesting. It is the ongoing honesty layer for the actual weekly operating process.

## Product Implications

The product should continue to feel like a weekly decision cockpit for one user.

The strategy operating system should appear through better weekly outputs, sharper strategy pages, archive review, and outcome scorecards rather than through a complex institutional dashboard.

Near-term product surfaces should preserve:

- weekly report as the main decision session,
- daily checks as exception handling,
- strategy pages as live operating surfaces,
- archive as historical accountability,
- and outcomes as the learning loop.

## Finance Implications

The finance layer should keep strategies, risk rules, and context lenses separate.

Each strategy should have:

- a clear behavioral thesis,
- measurable rules,
- decision-time data requirements,
- expected holding period,
- invalidation logic,
- regime assumptions,
- failure modes,
- replay evidence,
- and promotion status.

The system should not overclaim edge. A canonical strategy can remain research-only until evidence earns promotion.

## Engineering Implications

The architecture should treat strategies as versioned operating assets.

Required contracts include:

- strategy definitions,
- strategy versions,
- strategy registry versions,
- per-strategy candidate evaluations,
- risk suppressors,
- board promotion records,
- weekly published runs,
- backtest runs,
- and live outcome records.

Each weekly run should pin:

- input snapshot,
- engine version,
- strategy registry version,
- active strategy versions,
- generated candidates,
- suppressors,
- promoted board rows,
- and output snapshot.

This allows the system to improve strategy logic without mutating old reports or losing the ability to explain past decisions.

## Build Guidance

Build fast, but keep the bare bones scalable:

- start with the four current canonical strategies,
- keep CSV/file-backed bridges acceptable while contracts are stabilizing,
- avoid collapsing strategy evaluation into one monolithic recommendation table,
- promote only evidence-backed strategy versions into the board,
- store enough run and outcome history to support review,
- and make the eventual database shape match the strategy operating loop.

The point is not to overbuild. The point is to make sure each fast iteration strengthens the same operating spine.

## Success Criteria

The medium-term vision is working when Trading System can answer:

- Which strategy versions are active this week?
- Why are these versions promoted?
- Which candidates did each strategy produce?
- Which candidates were suppressed and why?
- Which names made the final board?
- What happened after the weekly report was published?
- Which strategy versions are improving, decaying, or ready to retire?
- What should be changed in the next research cycle?

If the system can answer those questions for four strategies, it can later support more strategies without changing its core operating model.
