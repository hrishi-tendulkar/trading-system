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
