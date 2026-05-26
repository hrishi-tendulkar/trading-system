# FINANCE

## Purpose

The finance layer defines how Trading System evaluates stocks, separates signal families, and converts evidence into weekly actions. It is the domain north star for investing logic, not a running market diary.

## Finance Principles

- Separate long-term conviction from short-term tradeability
- Treat options overlays as expressions of an equity view, not standalone alpha
- Prefer measurable, storable, backtestable signals over narrative heuristics
- Keep facts, inferences, and unknowns distinct
- Use qualitative analysis to refine or disqualify quantitative candidates, not replace them

## Core Outputs

- Buy now
- Buy on pullback
- Hold or add
- Trim or exit
- Covered call candidates
- Cash-secured put candidates

## Decision-basis terminology

The finance layer should distinguish between:

- `Trade setup`: a repeatable tactical pattern with entry rules, invalidation, and an expected holding period
- `Risk rule`: a rule that suppresses or modifies action even when the chart looks acceptable
- `Context lens`: a market or benchmark interpretation aid that informs a decision but is not itself a stock-picking edge

Do not call every named row a `strategy`. Some rows represent trade setups, others exist to prevent errors or add context.

## Core Analytical Spine

1. Market regime
2. Price and relative strength
3. Setup and risk geometry
4. Event and fundamental filter
5. Qualitative red-team
6. Execution choice

## Non-Goals

- Intraday prediction
- Market commentary without portfolio relevance
- One opaque master score that blends business quality, timing, and options attractiveness
- Unsupported claims that cannot be mapped to persistent data fields

## Canonical References

- `docs/strategy/canonical-trading-strategies.md`
- `docs/strategy/weekly-equity-intelligence-strategy-blueprint.md`
- `docs/finance/frameworks/weekly-equity-intelligence-analysis-framework.md`
- `docs/finance/frameworks/daily-data-short-term-strategy-upgrade.md`
- `skills/public-equity-intelligence/references/analysis-framework.md`
