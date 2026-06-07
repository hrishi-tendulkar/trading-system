# Goal Prompt: Improve Breakout Confirmation

```text
/goal Refine `breakout-confirmation` into the next promotion-worthy version after `breakout-confirmation.v2`, or prove that no change should be promoted.

Context:
- Work in the Trading System repo.
- Start by reading `.codex/agents/public-equity-strategist.md`, `.codex/agents/tech-architect.md`, `docs/strategy/strategy-versioning-and-revision-archive.md`, `docs/finance/FINANCE.md`, `docs/agents/CONTEXT_FINANCE.md`, `docs/agents/memory/MEMORY_FINANCE.md`, and active strategy docs.
- Current active version: `breakout-confirmation.v2`.
- Current rule: triggered close above prior 20-day high, intact trend, positive 20D/60D RS vs SPY, ATR <= 6%, within 15% of 52-week high, supportive regime, and confirmed sector.

Scope:
- Test whether board construction, ranking, same-sector caps, trigger freshness, ATR burden, volume confirmation, or trigger-proximity rules improve Strategy 1 without changing its behavioral thesis.
- Compare against current `breakout-confirmation.v2`, SPY buy-and-hold, and exposure-aware SPY.
- Preserve daily OHLCV-only feasibility unless a point-in-time dataset already exists in repo.
- Do not create a new strategy family unless the behavioral thesis changes materially.

Promotion Bar:
- Beat current `breakout-confirmation.v2` on exposure-aware risk-adjusted performance.
- Beat SPY buy-and-hold by at least 3% annualized after conservative friction.
- Max drawdown must not be materially worse than SPY or v2.
- Results must not be driven by one ticker, sector, regime, or narrow period.
- Rule set must be explainable, measurable, storable, replayable, and compatible with `config/strategy_registry.json`.

Done When:
- Produce either a new promoted version, likely `breakout-confirmation.v3`, or a clear research-only/no-change decision.
- Update research docs, relevant strategy docs, registry/versioning docs if promoted, and `MEMORY_FINANCE.md`.
- If promoted, make sure weekly report generation can use the new version and weekly manifests pin the active version.
- Include tests or a clear implementation test plan.
```
