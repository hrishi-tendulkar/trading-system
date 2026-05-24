# TDD: Published-Run Presentation Slice

## Status

- Owner: Engineering
- Status: Proposed
- Last updated: 2026-05-24

## Purpose

Define the technical design for the first durable implementation slice that turns the current web app from placeholder shells into a structured product experience backed by stored recommendation data.

This slice is intentionally smaller than the full Phase 1 plus Phase 2 roadmap, but it is designed to move the repo in that direction without throwaway work.

## Build target

Ship a server-rendered web app that:

- renders `weekly`, `daily`, `watchlist`, and `deep dive` from stored recommendation and watchlist files,
- uses stable typed view contracts rather than ad hoc template payloads,
- keeps a clean repository boundary so storage can later move from file-backed sources to Supabase,
- and preserves the product mental model required by the current PRDs.

## Why this slice

The repo already contains:

- stored watchlist reference files,
- stored processed recommendation CSVs,
- and a lightweight FastAPI + Jinja app.

The current gap is not the total lack of data. The gap is that the app still renders generic placeholders instead of product-shaped outputs from a durable contract.

This slice closes that gap.

## Scope

Included:

- typed recommendation and watchlist loading
- file-backed repository implementation
- weekly decision-session mapping
- daily exception-layer mapping
- stock deep-dive mapping
- active-universe watchlist mapping
- route and view-model refactor
- server-rendered UI refresh for these screens
- unit and route tests

Excluded:

- Supabase persistence
- migrations
- write-capable watchlist CRUD
- admin-triggered job execution
- daily-over-daily historical diffing
- options-overlay expansion

## Architecture decision

### 1. Repository boundary

The web layer must not parse CSVs directly.

Introduce a repository-style loader in shared core code that:

- discovers the preferred published dataset,
- loads recommendation rows,
- loads watchlist rows,
- normalizes types,
- and exposes structured records to page-mapping functions.

This creates a clean swap point for later database-backed implementations.

### 2. Typed recommendation contract

Each stored recommendation row should normalize into a typed internal object that preserves:

- action label
- basis type
- strategy name
- entry, stop, and target fields
- event-risk context
- observed rationale
- strategy rationale
- ranking
- and relevant market metrics

The normalized object is the source for weekly, daily, and deep-dive projections.

### 3. Projection layer

Create view-projection functions that map normalized records into page-specific structures:

- weekly review projection
- daily digest projection
- watchlist projection
- stock detail projection

This keeps templates simple and protects them from raw source schema noise.

### 4. Storage abstraction

This slice will be file-backed first.

Expected next step later:

- replace file loaders with database queries returning the same normalized contract

The page layer should not need to change when that happens.

## Data source selection

Preferred source order for recommendations:

1. `data/processed/phase2/mlp_current_recommendations.csv`
2. `data/processed/mlp/mlp_current_recommendations.csv`

Preferred source order for watchlist:

1. `data/reference/phase2_watchlist.csv`
2. `data/reference/mlp_watchlist.csv`

The loader should fail loudly if no supported source exists.

## Page-mapping requirements

### Weekly

Must project:

- as-of date
- market posture summary
- top `1-3` actions
- fresh-cash buckets
- holder-action buckets
- deep-dive queue
- a compact view of focus breadth without flattening selectivity

### Daily

Must project:

- a top-line verdict
- action-required changes
- carry-forward queue

For this slice, daily items may be derived heuristically from the latest stored recommendation set rather than a true day-over-day diff.

### Watchlist

Must project:

- active universe members
- sector grouping or another scan-friendly grouping
- current recommendation state where available
- benchmark or ETF context rows

### Deep dive

Must project:

- current action
- holder guidance
- confidence proxy
- observed evidence
- derived explanation
- setup plan
- event risk
- strategy basis metadata

## Implementation plan

1. Add normalized record loaders and repository helpers in shared core code.
2. Replace current placeholder `sample_*` page functions with structured projections.
3. Update route handlers to use the new projections.
4. Redesign templates to match the decision-session model.
5. Expand CSS to support the new layout.
6. Add unit tests for loaders and projections.
7. Add route smoke tests for authenticated pages.

## Testing requirements

### Unit tests

- recommendation loader chooses a supported source
- normalized records preserve expected key fields
- weekly projection emits top actions and bucket groups
- stock detail projection uppercases ticker and fails cleanly for missing symbols

### Route tests

- authenticated `/weekly` renders `This Week's Plan`
- authenticated `/daily` renders the verdict section
- authenticated `/watchlist` renders the active universe page
- authenticated `/stocks/{ticker}` renders deep-dive content
- unauthenticated access redirects to `/login`

## Risks

- source CSV schema drift
- UI overfitting to the current recommendation export
- pretending daily is a true diff when it is presently a latest-state projection

## Mitigations

- keep the loader explicit and narrow
- isolate schema assumptions in one loader layer
- label the source as the latest published dataset
- keep projection functions additive and extensible

## Acceptance criteria

- the app no longer renders placeholder product text on weekly, daily, watchlist, and stock pages
- all four core screens render from the stored recommendation/watchlist sources
- templates are driven by structured projections, not raw CSV rows
- test coverage catches missing-source and route-auth regressions
