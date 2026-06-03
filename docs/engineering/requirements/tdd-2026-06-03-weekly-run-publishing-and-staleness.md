# TDD: Weekly Run Publishing And Staleness Protection

- Date: 2026-06-03
- Owner: Tech Architect / Engineer
- Status: Proposed implementation requirement
- Related PRD: `docs/product/requirements/prd-2026-06-03-weekly-run-publishing-and-staleness.md`
- Related TDD: `docs/engineering/requirements/tdd-2026-06-02-weekly-archive-and-addenda.md`

## Goal

Make weekly report publishing an explicit, validated lifecycle so the app cannot accidentally show an old recommendation dataset as if it were current.

The immediate failure mode to prevent:

- `/weekly` renders `Week of 2026-05-22`
- the user expects `Week of 2026-06-01`
- the system gives no warning that a newer weekly run is missing

## Design Principle

The weekly page reads from the latest successfully published weekly run.

It must not infer currentness from:

- the first row date of a recommendation CSV,
- the file with the newest mtime,
- page refresh time,
- or an ad hoc script default.

## Required Run Lifecycle

Use explicit run states:

- `building`
- `validation_failed`
- `failed`
- `published`
- `superseded`

Rules:

- only `published` runs can become the current `/weekly` source,
- a failed or validation-failed run never replaces the previous published run,
- publishing a new run marks the previous current run as `superseded`,
- archived views must be able to reconstruct superseded runs.

## Weekly Run Identity

Every weekly run needs stable metadata:

- `run_id`
- `recommendation_week_start`
- `recommendation_week_end`
- `published_at`
- `timezone`
- `market_data_through`
- `source_data_through`
- `engine_version`
- `strategy_registry_version`
- `input_snapshot_id`
- `output_snapshot_id`
- `run_status`
- `created_at`

For the current MLP bridge, `run_id` may be deterministic:

`weekly_{recommendation_week_start}_published_{published_date}`

Example:

`weekly_2026-06-01_published_2026-05-31`

## File-Backed Bridge

Before Supabase-backed persistence is fully wired, implement a file-backed published-run store.

Recommended layout:

```text
data/processed/weekly_runs/
├── current.json
├── weekly_2026-05-22_published_2026-05-22/
│   ├── manifest.json
│   ├── recommendations.csv
│   ├── overview_payload.json
│   ├── stock_detail_payloads.json
│   └── strategy_snapshot_payloads.json
└── weekly_2026-06-01_published_2026-05-31/
    ├── manifest.json
    ├── recommendations.csv
    ├── overview_payload.json
    ├── stock_detail_payloads.json
    └── strategy_snapshot_payloads.json
```

`current.json` points to the latest `published` run only.

The app may keep reading legacy `data/processed/phase2/mlp_current_recommendations.csv` during the transition, but it must also compute and display staleness status. The legacy CSV should not be treated as proof that the weekly plan is current.

## Weekly Publish Job

Create or refactor a weekly publish command that performs:

1. resolve target recommendation week,
2. refresh or verify source data through the latest expected prior trading close,
3. compute features,
4. run promoted strategy candidates,
5. assemble the weekly board,
6. generate UI projection payloads,
7. validate completeness and freshness,
8. write a run snapshot,
9. atomically update `current.json` only if validation passes.

Recommended command shape:

```bash
python3 -m services.intelligence.publish_weekly_run --target-week 2026-06-01
```

or, while scripts remain the bridge:

```bash
python3 scripts/mlp/publish_weekly_run.py --target-week 2026-06-01
```

## Publish Gates

The weekly publish job must fail before publication if:

- source price data does not include the latest expected prior-week trading close,
- benchmark data is missing,
- active watchlist coverage is materially incomplete,
- strategy candidate generation fails,
- board assembly fails,
- required metadata is missing,
- generated payloads cannot be loaded by the web projection layer.

The old published run must remain current when any gate fails.

## Staleness Detection

Add a projection-layer freshness check that compares:

- expected recommendation week,
- current published run recommendation week,
- source data through date,
- and current date.

The check should return:

- `current`
- `missing_current_week`
- `source_data_stale`
- `unknown`

The weekly page should display warnings for every state except `current`.

## Expected Week Logic

For v1, the expected recommendation week can be computed conservatively:

- weekly reports cover Monday through Friday market weeks,
- the target week starts on the next Monday after the latest complete Friday close,
- Sunday publish targets the Monday that follows the prior Friday close.

The implementation should isolate this logic in one helper so market-holiday handling can be added later without touching templates.

## Archive Integration

When a new run is published:

- the previous `current.json` target remains in `data/processed/weekly_runs/`,
- archive index includes both old and new run manifests,
- archive detail reads the run-specific snapshot, not current strategy logic,
- daily addenda attach to the published run ID rather than replacing it.

This aligns with `tdd-2026-06-02-weekly-archive-and-addenda.md`.

## Current Code Hotspots

Known current behavior:

- `packages/core/ui_data.py` loads `data/processed/phase2/mlp_current_recommendations.csv`.
- `_run_metadata()` builds recommendation week and published labels from the first row date.
- `scripts/mlp/fetch_watchlist_prices.py` defaults to `--end 2026-05-23`, producing data through `2026-05-22`.

These are acceptable as temporary bridge pieces, but not as the final weekly publishing contract.

## Implementation Sequence

1. Add weekly-run manifest schema and file-backed run repository.
2. Add freshness / expected-week helper.
3. Add staleness banner data to weekly projections.
4. Add weekly publish script that writes a run snapshot and updates `current.json` atomically.
5. Make `/weekly` prefer the file-backed published run store.
6. Make `/archive` list run snapshots rather than only reconstructing the current CSV.
7. Move the same contracts into Supabase when persistence phase resumes.

## Tests

Required tests:

- latest published run renders as current when recommendation week matches expected week,
- stale legacy CSV produces a `missing_current_week` warning,
- validation-failed weekly run does not update `current.json`,
- archive can render a superseded run after a newer run is published,
- source-data-through date appears on weekly page,
- page refresh does not start the publish job.

## Acceptance Criteria

- The app cannot silently present `2026-05-22` as the current weekly plan when `Week of 2026-06-01` is expected.
- A missing weekly run is visible to the user on `/weekly`.
- The weekly publish job has explicit validation gates.
- The last good run remains visible when a new run fails.
- Archive reconstruction reads saved run snapshots, not mutable current logic.
