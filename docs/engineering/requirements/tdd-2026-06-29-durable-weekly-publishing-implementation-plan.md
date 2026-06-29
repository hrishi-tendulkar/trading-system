# TDD: Durable Weekly Publishing Implementation Plan

## Status

- Owner: Engineering
- Status: Proposed implementation plan
- Last updated: 2026-06-29
- Related design: `docs/engineering/architecture/tech-design-2026-06-29-durable-weekly-publishing.md`
- Related RCA: `docs/engineering/rcas/rca-2026-06-29-weekly-run-automation.md`

## Goal

Implement the durable weekly publishing architecture so the scheduled weekly job can publish the current weekly report into production without manual local execution, Git commits, or web redeploys.

## High-Level Strategy

Ship this as a reliability migration in thin vertical slices:

1. Preserve the current file-backed behavior behind a repository interface.
2. Add Supabase-backed persistence behind the same interface.
3. Move `/weekly`, `/archive`, and the publisher onto the interface.
4. Backfill existing weekly snapshots into Supabase.
5. Add production validation and alerting.
6. Deploy Railway cron services and run the QA loop until the publish invariant holds.

## Product Manager Notes

The existing weekly publishing PRD already covers the user-facing requirements. Product does not need new scope unless the user wants:

- a visible admin operations page for job history,
- or richer user-facing failure copy.

For this implementation, product acceptance should stay narrow:

- `/weekly` is current when automation succeeds,
- `/weekly` is loudly stale/missing when automation fails,
- archive history remains reconstructable.

## Engineering Workstreams

### Workstream 1: Repository Boundary

Add a repository interface in core code.

Deliverables:

- `WeeklyRunRepository` protocol or abstract base.
- `LocalWeeklyRunRepository` wrapping existing `data/processed/weekly_runs` behavior.
- Repository factory controlled by configuration:
  - `WEEKLY_RUN_REPOSITORY=local|supabase|auto`.
- Unit tests proving local behavior matches current file-backed behavior.

Acceptance:

- Existing weekly run tests pass through the local repository.
- No production web or publisher code calls weekly-run filesystem helpers directly except through the local adapter.

### Workstream 2: Supabase Schema

Add migration for durable weekly publishing.

Deliverables:

- Extend `intelligence.weekly_review_runs` with durable manifest fields, or add companion table if safer.
- Add `intelligence.weekly_current_run`.
- Add `intelligence.weekly_recommendation_records`.
- Add `intelligence.weekly_run_payloads`.
- Add indexes and constraints for current-run reads and run lookup.
- Add model/schema tests or SQL migration smoke tests.

Acceptance:

- Migration applies cleanly.
- There is an explicit current pointer.
- Failed runs can be retained without becoming current.
- Published current read is indexed and deterministic.

### Workstream 3: Supabase Repository

Implement `SupabaseWeeklyRunRepository`.

Deliverables:

- Insert building run.
- Upsert recommendations.
- Store manifest and payload snapshots.
- Atomically publish current run.
- Supersede previous run.
- Read current manifest, run manifest, archive list, recommendations, and payloads.
- Error handling for missing credentials and connection failures.

Acceptance:

- Repository contract tests pass against a test Supabase/local Postgres target or mocked database boundary.
- Publishing a failed run does not alter the current pointer.
- Publishing a new run supersedes the old current run.

### Workstream 4: Publisher Integration

Move the weekly publishing command onto the repository.

Deliverables:

- `services.jobs.cli weekly-run` writes via repository.
- `scripts/mlp/publish_weekly_run.py` no longer assumes production writes to local files.
- Run status transitions:
  - `building`,
  - `validation_failed`,
  - `failed`,
  - `published`.
- Existing publish gates still run before current pointer update.
- Target-week logic uses latest expected prior market close and correctly handles Saturday/Sunday runs.

Acceptance:

- Saturday or Sunday automated run targets the following Monday recommendation week.
- Stale source data blocks publication.
- Previous current run remains current on failure.
- CLI exits non-zero on failure.

### Workstream 5: Web Integration

Move web projections onto the repository.

Deliverables:

- `/weekly` loads current run through repository.
- `/archive` lists repository manifests.
- Archive detail loads run-specific records through repository.
- Staleness warnings use repository metadata.
- Local file-backed mode still works for dev.

Acceptance:

- Production can show a newly published Supabase run without redeploy.
- `/weekly` displays current metadata from Supabase.
- Missing current-week warnings still render.
- Archive pages render previous Supabase runs.

### Workstream 6: Backfill

Migrate current file snapshots into Supabase.

Deliverables:

- Backfill command:

```bash
python3 -m services.jobs.cli backfill-weekly-runs-to-supabase
```

- Idempotent import from `data/processed/weekly_runs`.
- Preserve run IDs, manifest metadata, recommendations, and current pointer.
- Dry-run mode.

Acceptance:

- Existing published runs are present in Supabase.
- Current pointer matches `data/processed/weekly_runs/current.json`.
- Re-running backfill does not duplicate records.

### Workstream 7: Validation And Alerting

Add operational validation.

Deliverables:

- CLI command:

```bash
python3 -m services.jobs.cli validate-weekly-current
```

- Checks:
  - expected recommendation week,
  - expected source-through date,
  - current run status,
  - current pointer,
  - production `/weekly` metadata,
  - absence of missing-current warning.
- Alert interface and first channel implementation.
- Email notifications to `hrishi00@gmail.com` for both success and failure.
- `ops.job_runs` and `ops.job_run_steps` writes for publish and validation.

Acceptance:

- Command exits zero only when production invariant is true.
- Command exits non-zero and alerts when current run is missing or stale.
- Success and failure notifications are sent for publish and validation outcomes.
- Validation can run locally with `--as-of-date`.

### Workstream 8: Railway Deployment

Deploy scheduled production workflow.

Deliverables:

- Railway web service env configured for Supabase repository reads.
- Railway weekly cron service env configured for Supabase repository writes.
- Railway validation cron service env configured for Supabase repository reads and production URL check.
- Engineer verifies `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_URL`, and `APP_BASE_URL` are present and non-placeholder in Railway without printing secret values.
- Document exact deploy/config commands in a runbook.

Acceptance:

- Weekly publish can run in Railway and update Supabase.
- Web service shows the new run without redeploy.
- Validation cron checks the live app after publish.
- Failure alert reaches `hrishi00@gmail.com`.
- Success heartbeat reaches `hrishi00@gmail.com`.

## Proposed Implementation Order

1. Add repository interface and local adapter.
2. Refactor current code to use the local adapter without behavior change.
3. Add Supabase schema migration.
4. Implement Supabase adapter and contract tests.
5. Backfill existing snapshots into Supabase.
6. Switch web reads to repository factory.
7. Switch publisher writes to repository factory.
8. Add publish job ops logging.
9. Add validation command.
10. Add alerting.
11. Configure Railway services.
12. Run QA loop and fix defects.

Implementation default:

- Store v1 weekly UI payloads in Postgres JSONB.
- Use Supabase Storage only for artifacts that are large, binary, or demonstrably unsuitable for JSONB.
- Treat Supabase/Railway credential verification as engineering-owned implementation work.

## QA Strategy

QA owns the user-visible invariant, not just unit tests.

### Automated QA

Required tests:

- local repository preserves existing current pointer behavior,
- Supabase repository publishes current atomically,
- validation-failed run does not replace current,
- Saturday/Sunday target-week logic chooses following Monday,
- source-through date respects market holidays,
- `/weekly` renders Supabase current metadata,
- `/weekly` warns when current week is missing,
- `/archive` renders Supabase-backed historical run,
- `validate-weekly-current` fails on stale repository state,
- `validate-weekly-current` fails on live web mismatch.

### Manual QA

Manual checks after Railway deploy:

1. Run a controlled weekly publish for a test target week.
2. Confirm Supabase run row, recommendation rows, current pointer, and ops job row.
3. Open production `/weekly`.
4. Confirm recommendation week, data-through date, published timestamp, run ID, and status.
5. Open `/archive`.
6. Confirm old run is still available.
7. Run `validate-weekly-current` against production.
8. Simulate stale expected week or wrong source-through date and confirm validation fails.

## Engineer And QA Loop

Use this loop until there are no P0/P1 defects:

1. Engineer implements a slice.
2. Engineer runs unit and route tests.
3. Engineer deploys or stages the slice where required.
4. QA runs the automated and manual checks for that slice.
5. QA files defects with:
   - exact URL or command,
   - expected result,
   - actual result,
   - logs/screenshots when available,
   - severity.
6. Engineer fixes defects.
7. QA retests the same checks plus one regression pass.
8. Tech Architect signs off when the weekly publish invariant holds end to end.

## Definition Of Done

- Supabase is the production weekly-run source of truth.
- Railway weekly cron writes to Supabase.
- Railway web service reads from Supabase.
- Production `/weekly` updates after scheduled publish without redeploy.
- Previous current run remains live on failed publish.
- Missing or stale current week is visible on `/weekly`.
- Post-cron validation runs automatically.
- Publish and validation success/failure emails reach `hrishi00@gmail.com`.
- Existing archive behavior is preserved.
- Runbook documents deploy, manual repair, and validation commands.

## Implementation Decisions

1. Alert channel: email to `hrishi00@gmail.com`.
2. Notification policy: send both success heartbeats and failure alerts.
3. Railway schedule: Sunday 03:00 ET publish and Sunday 04:00 ET validation.
4. Supabase/Railway credentials: engineer verifies and configures them during implementation.
5. Artifact storage: keep v1 payloads in Postgres JSONB; move large/binary artifacts to Supabase Storage only when needed.
