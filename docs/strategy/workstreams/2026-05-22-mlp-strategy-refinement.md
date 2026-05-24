# MLP Strategy Refinement

## Purpose

Refine the CSV-first MLP from a generic score-led mock into a strategy-led weekly prototype that is easier to trust, critique, and improve.

## Why the first version was not enough

The first prototype had three important weaknesses:

- It could over-reward raw strength and accidentally tell the user to buy a good stock at a poor entry.
- The recommendation text, entry zone, invalidation, and target did not all come from the same underlying strategy logic.
- The HTML mostly surfaced a score and a short thesis rather than a named setup family with a backtestable rationale.

Those are not just UI issues. They are trust and strategy-definition issues.

## What changed

The MLP now uses explicit decision bases instead of one generic recommendation bucket.

Important terminology:

- `Setup family`: a repeatable tactical pattern with entry rules, invalidation logic, and a path to backtesting
- `Risk guardrail`: a rule that suppresses or modifies action when the setup would otherwise be misleading
- `Context lens`: a market or benchmark interpretation aid that informs decisions but is not itself a stock-picking edge

This matters because one of the earlier UX mistakes was calling everything a `strategy` even when some rows were really guardrails or context.

### 1. Constructive pullback continuation

Type:

- `Setup family`

Use when:

- price is above the `20-day` and `50-day` averages,
- relative strength versus `SPY` is clearly positive,
- and the stock is not too extended above the `20-day` average.

Why it exists:

- We want to buy leaders, but only when the entry still has defined risk geometry.

### 2. Breakout confirmation

Type:

- `Setup family`

Use when:

- trend is still intact,
- but relative strength or momentum confirmation is not strong enough yet,
- or price is too flat near support to justify an immediate entry.

Why it exists:

- This is the antidote to the trust-busting failure mode of buying simply because the stock is "good."

### 3. Index trend follow-through

Type:

- `Setup family`

Use when:

- the broad-market ETF is above the key moving averages,
- volatility is controlled,
- and the user wants market exposure with less single-name risk.

Why it exists:

- Sometimes the cleanest trade is broad exposure, not a high-beta stock.

### 4. Event freeze before earnings

Type:

- `Risk guardrail`

Use when:

- earnings are close enough that the next move is likely to be event-dominated.

Why it exists:

- A chart can look reasonable while still being a poor weekly entry because the event calendar dominates the setup.

### 5. Benchmark trend reference

Type:

- `Context lens`

Use for:

- `SPY` as market context.

Why it exists:

- The benchmark should set the posture for the week rather than automatically compete for capital.

## Current MLP outputs from the refined logic

- `TSLA`: `Buy now` via `Constructive pullback continuation`
- `VOO`: `Buy now` via `Index trend follow-through`
- `NVDA`: `Wait for confirmation` via `Breakout confirmation`
- `CRM`: `Hold / reassess after earnings` via `Event freeze before earnings`
- `SPY`: `Benchmark reference`

## First-principles improvement

The refined version is better because it now answers these questions directly:

1. What strategy is being used?
2. Why does that strategy exist?
3. Why is the stock eligible for that strategy right now?
4. What exact level invalidates the idea?
5. Is this a buy now, a wait, or just a benchmark/context row?

## Backtesting implication

The MLP replay is still small and mostly technical. That means:

- strategy-family backtests are directionally useful,
- but event-aware setups are not yet fully validated without historical point-in-time earnings and revision data.

Still, this is already a better loop:

- define a setup family,
- classify current names into it,
- replay it historically,
- and then show the user both the stock-level and strategy-level detail pages.
