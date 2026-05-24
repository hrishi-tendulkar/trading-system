# Weekly Product Expansion Summary

## Status

- Owner: Product + Finance + Engineering
- Status: Draft handoff summary
- Date: 2026-05-24

## Why this note exists

This summary captures the "add new features" workstream for the weekly product so it can later be combined with the separate "refine existing features" workstream in a new planning chat.

The goal is not to make final sequencing decisions here. The goal is to preserve the main conclusions, tensions, and recommended phasing inputs.

## What was reviewed

### Live product check

- The deployed weekly URL currently redirects to the login page, so the authenticated weekly experience could not be inspected directly without credentials.
- This still helped confirm that the live product is not yet ready for a feature-level UX review as if it were already fully wired.

### Codebase review

Reviewed:

- `apps/web/main.py`
- `apps/web/templates/weekly.html`
- `apps/web/templates/watchlist.html`
- `apps/web/templates/stock_detail.html`
- `packages/core/ui_data.py`

### Product and finance references

Reviewed:

- `docs/product/trading-system-product-strategy.md`
- `docs/product/weekly-equity-intelligence-prd.md`
- `docs/product/high-level-design.md`
- `docs/strategy/weekly-equity-intelligence-strategy-blueprint.md`
- `docs/strategy/workstreams/2026-05-23-broader-universe-phase2-plan.md`
- `docs/research/market/tradeable-board-2026-05-24.md`

## Current state

### Product shell is ahead of product wiring

Observed:

- The weekly page is still rendering sample payloads rather than published run data.
- The watchlist page is explicitly scaffolded and not yet a real watchlist workspace.
- The stock detail page is also shell-level and not yet connected to persistent recommendation, evidence, and history data.

Plain-English takeaway:

- The immediate bottleneck is not visual polish.
- The immediate bottleneck is the missing bridge between research outputs and product surfaces.

## Core product question addressed

The user asked two related questions:

1. Should the system support adding and removing stocks from the watchlist?
2. Should the system review more stocks each week and give perspectives on roughly `15-20` names to watch, monitor, or invest in?

## Refined view

Yes, the system should support adding and removing stocks.

But the product should not treat this as one flat watchlist plus one flat ranked board.

The better product shape is a funnel with three layers:

1. `Canonical universe`
- Roughly `50-70` names
- Includes holdings, high-conviction names, tactical names, and ETF context rows

2. `Weekly focus queue`
- Roughly `15-20` names
- The names that deserve attention this week
- Includes actionable names and non-actionable but important watch names

3. `Action board`
- Roughly `3-5` names
- Only the highest-conviction current actions

This matters because reviewing `15-20` names weekly makes sense.

Investing in `15-20` names weekly usually does not.

The system should help the user review broadly, then act selectively.

## Why this view is stronger than "just add more stocks"

### Product reason

The product strategy already says the system should optimize for a curated universe of roughly `50-70` names and a weekly decision cockpit, not broad market scanning.

### Finance reason

The current research does not yet justify making many names look equally actionable.

The broader-universe workstream already showed:

- the workflow shell is useful,
- the data path is real,
- but the strategy still needs more signal discrimination.

### Trust reason

If the system broadens coverage too quickly without preserving selectivity, the weekly board will become noisy and less believable.

The current engine is more trustworthy when it says:

- here are a handful of real action candidates,
- here are a dozen names worth monitoring,
- and here are many names that deserve no action.

## Recommended feature shape

### 1. Watchlist workspace

Support:

- add ticker
- remove ticker
- activate or deactivate
- tag as `holding`, `core watch`, `tactical`, `ETF`, or similar
- sector / theme metadata
- notes
- history of watchlist changes

This should become the system's canonical universe management surface.

### 2. Weekly focus queue

A dedicated weekly review section for roughly `15-20` names with clear buckets such as:

- `Tradeable now`
- `Buy on pullback`
- `Wait for confirmation`
- `Event-risk freeze`
- `Hold / review`
- `No action`

This is the right place for "perspectives on more stocks" without pretending all of them deserve capital now.

### 3. Small action board

A more selective board of only the top `3-5` weekly actions.

This should remain the main "fresh cash deployment" surface.

### 4. Stock perspective card

For each weekly focus name, show:

- why this week
- why not stronger
- trigger or preferred entry
- invalidation or cancel condition
- catalyst or event context
- requested horizon
- confidence
- what would change the call next week

This keeps the system evidence-first and decision-useful.

## Important constraint

The current live/web implementation is not yet ready for full feature layering.

Before or alongside feature expansion, the system needs a real data-backed product spine:

- published weekly run data
- persistent watchlist model
- persistent stock detail payloads
- mapping from research outputs into UI-ready structures

Without that wiring, new screens risk becoming additional shells.

## Practical phasing input

This workstream suggests the following sequence candidate:

### Phase A: Foundation for expansion

- replace sample weekly data with published run data
- create canonical watchlist / universe model
- wire stock detail pages to real recommendation and evidence payloads

### Phase B: Controlled expansion

- launch watchlist CRUD
- support tags and active/inactive states
- introduce weekly focus queue for `15-20` names

### Phase C: Decision-quality layer

- keep the main action board selective at `3-5` names
- add perspective cards and movement between weekly buckets
- preserve historical state so weekly changes are inspectable

### Phase D: Strategy tightening alongside product work

- continue improving signal discrimination, setup gating, and broader-universe replay
- do not mistake broader coverage for validated edge

## Key tension to carry into the next planning chat

There are two parallel truths:

1. The product should expand from a tiny shell into a real watchlist and weekly review system.
2. The finance engine must remain selective enough that broader coverage does not reduce trust.

So the correct question is not:

- "Should we add more stocks?"

It is:

- "How do we expand review coverage while preserving a small, high-trust action layer?"

## Suggested combined planning question for the next chat

Use this summary together with the separate "refine existing features" summary to answer:

1. What must be wired or cleaned up first before feature expansion creates real user value?
2. Which parts of watchlist expansion are foundational versus optional?
3. How should we phase:
   - data wiring,
   - weekly board refinement,
   - watchlist CRUD,
   - weekly focus queue,
   - and strategy-quality improvements?

## Canonical references

- [Trading System Product Strategy](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/trading-system-product-strategy.md)
- [Weekly Equity Intelligence PRD](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/weekly-equity-intelligence-prd.md)
- [Trading System High-Level Design](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/high-level-design.md)
- [Weekly Equity Intelligence Strategy Blueprint](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/weekly-equity-intelligence-strategy-blueprint.md)
- [Broader Universe Phase 2 Plan](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/workstreams/2026-05-23-broader-universe-phase2-plan.md)
- [Tradeable Board 2026-05-24](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/research/market/tradeable-board-2026-05-24.md)
