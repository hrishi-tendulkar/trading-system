# PRD: Lean V1 Budget Launch

## Status

- Owner: Product
- Status: Draft
- Last updated: 2026-05-24

## Purpose

Define a budget-constrained `v1` of the Weekly Equity Intelligence product that can launch on approximately `~$22-$30/month` of third-party data spend.

This PRD intentionally narrows scope from the broader long-term vision. It focuses on shipping a useful weekly stock-intelligence product first, rather than prematurely building a richer research platform or options-overlay system.

## Problem Statement

The full Weekly Equity Intelligence vision is broad, but the current user goal is narrower:

- keep recurring data cost extremely low,
- avoid real-time dependencies,
- and still produce a useful weekly decision workflow.

Without deliberate scope cuts, the product will drift into:

- data spend that is too high for a personal project,
- excessive integration complexity,
- and features that sound impressive but do not materially improve the weekly user outcome.

## User

- One technically capable investor
- Roughly `$200,000` of capital under active management
- Limited weekday time
- Wants concise weekly buy / hold / trim / monitor guidance
- Is comfortable with delayed data and daily or weekly refreshes

## Product Goal

Launch the first useful version of the product at a recurring data cost of roughly `~$22-$30/month`, using:

- `Financial Modeling Prep Starter`
- `SEC EDGAR`

Before that launch, the team may use a `free bootstrap mode` for local-only validation:

- `yfinance` / Yahoo Finance for EOD watchlist prices where available
- `SEC EDGAR` for filings

The product should produce a weekly stock review workflow that helps the user:

- rank current watchlist names,
- identify possible buys,
- identify names to hold or trim,
- and preserve a historical record of recommendations and outcomes.

## Product Principles

- Weekly decision quality over data completeness
- Stock engine first, options later
- End-of-day data is sufficient
- Delayed insight is acceptable if it is actionable and reliable
- Explainability matters more than sophistication theater
- Product scope should reflect actual personal-project constraints
- Free bootstrap data is acceptable for learning, but not automatically good enough for the durable product

## In-Scope Outcome

The user should be able to open the system once a week and quickly answer:

- Which stocks on my list look strongest now?
- Which ones are breaking down or becoming less attractive?
- Which names deserve more research this week?
- What changed since last week?

## Out-of-Scope Outcome for This Version

This version is not trying to answer:

- which covered call should I sell this week,
- which cash-secured put should I sell this week,
- how should I optimize options premium,
- or how should I act intraday after market-moving events.

Those are explicitly deferred.

## Product Summary

Lean `v1` is a single-user weekly stock-intelligence tool built around a curated watchlist of roughly `50-70` names.

It will combine:

- daily price and volume data,
- earnings calendar awareness,
- lightweight fundamentals,
- direct SEC filing capture,
- and a small set of deterministic technical and event-driven signals

to produce a weekly ranked review and a lightweight daily change digest.

## Core User Workflow

### Weekly workflow

Frequency:

- once per week, ideally on the weekend

Steps:

1. Open the weekly review.
2. See market context and ranked watchlist names.
3. Review top `Buy / Improve / Hold / Deteriorate / Avoid` candidates.
4. Open stock detail pages for names that materially changed.
5. Decide whether to buy, hold, trim, or monitor.

### Daily workflow

Frequency:

- optional, brief review after market close

Steps:

1. Open the daily change digest.
2. See which stocks moved materially, had earnings, or received new filings.
3. Decide whether anything deserves attention before the next weekly review.

## Core Product Jobs

Lean `v1` must help the user:

- maintain a canonical watchlist,
- score names on a small set of weekly-relevant signals,
- identify change since last review,
- avoid broken setups,
- and build a recommendation history for future refinement.

## P0 Scope

These are the must-have features for the budget launch.

### 1. Watchlist workspace

- manually manage active tickers
- store ticker, company name, sector, strategy tags, and position status
- preserve watchlist history

### 2. Daily batch ingestion

- EOD prices and volume
- benchmark and sector ETF prices
- basic corporate actions if available from provider
- earnings calendar and actual results where available
- core fundamentals
- direct SEC filing metadata and text capture

Bootstrap note:

- a local validation pass may use `yfinance` for the price-history subset of this ingestion
- the launch-grade product should still assume a more stable provider-backed source for scheduled unattended refreshes

### 3. Lean signal engine

The first version should compute only a minimal but useful set of signals:

- price vs key moving averages
- relative strength vs `SPY`
- relative strength vs sector ETF
- pullback or extension distance from recent highs and support zones
- ATR / simple volatility context
- volume ratio vs trailing average
- earnings proximity
- post-earnings reaction
- basic fundamental trend flags

### 4. Weekly ranking and review

For each stock:

- score summary
- key changes since last week
- action label
- short evidence summary

### 5. Daily change digest

- biggest watchlist movers
- stocks with earnings
- new filings
- notable score changes

### 6. Recommendation history

- save each weekly run
- store scores, action labels, and evidence summaries
- track forward performance windows for later review

## P1 Scope

These improve the product but should not block launch.

### 1. Transcripts

- earnings call transcripts for top-ranked names or holdings

### 2. Richer analyst revision history

- deeper revision and target-price-change workflows if the chosen provider or later upgrade supports it credibly

Why free Yahoo-style access is not enough by itself:

- it may cover price history surprisingly well for a personal watchlist
- it does not cleanly answer the product need for stable fundamentals, revision history, transcripts, and durable unattended jobs
- therefore it can reduce early spend, but it does not eliminate the need for a paid provider once the product moves beyond bootstrap validation

### 3. Better news ingestion

- more complete company news coverage and classification

### 4. Broader regime analysis

- breadth and internal market-health measures beyond simple benchmark and sector context

## P2 Scope

These are intentionally deferred.

### 1. Covered-call and cash-secured-put workflows

- option chain ingestion
- overlay ranking
- option-specific recommendation cards

### 2. Advanced qualitative workflows

- transcript-driven tone shifts
- filing delta comparison
- narrative change scoring

### 3. Rich backtesting UI

- interactive signal and setup analysis interface

### 4. Real-time or intraday workflows

- intraday bars
- live event alerts
- streaming updates

## Explicit Non-Goals

- brokerage integration
- automated order execution
- options engine in v1
- institutional-grade data breadth
- complex portfolio optimization
- fully autonomous trade recommendations

## Data Budget Constraint

Target monthly third-party data cost:

- preferred: `~$22/month`
- acceptable ceiling for this phase: `~$30/month`

Recommended stack:

- `FMP Starter`
- `SEC EDGAR`

This means the product must be designed to work well with delayed, incomplete, and narrower data relative to the full future vision.

## Core Outputs

### Weekly review

Must include:

- market context
- ranked watchlist
- top opportunities
- deteriorating names
- weekly changes

### Stock detail view

Must include:

- price context
- signal summary
- upcoming earnings or recent event context
- recent filings
- weekly history of recommendation and score movement

### Daily digest

Must include:

- material movers
- event flags
- names worth checking before the next weekly review

## Action Taxonomy

Lean `v1` should use a simpler action set than the full roadmap:

- `Buy candidate`
- `Watch for entry`
- `Hold`
- `Deteriorating`
- `Avoid / no action`

This is intentionally narrower than the broader long-term action model.

## Success Criteria

Lean `v1` is successful if:

- the user can complete a weekly review in roughly `15-30 minutes`
- the ranked watchlist feels directionally useful and explainable
- the product consistently surfaces changes that matter
- the product creates a trustworthy recommendation history
- the system runs on the target budget without fragile manual effort

## Risks

### 1. Data breadth risk

`FMP Starter` may not provide enough estimate-history depth for the full strategy vision.

Mitigation:

- design around a lean stock engine first
- treat richer revision workflows as upgrade paths

### 2. Over-promising on options

The larger strategy includes covered calls and cash-secured puts, but this budget version should not pretend to fully support them.

Mitigation:

- explicitly defer options to later phases

### 3. False precision

With lean data, the system may be tempted to produce overly confident outputs.

Mitigation:

- favor simple rankings and evidence summaries over complex composite scores

## Release Recommendation

Ship this as:

- a lean stock-intelligence launch
- budget-optimized
- delayed-data friendly
- intentionally narrower than the full product vision

The right test is not “does it do everything?” but “does it help the user make better weekly stock decisions at very low recurring cost?”
