# TDD: Weekly Archive and Scheduled Addenda

- Date: 2026-06-02
- Owner: Tech Architect / Engineer
- Status: Initial implementation slice
- Related PRD: `docs/product/weekly-equity-intelligence-prd.md`

## Goal

Implement the product rule that weekly recommendations are immutable published artifacts, while weekday jobs produce scheduled addenda that update current state without rewriting the original weekly plan.

## Current Implementation Slice

The current app is a FastAPI/Jinja presentation slice backed by CSV recommendation data. This slice adds:

- `GET /archive`
- `GET /archive/{week_id}`
- archive navigation
- weekly metadata labels on `GET /weekly`
- archive data projections in `packages/core/ui_data.py`
- route and data tests

This is intentionally a presentation-safe bridge until Supabase-backed run persistence is wired.

## Target Data Model

### `weekly_report_runs`

Stores immutable weekly report headers.

Required fields:

- `id`
- `recommendation_week_start`
- `recommendation_week_end`
- `published_at`
- `timezone`
- `market_data_through`
- `source_data_through`
- `last_checked_at`
- `run_status`
- `engine_version`
- `strategy_registry_version`
- `scoring_config_hash`
- `universe_snapshot_id`
- `holdings_snapshot_id`
- `source_snapshot_id`
- `model_config`
- `created_at`

### `weekly_report_snapshots`

Stores the rendered or renderable product state for the weekly report.

Required fields:

- `weekly_report_run_id`
- `overview_payload`
- `market_posture_payload`
- `fresh_cash_payload`
- `holder_payload`
- `trim_exit_payload`
- `options_overlay_payload`
- `deep_dive_queue_payload`
- `strategy_snapshot_payload`
- `source_metadata_payload`

### `weekly_recommendation_records`

Stores every recommendation row at publish time.

Required fields:

- `weekly_report_run_id`
- `ticker`
- `recommendation_category`
- `decision_basis_type`
- `decision_basis_name`
- `source_strategy_id`
- `action_rank`
- `tradeability_score`
- `conviction_score`
- `overlay_suitability_score`
- `risk_penalty`
- `entry_zone`
- `invalidation`
- `target_1`
- `target_2`
- `expected_holding_period`
- `key_catalyst`
- `evidence_summary`
- `why_now`
- `why_not_stronger`
- `recommended_expression`
- `published_status`

### `weekly_report_addenda`

Stores scheduled weekday checks and event-driven updates.

Required fields:

- `id`
- `weekly_report_run_id`
- `checked_at`
- `addendum_type`
- `ticker`
- `previous_status`
- `new_status`
- `summary`
- `materiality`
- `source_snapshot_id`
- `supersedes_recommendation_record_id` when applicable

### `weekly_report_outcomes`

Stores later evaluation without mutating original recommendations.

Required fields:

- `weekly_report_run_id`
- `ticker`
- `window`
- `forward_return`
- `benchmark_return`
- `hit_entry`
- `hit_target`
- `hit_invalidation`
- `review_label`
- `review_note`
- `computed_at`

## Job Behavior

### Weekly publish job

Runs Sunday evening ET by default.

Steps:

1. Load source snapshots and watchlist / holdings state.
2. Recompute full-universe features and strategy candidates.
3. Promote board rows.
4. Generate weekly report projections and deep-dive queue.
5. Persist immutable run, snapshot, and recommendation records.
6. Publish only after all required sections pass completeness checks.

### Weekday scheduled addendum job

Runs after market close on weekdays.

Steps:

1. Load latest published weekly run.
2. Refresh market, event, filing, transcript, analyst, and news inputs as available.
3. Recompute only enough state to detect material changes.
4. Append addenda for triggered, invalidated, frozen, promoted-for-review, or demoted names.
5. Update `last_checked_at`.
6. Do not replace original weekly recommendation records.

### Page refresh

Page refresh only reads the latest completed run and addenda. It must not start analysis jobs.

## Implementation Plan

1. Add presentation-layer archive projections from the current recommendation contract.
2. Add `/archive` and `/archive/{week_id}` routes and templates.
3. Add weekly metadata labels to the weekly page.
4. Add tests for archive route rendering and archive data reconstruction.
5. Prepare Supabase migrations for the target model in the next persistence phase.
6. Wire weekly and weekday jobs to persist real archive objects after the job layer is database-backed.

## QA Requirements

- Verify archive routes require login.
- Verify archive detail returns 404 for unknown week IDs.
- Verify the weekly page shows recommendation week, published, data-through, and last-checked metadata.
- Verify archive detail separates original weekly plan, daily addenda, deep dives, outcomes, and captured scope.
- Verify page refresh does not trigger job execution.
- Verify mobile and desktop layouts do not overlap or hide metadata.
