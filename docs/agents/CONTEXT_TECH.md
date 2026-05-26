# CONTEXT_TECH

## Decisions

## [2026-05-22] v1 is batch-first and operationally light
**Decision** · Source: `docs/product/high-level-design.md`
The core system should rely on daily refreshes, weekly synthesis, and simple scheduled jobs rather than real-time streaming.
**Why it matters:** This affects architecture shape, hosting, observability, and the acceptable complexity budget for every implementation choice.

## [2026-05-22] Separate raw, normalized, and derived layers
**Decision** · Source: `docs/engineering/requirements/high-level-technical-requirements.md`
Raw source captures, cleaned datasets, and derived features or recommendations should be stored separately.
**Why it matters:** This is necessary for traceability, reproducibility, and later debugging of score changes.

## [2026-05-25] Strategy persistence should be candidate-first, board-second
**Decision** · Source: `docs/engineering/requirements/tdd-2026-05-25-strategy-decision-basis-schema.md`
The persistence model should center on per-strategy candidate evaluation, first-class suppressors, and promoted board rows, rather than treating board rows as the primary recommendation source.
**Why it matters:** This keeps the storage model aligned with the strategy-lab architecture, preserves lineage, and prevents the database from collapsing back into a monolithic recommendation table.

## [2026-05-26] The real implementation unit is the strategy engine, not a generic ranker
**Decision** · Source: `docs/engineering/architecture/tech-architecture-2026-05-26-strategy-engine-mainline.md`
The hosted weekly engine should be built as `feature snapshots -> strategy candidates -> suppressors -> board promotion -> page projections`, with only `Breakout Confirmation` and narrowed `Sector-Confirmed Pullback Continuation` feeding the current mainline board.
**Why it matters:** This is the implementation-ready architecture that connects finance doctrine, product surfaces, and persistence without silently falling back to a monolithic recommendation path.

## Patterns

## [2026-05-22] Modular provider boundaries matter early
**Pattern** · Source: `docs/engineering/requirements/high-level-technical-requirements.md`
The system should prefer explicit source adapters and swappable analysis modules instead of hard-wiring provider-specific assumptions everywhere.
**Why it matters:** Early modularity reduces rewrite risk when provider quality, coverage, or cost changes.

## Don'ts

## [2026-05-22] Do not collapse the stack into one giant script
**Don't** · Source: `docs/engineering/requirements/high-level-technical-requirements.md`
Even in a small v1, ingestion, transformations, intelligence logic, and delivery should remain separable.
**Why it matters:** This prevents brittle code paths and preserves the ability to validate or replace layers independently.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
