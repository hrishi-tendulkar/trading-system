# CONTEXT_QA

## Decisions

## [2026-05-22] Review for decision-risk, not only implementation correctness
**Decision** · Source: `docs/qa/QA.md`
QA must assess whether the system's outputs are trustworthy enough for capital-allocation decisions, not just whether the code path executed.
**Why it matters:** This raises the bar on release readiness and keeps reviews aligned with the product's real-world stakes.

## Patterns

## [2026-05-22] Hidden data staleness is a first-class test target
**Pattern** · Source: `docs/qa/QA.md`
Pipelines that use stale or partial upstream data can produce believable outputs while violating user trust.
**Why it matters:** QA plans should include freshness, completeness, and provenance checks in addition to functional tests.

## Don'ts

## [2026-05-22] Do not approve changes with unresolved lineage gaps
**Don't** · Source: `docs/engineering/requirements/high-level-technical-requirements.md`
If major outputs cannot be tied back to their source inputs and run timestamps, the system is not review-ready.
**Why it matters:** Traceability is a core quality gate for this project, not optional polish.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
