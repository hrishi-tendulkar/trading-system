# TDD: Strategy Mainline Implementation Plan

## Status

- Owner: Engineering
- Status: Active
- Last updated: 2026-05-26

## Purpose

Turn the new strategy-lab architecture into a build sequence that can be executed without re-deciding product, finance, or platform shape during implementation.

This is the missing “yes and we build” document.

## Build Goal

Ship a working internal weekly engine that:

- computes per-strategy candidates,
- persists suppressors and board promotions,
- renders a sparse promoted weekly board,
- and supports the first strategy detail pages from stored data.

## In-Scope Build

### Mainline now

- `Breakout Confirmation`
- narrowed `Sector-Confirmed Pullback Continuation`

### Present but off-board

- `ETF Trend / Rotation`
- `Selective Mean Reversion`

### Pages

- weekly overview
- stock detail
- first strategy detail pages

## Out Of Scope For This Build Slice

- live ETF rotation promotion
- live mean reversion promotion
- options overlays
- point-in-time revision history
- transcript-heavy AI analysis
- production-grade auth expansion beyond current shared-password direction

## Working Assumptions

- storage remains `Supabase Postgres`
- jobs remain Python batch jobs
- web remains server-rendered
- replay already exists as an offline validation input
- the repo is the source of truth for docs, migrations, and code

## Implementation Phases

## Phase 0: Contract lock

Goal:

- freeze the contracts before wiring runtime code

Tasks:

1. Treat these docs as implementation inputs:
   - `docs/engineering/architecture/tech-architecture-2026-05-26-strategy-engine-mainline.md`
   - `docs/engineering/requirements/tdd-2026-05-25-strategy-decision-basis-schema.md`
   - `docs/strategy/weekly-board-assembly-spec.md`
   - `docs/product/requirements/prd-2026-05-25-strategy-detail-page.md`
2. Freeze canonical action vocabulary in code constants and typed schemas.
3. Freeze canonical basis codes:
   - `breakout-confirmation`
   - `sector-confirmed-pullback-continuation`
   - `etf-trend-rotation`
   - `selective-mean-reversion`
   - risk and context rows separately

Acceptance criteria:

- no unresolved naming drift in the implementation target

## Phase 1: Database foundation

Goal:

- create the minimal persistence layer for the new architecture

Tasks:

1. Add SQL migrations for:
   - `ref.decision_bases`
   - `ref.decision_basis_versions`
   - `research.replay_runs`
   - `research.replay_signal_events`
   - `research.replay_strategy_summaries`
   - `intelligence.strategy_candidates`
   - `intelligence.candidate_suppressors`
   - `intelligence.board_runs`
   - `intelligence.board_rows`
   - `intelligence.board_row_supporting_strategies`
2. Add enum support for:
   - `fresh_cash_action_code`
   - `position_action_code`
   - `expression_code`
   - trust and status enums where needed
3. Add Python DB models and migration validation tests.

Recommended file targets:

- `supabase/migrations/*`
- `packages/db/models.py`
- `tests/` migration and model drift checks

Acceptance criteria:

- schema migrates locally
- model drift checks pass
- deprecated monolithic tables remain untouched for backward compatibility

## Phase 2: Strategy registry and metadata loader

Goal:

- make strategy metadata versioned and queryable

Tasks:

1. Add repo-side registry source:
   - `config/strategy_registry.yaml` or `config/decision_bases/*.yaml`
2. Build loader that syncs registry metadata into:
   - `ref.decision_bases`
   - `ref.decision_basis_versions`
3. Include structured content for strategy pages:
   - purpose
   - rule spine
   - risks
   - trust level
   - promotion status

Recommended file targets:

- `config/strategy_registry.yaml`
- `packages/core/strategy_registry.py`
- `services/jobs/...` loader command

Acceptance criteria:

- latest decision-basis metadata can be loaded and versioned
- strategy detail pages have one source for names, trust, and page copy

## Phase 3: Candidate-first weekly engine

Goal:

- replace the old monolithic weekly recommendation path

Tasks:

1. Build feature snapshot generator for weekly runs.
2. Build candidate evaluators for:
   - `Breakout Confirmation`
   - narrowed `Sector-Confirmed Pullback Continuation`
3. Persist one row per `(weekly_run, ticker, strategy)`.
4. Emit explicit `NO_ACTION` or board-ineligible candidates where appropriate.

Recommended file targets:

- `packages/core/strategy_candidates.py`
- `packages/core/strategy_payloads.py`
- `services/jobs/weekly_*`

Acceptance criteria:

- one weekly run produces persisted candidate rows for both promoted sleeves
- breakout `BUY_NOW` requires triggered supportive-regime entry
- pullback uses narrowed rules, not the broad aggregate form

## Phase 4: Suppressors and board assembly

Goal:

- make board promotion explicit and auditable

Tasks:

1. Implement suppressor evaluation:
   - start with earnings/event freeze
2. Persist suppressor rows with hard-block behavior.
3. Implement board assembly using:
   - promoted sleeves only
   - one ticker one row
   - `primary_source_strategy`
   - zero-to-many `supporting_strategies`
   - sparse board allowed
4. Implement current board types:
   - `fresh_cash_main`
   - `start_here`

Recommended file targets:

- `packages/core/risk_suppressors.py`
- `packages/core/board_assembly.py`
- `services/jobs/weekly_*`

Acceptance criteria:

- weekly board renders from persisted board rows
- suppressed names stay visible in strategy detail but do not hit the main board
- only breakout and narrowed pullback can feed the main board

## Phase 5: Projection layer for product pages

Goal:

- make pages render from stable read models instead of raw tables

Tasks:

1. Build projection helpers or materialized read models for:
   - weekly board
   - stock detail strategy section
   - strategy detail page
2. Include row-level state:
   - `Board-promoted`
   - `Strategy-only`
   - `Suppressed`
3. Include replay summary joins for strategy pages.

Recommended file targets:

- `packages/core/projections/*.py`
- `packages/db/repositories/*.py`
- optional SQL views if useful

Acceptance criteria:

- web surfaces do not reconstruct logic ad hoc
- one normalized contract powers both data and copy

## Phase 6: First UI delivery

Goal:

- ship the first useful user-facing slice

Tasks:

1. Update weekly overview to render from `board_rows`.
2. Update stock detail to show strategy lineage and suppressor-aware state.
3. Implement first strategy detail pages:
   - `Breakout Confirmation`
   - narrowed `Sector-Confirmed Pullback Continuation`
4. Render trust level, promotion status, and live candidate state separately.

Recommended file targets:

- `apps/web/...`
- templates and CSS modules

Acceptance criteria:

- weekly board is sparse and explainable
- stock page shows why a name is on or off the board
- strategy pages show live output, replay, and rule spine

## Phase 7: Offline replay ingestion

Goal:

- connect replay evidence to product surfaces and future tuning

Tasks:

1. Add import job for:
   - `canonical_strategy_comparison.csv`
   - `canonical_strategy_summary.csv`
   - slice summary CSVs
2. Persist run metadata and summary rows.
3. Make strategy pages render from imported replay rows.

Recommended file targets:

- `services/jobs/import_replay_*`
- `packages/core/replay_import.py`

Acceptance criteria:

- strategy pages read replay evidence from structured storage
- replay run versions are queryable by page and future jobs

## Phase 8: Cleanup and old-path retirement

Goal:

- reduce confusion after the new path works

Tasks:

1. Deprecate old monolithic recommendation projections.
2. Remove old label-mapping shortcuts from UI helpers.
3. Point weekly generation commands to the new path by default.
4. Document migration notes for any surviving legacy tables.

Acceptance criteria:

- no primary product page depends on legacy recommendation shape

## Concrete Repo Targets

### Migrations and DB

- `supabase/migrations/`
- `packages/db/models.py`
- `packages/db/repositories/`

### Core logic

- `packages/core/strategy_registry.py`
- `packages/core/strategy_candidates.py`
- `packages/core/risk_suppressors.py`
- `packages/core/board_assembly.py`
- `packages/core/replay_import.py`
- `packages/core/projections/`

### Jobs

- `services/jobs/` or current job entrypoint equivalents
- `scripts/` only for transition helpers, not final runtime orchestration

### Web

- `apps/web/`

### Tests

- migration tests
- candidate evaluator tests
- suppressor tests
- board assembly tests
- projection tests
- UI smoke tests where practical

## Testing Strategy

### Must-have tests

1. Breakout emits `BUY_NOW` only on triggered supportive-regime entries.
2. Pullback candidate generation respects narrowed rules.
3. Suppressed names cannot promote to the main board.
4. One ticker cannot render as multiple board rows.
5. `primary_source_strategy` and `supporting_strategies` persist correctly.
6. Strategy detail projection correctly separates:
   - `Board-promoted`
   - `Strategy-only`
   - `Suppressed`

### Nice-to-have tests

7. Replay import preserves summary metrics and version label.
8. Legacy mapping aliases resolve to canonical action codes during migration only.

## Rollout Order

### Milestone 1

- migrations
- strategy registry
- promoted strategy candidate generation

### Milestone 2

- suppressors
- board assembly
- weekly overview rendering from new tables

### Milestone 3

- stock detail lineage
- first strategy detail pages
- replay import

### Milestone 4

- legacy cleanup
- ETF shadow appendix path
- future refinement hooks

## What We Should Not Wait For

Do not block the new mainline on:

- ETF ranked rotation redesign
- mean reversion promotion
- options support
- transcript integration
- broader AI evidence layers

Those are later improvements, not prerequisites.

## Ready-To-Implement Recommendation

The system is now ready for implementation.

The first concrete build sequence should be:

1. create migrations and DB models
2. load decision-basis metadata
3. implement breakout and narrowed pullback candidate generation
4. implement suppressors and board assembly
5. switch weekly board rendering to persisted board rows
6. ship the first strategy detail pages

At that point, we can say the new multi-strategy engine is operational rather than just specified.
