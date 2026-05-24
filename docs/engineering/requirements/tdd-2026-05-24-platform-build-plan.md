# TDD: Platform Build Plan V1

## Status

- Owner: Engineering
- Status: Draft
- Last updated: 2026-05-24

## Purpose

Translate the platform architecture into an execution-oriented build plan for the first hosted version of Trading System.

## Build Target

Ship an internal hosted product with:

- one password-protected web app,
- one daily refresh job,
- one weekly review job,
- manual backfill capability,
- Supabase-backed history,
- and GitHub-managed code plus migrations.

## Scope

Included:

- repo structure
- deployment shape
- data model foundation
- security approach
- job boundaries
- CI expectations

Excluded:

- complex multi-user auth
- real-time streams
- options engine
- external observability stack

## Required Deliverables

### 1. Repo skeleton

Must exist:

- `apps/web`
- `services/jobs`
- `packages/core`
- `packages/db`
- `packages/schemas`
- `supabase/migrations`
- `tests`

### 2. Platform config

Must exist:

- Python dependency and lock setup
- Railway service start-command definitions documented in repo
- Supabase migration workflow documented in repo
- `.env.example` without real secrets

### 3. Database foundation

Must exist:

- watchlist tables
- reference security tables
- raw payload tables
- normalized market tables
- intelligence output tables
- ops job-run tables
- published-run state fields for digest and weekly review outputs

### 4. Web shell

Must exist:

- login page
- weekly review shell
- daily digest shell
- stock detail shell
- admin shell

### 5. Jobs CLI

Must exist:

- `daily-run`
- `weekly-run`
- `backfill-symbol`
- `rebuild-features`
- `rebuild-weekly-review`
- `validate-run-completeness`

## Non-Functional Requirements

- all business logic should be callable outside the web layer
- all scheduled jobs should be runnable locally from CLI
- all database changes should be migration-backed
- all product pages should render from stored data, not live provider calls
- all provider integrations should write raw captures before normalized writes
- incomplete runs must not overwrite currently published outputs
- schema drift between SQL migrations and Python models must be test-detected

## Service Contracts

### Web service contract

Inputs:

- Supabase database
- Supabase storage

Responsibilities:

- authenticate via shared password
- render all pages from stored data
- accept small admin write actions
- never call third-party providers directly on page load

### Daily job contract

Inputs:

- active watchlist
- provider credentials

Responsibilities:

- ingest and normalize daily data
- update derived features for changed names
- refresh digest state
- record job status

### Weekly job contract

Inputs:

- normalized daily and fundamental data

Responsibilities:

- recompute scores
- generate recommendations
- generate weekly review artifacts
- record job status

### Manual job contract

Inputs:

- operator-supplied command parameters

Responsibilities:

- perform targeted backfills or repairs
- avoid hidden side effects
- record job status

## Web UX Requirements

The web app should feel like an internal decision cockpit, not a generic dashboard.

Requirements:

- weekly review is the default landing experience after login
- all key action labels visible above the fold
- stock detail pages separate observed facts from derived views
- admin functions should not dominate primary navigation
- mobile should remain usable for quick checks even if desktop is the main mode

## Security Requirements

- shared password must be hashed, not stored in plaintext
- session cookies must be `HttpOnly`, `Secure`, and signed
- session cookies must also be `SameSite=Strict`
- provider keys must remain server-side
- all admin mutation endpoints require authenticated session
- raw document buckets must stay private
- login attempts must be rate-limited
- password rotation must invalidate old sessions

## Data Requirements

### Day-one required provider coverage

- daily OHLCV
- benchmark and sector prices
- earnings calendar
- basic fundamentals
- SEC filing metadata

### Day-one required derived outputs

- moving averages
- relative strength
- ATR or equivalent volatility context
- earnings proximity
- post-earnings flag
- recommendation label

### Day-one required publication safety

- explicit `published` versus `building` run states
- completeness thresholds for daily and weekly publish
- stale-data suppression for core outputs
- prior published run remains visible if a replacement run fails

### Day-one required UI outputs

- weekly board
- daily digest
- stock detail
- job freshness status

## Build Order

1. Set up repo skeleton and dependency management.
2. Initialize `supabase/migrations`.
3. Create schema foundation and job-run tables.
4. Build web app shell and password gate.
5. Build database access layer.
6. Build `daily-run`.
7. Add run-state and completeness-validation logic.
8. Build weekly score generation and review rendering.
9. Add admin rerun actions.
10. Add CI.
11. Add transcript and AI layers only after the core loop works.

## Acceptance Criteria

The platform build plan is complete when:

- the site is reachable on Railway behind the shared password gate
- the latest weekly review can render from stored database rows
- the daily job can run without manual edits
- the weekly job can run without dashboard-only steps
- a failed daily or weekly run does not replace the currently published output
- login rate-limiting and session invalidation behavior exist
- new migrations are applied through the Supabase CLI flow
- GitHub remains the source of truth for code and schema
