# Trading System Agent + Context System

## Purpose

This repo adopts the agent-and-context blueprint from `Job App Agent/docs/system/agent-context-system.md` and applies it to Trading System's actual domains, documents, and operating constraints.

## Canonical Repo Root

All agent paths in this repo are anchored to the Trading System repository root: the directory that contains `.codex/agents/`, `docs/`, `apps/`, `services/`, `packages/`, and `skills/`.

If an agent cannot read required files from that root, it must stop and report the failure rather than guess.

## Agent Roster

- `product-strategist`: owns product north star, product curated context, and product requirements
- `tech-architect`: owns engineering north star, tech curated context, and technical design artifacts
- `public-equity-strategist`: owns finance north star, finance curated context, and finance frameworks
- `public-equity-analyst`: owns applied stock analysis, trade setup evaluation, and recommendation synthesis within the finance guardrails defined by the finance north star and frameworks
- `engineer`: owns implementation work and the bugs/gotchas context
- `designer`: owns design north star, design curated context, and UX artifacts
- `qa-reviewer`: owns QA north star, QA curated context, and readiness checklists
- `context-curator`: maintains the context layer itself and manages archives and Inbox hygiene

## Layer Mapping

### Layer 1: North-star docs

- `docs/product/PRODUCT.md`
- `docs/engineering/ENGINEERING.md`
- `docs/finance/FINANCE.md`
- `docs/design/DESIGN.md`
- `docs/qa/QA.md`

These files define stable mission, principles, non-goals, and domain boundaries. They should stay short and only change on genuine strategic shifts.

### Layer 2: Curated context

- `docs/agents/CONTEXT_PRODUCT.md`
- `docs/agents/CONTEXT_TECH.md`
- `docs/agents/CONTEXT_FINANCE.md`
- `docs/agents/CONTEXT_BUGS.md`
- `docs/agents/CONTEXT_DESIGN.md`
- `docs/agents/CONTEXT_QA.md`
- `docs/agents/CONTEXT_CURATION.md`

Each file should remain slim, decision-relevant, and organized around durable facts rather than task lists.

### Layer 3: Active work

Canonical active-work locations:

- `docs/product/requirements/`
- `docs/engineering/requirements/`
- `docs/engineering/architecture/`
- `docs/design/ux/`
- `docs/design/flows/`
- `docs/qa/checklists/`

When practical, new active specs should use sortable date-stamped filenames such as `prd-YYYY-MM-DD-feature.md` or `tdd-YYYY-MM-DD-feature.md`.

### Layer 4: Archive

Canonical archive folders:

- `docs/product/requirements/archive/`
- `docs/engineering/requirements/archive/`
- `docs/engineering/architecture/archive/`
- `docs/design/ux/archive/`
- `docs/design/flows/archive/`
- `docs/qa/checklists/archive/`

Existing long-lived reference docs such as the strategy blueprint, analysis framework, and integration inventories remain valid reference artifacts and do not need to be forced into archive immediately.

## Cross-Domain Inbox Rule

Every curated context file ends with an Inbox section. Agents may propose durable facts for another domain there, but only the owning agent promotes those items into the main body.

## Curator Operating Rules

- Back up files before major maintenance passes in `docs/_backups/`
- Never auto-edit north-star docs without explicit approval
- Auto-apply only low-risk context maintenance
- Escalate contradictions, identity changes, and risk-posture changes
- Keep context files slim and archive inactive specs instead of letting active layers bloat

## Current Adoption Notes

- The repo already had strong domain reference docs before this system was added.
- Those documents remain source material for the new north-star and context layer.
- Going forward, the agent roster and context files above are the canonical coordination system for repository-aware agent work.
