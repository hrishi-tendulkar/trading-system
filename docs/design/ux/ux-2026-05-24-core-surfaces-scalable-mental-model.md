# UX Note: Core Surfaces Scalable Mental Model

## Status

- Owner: Design
- Status: Proposed
- Last updated: 2026-05-24

## Purpose

Define the UX rule for scaling the product as the finance engine improves.

## Core rule

Do not redesign the product every time the strategy becomes more sophisticated.

Keep the same top-level mental model:

- `Weekly` is the decision session.
- `Daily` is the exception layer.
- `Deep dive` is the expandable stock memo.
- `Watchlist` is the managed universe workspace.

## What should scale

As strategy quality improves, the interface should scale through:

- sharper action ordering
- better bucket placement
- richer evidence modules
- more precise trigger and invalidation logic
- stronger history views
- deeper drill-downs on stock pages

## What should not scale

Do not scale by:

- inventing more dashboard surfaces
- forcing the user to relearn navigation
- turning weekly into a giant ranking table
- turning daily into a feed
- turning deep dive into an article dump

## Weekly page guidance

- Put `start here` above all detailed lists.
- Keep the top actions visibly more important than the broader review set.
- Use grouped sections so breadth feels controlled.

## Daily page guidance

- The first line should answer whether attention is required.
- Keep the list short enough that `no material change` is a good outcome, not a failure.

## Deep-dive page guidance

- Lead with the current call and setup plan.
- Keep evidence modular so more detail can be added later without changing the page identity.
- Separate observed facts from derived interpretation visually.

## Watchlist guidance

- Make the universe scannable before it becomes editable.
- Show the current action context for each name where possible.
- Preserve role clarity for benchmark, ETF, and active stock names.
