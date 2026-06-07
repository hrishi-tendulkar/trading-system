# Goal Prompt: Improve Selective Mean Reversion

```text
/goal Refine `selective-mean-reversion` into a promotion-worthy sandbox or prove that it should remain research-only.

Context:
- Work in the Trading System repo.
- Start by reading `.codex/agents/public-equity-strategist.md`, `.codex/agents/tech-architect.md`, `docs/strategy/strategy-versioning-and-revision-archive.md`, `docs/finance/FINANCE.md`, `docs/agents/CONTEXT_FINANCE.md`, `docs/agents/memory/MEMORY_FINANCE.md`, and active strategy docs.
- Current active version: `selective-mean-reversion.v1`.
- Current status: research-only/off-board. Prior replay suggested only narrow defensive/stress buckets looked interesting.

Scope:
- Test defensive or stress-regime-only rebound variants.
- Explicitly separate true mean reversion from damaged trend continuation and broad dip-buying.
- Test oversold bands, close reclaim behavior, 50DMA proximity, ATR caps, benchmark regime, sector context, and holding windows.
- Compare against SPY buy-and-hold and exposure-aware SPY.
- Preserve daily OHLCV-only feasibility.

Promotion Bar:
- A main-board promotion requires beating SPY buy-and-hold by at least 3% annualized after conservative friction and acceptable drawdown.
- A sandbox/paper-live promotion may be acceptable only if rules are narrow, evidence is stable, and the strategy remains excluded from fresh-capital board slots.
- Results must not be driven by one crash/rebound window, one sector, one ticker cluster, or tiny sample wins.
- Rule set must be explainable, measurable, storable, replayable, and compatible with `config/strategy_registry.json`.

Done When:
- Produce either a promoted sandbox/paper-live version, a true promoted version, or a clear research-only rejection.
- Update research docs, strategy docs, registry/versioning docs if status changes, and `MEMORY_FINANCE.md`.
- If promoted in any form, make clear whether it is board-eligible, appendix-only, or paper-live.
- Include tests or a clear implementation test plan.
```
