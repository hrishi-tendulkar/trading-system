# PRD: Holistic Watchlist And Universe Expansion

## Status

- Owner: Product Strategist + Public Equity Strategist
- Status: Active
- Date: 2026-06-06
- Workstream: Holistic watchlist / broader universe

## Problem

The current app-facing watchlist is still the `33`-name Phase 2 pilot. That is enough to prove the weekly report shape, but it is too narrow for a real opportunity-discovery workflow.

The repo already contains a broader `S&P 100 + ETF` watchlist and historical research built on that broader base. The product now needs a canonical universe system that can grow toward the `S&P 500` without turning the weekly review into a noisy 500-name research feed.

## Product Goal

Let the system scan a broad market universe while keeping the user-facing workflow selective, explainable, and weekly-decision shaped.

The product should support:

- broad coverage for quantitative screening and replay,
- a smaller active watchlist for recurring human attention,
- a weekly focus board for names worth review,
- and a sparse action board for capital decisions.

## Target User

One technically capable investor with limited weekday time who wants broad opportunity discovery but does not want to manually inspect hundreds of names every week.

## Product Principles

- Breadth belongs in the engine, not in the user workload.
- The active watchlist is not the same as the full coverage universe.
- The weekly board must stay sparse and action-oriented.
- Qualitative or AI-heavy review should be reserved for high-rank, changed, held, or risk-sensitive names.
- Every published weekly run must record which universe snapshot produced it.

## Universe Tiers

### 1. Coverage Universe

The full set the system can scan and backtest.

Initial target:

- `S&P 500` constituents,
- `S&P 100` as a smaller validated bridge,
- current holdings,
- user-added tactical candidates,
- benchmark ETFs,
- sector ETFs.

This layer is for deterministic screening, features, ranking, replay, and coverage diagnostics.

### 2. Active Watchlist

The recurring human-review set.

Target shape:

- initially `S&P 100 + ETFs`,
- later a curated `75-150` name subset of the coverage universe,
- includes current holdings, high-conviction long-term names, and tactical candidates.

This layer feeds the watchlist workspace and can receive richer stock-detail treatment.

### 3. Weekly Focus Board

The names that deserve attention this week.

Inputs:

- top promoted-strategy candidates,
- newly actionable names,
- deteriorating holdings,
- material event-risk names,
- names with major rank or setup-state changes.

Target size:

- `5-15` names.

### 4. Action Board

The capital-decision set.

Target size:

- `3-5` names in normal weeks.

Allowed action language stays aligned with the existing product:

- `Buy now`
- `Buy on pullback`
- `Hold / add`
- `Trim / exit`
- `Covered call candidate`
- `Cash-secured put candidate`
- `No action`

## User Workflows

### Weekly Review

1. User opens the weekly plan.
2. System shows market posture and freshness metadata.
3. System shows the sparse action board.
4. User can inspect the weekly focus board.
5. User can open stock detail pages for focus names or holdings.
6. User can see which universe snapshot and source data window powered the run.

### Watchlist Review

1. User opens the watchlist workspace.
2. System shows active universe metadata.
3. System groups names by role and recommendation status.
4. Names in the active universe but without a published recommendation are explicitly marked as awaiting projection.
5. The view remains scannable even when the active universe expands beyond the Phase 2 pilot.

### Universe Maintenance

1. System can regenerate broad reference universes such as `S&P 500` and `S&P 100`.
2. User can later promote or demote names between coverage, active watchlist, and custom candidate sets.
3. Historical weekly runs retain the universe snapshot used at publish time.

## Functional Requirements

### P0

- Introduce a canonical file-backed active universe source.
- Support `S&P 100 + ETF` as the first broader active universe.
- Add a repeatable `S&P 500 + ETF` reference builder.
- Wire app watchlist loading through the canonical universe source instead of hard-coded pilot fallbacks.
- Record universe name and source watchlist path in weekly run manifests.
- Add coverage facts to the watchlist workspace.
- Preserve existing Phase 2 weekly output behavior.

### P1

- Add a universe snapshot artifact per weekly run.
- Add active-watchlist subset support separate from coverage universe.
- Add coverage diagnostics: missing prices, missing sector, stale earnings date, missing recommendation projection.
- Add UI filters for sector, role, and recommendation state.

### P2

- Add database-backed universe and watchlist management using the existing Supabase schema direction.
- Add watchlist change history and user notes.
- Add rank-change and setup-state-change tracking across weekly runs.

## Finance Requirements

- The broader universe may increase candidate discovery but must not lower the promotion bar for the weekly board.
- The action board should only consume promoted or explicitly trusted decision bases.
- `S&P 500` coverage should improve replay sample size and sector breadth, not imply that every constituent has enough evidence for qualitative conviction.
- Board assembly should continue to prefer fewer higher-quality setups over filling rows.

## Non-Goals

- No intraday scanning.
- No brokerage execution.
- No AI deep dive for every `S&P 500` name.
- No broad-market recommendation feed that replaces the weekly action board.
- No immediate full CRUD requirement for watchlist management in the first slice.

## Success Criteria

- The app can render a broader active universe without code edits.
- The system can generate an `S&P 500 + ETF` reference file repeatably.
- Weekly run metadata identifies the source universe used.
- The watchlist page distinguishes active universe size from published recommendation coverage.
- Existing weekly, daily, archive, strategy, and stock pages continue to pass tests.

## Open Questions

- Should the default active universe become `S&P 100 + ETFs` immediately, or should it remain Phase 2 until a fresh S&P 100 weekly run is published?
- What is the preferred active-watchlist size once `S&P 500` coverage exists: `75`, `100`, or `150`?
- Which provider should become the long-term source of record for constituent membership once this moves beyond CSV bootstrap?
