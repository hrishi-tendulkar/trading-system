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

## [2026-05-25] Promote only the sleeves the replay actually earned
**Decision** · Source: `docs/research/market/sp100-canonical-strategy-replay-2026-05-25.md`
The current live mainline should be narrower than the four-strategy canonical architecture: `Breakout Confirmation` is promoted now, `Sector-Confirmed Pullback Continuation` is promoted only as a narrowed trust-calibrated sleeve, `ETF Trend / Rotation` remains canonical but not mainline-promoted, and `Selective Mean Reversion` remains research only.
**Why it matters:** This keeps the finance doctrine honest about what has actually been validated and prevents product surfaces from implying equal trust across unequal sleeves.

## [2026-05-25] The weekly board should only consume promoted sleeves
**Decision** · Source: `docs/strategy/weekly-board-assembly-spec.md`
The weekly board is a promotion layer after per-strategy evaluation; canonical status alone does not make a sleeve board-eligible.
**Why it matters:** This preserves strategy separation, sparse-board discipline, and source-strategy lineage while avoiding quiet fallback to a blended ranking model.

## [2026-06-02] Strategy 1 promotion is narrowed to supportive sector-confirmed breakouts
**Decision** · Source: `docs/research/market/strategy1-breakout-refinement-2026-06-02.md`
`Breakout Confirmation` remains promoted only when the breakout is triggered, market regime is `Risk-on` or `Selective risk-on`, and sector context is confirmed. The broad current breakout baseline remains research context because it missed the `SPY` buy-and-hold hurdle and had worse drawdown.
**Why it matters:** This prevents the strongest sleeve from being overclaimed and keeps board eligibility tied to the rule variant that actually cleared the promotion bar.

## [2026-06-07] Strategy 1 v2 is the production weekly rule
**Decision** · Source: `scripts/mlp/run_watchlist_analysis.py`
`breakout-confirmation.v2` is now wired into weekly generation: triggered supportive sector-confirmed breakouts become `Buy now`, while near-trigger setups remain `Wait for confirmation`.
**Why it matters:** The weekly report now uses the same measurable Strategy 1 rule that was validated in replay instead of the older broad breakout interpretation.

## [2026-06-07] Selective Mean Reversion remains research-only after defensive/stress replay
**Decision** · Source: `docs/research/market/selective-mean-reversion-refinement-2026-06-07.md`
Defensive and stress-only rebound variants were tested with daily `OHLCV`, `20 bps` friction, weekly top-`5` portfolios, `5D` / `10D` / `15D` holds, `SPY` buy-and-hold, and exposure-aware `SPY`. The best `stress_v1` `15D` variant beat exposure-aware `SPY` by `+6.10%` annualized but lagged `SPY` buy-and-hold by `-7.22%` annualized and had `43.04%` of signals in one year.
**Why it matters:** Selective Mean Reversion may remain an appendix research lens, but it should not receive sandbox, paper-live, or fresh-capital board promotion without stronger, less regime-concentrated evidence.

## [2026-06-07] Ranked weekly ETF rotation stays research-only
**Decision** · Source: `docs/research/market/etf-trend-rotation-refinement-2026-06-07.md`
`ETF Trend / Rotation` was retested as a ranked weekly ETF-only sleeve across top `1`/top `2`, broad versus sector ETF treatment, regime gates, RS windows, volatility caps, and friction sensitivity. The best variant beat exposure-aware `SPY` but missed `SPY` buy-and-hold by `8.28%` annualized after `20 bps` friction, so `etf-trend-rotation.v2` is not promoted.
**Why it matters:** ETF rotation can remain an exposure appendix or context lens for cleaner group exposure, but it should not feed the main action board as promoted `Buy now` logic.

## Patterns

## [2026-05-22] Event reaction matters more than static facts alone
**Pattern** · Source: `docs/finance/frameworks/weekly-equity-intelligence-analysis-framework.md`
Guidance changes, revisions, and post-event price behavior often matter more than isolated absolute metrics.
**Why it matters:** Signal design should capture changing expectations and market reaction, not just trailing fundamentals.

## [2026-05-23] Better short-term results are more likely to come from fewer bad entries than from more aggressive prediction
**Pattern** · Source: `docs/finance/frameworks/daily-data-short-term-strategy-upgrade.md`
In the current daily-data-only stack, the biggest improvement lever is filtering out extended, low-clarity, and regime-misaligned entries rather than expanding indicator breadth.
**Why it matters:** This points the strategy toward decision quality and expectancy discipline instead of indicator accumulation.

## [2026-06-02] Stricter momentum filters can select later breakouts instead of better breakouts
**Pattern** · Source: `docs/research/market/strategy1-breakout-refinement-2026-06-02.md`
Leadership-quality and strict-entry variants sounded appealing but reduced risk-adjusted performance versus the simpler supportive sector-confirmed breakout rule.
**Why it matters:** Future refinements should test board construction and exposure caps before adding more relative-strength thresholds to Strategy 1.

## [2026-06-07] Stress-only mean reversion can beat sparse SPY exposure but still fail capital allocation
**Pattern** · Source: `docs/research/market/selective-mean-reversion-refinement-2026-06-07.md`
The stronger Selective Mean Reversion variants showed positive exposure-aware excess but still materially lagged `SPY` buy-and-hold after friction.
**Why it matters:** Sparse-sleeve benchmarks are necessary but not sufficient; a rebound sleeve should not be promoted merely because it beats a low-exposure benchmark while failing the user's main capital hurdle.

## Don'ts

## [2026-05-22] Do not recommend options without a valid stock thesis
**Don't** · Source: `docs/strategy/weekly-equity-intelligence-strategy-blueprint.md`
Covered calls and cash-secured puts should only appear after the underlying equity case has already passed eligibility checks.
**Why it matters:** This keeps overlay suggestions aligned with capital ownership logic instead of premium-chasing.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
