# PRD: Weekly Run Publishing And Staleness Protection

## Status

- Owner: Product
- Status: Proposed
- Last updated: 2026-06-03

## Purpose

Define the product requirements for making the weekly recommendation report an explicit published run, not an incidental view of whichever CSV or data file happens to be newest.

This closes the product gap exposed when the current weekly page showed `Week of 2026-05-22` even though the user expected the next weekly plan for `Week of 2026-06-01`.

## User Job

Every weekend, the user needs one trustworthy weekly plan for the next market week.

The product should answer:

- what should I review before Monday or Tuesday trading?
- which recommendations are current for the upcoming week?
- what data did the system use?
- when was the plan published?
- if the plan is stale or missing, what exactly failed?

## Product Decision

The product must treat weekly recommendations as a lifecycle:

1. refresh source data,
2. run the strategy engine,
3. validate completeness,
4. publish a new weekly report,
5. make that report the current `/weekly` view,
6. preserve the prior report as an immutable archive object.

The weekly page must never silently imply that an old report is current.

## Cadence

### Daily data refresh

The system should refresh end-of-day market and event data on trading days after market close.

This refresh supports both:

- weekday addenda against the current published plan,
- and the next weekend weekly run.

### Weekly publish

The system should publish one official weekly report after the prior trading week has closed.

Default target:

- Sunday evening ET.

Acceptable manual fallback:

- Saturday or Sunday after the latest complete prior-week data is available.

The published report is the plan for the following market week.

Example:

- data through: `2026-05-29`
- recommendation week: `Week of 2026-06-01`
- published: Sunday evening before Monday open

## Required Weekly Run Metadata

Every weekly report must show:

- recommendation week
- publish timestamp
- data-through timestamp
- source-data freshness status
- timezone
- run ID
- engine version
- strategy registry version
- current lifecycle status

The weekly page should make this metadata visible near the top of the page.

## Staleness Rules

The product must detect when the current weekly report is stale or missing.

### Missing current-week report

If the current date is inside or after a new recommendation week and no published run exists for that week, the weekly page must show a warning.

Example:

`No weekly report has been published for Week of 2026-06-01. Latest available report is Week of 2026-05-22.`

### Stale source data

If the source data used for a weekly run does not reach the latest expected prior-week trading close, the system must block publication or mark the run as incomplete.

The page must not present an incomplete run as the current weekly plan.

### Failed weekly run

If the weekly job fails, the prior published run remains visible, but the page must clearly say that the current week is missing.

The failure should be visible in admin or operational output, not buried in logs only.

## Archive Requirements

When a new weekly report is published:

- the previous weekly report remains accessible in Archive,
- its overview, stock details, strategy outputs, metadata, and recommendation records must remain reconstructable,
- later addenda and outcomes may be appended,
- the original weekly recommendation content must not be rewritten by later strategy or data changes.

Archive is not a list of old rows. It is a time-travel view of what the product believed at publish time.

## Current MLP Bridge

The current file-backed MLP may satisfy this requirement with file snapshots before full Supabase persistence exists.

Acceptable bridge shape:

- keep a latest published run pointer,
- write run-specific snapshot folders under `data/processed/weekly_runs/`,
- store the current run metadata as structured JSON,
- make `/weekly` read the current published run pointer,
- make `/archive` list prior published run snapshots.

This bridge is acceptable only if it preserves the lifecycle and staleness semantics.

## Non-Goals

- intraday monitoring
- automated trade execution
- silently generating reports on page refresh
- replacing weekly reports with weekday daily checks
- broad options workflow expansion before the stock-first weekly run is reliable

## Acceptance Criteria

- The user can open `/weekly` and immediately know whether the report is current for the upcoming market week.
- A stale May report cannot look like the current June report.
- The system can explain which data date the report used.
- A failed or incomplete weekly job does not overwrite the last good published report.
- A newly published report automatically moves the prior full report into Archive.
- The archive can reconstruct the old weekly overview and related detail surfaces without depending on current strategy logic.

## Success Test

This requirement is satisfied when the user can ask:

`What is my current weekly plan?`

and the product can answer with either:

- the correct published plan for the upcoming market week,
- or a loud, specific explanation that the current weekly plan is missing.
