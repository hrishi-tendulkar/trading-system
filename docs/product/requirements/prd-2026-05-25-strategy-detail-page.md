# PRD: Strategy Detail Page

## Status

- Owner: Product + Finance
- Status: Proposed
- Last updated: 2026-05-25

## Purpose

Define the product requirements for a `strategy deep dive page` that sits alongside:

- the weekly overview page,
- and the stock detail page.

This page exists to make each canonical strategy inspectable, trust-calibrated, and usable in the weekly decision loop.

It is not a passive wiki page.

It should help the user answer:

- whether this strategy deserves live trust,
- what it is surfacing this week,
- how much of that output should influence capital deployment,
- and how current recommendations connect to the overview board and stock pages.

## Why this page matters

The system is no longer one monolithic ranking model.

It is now a small strategy lab with unequal strategy maturity and unequal live trust:

- `Breakout Confirmation`: `Core`
- `Sector-Confirmed Pullback Continuation`: `Core but narrowed / trust-calibrated`
- `ETF Trend / Rotation`: `Refine before promotion`
- `Selective Mean Reversion`: `Research only`

That means the product needs a dedicated strategy surface that can:

- show what a strategy is,
- show what it is doing this week,
- show why it should or should not influence the main action board,
- and preserve the distinction between `canonical`, `mainline`, `board-eligible`, and `research`.

Without this page, the product risks either:

- hiding too much strategy logic behind the weekly board,
- or dumping too much strategy detail into stock pages and overview.

## Product job

Primary job:

- `For this strategy, should I trust it this week, what is it recommending, and how should that affect my weekly actions?`

Secondary jobs:

- inspect exact canonical logic and recent rule changes
- evaluate replay quality and known failure modes
- review strategy-specific candidate lists before or alongside board promotion
- understand why a stock appeared on the overview board through this strategy

## Goals

- Make every canonical strategy inspectable through one stable page shape.
- Make trust level and promotion status impossible to miss.
- Show live/current strategy outputs before deeper documentation.
- Support canonical strategies that are not currently feeding the overview action board.
- Preserve board doctrine:
  - strategies are evaluated independently first
  - overview is a promotion layer
  - one ticker appears once on overview with primary and supporting lineage
- Align to schema direction:
  - versioned strategy metadata
  - replay summaries
  - live/current strategy matches
  - suppressor-aware interpretation
- Help the user make the weekly decision faster and with better calibration.

## Non-goals

- Replacing the weekly overview board as the main entry point
- Replacing stock detail as the place for full single-name synthesis
- Showing raw research exhaust or every backtest table by default
- Treating all canonical strategies as equally trusted or equally live-ready
- Rebuilding one opaque cross-strategy master score on this page

## User questions this page must answer

### Identity and trust

- What is this strategy trying to capture?
- Is it a `trade setup`, `risk rule`, or `context lens`?
- Is it `Core`, `Core but narrowed / trust-calibrated`, `Refine before promotion`, or `Research only`?
- Is it canonical but not currently feeding the main action board?
- What should I trust about it, and what should I treat cautiously?

### This week

- What is this strategy recommending this week?
- Which names are live now versus waiting for confirmation or pullback?
- Which outputs are suppressed by risk rules and therefore not board-eligible?
- Which names were promoted to the overview board from this strategy?
- Which names are strategy-only and why were they not promoted?

### Historical evidence

- How has this strategy performed historically in replay?
- In which regimes or sub-buckets has it worked best?
- Where has it failed, degraded, or become noisy?
- How much evidence supports current live usage?

### Rules and change management

- What exact canonical rules define the current version?
- What was narrowed, tightened, or changed recently?
- Did recent changes increase trust, reduce scope, or move it out of live promotion?

### Weekly operating implication

- Should this strategy directly influence fresh-cash decisions this week?
- Should I use it as an action source, a watchlist source, or a research source only?
- If I open a candidate from here, how does it connect to the stock page and overview board?

## Trust and promotion model

The page must show two separate but related concepts:

### 1. Strategy trust level

Allowed labels:

- `Core`
- `Core but narrowed / trust-calibrated`
- `Refine before promotion`
- `Research only`

This is the strategy-level trust statement.

It reflects both:

- replay quality,
- and the current degree of rules confidence.

### 2. Current promotion status

Allowed labels:

- `Feeding main action board`
- `Board-eligible only through narrowed rules`
- `Canonical, not currently feeding main action board`
- `Research only, excluded from main board`

This is the workflow-level status statement.

It answers whether the strategy can currently promote names into the weekly overview action board.

Important product rule:

- trust level and promotion status must never be collapsed into one badge

Example:

- `ETF Trend / Rotation` can remain canonical while showing:
  - trust level: `Refine before promotion`
  - promotion status: `Canonical, not currently feeding main action board`

## Recommended page structure

### 1. Header

Must show:

- strategy name
- decision-basis type
- trust level badge
- promotion status badge
- current version id
- last updated date
- one-sentence strategy purpose

### 2. This week at a glance

This is the decision-first module.

Must show:

- as-of week
- number of live matches
- number of board-promoted names
- number of suppressed matches
- dominant action mix:
  - `Buy now`
  - `Buy on pullback`
  - `Wait for confirmation`
  - `Do not chase`
  - `No action`
- one-sentence interpretation such as:
  - `Useful this week, but only through narrowed confirmed setups`
  - `Producing watch names, but not trusted for main-board promotion`

### 3. Current recommendations

Must show a strategy-specific table or card list of live/current matches.

Required fields per row:

- ticker
- current action
- setup quality band
- historical evidence tier
- current live status
  - `Board-promoted`
  - `Strategy-only`
  - `Suppressed`
- primary or supporting lineage status
- why now
- why not stronger
- suppression reason if applicable
- link to stock detail

This section should default to:

- board-promoted first
- then live but not promoted
- then suppressed

### 4. Strategy interpretation

Must explain:

- what the strategy is really expressing
- when to use it
- what kind of entries it prefers
- what a good current signal looks like
- what a false positive usually looks like

This is the human-readable strategy memo, but it should stay concise and decision-linked.

### 5. Historical evidence

Must summarize replay quality in a compact, decision-usable way.

Required content:

- replay sample window
- universe
- sample size
- forward-return horizons used
- average returns
- excess returns vs `SPY`
- win rates
- short verdict
  - `Promote now`
  - `Promote cautiously via narrowed rules`
  - `Refine before promotion`
  - `Research only`

Must also show:

- best-performing contexts
- weak or negative contexts
- why the aggregate should or should not be trusted

### 6. Where it works and fails

Must break out:

- supportive regimes
- weak regimes
- supportive sector states
- weak sector states
- setup sub-buckets that helped
- sub-buckets that degraded outcomes
- known structural failure modes

This should connect directly to live interpretation, not read like an academic appendix.

### 7. Canonical rules

Must show the exact rule spine for the current version.

Required structure:

- entry conditions
- context requirements
- exclusion or suppression rules
- expected holding style
- invalidation or reassess logic
- board-eligibility rules

Important display rule:

- canonical rules should be shown in plain language first
- with expandable exact field-level logic underneath

### 8. Recent changes

Must show version-aware change history.

Required fields:

- version changed from and to
- date changed
- what changed
- why it changed
- expected product impact
  - more selective
  - higher trust
  - reduced board eligibility
  - moved to research-only

### 9. Lineage and connections

Must show:

- overview board names currently sourced from this strategy
- names where this strategy is supporting but not primary
- link to stock detail pages for live candidates
- link to canonical strategy doc and replay summary

## Above the fold

Above the fold should answer four things immediately:

1. What is this strategy?
2. How much should I trust it?
3. Is it influencing the main board this week?
4. What is it recommending right now?

Recommended above-the-fold composition:

- header with trust and promotion badges
- one-sentence purpose and one-sentence current interpretation
- `This week at a glance` summary strip
- top `3-5` live matches with status:
  - `Board-promoted`
  - `Strategy-only`
  - `Suppressed`

Above the fold should not start with:

- long historical prose
- full rule docs
- raw replay tables
- generic definition text without current-week relevance

## Backtest information that should be shown

The page should show backtest information in two layers.

### MVP backtest layer

Show compact summary cards:

- test window
- universe
- sample size
- average `5D`, `10D`, `15D`
- average excess return vs `SPY`
- `5D`, `10D`, `15D` win rate
- one-line interpretation of evidence quality

Show context summary:

- best regime/context bucket
- weakest regime/context bucket
- whether aggregate performance is trustworthy or only narrowed sub-buckets are

### Later richer backtest layer

Add:

- subgroup tables by regime, sector confirmation, pullback depth, extension band, or breakout context
- time-sliced stability views
- distribution views, not just averages
- degradation or drift warnings after rule changes
- side-by-side comparison across versions
- links to signal logs and replay artifacts for auditability

Important product rule:

- historical evidence must support a present-tense decision
- it should not become a raw research dump on the default view

## How this page supports real weekly decisions

The page should be built around the weekly loop, not timeless documentation.

### Decision roles

For a given week, the strategy page should help the user do four things:

1. Judge whether this strategy deserves live attention this week.
2. Review all current strategy matches before or alongside board promotion.
3. Understand why some names made the overview board and others did not.
4. Open stock deep dives with the right prior context about setup family and trust level.

### Required weekly behaviors

- A user should be able to start from overview, open a strategy page, and quickly understand the source sleeve behind a promoted name.
- A user should be able to review strategy-only candidates without confusing them with main-board actions.
- A user should be able to see suppressor-aware outcomes so `good chart, no action` is understandable.
- A user should be able to tell whether a strategy is acting as:
  - a live action source
  - a waitlist source
  - a research source

### Product implication

The strategy page is the place where strategy output becomes legible before it becomes persuasive.

It should reduce blind trust and reduce accidental dismissal.

## Connection to overview and stock pages

### Connection to overview page

The overview page should link to the strategy page from:

- source-strategy labels on action-board rows
- supporting-strategy lineage chips
- strategy summary modules if present

The strategy page should explain:

- which overview rows came from this strategy
- why those rows were promoted
- what other names stayed strategy-only

### Connection to stock detail page

The strategy page should link into stock detail for every live match.

The stock detail page should link back to:

- the primary source strategy
- any supporting strategies

The boundary should be:

- strategy page answers `how this setup family behaves`
- stock page answers `whether this ticker deserves action`

### Cross-page consistency rules

- action labels must match across pages
- trust language must be consistent across pages
- board lineage must be preserved across pages
- a ticker must appear once on overview even if multiple strategies support it

## MVP scope

MVP should ship when the page can support real weekly use for the current canonical set.

### Must have

- strategy header with trust level and promotion status
- current version and last updated
- this-week summary strip
- current live matches table with board-promoted, strategy-only, and suppressed states
- concise strategy explanation
- compact replay summary
- `where it works / where it fails` summary
- canonical rules section in plain language
- recent changes section
- links to overview lineage and stock pages

### Can be simplified in MVP

- use summary stats instead of full distributions
- use one replay summary per strategy version rather than multi-version comparison
- use text summaries for failure modes rather than full charts
- use expandable raw rules later instead of day-one field-level rule trees

## Later richer versions

### Version 2

- richer subgroup performance breakdowns
- visual stability and drift panels
- strategy output timeline across recent weeks
- explicit narrowed-rule badges on candidate rows
- comparison between current and prior canonical versions

### Version 3

- deeper suppressor diagnostics
- chart overlays showing why a candidate qualifies
- strategy-specific quality diagnostics
- replay-to-live consistency checks
- user-tunable view filters by regime, action, suppression, and board status

## Notes on trust level and promotion status in the product

### Trust level presentation

Trust level should appear:

- in the page header
- in current recommendation rows where helpful
- in any overview links into the strategy page

It should be visually prominent and text-explicit, not implied by color alone.

### Promotion status presentation

Promotion status should appear:

- beside trust level in the header
- in the above-the-fold summary
- on live candidate rows through status labels

It should answer whether the strategy currently contributes to the main action board.

### Messaging guidance

- `Core` should read as live-usable, not infallible.
- `Core but narrowed / trust-calibrated` should read as usable only through the narrowed implementation, not the broad family.
- `Refine before promotion` should read as canonical and worth monitoring, but not trusted as a main-board feeder.
- `Research only` should read as visible and inspectable, but clearly excluded from fresh-cash promotion.

## Acceptance criteria

This page is successful when the user can open any canonical strategy and quickly understand:

- what it is
- how much to trust it
- what it is surfacing this week
- whether those outputs can influence the main action board
- how strong the historical evidence is
- and what changed recently

It should feel like an operating surface for weekly decisions, not a static strategy memo.
