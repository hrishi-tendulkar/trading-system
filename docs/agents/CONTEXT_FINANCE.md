# CONTEXT_FINANCE

## Decisions

## [2026-05-22] Keep tradeability, conviction, and overlay logic separate
**Decision** · Source: `docs/strategy/weekly-equity-intelligence-strategy-blueprint.md`
The system must produce distinct judgments for near-term tradeability, longer-term conviction, and options overlay suitability.
**Why it matters:** This is the core protection against misleading recommendations and unexplainable blended scores.

## [2026-05-22] Use qualitative analysis as a filter, not the primary engine
**Decision** · Source: `docs/finance/frameworks/weekly-equity-intelligence-analysis-framework.md`
Quantitative analysis should drive the ranking engine, while qualitative review confirms, refines, or disqualifies candidates.
**Why it matters:** This keeps the finance system measurable, backtestable, and less vulnerable to narrative drift.

## [2026-05-23] Distinguish trade setups, risk rules, and context lenses
**Decision** · Source: `docs/finance/FINANCE.md`
The system should not call every named row a strategy. It must distinguish trade setups from risk rules and context lenses.
**Why it matters:** This improves analytical honesty and prevents product surfaces from implying more edge than a row actually represents.

## [2026-05-23] Daily-data short-term edge should come from setup quality, not broader narrative ambition
**Decision** · Source: `docs/finance/frameworks/daily-data-short-term-strategy-upgrade.md`
Given the current data reality of daily OHLCV plus limited event history, the short-term engine should prioritize regime filters, relative-strength quality, entry discipline, and setup-level expectancy before richer event or revision logic.
**Why it matters:** This keeps the system aligned with signals we can actually store, explain, and validate today.

## Patterns

## [2026-05-22] Event reaction matters more than static facts alone
**Pattern** · Source: `docs/finance/frameworks/weekly-equity-intelligence-analysis-framework.md`
Guidance changes, revisions, and post-event price behavior often matter more than isolated absolute metrics.
**Why it matters:** Signal design should capture changing expectations and market reaction, not just trailing fundamentals.

## [2026-05-23] Better short-term results are more likely to come from fewer bad entries than from more aggressive prediction
**Pattern** · Source: `docs/finance/frameworks/daily-data-short-term-strategy-upgrade.md`
In the current daily-data-only stack, the biggest improvement lever is filtering out extended, low-clarity, and regime-misaligned entries rather than expanding indicator breadth.
**Why it matters:** This points the strategy toward decision quality and expectancy discipline instead of indicator accumulation.

## Don'ts

## [2026-05-22] Do not recommend options without a valid stock thesis
**Don't** · Source: `docs/strategy/weekly-equity-intelligence-strategy-blueprint.md`
Covered calls and cash-secured puts should only appear after the underlying equity case has already passed eligibility checks.
**Why it matters:** This keeps overlay suggestions aligned with capital ownership logic instead of premium-chasing.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
