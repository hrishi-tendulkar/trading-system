# Tech Strategy: Lean V1

## Status

- Owner: Engineering
- Status: Draft
- Last updated: 2026-05-24

## Purpose

Define the overall technical strategy for the lean, budget-constrained first version of the Weekly Equity Intelligence system.

This strategy assumes:

- one user
- batch-first operation
- delayed data is acceptable
- roughly `~$22-$30/month` data budget
- a temporary `free` bootstrap path is allowed for local validation
- stock engine first
- options overlays deferred

## North Star

Build a technically simple, traceable, and upgradeable weekly stock-intelligence system that works well enough to prove the workflow before we pay for broader or higher-quality data.

## Strategy Summary

The technical strategy for lean `v1` is:

- use one broad low-cost vendor for most stock-engine data,
- use direct SEC EDGAR for filings and source-of-truth traceability,
- run daily batch jobs and one weekly synthesis job,
- store raw, normalized, and derived layers separately,
- and design the system so richer providers can be swapped in later without rewriting the whole product.

Recommended vendor stack:

- `FMP Starter`
- `SEC EDGAR`

Allowed bootstrap stack for local validation only:

- `yfinance` / Yahoo Finance data where available
- `SEC EDGAR`

## Architectural Priorities

### 1. Optimize for simplicity

Use the fewest moving parts that can still support:

- daily ingestion
- weekly scoring
- recommendation history
- and future upgrades

### 2. Preserve separation of layers

Even in a lean build, keep separate:

- source capture
- normalized tables
- derived features
- recommendation outputs

### 3. Avoid provider lock-in in the schema

Even if the first version uses mostly one provider, the internal schema should not mirror that provider’s JSON directly.

### 4. Build for degraded data gracefully

If a field is missing, the system should downgrade confidence or skip a feature rather than break the weekly workflow.

### 5. Keep options out of the critical path

Do not design the first architecture around options overlays. They can be added later as a separate data and feature module.

## Recommended Technical Shape

### Runtime model

- daily scheduled ingestion jobs
- one weekly synthesis job
- optional lightweight local or hosted review UI

### Storage model

- `Supabase Postgres` for normalized, derived, and recommendation data
- `Supabase Storage` or local file storage for raw source payloads if needed

### Compute model

- Python jobs on `Railway` or local-first execution initially
- SQL and Python for feature generation
- OpenAI only for limited summarization or evidence compression where justified

## Recommended Layering

### Layer 1: Source adapters

Inputs:

- `FMP`
- `SEC EDGAR`

Responsibilities:

- fetch raw payloads
- map source-specific IDs
- apply minimal source validation

### Layer 2: Normalization

Responsibilities:

- standardize price, earnings, fundamentals, and filing data
- attach timestamps, ticker mappings, and source lineage
- preserve point-in-time context where available

### Layer 3: Feature computation

Responsibilities:

- compute moving averages, ATR, relative strength, and event flags
- create simple fundamental trend fields
- detect weekly changes

### Layer 4: Recommendation synthesis

Responsibilities:

- generate weekly action labels
- attach compact evidence summaries
- persist each run for historical review

### Layer 5: Delivery

Responsibilities:

- produce weekly review artifact
- produce daily change digest
- support stock detail lookup

## Data Strategy

### Use `FMP Starter` for

- daily prices
- benchmark and sector context
- basic fundamentals
- earnings calendar and basic event fields
- any lightweight stock-engine support it can provide under the starter plan

### Use `SEC EDGAR` for

- filing metadata
- filing text
- traceable evidence capture

### Use `yfinance` only for bootstrap validation

- personal-use local prototyping
- quick watchlist price history pulls
- lightweight earnings-date checks if they happen to resolve cleanly

Do not treat `yfinance` as the durable system-of-record source for lean `v1`.

Reasons:

- the project itself describes `yfinance` as intended for research and educational use and reminds users that Yahoo Finance data is intended for personal use only
- Yahoo-based access is unofficial from our perspective and can change without notice
- non-price surfaces such as earnings metadata have a history of being more fragile than simple historical chart pulls
- the free path does not solve the broader `P0/P1` requirements around fundamentals, revisions, transcripts, or stable backfill behavior

Implication:

- `yfinance + SEC` is acceptable to prove the signal spine cheaply
- `FMP Starter + SEC` remains the recommended first durable operating stack once we want unattended jobs and a repeatable historical record

### What we are intentionally not solving in lean v1

- robust transcripts
- robust options chains
- institutional-grade revision history
- real-time event or quote handling

## System Boundaries

### In scope

- watchlist-centric stock intelligence
- daily batch ingestion
- weekly recommendation generation
- historical recommendation storage

### Out of scope

- broker connectivity
- options pipeline
- streaming jobs
- multi-user auth model
- interactive heavy analytics stack

## Recommended Evolution Path

### Phase 1

- prove the signal spine with `yfinance + SEC` if we want zero recurring spend first, or start directly with `FMP Starter + SEC` if we want the first durable implementation

### Phase 2

- upgrade to `FMP Premium` or `Ultimate` only if the stock engine proves valuable and the missing data materially hurts quality

### Phase 3

- add a dedicated options provider such as `Massive` or `ThetaData` only when options overlays become a real product priority

### Phase 4

- split broader data responsibilities across specialist vendors only if the current stack becomes a clear bottleneck

## Technical Trade-Offs

### Accepted trade-off 1: lower cost over richer data

This version accepts narrower coverage and lower confidence in some advanced signals in exchange for very low recurring cost.

Additional note:

- zero-cost market data is acceptable for bootstrap validation, but not assumed to be operationally stable enough for the long-lived system of record

### Accepted trade-off 2: end-of-day over real-time

The system is intentionally delayed and batch-driven.

### Accepted trade-off 3: deterministic spine over ambitious AI

The first version should rely mainly on deterministic logic and use AI sparingly.

### Accepted trade-off 4: stock engine over full strategy vision

The technical foundation should prove the stock-ranking workflow before carrying the complexity of options overlays.

## Architecture Risks

### 1. Provider undercoverage

If `FMP Starter` is too shallow in practice, the product may need a faster upgrade than planned.

### 2. Overloading one provider

Using one main provider is efficient, but it can create hidden fragility.

Mitigation:

- keep normalization boundaries explicit
- keep SEC direct ingestion independent

### 3. Schema drift later

If schemas mirror vendor payloads too closely, upgrades will be painful.

Mitigation:

- design canonical internal tables now

## Recommendation

Architect lean `v1` as a small but real system:

- one broad provider
- one official filings source
- one database
- a few scheduled jobs
- explicit layers
- and clear room to upgrade later

This is the right technical posture for a personal project that is trying to prove decision quality, not build an institutional platform on day one.

Practical stance:

- if we want the cheapest possible learning loop, start with `yfinance + SEC` for local experiments and CSV/backfill validation
- if we want the first unattended, durable weekly engine, spend the `~$22/mo` and use `FMP Starter + SEC`
