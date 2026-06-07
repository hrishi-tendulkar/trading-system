# Goal Prompt: Improve Sector-Confirmed Pullback Continuation

```text
/goal Refine `sector-confirmed-pullback-continuation` into a promotion-worthy next version, or prove that it should remain narrowed/research-limited.

Context:
- Work in the Trading System repo.
- Start by reading `.codex/agents/public-equity-strategist.md`, `.codex/agents/tech-architect.md`, `docs/strategy/strategy-versioning-and-revision-archive.md`, `docs/finance/FINANCE.md`, `docs/agents/CONTEXT_FINANCE.md`, `docs/agents/memory/MEMORY_FINANCE.md`, and active strategy docs.
- Current active version: `sector-confirmed-pullback-continuation.v1`.
- Current doctrine: controlled pullback in a strong stock, supportive regime preferred, sector confirmation matters, avoid deep 10-15% pullbacks, and use controlled extension bands.

Scope:
- Test explicit narrowed pullback variants by pullback depth, extension band, sector confirmation, regime, RS consistency, ATR burden, and support proximity.
- Separate live `Buy on pullback` rules from watch-only pullback candidates.
- Compare against current v1, SPY buy-and-hold, and exposure-aware SPY.
- Preserve daily OHLCV-only feasibility.
- Do not promote broad dip-buying or deep-damage rebounds as this strategy.

Promotion Bar:
- Beat current v1 on exposure-aware risk-adjusted performance.
- Beat SPY buy-and-hold by at least 3% annualized after conservative friction.
- Max drawdown must not be materially worse than SPY.
- Results must not be driven by one sector, ticker cluster, regime, or tiny sub-bucket.
- Rule set must be explainable, measurable, storable, replayable, and compatible with `config/strategy_registry.json`.

Done When:
- Produce either a new promoted version, likely `sector-confirmed-pullback-continuation.v2`, or a clear research-only/no-change decision.
- Update research docs, strategy docs, registry/versioning docs if promoted, and `MEMORY_FINANCE.md`.
- If promoted, make sure weekly report generation can use the new version and weekly manifests pin the active version.
- Include tests or a clear implementation test plan.
```
