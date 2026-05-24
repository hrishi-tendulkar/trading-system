# Tech Architecture: Internal Platform V1

## Status

- Owner: Engineering
- Status: Draft
- Last updated: 2026-05-24

## Purpose

Define the implementation-ready technical architecture for the first real hosted version of Trading System.

This document answers:

- what we should build,
- how it should be deployed on `Railway` and `Supabase`,
- how GitHub should fit into the workflow,
- how the internal app should be protected,
- and how to keep the system small, traceable, and upgradeable.

## Executive Decision

Build `v1` as a Python-first internal platform with:

- one server-rendered internal web app,
- short-lived scheduled job services on `Railway`,
- `Supabase Postgres` as the system of record,
- `Supabase Storage` for raw artifacts and generated reports,
- `Financial Modeling Prep` plus `SEC EDGAR` as the initial data backbone,
- and a simple shared-password gate instead of full user-account infrastructure.

This is the lowest-complexity architecture that still gives us:

- a real hosted product,
- historical traceability,
- clean daily and weekly jobs,
- manual control surfaces,
- and a credible path to scale later.

## Why Python-First

The repo already leans Python-first for early data work, and the current mockup generation work also uses Python plus Jinja.

For this product, Python-first is the right technical default because it lets us:

- keep ingestion, scoring, and the web layer in one language,
- reuse finance logic directly between jobs and the UI,
- avoid a split frontend-plus-worker stack too early,
- render calm HTML pages server-side without building unnecessary client complexity,
- and keep Railway deployment simple.

Recommended framework choices:

- Web app: `FastAPI` with server-rendered `Jinja2` templates
- Styling: hand-authored CSS with a design system extracted from the mockup work
- Background and CLI tasks: `Typer`
- HTTP clients: `httpx`
- Data work: `pandas` only where it materially helps, otherwise SQL-first and typed Python
- Validation: `pydantic`
- Database access: `SQLAlchemy` plus `psycopg`
- Migrations: `Supabase SQL migrations` committed in repo

Do not introduce a React-heavy application layer in `v1` unless the UI later proves meaningfully more interactive than currently required.

## Hosting Topology

### Railway services

Use separate Railway services instead of one always-on worker with an in-process scheduler.

Recommended services:

1. `trading-system-web`
2. `trading-system-daily-job`
3. `trading-system-weekly-job`
4. `trading-system-manual-job`

Service roles:

- `trading-system-web`
  - public internal site
  - password gate
  - watchlist management
  - weekly review
  - daily digest
  - stock detail pages
  - manual rerun triggers

- `trading-system-daily-job`
  - Railway cron service
  - runs daily ingestion, normalization, and digest refresh
  - exits when complete

- `trading-system-weekly-job`
  - Railway cron service
  - runs full weekly recompute, ranking, and report generation
  - exits when complete

- `trading-system-manual-job`
  - no cron schedule
  - same codebase as jobs
  - used for backfills, provider replays, and one-off repair jobs via `railway run`

Why separate cron services:

- Railway’s official cron guidance expects scheduled services to run a task and terminate
- if a previous cron execution is still active, Railway skips the next one
- this fits our daily and weekly batch model well

Sources:

- [Railway cron jobs](https://docs.railway.com/reference/cron-jobs)
- [Railway cron, workers, queues guide](https://docs.railway.com/guides/cron-workers-queues)

### Supabase responsibilities

Use Supabase for:

- the primary relational database
- raw metadata and lineage
- derived features and score history
- run history and operational job status
- raw document and payload storage
- generated report artifacts

Do not use Supabase Edge Functions as the primary orchestration layer in `v1`.

## Security Model

## Decision

Do not build real multi-user auth in `v1`.

Use:

- one shared site password
- one signed HTTP-only session cookie
- server-side rendered pages
- server-only database access from the app

This matches the actual use case:

- you and your wife share one internal tool
- there is no real permissions model yet
- we want minimal operational burden

## Shared-password gate design

Implement an app-level password gate in `trading-system-web`:

- unauthenticated requests are redirected to `/login`
- login form posts the shared password
- the submitted password is compared against `APP_SHARED_PASSWORD_HASH`
- on success, the app issues a signed session cookie
- all product pages require a valid session cookie

Environment variables:

- `APP_SHARED_PASSWORD_HASH`
- `APP_SESSION_SECRET`
- `APP_ALLOWED_EMAILS` is intentionally not needed in `v1`

Why not Supabase Auth now:

- it adds user lifecycle and auth UI complexity we do not currently need
- the app will be server-rendered and server-owned anyway
- direct browser-to-database access is not required in `v1`

When to upgrade later:

- if you want named accounts
- if you want audit trails per user
- if you want per-user watchlists or preferences
- if you want to expose upload or edit capabilities from the browser using Supabase clients directly

Important constraint:

- the shared-password gate is operational protection, not enterprise identity
- all sensitive provider keys remain server-side only

## Database Architecture

Use separate schemas to preserve raw, normalized, derived, and operational boundaries.

Recommended schemas:

- `app`
- `ref`
- `raw`
- `market`
- `fundamentals`
- `intelligence`
- `ops`

### `app` schema

Purpose:

- application-managed entities and user-facing state

Core tables:

- `app.watchlists`
- `app.watchlist_entries`
- `app.watchlist_entry_history`
- `app.holdings`
- `app.tags`
- `app.watchlist_entry_tags`

### `ref` schema

Purpose:

- canonical reference entities used across the stack

Core tables:

- `ref.securities`
- `ref.security_identifiers`
- `ref.benchmarks`
- `ref.sectors`
- `ref.sector_etf_map`
- `ref.provider_symbols`

### `raw` schema

Purpose:

- immutable or append-only raw captures from providers

Core tables:

- `raw.provider_payloads`
- `raw.price_bars_fmp`
- `raw.earnings_calendar_fmp`
- `raw.fundamentals_fmp`
- `raw.news_fmp`
- `raw.transcripts_fmp`
- `raw.filing_index_sec`
- `raw.filing_sections_sec`

Key columns for `raw.provider_payloads`:

- `id`
- `provider`
- `endpoint`
- `symbol`
- `request_params_json`
- `payload_json`
- `fetched_at`
- `content_hash`
- `http_status`

### `market` schema

Purpose:

- normalized time-series and market-event facts

Core tables:

- `market.daily_prices`
- `market.benchmark_prices`
- `market.earnings_events`
- `market.news_items`
- `market.corporate_actions`
- `market.technical_indicator_snapshots`

### `fundamentals` schema

Purpose:

- normalized financial statements and fundamental trend facts

Core tables:

- `fundamentals.periods`
- `fundamentals.income_statements`
- `fundamentals.balance_sheets`
- `fundamentals.cash_flow_statements`
- `fundamentals.estimate_snapshots`
- `fundamentals.estimate_revision_events`

### `intelligence` schema

Purpose:

- derived features, score components, recommendations, and summaries

Core tables:

- `intelligence.feature_runs`
- `intelligence.stock_feature_snapshots`
- `intelligence.score_runs`
- `intelligence.stock_score_components`
- `intelligence.stock_scores`
- `intelligence.recommendations`
- `intelligence.stock_summaries`
- `intelligence.daily_digest_runs`
- `intelligence.daily_digest_items`
- `intelligence.weekly_review_runs`
- `intelligence.weekly_review_sections`
- `intelligence.outcome_windows`

### `ops` schema

Purpose:

- platform operations without a separate logging stack

Core tables:

- `ops.job_runs`
- `ops.job_run_steps`
- `ops.provider_request_stats`
- `ops.data_freshness`
- `ops.manual_actions`

This is the minimal observability layer we should keep even if we do not build centralized logging.

## Storage Architecture

Use private Supabase buckets for non-public assets.

Recommended buckets:

- `raw-filings`
- `raw-transcripts`
- `raw-provider-archives`
- `generated-reports`

Rules:

- keep buckets private
- store storage metadata and linkage in Postgres
- serve downloads through the web app, not public URLs by default

Relevant docs:

- [Supabase storage overview](https://supabase.com/docs/guides/storage)
- [Supabase storage buckets fundamentals](https://supabase.com/docs/guides/storage/buckets/fundamentals)
- [Supabase storage access control](https://supabase.com/docs/guides/storage/security/access-control)

## Data Flow

### Daily pipeline

1. Load active watchlist and required benchmark tickers.
2. Fetch latest EOD prices from `FMP`.
3. Fetch benchmark and sector ETF prices from `FMP`.
4. Fetch earnings calendar updates from `FMP`.
5. Fetch basic fundamentals refresh for changed names from `FMP`.
6. Fetch new SEC filing metadata and selected text.
7. Persist raw captures.
8. Normalize into `market` and `fundamentals`.
9. Recompute features for changed securities.
10. Refresh daily digest items.
11. Update `ops.job_runs` and `ops.data_freshness`.

### Weekly pipeline

1. Recompute all active watchlist features.
2. Rebuild short-term and long-term score components separately.
3. Generate recommendation rows and evidence summaries.
4. Generate weekly review sections.
5. Render and save weekly HTML artifact.
6. Save outcome anchor rows for later evaluation.
7. Update `ops.job_runs`.

### On-demand manual pipeline

Use `trading-system-manual-job` for:

- backfill a symbol
- rerun one day
- rerun one weekly review
- replay one provider payload
- rebuild indicators
- repair a stale digest

## UI Architecture

The UI should be server-rendered and calm, not terminal-like and not consumer-trading-noisy.

Primary pages:

- `/login`
- `/`
  - redirect to latest weekly review
- `/weekly`
  - latest weekly review
- `/weekly/{run_date}`
  - historical weekly review
- `/daily`
  - daily change digest
- `/watchlist`
  - manage active universe
- `/stocks/{ticker}`
  - stock detail page
- `/decision-bases/{slug}`
  - decision-basis detail page
- `/runs`
  - job run history
- `/admin`
  - rerun controls and freshness status

Page priorities:

- weekly review first
- daily digest second
- stock detail third
- admin controls simple and secondary

### Rendering strategy

Use:

- server-side HTML rendering
- minimal JavaScript
- optional `htmx` for small partial updates if useful

Do not rely on client-side state synchronization with Supabase in `v1`.

## Application API Design

Keep the app mostly page-first, not API-first.

Use internal endpoints only where they help:

- `POST /login`
- `POST /admin/jobs/daily-run`
- `POST /admin/jobs/weekly-run`
- `POST /admin/jobs/backfill`
- `POST /watchlist`
- `POST /watchlist/{id}/archive`

Admin-trigger endpoints must require:

- valid authenticated session
- a CSRF-safe form pattern
- server-side validation of allowed actions

## GitHub and Repository Strategy

Repository:

- owner: `hrishi-tendulkar`
- repo: `trading-system`

Monorepo structure:

```text
apps/
  web/
services/
  jobs/
packages/
  core/
  db/
  schemas/
infra/
supabase/
tests/
```

Recommended code layout:

- `apps/web`
  - FastAPI app
  - routes
  - templates
  - static assets
  - auth middleware

- `services/jobs`
  - Typer CLI
  - ingestion commands
  - normalization commands
  - feature computation
  - weekly review generation
  - backfill utilities

- `packages/core`
  - finance logic
  - score composition
  - recommendation labeling

- `packages/db`
  - SQLAlchemy models
  - connection helpers
  - repository layer

- `packages/schemas`
  - pydantic contracts
  - provider DTOs
  - response models

## CI Strategy

Use GitHub Actions for:

- lint
- unit tests
- template render smoke tests
- migration validation

Initial workflows:

1. `ci.yml`
   - run on pull requests and pushes
   - install Python
   - run formatter and linter
   - run tests

2. `supabase-migration-check.yml`
   - validate migration files exist and are ordered correctly
   - optionally run `supabase db push --dry-run` once local config is in place

Do not make GitHub Actions responsible for running production jobs in `v1`.

## Railway Deployment Model

Recommended source strategy:

- one repo
- multiple Railway services pointing at the same repo
- different start commands per service

Suggested start commands:

- `trading-system-web`
  - `uv run uvicorn apps.web.main:app --host 0.0.0.0 --port $PORT`

- `trading-system-daily-job`
  - `uv run python -m services.jobs.cli daily-run`

- `trading-system-weekly-job`
  - `uv run python -m services.jobs.cli weekly-run`

- `trading-system-manual-job`
  - `uv run python -m services.jobs.cli help`

Cron schedule recommendations:

- daily job:
  - `30 22 * * 1-5`
  - interpret as `22:30 UTC`
  - equivalent to `6:30 PM ET` during Eastern Daylight Time

- weekly job:
  - `0 14 * * 6`
  - interpret as `14:00 UTC Saturday`

Important note:

- Railway cron schedules are UTC-based
- keep seasonal timezone shifts in mind

Relevant docs:

- [Railway cron jobs](https://docs.railway.com/reference/cron-jobs)
- [Railway variables](https://docs.railway.com/variables)
- [Railway CLI variable command](https://docs.railway.com/cli/variable)

## Secrets and Environment Variables

### Shared across app and job services

- `ENVIRONMENT`
- `APP_BASE_URL`
- `APP_SESSION_SECRET`
- `APP_SHARED_PASSWORD_HASH`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`
- `FMP_API_KEY`
- `OPENAI_API_KEY`
- `SEC_USER_AGENT`

### Web-only

- `CSRF_SECRET`

### Job-only

- `DAILY_RUN_ENABLED`
- `WEEKLY_RUN_ENABLED`
- `AI_SUMMARY_MAX_SYMBOLS`

Rules:

- do not expose `SUPABASE_SERVICE_ROLE_KEY` to the browser
- do not use the public `anon` key in the browser in `v1`
- keep all data access server-side

## Supabase Migration Strategy

Manage schema in-repo through SQL migrations.

Why:

- explicit history
- easy review in GitHub
- clean deploy path
- less dashboard drift

Official CLI guidance supports:

- project linking
- SQL migrations
- `supabase db push` for applying local migrations to the linked project

Relevant docs:

- [Supabase CLI reference](https://supabase.com/docs/reference/cli/supabase-secrets.)
- [Supabase row level security](https://supabase.com/docs/guides/database/postgres/row-level-security)

## RLS Strategy

Because the browser will not connect directly to the database in `v1`, RLS is not the primary security boundary for app tables.

Recommended posture:

- keep app writes on server-side code using service-role access
- still enable RLS on tables in the exposed `public` schema if any are created there
- keep product tables in non-public schemas unless there is a clear reason not to
- keep storage buckets private

This reduces accidental exposure and keeps authorization simple.

## Provider Strategy

### V1 durable provider stack

- `Financial Modeling Prep`
- `SEC EDGAR`
- `OpenAI API`

### Bootstrap fallback

- `yfinance` may still be used for local validation, but not as the hosted system-of-record

Why `FMP` remains the durable default:

- official docs show broad endpoint coverage from one API family
- official pricing still supports the low-cost `Starter` entry point
- it reduces integration count materially

Relevant docs:

- [FMP quickstart](https://site.financialmodelingprep.com/developer/docs/quickstart)
- [FMP stock price and volume API](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full)
- [FMP pricing plans](https://site.financialmodelingprep.com/pricing-plans)

## Minimal Operability

The user said we do not need a heavy logging platform.

That is fine, but we still need operability.

Minimum acceptable operational features:

- `ops.job_runs` table
- status per run
- affected ticker counts
- provider request counts
- last-success timestamp per domain
- Railway deployment logs for debugging
- admin page showing stale domains and most recent failures

Do not add external log aggregation in `v1`.

## Backup and Recovery

Use:

- Supabase managed backups for the database
- raw artifacts in Supabase Storage
- GitHub as the source of truth for code and migrations

Recovery path:

1. restore code from GitHub
2. restore database from Supabase backup if needed
3. replay raw documents or provider backfills through manual job commands

## Implementation Phases

### Phase 1: Platform foundation

- create app and jobs code layout
- add Supabase migration structure
- create core schemas and watchlist tables
- build shared-password auth gate
- deploy web service shell

### Phase 2: Daily stock engine

- FMP price ingestion
- benchmark and sector ingestion
- SEC filing metadata ingestion
- normalized daily prices
- indicator snapshots
- daily digest page

### Phase 3: Weekly decision engine

- score components
- recommendation generation
- weekly review page
- stock detail page
- run history and admin reruns

### Phase 4: Qualitative depth

- transcript ingestion
- filing section extraction
- AI summaries
- richer event evidence

### Phase 5: Evaluation and refinement

- outcome windows
- recommendation replay
- decision-basis detail pages
- later options module planning

## Current Platform State

As of `2026-05-24` in this workspace:

- GitHub CLI is authenticated
- Supabase CLI is authenticated and the `Trading System` project is linked
- Railway CLI is installed, but the current local auth session has expired and needs a fresh `railway login`

Implication:

- GitHub and Supabase work can proceed from CLI now
- Railway mutations are currently blocked until the CLI session is refreshed

## Final Recommendation

The best holistic `v1` architecture is:

- `FastAPI + Jinja2` internal web app
- `Typer`-driven Python job services
- `Railway` web plus short-lived cron services
- `Supabase Postgres` plus private storage buckets
- `FMP + SEC EDGAR + OpenAI`
- shared-password session gate
- migration-first schema management in GitHub

This gives us the smallest serious product that is still worthy of being the real system backbone.
