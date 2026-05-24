# Repository Structure

## Recommended layout

```text
Trading System/
├── .codex/
│   └── agents/
│       ├── product-strategist.md
│       ├── tech-architect.md
│       ├── public-equity-strategist.md
│       ├── public-equity-analyst.md
│       ├── engineer.md
│       ├── designer.md
│       ├── qa-reviewer.md
│       └── context-curator.md
├── docs/
│   ├── product/
│   │   ├── PRODUCT.md
│   │   └── requirements/
│   │       └── archive/
│   ├── agents/
│   │   ├── CONTEXT_PRODUCT.md
│   │   ├── CONTEXT_TECH.md
│   │   ├── CONTEXT_FINANCE.md
│   │   ├── CONTEXT_BUGS.md
│   │   ├── CONTEXT_DESIGN.md
│   │   ├── CONTEXT_QA.md
│   │   ├── CONTEXT_CURATION.md
│   │   └── memory/
│   ├── strategy/
│   │   └── workstreams/
│   ├── research/
│   │   ├── market/
│   │   └── company/
│   ├── finance/
│   │   ├── FINANCE.md
│   │   └── frameworks/
│   ├── engineering/
│   │   ├── ENGINEERING.md
│   │   ├── requirements/
│   │   │   └── archive/
│   │   ├── architecture/
│   │   │   └── archive/
│   │   ├── decisions/
│   │   ├── runbooks/
│   │   ├── rcas/
│   │   └── integrations/
│   ├── design/
│   │   ├── DESIGN.md
│   │   ├── ux/
│   │   │   └── archive/
│   │   └── flows/
│   │       └── archive/
│   ├── qa/
│   │   ├── QA.md
│   │   └── checklists/
│   │       └── archive/
│   ├── system/
│   │   └── agent-context-system.md
│   ├── _backups/
│   └── operations/
│       ├── access/
│       └── vendors/
├── skills/
│   └── public-equity-intelligence/
├── apps/
├── services/
├── packages/
├── infra/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── scripts/
├── tests/
├── notebooks/
└── Trading System - Core Thesis.rtf
```

## Intent by top-level folder

- `.codex/agents/`: agent definitions with startup contracts, file ownership, and fail-loud rules
- `docs/`: all non-code artifacts for product, finance, design, engineering, and operations
- `skills/`: local Codex skills that should stay versioned with the project
- `apps/`: user-facing surfaces such as dashboards, internal tools, or report UIs
- `services/`: backend jobs and service code such as ingestion, scoring, and orchestration
- `packages/`: shared libraries, schemas, utilities, and finance logic reused across apps/services
- `infra/`: deployment, environment, and infrastructure-as-code assets
- `data/`: local project-managed datasets, snapshots, and static references
- `scripts/`: ad hoc operational utilities and developer scripts
- `tests/`: integration, unit, and workflow-level test coverage
- `notebooks/`: temporary exploration and one-off research that may later graduate into code

## Context-layer model

The repo now follows a four-layer agent context system:

- Layer 1, north star: short domain anchors such as `docs/product/PRODUCT.md`, `docs/finance/FINANCE.md`, `docs/engineering/ENGINEERING.md`, `docs/design/DESIGN.md`, and `docs/qa/QA.md`
- Layer 2, curated context: shared domain memory in `docs/agents/CONTEXT_*.md`
- Layer 3, active work: live specs in folders such as `docs/product/requirements/` and `docs/engineering/architecture/`
- Layer 4, archive: `archive/` folders under active-work directories

The lightweight operating guide for this system lives at `docs/system/agent-context-system.md`.

## Document placement guidance

- Put product north-star guidance in `docs/product/PRODUCT.md`
- Put active product specs and new PRDs in `docs/product/requirements/`
- Put shared curated context in `docs/agents/`
- Put planning threads and major workstreams in `docs/strategy/workstreams/`
- Put finance north-star guidance in `docs/finance/FINANCE.md`
- Put finance frameworks, rubrics, and taxonomies in `docs/finance/frameworks/`
- Put engineering north-star guidance in `docs/engineering/ENGINEERING.md`
- Put architecture docs, ADRs, runbooks, RCAs, and integration inventories under `docs/engineering/`
- Put design north-star guidance in `docs/design/DESIGN.md`
- Put wireframes, UX notes, and journey maps under `docs/design/`
- Put QA north-star guidance and release checklists under `docs/qa/`
- Put vendor notes, credentials process docs, and access checklists under `docs/operations/`

## Code placement guidance

- Put ingestion jobs in `services/ingestion/` once we start building
- Put scoring and intelligence orchestration in `services/intelligence/`
- Put reusable finance schemas and signal logic in `packages/finance/`
- Put shared data contracts in `packages/schemas/`
- Put report or dashboard code in `apps/`

## Working rule

If something is reusable product or engineering knowledge, put it in `docs/`. If it executes logic, put it in `apps/`, `services/`, `packages/`, or `scripts/` depending on lifespan and reuse.

## Naming rule

For new active specs, prefer sortable date-stamped names such as `prd-YYYY-MM-DD-feature.md`, `tdd-YYYY-MM-DD-feature.md`, and `ux-YYYY-MM-DD-flow.md`.
