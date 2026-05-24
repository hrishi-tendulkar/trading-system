# CONTEXT_BUGS

## Decisions

## [2026-05-22] Fail loud on missing context or source dependencies
**Decision** · Source: `docs/system/agent-context-system.md`
Agents and jobs should stop when required context or source inputs cannot be loaded instead of proceeding with partial assumptions.
**Why it matters:** Silent degradation is especially dangerous in a system that influences real trading decisions.

## Patterns

## [2026-05-22] The most dangerous failures are plausible-looking outputs from incomplete inputs
**Pattern** · Source: project operating principle
Incorrect recommendations often come from stale, partial, or missing data that still produces superficially coherent summaries.
**Why it matters:** Verification and instrumentation should target hidden incompleteness, not only crashes.

## Don'ts

## [2026-05-22] Do not treat successful execution as sufficient validation
**Don't** · Source: `docs/qa/QA.md`
A completed run is not enough if source lineage, completeness, or historical consistency are unknown.
**Why it matters:** Engineering and QA must validate output trustworthiness, not just whether a pipeline finished.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
