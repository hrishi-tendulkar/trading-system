# Repository Structure

## Recommended layout

```text
Trading System/
├── docs/
│   ├── product/
│   ├── strategy/
│   │   └── workstreams/
│   ├── research/
│   │   ├── market/
│   │   └── company/
│   ├── finance/
│   │   └── frameworks/
│   ├── engineering/
│   │   ├── requirements/
│   │   ├── architecture/
│   │   ├── decisions/
│   │   ├── runbooks/
│   │   ├── rcas/
│   │   └── integrations/
│   ├── design/
│   │   ├── ux/
│   │   └── flows/
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

## Document placement guidance

- Put product briefs, roadmap notes, and PRDs in `docs/product/`
- Put planning threads and major workstreams in `docs/strategy/workstreams/`
- Put finance frameworks, rubrics, and taxonomies in `docs/finance/frameworks/`
- Put architecture docs, ADRs, runbooks, RCAs, and integration inventories under `docs/engineering/`
- Put wireframes, UX notes, and journey maps under `docs/design/`
- Put vendor notes, credentials process docs, and access checklists under `docs/operations/`

## Code placement guidance

- Put ingestion jobs in `services/ingestion/` once we start building
- Put scoring and intelligence orchestration in `services/intelligence/`
- Put reusable finance schemas and signal logic in `packages/finance/`
- Put shared data contracts in `packages/schemas/`
- Put report or dashboard code in `apps/`

## Working rule

If something is reusable product or engineering knowledge, put it in `docs/`. If it executes logic, put it in `apps/`, `services/`, `packages/`, or `scripts/` depending on lifespan and reuse.
