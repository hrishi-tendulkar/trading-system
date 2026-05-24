# Phase 3 PRD: Watchlist And Weekly Focus Queue

## Status

- Owner: Product + Engineering
- Status: Proposed
- Last updated: 2026-05-24

## Phase objective

Expand the product from a narrow action board into a real universe-management and broader weekly-review system without diluting trust.

## Why this phase is later

This phase depends on:

- the persistent data model from Phase 1,
- and the clear decision jobs from Phase 2.

Without those earlier phases, this expansion would mostly add surface area.

## Goals

- Launch canonical watchlist and universe management.
- Introduce a structured weekly focus queue of roughly `15-20` names.
- Preserve a smaller `3-5` name action board for high-conviction decisions.
- Let the user review more names weekly without treating them as equally actionable.
- Keep the broader review layer compatible with future strategy refinement rather than locked to today's simplest analysis shape.

## Non-goals

- market-wide discovery engine
- all-universe weekly deep dives
- expanding daily into a broad monitoring dashboard
- replacing the selective action board with a larger flat ranking table

## Product decisions

### 1. The watchlist becomes the canonical universe workspace

It is not just a saved list.

It is the system of record for:

- what is actively tracked,
- which names are holdings,
- which names are tactical,
- which names are context ETFs,
- and what status changes happened over time.

### 2. The weekly focus queue is a review layer

It is not the same thing as:

- the canonical universe,
- or the action board.

It exists to answer:

- `Which names deserve review this week even if they are not all buys?`

### 3. The action board stays selective

The product should still reserve top billing for roughly `3-5` current actions.

Coverage expands, but selectivity remains visible.

## Watchlist requirements

### CRUD and state

Must support:

- add ticker
- remove ticker
- activate ticker
- deactivate ticker
- edit tags
- edit notes

### Metadata

Must support:

- role tags such as `holding`, `core watch`, `tactical`, `ETF`
- sector and theme metadata
- optional thesis or reason note

### History

Must preserve:

- when a name was added,
- when a name changed role,
- when a name was deactivated,
- and who or what changed it if that distinction exists in the system.

## Weekly focus queue requirements

### Size and purpose

- target size: roughly `15-20` names
- purpose: broad weekly review, not direct capital deployment

### Buckets

Must support structured states such as:

- `Tradeable now`
- `Buy on pullback`
- `Wait for confirmation`
- `Event-risk freeze`
- `Hold / review`
- `No action`

### Per-name fields

Each focus-queue card or row must show:

- why this name is in this week's queue
- current bucket
- why not stronger
- trigger or preferred entry
- invalidation or cancel condition
- next catalyst
- confidence
- what would change the call next week
- link to deep dive if available

The queue should also tolerate later additions such as:

- richer rationale labels,
- more precise catalyst states,
- stronger regime context,
- and more detailed bucket explanations,

without changing the queue's role in the workflow.

## Relationship to other surfaces

### Weekly page

- The weekly page should summarize the focus queue, not duplicate it in full.
- The action board remains the primary fresh-cash surface.

### Deep dive

- Deep dives should be available for top actions, high-priority wait names, and risk-sensitive holdings.
- Manual deep dives for any active watchlist name can come later, but should not block this phase.

### Daily page

- The daily page may promote or demote names into or out of the focus queue.
- It should still remain exception-based.

## Acceptance criteria

- The user can manage a canonical universe without touching source files manually.
- The product can review `15-20` names weekly without making them all look like buys.
- The weekly page still foregrounds the `3-5` highest-conviction actions.
- A name can move between queue buckets across weeks with inspectable history.

## Release test

This phase is complete when broader weekly review feels useful and controlled rather than noisy.

## Risks to manage

- letting the focus queue overpower the action board
- confusing `watched` with `actionable`
- adding too many free-form tags and weakening consistency
- broadening faster than signal quality can support
- turning future strategy improvements into new surface clutter instead of deeper, better-explained rows and drill-downs
