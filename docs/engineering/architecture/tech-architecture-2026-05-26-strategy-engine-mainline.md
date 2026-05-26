# Tech Architecture: Strategy Engine Mainline

## Status

- Owner: Engineering + Finance + Product
- Status: Active
- Last updated: 2026-05-26

## Purpose

Translate the new multi-strategy doctrine into an implementation-ready technical architecture for the real weekly engine.

This document answers:

- what the mainline engine should compute,
- how strategy evaluation, suppressors, and board promotion should be separated,
- which sleeves are in or out of the current mainline,
- and what data contracts the web app and jobs should rely on.

## Problem Statement

The repo has moved beyond a monolithic ranking model.

The current product and finance doctrine now requires:

- separate strategy evaluation,
- explicit risk suppressors,
- board promotion as a second-stage process,
- strategy detail pages driven by structured data,
- and unequal trust across canonical strategies.

That means the old mental model:

- `raw features -> one recommendation row`

must be replaced with:

- `raw features -> per-strategy candidates -> suppressors -> promoted board rows`

## Current Mainline Scope

### Promoted now

- `Breakout Confirmation`
- narrowed `Sector-Confirmed Pullback Continuation`

### Canonical but not currently feeding the main action board

- `ETF Trend / Rotation`

### Research only

- `Selective Mean Reversion`

## Architectural Decision

Implement the strategy engine as a candidate-first batch pipeline with four layers:

1. `feature preparation`
2. `strategy evaluation`
3. `risk suppression`
4. `board promotion`

The web layer should read only persisted outputs from this pipeline.

## Target System Shape

### Layer 1: Feature preparation

Input:

- normalized daily prices
- benchmark and sector context
- earnings proximity and event flags
- watchlist and security reference data

Responsibilities:

- compute shared technical features
- attach sector and benchmark relationships
- classify regime state
- emit one feature snapshot per security per run date

Persistence target:

- existing normalized tables plus derived feature snapshots

### Layer 2: Strategy evaluation

Input:

- feature snapshots
- canonical strategy version metadata

Responsibilities:

- evaluate each promoted or canonical strategy independently
- produce one `strategy_candidate` row per security per strategy per weekly run
- attach action code, rank, setup quality, evidence tier, and rationale fields
- keep strategy-specific logic isolated from board logic

Persistence target:

- `intelligence.strategy_candidates`

Important rule:

- `No action` is still a valid candidate outcome
- a candidate exists even when it never reaches the board

### Layer 3: Risk suppression

Input:

- strategy candidates
- shared risk rules

Responsibilities:

- evaluate event freezes and future suppressors after strategy detection
- mark hard blocks for fresh-cash promotion
- preserve suppression reason and details

Persistence target:

- `intelligence.candidate_suppressors`

Important rule:

- suppressors do not delete candidates
- they downgrade or block promotion

### Layer 4: Board promotion

Input:

- unsuppressed or partially suppressed strategy candidates
- weekly board assembly rules

Responsibilities:

- apply board eligibility rules
- dedupe by ticker
- select one `primary_source_strategy`
- preserve zero-to-many `supporting_strategies`
- assign final board rank and board type

Persistence targets:

- `intelligence.board_runs`
- `intelligence.board_rows`
- `intelligence.board_row_supporting_strategies`

## Service And Module Boundaries

### `packages/core`

Use for:

- shared feature logic
- strategy evaluation functions
- suppressor evaluation
- board promotion logic
- typed recommendation payload builders

Recommended new modules:

- `packages/core/strategy_registry.py`
- `packages/core/strategy_candidates.py`
- `packages/core/risk_suppressors.py`
- `packages/core/board_assembly.py`
- `packages/core/strategy_payloads.py`

### `packages/db`

Use for:

- SQLAlchemy models
- repositories and query helpers
- run-state helpers

Recommended repository targets:

- `DecisionBasisRepository`
- `ReplayRepository`
- `WeeklyReviewRepository`
- `StrategyCandidateRepository`
- `BoardRepository`

### `packages/schemas`

Use for typed contracts:

- strategy candidate DTOs
- suppressor DTOs
- board row DTOs
- strategy detail page DTOs
- replay summary DTOs

### `services/jobs`

Use for orchestration entrypoints:

- `weekly-run`
- `daily-run`
- `rebuild-weekly-review`
- `rebuild-strategy-candidates`
- `rebuild-board`

Weekly job sequence:

1. load latest normalized inputs
2. compute feature snapshots
3. evaluate strategy candidates
4. evaluate suppressors
5. assemble board outputs
6. build page-ready strategy and stock projections
7. validate completeness
8. publish run

### `apps/web`

Read-only rendering from persisted tables and projections.

Required surfaces:

- weekly overview
- stock detail
- strategy detail

Important rule:

- page loads must not call provider APIs or rerun strategy logic

## Runtime Flow

### Weekly job flow

```text
normalized market inputs
  -> derived feature snapshot
  -> strategy candidate generation
  -> suppressor generation
  -> board assembly
  -> strategy detail projections
  -> stock detail projections
  -> weekly publish
```

### Strategy detail page data flow

```text
decision basis version metadata
  + latest weekly strategy candidates
  + latest board rows referencing this strategy
  + replay summaries and slice stats
  -> strategy detail page view model
```

## Data Contracts

### Weekly board contract

The weekly board must render from:

- `board_run`
- `board_rows`
- `board_row_supporting_strategies`

Each row must include:

- `primary_source_strategy`
- `supporting_strategies`
- `fresh_cash_action_code`
- `setup_quality_band`
- `historical_evidence_tier`
- `why_now`
- `why_not_stronger`
- `invalidation_or_reassess`

### Strategy detail contract

The strategy detail page must render from:

- one `decision_basis_version`
- one current `weekly_review_run`
- candidate rows for this strategy
- board rows where this strategy is primary or supporting
- replay summary rows
- replay slice stats

Must support live candidate states:

- `Board-promoted`
- `Strategy-only`
- `Suppressed`

### Stock detail contract

The stock page must be able to show:

- current board status
- current strategy lineage
- all strategy candidates for the stock
- suppressor state

## Canonical Action Handling

Use the persisted enum layer from:

- `docs/engineering/requirements/tdd-2026-05-25-strategy-decision-basis-schema.md`

Important separation:

- fresh-cash actions belong on strategy candidates and board rows
- holder actions belong on position review objects
- context lenses and risk rules are not fresh-cash strategies

## Immediate Technical Constraints

### 1. Pullback implementation must narrow

Do not implement the broad aggregate pullback rules as the live mainline.

The first shipped pullback candidate evaluator should enforce:

- supportive regime preference
- explicit sector confirmation handling
- narrower pullback-depth bands
- controlled extension bands

### 2. Breakout implementation must stay triggered

Do not let breakout drift into:

- watchlist-near-high rows being treated as live buys

The live `BUY_NOW` path must require a triggered breakout in a supportive regime.

### 3. ETF rotation must stay off-board

Keep ETF candidates out of mainline board promotion until:

- a ranked weekly rotation variant is defined and replayed

ETF outputs may still appear in a shadow or research appendix later.

## Build Risks

### Risk 1: accidental monolithic fallback

If engineers shortcut directly to board rows without candidate persistence, the architecture collapses back into one opaque ranking table.

### Risk 2: label drift

If UI copy or old scripts keep inventing labels, strategy pages and weekly outputs will contradict the persisted action model.

### Risk 3: replay/prod mismatch

If mainline rules are implemented differently from replay-backed doctrine, trust will erode immediately.

### Risk 4: mixed strategy and holder logic

Fresh-cash actions and holder actions must remain separate tables and code paths.

## Acceptance Criteria

This architecture is correctly implemented when:

- each strategy is evaluated independently and persisted before board assembly
- suppressors can block promotion without deleting candidates
- the board uses `primary_source_strategy` and `supporting_strategies`
- strategy detail pages render from persisted metadata, replay, and live candidates
- breakout and narrowed pullback are the only mainline board feeders
- ETF and mean reversion remain off-board without special-case UI hacks

## Ready-To-Build Conclusion

The system is ready to move from planning to implementation.

The first engineering milestone is no longer “build a ranking engine.”

It is:

- build the candidate-first strategy engine,
- persist suppressors and board rows,
- and ship the weekly board plus first strategy detail pages on top of that contract.
