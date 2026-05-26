# CONTEXT_DESIGN

## Decisions

## [2026-05-22] Weekly decision workflow is the primary UX
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The most important interface is the weekly review flow, with daily monitoring as a lightweight supporting layer.
**Why it matters:** Design effort should emphasize scanability, action grouping, and thesis continuity in the weekly view.

## [2026-05-25] Strategy pages must separate trust, promotion, and live state
**Decision** · Source: `docs/design/ux/ux-2026-05-25-strategy-detail-page-notes.md`
Strategy detail pages must visually distinguish strategy trust level, workflow promotion status, and row-level live candidate state rather than collapsing them into one confidence signal.
**Why it matters:** Without this separation, the UI overstates confidence and blurs the difference between canonical, promoted, suppressed, and research-only outputs.

## Patterns

## [2026-05-22] The UI must separate evidence layers visually
**Pattern** · Source: `docs/product/high-level-design.md`
Users need to distinguish market regime, tactical setup, business support, and options overlay logic at a glance.
**Why it matters:** Clear visual separation prevents the system from feeling like one opaque recommendation engine.

## Don'ts

## [2026-05-22] Do not mimic noisy consumer trading dashboards
**Don't** · Source: `docs/design/DESIGN.md`
The product should not default to dense, novelty-driven market UIs that hide priorities under visual clutter.
**Why it matters:** The design should reduce cognitive load for a weekly operator, not increase it.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
