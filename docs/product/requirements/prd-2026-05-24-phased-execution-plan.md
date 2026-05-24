# Weekly Equity Intelligence Phased Execution Plan

## Status

- Owner: Product
- Status: Proposed
- Last updated: 2026-05-24

## Why this exists

Two separate workstreams reached complementary conclusions on 2026-05-24:

- `refine existing features` concluded the current product surfaces need sharper jobs before more breadth is added.
- `weekly product expansion` concluded the product should eventually expand into a canonical watchlist, a `15-20` name weekly focus queue, and a selective action board.

This document combines those recommendations into one execution plan so the repo has a single answer to:

- what to build first,
- what to delay,
- and how to avoid throwaway UI work.

## Executive conclusion

The two workstreams do **not** conflict.

They describe a valid sequence:

1. create a real data-backed product spine,
2. sharpen the existing weekly, daily, and deep-dive jobs,
3. then expand into watchlist management and broader weekly review coverage,
4. while preserving a small, high-trust action layer.

The main mistake to avoid is building `watchlist breadth` or `15-20` stock review UI on top of shell pages that still lack persistent data, explicit action contracts, and trustworthy stock-level evidence.

## Product decision

The product should be built as a `funnel`, not a flat board:

1. `Canonical universe`
- roughly `50-70` names
- the managed set of holdings, core watches, tactical candidates, and ETF context names

2. `Weekly focus queue`
- roughly `15-20` names
- the names that deserve review this week
- includes actionable names and important non-actionable names

3. `Action board`
- roughly `3-5` names
- the highest-conviction actions for fresh capital or urgent holder decisions

This preserves the product's core identity:

- broad enough to be useful,
- selective enough to stay trusted.

## Planning principles

- Weekly decision quality comes before page-count expansion.
- Persistent data contracts come before UI layering.
- Stock detail must be evidence-first before it becomes a scalable product object.
- Daily usage remains exception-based, not feed-based.
- Broader review coverage is good only if the action layer stays selective.
- History and inspectability are `P0` requirements, not later polish.
- The front-end mental model should stay stable even as the finance engine becomes more sophisticated.

## Scalability principle

The product should scale by increasing `depth`, `evidence quality`, and `decision precision` inside the same core workflow, not by inventing a new top-level product shape every time the strategy improves.

That means:

- `Weekly` should always remain the main decision session.
- `Daily` should always remain the exception and change-detection layer.
- `Deep dive` should always remain the expandable stock-level decision memo.

As strategies improve, the user should experience:

- better ranking,
- sharper bucket placement,
- richer evidence,
- clearer invalidation logic,
- and more trustworthy historical comparisons,

without needing to relearn the product.

## What not to build first

Do **not** build these before the earlier phases are complete:

- a rich watchlist UI backed only by temporary sample payloads,
- a large `15-20` name focus board without bucket logic and persistent history,
- broad deep-dive generation for the full universe every week,
- feed-style daily monitoring that trains the user to check noise,
- options-heavy workflow expansion before the stock decision loop is credible.

## Recommended build sequence

### Phase 1. Data spine and decision contracts

Goal:

- replace scaffold-level product wiring with persistent product objects that can support all later surfaces

Primary output:

- a trustworthy product backbone for weekly runs, stock decisions, and watchlist membership

Phase PRD:

- [prd-2026-05-24-phase-1-data-spine-and-decision-contracts.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/requirements/prd-2026-05-24-phase-1-data-spine-and-decision-contracts.md)

### Phase 2. Weekly, daily, and deep-dive operating loop

Goal:

- make the existing core surfaces genuinely useful for the weekly operating cadence

Primary output:

- a clear `This Week's Plan`, an exception-based daily page, and a decision-first deep-dive page

Phase PRD:

- [prd-2026-05-24-phase-2-core-decision-surfaces.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/requirements/prd-2026-05-24-phase-2-core-decision-surfaces.md)

### Phase 3. Canonical watchlist and weekly focus queue expansion

Goal:

- expand coverage in a controlled way after the core loop and data model are real

Primary output:

- canonical universe management plus a structured weekly review queue of `15-20` names

Phase PRD:

- [prd-2026-05-24-phase-3-watchlist-and-focus-queue.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/requirements/prd-2026-05-24-phase-3-watchlist-and-focus-queue.md)

### Phase 4. History, evaluation, and strategy-tightening loop

Goal:

- make the product inspectable, reviewable, and improvable over time

Primary output:

- recommendation history, movement history, outcome review, and feedback into signal quality

Phase PRD:

- [prd-2026-05-24-phase-4-history-evaluation-and-strategy-tightening.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/requirements/prd-2026-05-24-phase-4-history-evaluation-and-strategy-tightening.md)

## Dependency logic

### Why Phase 1 comes first

Without persistent weekly runs, stock-level recommendation objects, and a canonical universe model, every later surface becomes presentation-only.

That would create the exact throwaway work this plan is meant to avoid.

### Why Phase 2 comes before Phase 3

The user's most important job is still:

- `What should I do this week?`

So the current weekly, daily, and deep-dive surfaces must become crisp before adding breadth.

Otherwise the system gets wider without getting clearer.

### Why Phase 3 is still early enough to matter

The expansion workstream is still directionally right:

- the system should support broader review than just `3-5` names,
- and the user should manage a real canonical universe.

Phase 3 is where that becomes real, but only after the product can already make trusted weekly decisions.

### Why Phase 4 is not optional

This repo's strategy and product doctrine repeatedly require:

- historical traceability,
- explainability,
- and learning from prior recommendations.

So history and evaluation are not a nice-to-have archive project. They are the mechanism that keeps the product from becoming unsupported commentary.

## Cross-functional contracts

### Product contract

- Keep the weekly page centered on action order, not information abundance.
- Treat the weekly focus queue as a review layer, not an all-equal ranking board.
- Preserve explicit separation between new-position decisions and holder decisions.

### Finance contract

- Maintain separate views for short-term tradeability, medium-term setup, and long-term conviction.
- Preserve evidence lineage and clear `why now` versus `why not stronger` framing.
- Do not let broader coverage flatten selectivity.

### Engineering contract

- Model persistent weekly runs, stock decision objects, watchlist state, and historical transitions before surface expansion.
- Prefer durable UI-ready contracts over ad hoc payload transforms embedded in templates.
- Keep each phase releasable without requiring the entire roadmap to land first.
- Design contracts so new strategy outputs can be added as additional fields, evidence modules, and drill-down sections without changing the top-level page mental model.

## Success criteria

This plan is successful if:

- each new phase uses artifacts created by the previous phase rather than replacing them,
- the weekly page becomes a trusted starting point for weekly action,
- the product can review `15-20` names without making them all look equally actionable,
- and recommendation history becomes inspectable enough to support future refinement.

## Supersedes

This phased plan supersedes the handoff role of:

- `docs/product/archive/refine-existing-features-handoff-2026-05-24.md`
- `docs/strategy/workstreams/archive/2026-05-24-weekly-product-expansion-summary.md`
- `docs/product/requirements/archive/prd-2026-05-24-review-surfaces-p0-refinement.md`

Those documents have been archived so the active product direction stays singular.
