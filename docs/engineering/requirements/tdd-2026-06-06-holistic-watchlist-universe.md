# TDD: Holistic Watchlist And Universe Expansion

## Status

- Owner: Tech Architect
- Status: Active
- Date: 2026-06-06
- Related PRD: `docs/product/requirements/prd-2026-06-06-holistic-watchlist-universe.md`

## Technical Objective

Introduce a lightweight canonical universe layer that lets the current CSV-backed app move beyond the `33`-name Phase 2 pilot while preserving traceability, weekly publish safety, and a path toward database-backed watchlist management.

## Current State

- `packages/core/ui_data.py` loads watchlist members from hard-coded fallbacks: `phase2_watchlist.csv`, then `mlp_watchlist.csv`.
- `scripts/mlp/publish_weekly_run.py` defaults to `data/reference/phase2_watchlist.csv`.
- `data/reference/sp100_watchlist.csv` already exists and has been used in research/replay flows.
- The Supabase schema already contains `ref.securities`, `app.watchlists`, `app.watchlist_entries`, and watchlist history tables, but the app bridge is file-backed today.

## Design Summary

Add a small file-backed universe module:

- defines known universe source paths,
- exposes the default active universe path,
- loads universe members from CSV,
- supports environment/config override without changing code,
- and gives publishing code metadata to persist in weekly manifests.

Keep this implementation deliberately simple:

- no database migration in this slice,
- no UI CRUD yet,
- no automatic run against all `S&P 500` names by default.

## Data Contracts

### Reference Universe CSV

Required columns:

- `ticker`
- `display_name`
- `sector`
- `is_benchmark`
- `is_active`

Optional future columns:

- `industry`
- `universe_tags`
- `source`
- `source_as_of_date`
- `constituent_type`

### Weekly Run Manifest Additions

Add optional manifest fields:

- `universe`
- `source_watchlist_path`

Existing manifests default to:

- `universe = "phase2"`
- `source_watchlist_path = "data/reference/phase2_watchlist.csv"`

## Implementation Plan

### 1. Universe Module

Create `packages/core/universes.py`.

Responsibilities:

- map known slugs to CSV paths,
- define `DEFAULT_ACTIVE_UNIVERSE = "phase2"` for compatibility,
- read `TRADING_SYSTEM_ACTIVE_UNIVERSE` or `TRADING_SYSTEM_WATCHLIST_PATH` overrides,
- validate required CSV columns,
- normalize tickers to uppercase and provider-safe hyphen format,
- expose `load_universe_members()`.

### 2. S&P 500 Builder

Create `scripts/mlp/build_sp500_watchlist.py`.

Responsibilities:

- fetch current S&P 500 constituents from Wikipedia,
- normalize ticker symbols for Yahoo-style downstream scripts,
- append benchmark and sector ETF context rows,
- write `data/reference/sp500_watchlist.csv`,
- preserve the same required CSV columns as current watchlist files.

### 3. UI Wiring

Update `packages/core/ui_data.py`.

Changes:

- use `active_universe_path()` instead of hard-coded Phase 2 fallback,
- expose watchlist facts:
  - active names,
  - published run,
  - active universe,
  - source file,
  - recommendation coverage.

### 4. Weekly Publish Metadata

Update `packages/core/weekly_runs.py` and `scripts/mlp/publish_weekly_run.py`.

Changes:

- add optional manifest fields for universe name and source watchlist path,
- populate them during publish,
- preserve backwards compatibility for existing manifest JSON.

### 5. Tests

Add or update tests for:

- default active universe stays Phase 2 compatible,
- explicit universe slug can load `sp100_watchlist.csv`,
- explicit path override works,
- weekly manifest round-trips universe metadata,
- watchlist view reports recommendation coverage.

## Feasibility Review

This is feasible as a small implementation slice because it does not require the database-backed watchlist model yet. It improves the system boundary while keeping the same CSV contracts the MLP scripts already consume.

The main risk is operator confusion if the active universe is switched to `S&P 100` or `S&P 500` without a corresponding fresh published recommendation run. The UI therefore must show recommendation coverage explicitly.

## QA Plan

- Run unit tests for universe loading and manifest serialization.
- Run existing UI and route tests.
- Run the S&P 500 builder in a smoke mode or against live source if network is available.
- Verify the watchlist page can render with the default Phase 2 universe and with an S&P 100 override.

## Future Database Path

When moving from CSV to Supabase:

- `ref.securities` becomes the security master,
- broad membership lives in a new `ref.universe_memberships` table or a versioned snapshot table,
- `app.watchlists` and `app.watchlist_entries` represent user-curated subsets,
- weekly runs pin a universe snapshot ID instead of only a source path.
