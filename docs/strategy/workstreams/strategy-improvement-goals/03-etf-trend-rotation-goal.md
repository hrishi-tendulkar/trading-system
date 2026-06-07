# Goal Prompt: Improve ETF Trend / Rotation

```text
/goal Refine `etf-trend-rotation` into a promotion-worthy ranked rotation version, or prove that it should remain research-only.

Context:
- Work in the Trading System repo.
- Start by reading `.codex/agents/public-equity-strategist.md`, `.codex/agents/tech-architect.md`, `docs/strategy/strategy-versioning-and-revision-archive.md`, `docs/finance/FINANCE.md`, `docs/agents/CONTEXT_FINANCE.md`, `docs/agents/memory/MEMORY_FINANCE.md`, and active strategy docs.
- Current active version: `etf-trend-rotation.v1`.
- Current status: research/off-board. Prior replay showed the broad daily eligibility version was too flat versus SPY.

Scope:
- Design and test a ranked weekly ETF rotation variant instead of broad daily ETF eligibility.
- Test top 1/top 2 ETF selection, broad ETF versus sector ETF treatment, regime gates, trend filters, RS ranking windows, volatility caps, and turnover/friction sensitivity.
- Compare against SPY buy-and-hold and exposure-aware SPY.
- Preserve ETF sleeve identity; do not blend this into single-name stock selection.

Promotion Bar:
- Beat SPY buy-and-hold by at least 3% annualized after conservative friction, or justify a lower hurdle only if drawdown reduction and exposure utility are materially better.
- Beat exposure-aware SPY.
- Max drawdown must not be materially worse than SPY.
- Results must not be driven by one ETF, one sector, or one narrow market regime.
- Rule set must be explainable, measurable, storable, replayable, and compatible with `config/strategy_registry.json`.

Done When:
- Produce either a promoted ranked version, likely `etf-trend-rotation.v2`, or a clear research-only decision.
- Update research docs, strategy docs, registry/versioning docs if promoted, and `MEMORY_FINANCE.md`.
- If promoted, specify whether the ETF sleeve can feed the main board or only an exposure appendix.
- Include tests or a clear implementation test plan.
```
