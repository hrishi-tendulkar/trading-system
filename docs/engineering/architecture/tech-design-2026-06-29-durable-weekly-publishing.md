# Tech Design: Durable Weekly Publishing

## Status

- Owner: Tech Architect
- Status: Proposed for implementation
- Last updated: 2026-06-29
- Related RCA: `docs/engineering/rcas/rca-2026-06-29-weekly-run-automation.md`
- Related PRD: `docs/product/requirements/prd-2026-06-03-weekly-run-publishing-and-staleness.md`
- Related TDD: `docs/engineering/requirements/tdd-2026-06-03-weekly-run-publishing-and-staleness.md`

## Purpose

Make the weekly recommendation report publish automatically and reliably without manual local execution, commits, or Railway web redeploys.

The system must guarantee this product invariant:

> After the scheduled weekly publish window, production `/weekly` either shows the correct current report for the upcoming market week or loudly explains why the current report is missing.

## Problem

The current bridge stores weekly snapshots under `data/processed/weekly_runs/`. That works locally because the publisher and web app share the same filesystem.

In production, the Railway weekly cron job and Railway web service run in separate containers. The weekly job can generate files, but those files are written inside the job container and are not visible to the already-running web service. The web service reads files baked into its Docker image, so generated reports only become visible after commit and redeploy.

This means Railway cron success is not equivalent to publish success.

## Product Requirements

No new broad product requirement is needed. The existing product requirement remains correct:

- one trustworthy weekly plan for the upcoming market week,
- visible recommendation week, publish timestamp, data-through date, timezone, run ID, engine version, strategy version, and lifecycle status,
- failed or incomplete runs must not replace the previous good run,
- stale or missing current-week reports must be visible on `/weekly`,
- archive views must reconstruct old reports from stored run snapshots.

Product clarification still needed before deployment:

- Send success and failure email notifications to `hrishi00@gmail.com`.

## Decision

Use Supabase as the production weekly-run system of record.

The weekly publisher and web app must both use the same `WeeklyRunRepository` contract:

- local development and tests use `LocalWeeklyRunRepository`,
- Railway production uses `SupabaseWeeklyRunRepository`,
- generated files inside Docker images are no longer the production source of truth.

## Why Supabase

Supabase is the preferred solution because the broader platform architecture already designates Supabase Postgres as the system of record and Supabase Storage as the artifact store.

Compared with alternatives:

- Railway shared volume: lower migration effort, but weaker historical/query model and less aligned with archive/outcome evaluation.
- GitHub Actions committing files: useful as an emergency fallback, but it keeps generated data in Git and still depends on redeploy semantics.
- Supabase: durable shared storage, queryable history, archive support, future outcome evaluation, and clean operational status records.

## Target Architecture

```text
Railway weekly cron service
  startCommand: python3 -m services.jobs.cli weekly-run
        |
        v
Weekly publisher
  - resolves target recommendation week
  - fetches/verifies source data
  - generates recommendations and UI payloads
  - validates publish gates
        |
        v
WeeklyRunRepository
  local: data/processed/weekly_runs
  prod: Supabase Postgres + Supabase Storage
        |
        v
Production web app
  - reads current published run from repository
  - renders /weekly and /archive from stored snapshots
        |
        v
Post-cron validator
  - checks repository current run
  - checks production /weekly metadata
  - alerts on failure
```

## Run Lifecycle

Use explicit lifecycle states:

- `building`
- `validation_failed`
- `failed`
- `published`
- `superseded`

Rules:

- Only `published` runs can become current.
- `validation_failed` and `failed` runs are retained for diagnosis but never replace the previous current run.
- Publishing a new current run marks the prior current run `superseded`.
- Archive reads run-specific snapshots, not current strategy logic.
- Page refresh never starts a publish job.

## Schedule Strategy

Default production schedule:

- Weekly publish: Sunday 03:00 America/New_York.
- Post-cron validation: Sunday 04:00 America/New_York.

Why Sunday 03:00 ET:

- the prior trading week has fully closed,
- provider data has had a buffer to settle,
- the run completes well before Monday pre-market review,
- a one-hour validation window leaves time for repair before the trading week starts.

The weekly command must compute the target week from the latest complete market close, not from a naive "current calendar week" default. A Saturday or Sunday run after the prior week has closed should publish the following Monday recommendation week.

## Repository Contract

Define a `WeeklyRunRepository` interface with these operations:

- `begin_run(manifest) -> run_id`
- `write_recommendations(run_id, records)`
- `write_payload(run_id, payload_name, payload)`
- `mark_validation_failed(run_id, reason)`
- `mark_failed(run_id, reason)`
- `publish_current(run_id)`
- `get_current_manifest()`
- `get_manifest(run_id)`
- `list_manifests()`
- `load_recommendations(run_id)`
- `load_payload(run_id, payload_name)`
- `validate_current(expected_week, expected_source_through)`

Production code must not call filesystem helpers directly except inside `LocalWeeklyRunRepository`.

## Supabase Data Model

Extend or normalize the existing `intelligence.weekly_review_runs` model rather than creating a separate schema island.

Minimum production tables:

### `intelligence.weekly_review_runs`

One row per weekly publish attempt.

Required fields:

- `id`
- `run_id`
- `recommendation_week_start`
- `recommendation_week_end`
- `published_at`
- `timezone`
- `market_data_through`
- `source_data_through`
- `last_checked_at`
- `status`
- `engine_version`
- `strategy_registry_version`
- `input_snapshot_id`
- `output_snapshot_id`
- `universe`
- `source_watchlist_path`
- `active_strategy_versions_json`
- `manifest_json`
- `failure_reason`
- `created_at`
- `updated_at`

Constraints:

- `run_id` unique.
- At most one current published run, enforced through a current pointer table or partial unique index.
- `status` constrained to the lifecycle states.

### `intelligence.weekly_current_run`

Singleton pointer to the current published run.

Required fields:

- `id`
- `run_id`
- `published_at`
- `updated_at`

This avoids computing currentness from newest timestamp or filesystem mtime.

### `intelligence.weekly_recommendation_records`

One row per stored recommendation row.

Required fields should preserve the current CSV contract while allowing richer future strategy rows:

- `weekly_review_run_id`
- `ticker`
- `company`
- `as_of_date`
- `action_label`
- `holder_bucket`
- `strategy_name`
- `observed_reason`
- `event_risk`
- `stop_label`
- `stop_value`
- `raw_record_json`

### `intelligence.weekly_run_payloads`

Stores generated UI payload snapshots as Postgres JSONB for v1.

This is the default implementation choice because the current weekly payloads are small enough to keep the system simple and queryable. Move individual artifacts to Supabase Storage only when payload size, binary format, or database bloat makes that necessary.

Required fields:

- `weekly_review_run_id`
- `payload_name`
- `payload_json`
- `content_hash`
- `created_at`

### Supabase Storage

Use a private bucket later for larger generated artifacts:

- reports,
- CSV snapshots,
- optional full UI projection payloads if they grow large.

The database row should store the storage path and content hash.

## Job Observability

Use `ops.job_runs` and `ops.job_run_steps` for every scheduled publish and validation run.

Required status values:

- `running`
- `succeeded`
- `failed`

For `weekly-run`, success means the run was published into the shared repository. It does not mean the Railway process merely exited.

For `validate-weekly-current`, success means:

- the repository current pointer exists,
- the current run is `published`,
- recommendation week matches expected week,
- source-through date matches expected prior market close,
- production `/weekly` renders matching metadata,
- no current-week-missing warning appears.

## Validation Command

Add:

```bash
python3 -m services.jobs.cli validate-weekly-current
```

Required options:

- `--as-of-date YYYY-MM-DD` for deterministic tests and manual repair.
- `--base-url URL` for checking the deployed web app.
- `--repository local|supabase|auto`.
- `--alert on|off`.

The command must exit non-zero on failure.

## Alerting

Alert on:

- weekly publish failure,
- validation failure,
- missing current run,
- stale source-through date,
- production `/weekly` mismatch,
- repository connection/auth failure.

Initial acceptable channels:

- email to `hrishi00@gmail.com`.

The implementation should keep alert dispatch behind a small interface so the channel can be changed without touching publish logic.

Send both success and failure notifications for the weekly publish and post-cron validation jobs.

## Railway Deployment Model

Use two scheduled services:

### Weekly publish service

- Schedule: Sunday 03:00 ET.
- Command: `python3 -m services.jobs.cli weekly-run`.
- Environment:
  - Supabase URL and service role key.
  - Repository mode set to Supabase.
  - Provider keys.
  - Alert configuration.

### Weekly validation service

- Schedule: Sunday 04:00 ET.
- Command: `python3 -m services.jobs.cli validate-weekly-current --base-url $APP_BASE_URL`.
- Environment:
  - Supabase URL and service role key.
  - App base URL.
  - Alert configuration.

The web service uses the same repository mode and Supabase credentials, but only reads published runs.

The engineer owns verifying and configuring the Railway environment. The local repo already defines `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_URL`, and `APP_BASE_URL`; implementation must confirm the corresponding Railway services have correct non-placeholder values and set any missing variables.

## Failure Behavior

If the weekly run fails before publication:

- persist the failed attempt,
- keep prior current run unchanged,
- show current-week missing warning on `/weekly`,
- send alert.

If publication succeeds but `/weekly` does not reflect it:

- validation fails,
- send alert,
- do not mutate the published run,
- treat this as a deployment/configuration bug.

If alert dispatch fails:

- record alert failure in `ops.job_run_steps`,
- keep the job failure exit code.

## Security

Use server-side Supabase access only.

Requirements:

- Supabase service role key must never be exposed to browser JavaScript.
- Railway environment variables hold production secrets.
- Local `.env.example` documents required variable names only.
- Tests use local repository or mocked Supabase client.
- Implementation must verify Railway service variables without printing secret values in logs or review notes.

## Migration Strategy

1. Add database migration for durable weekly publishing tables/columns.
2. Implement repository interface and local repository adapter over existing files.
3. Implement Supabase repository.
4. Backfill existing `data/processed/weekly_runs` snapshots into Supabase.
5. Make web reads use repository mode.
6. Make weekly publisher write to repository mode.
7. Add validation command and scheduled service.
8. Remove Docker-baked weekly files as production source of truth after Supabase path is verified.

## Acceptance Criteria

- A scheduled weekly publish can update production `/weekly` without a Git commit or web redeploy.
- The web app and publisher read/write the same production repository.
- The old current run remains visible when a new run fails.
- `/weekly` shows a warning when the expected current week is missing.
- `/archive` can render Supabase-backed historical runs.
- `validate-weekly-current` fails when production is stale.
- A post-cron scheduled validation exists and alerts without user prompting.
- Existing file-backed tests still pass through `LocalWeeklyRunRepository`.

## Open Decisions

- Exact Railway service names and whether validation is a separate service or a second cron entry if the platform supports it cleanly.
