# Phase 1 PRD: Data Spine And Decision Contracts

## Status

- Owner: Product + Engineering
- Status: Proposed
- Last updated: 2026-05-24

## Phase objective

Create the persistent product backbone required for all later weekly, daily, stock-detail, and watchlist surfaces.

This phase exists to eliminate shell-only product work.

## Why this phase comes first

The current weekly and stock-detail surfaces are ahead of their data model. If feature work continues at the UI layer without fixing that gap first, later work will need to be rewritten.

This phase makes later product work cumulative instead of disposable.

## User problem

The user can currently see product surfaces, but cannot yet trust them as a durable operating system because:

- weekly content is still scaffold-driven,
- stock detail is not yet a stable recommendation object,
- watchlist state is not yet the canonical universe model,
- and historical transitions are not yet first-class.

## Goals

- Replace sample weekly payloads with published run data.
- Define a persistent weekly decision object for each stock.
- Define a canonical universe and watchlist model.
- Define stock-detail payload contracts backed by real evidence and recommendation data.
- Preserve enough run history to support later movement tracking.
- Ensure the data model can absorb more refined strategy outputs later without forcing a front-end redesign.

## Non-goals

- Final visual redesign of product surfaces
- Full watchlist CRUD UX
- Full `15-20` name focus queue UI
- Broad deep-dive generation across the full universe
- Options-overlay expansion

## Required product objects

### 1. Weekly run

Must represent:

- run id
- as-of date
- generation timestamp
- market posture summary
- top action board snapshot
- focus queue membership snapshot
- holdings-action snapshot

### 2. Stock decision object

Must represent, at minimum:

- ticker
- company name
- as-of date
- requested horizon or applicable horizons
- current action for new capital
- current action for existing holder
- short-term tradeability view
- medium-term setup view
- long-term conviction view
- event-risk state
- `why now`
- `why not stronger`
- entry preference
- invalidation or reassessment trigger
- next catalyst
- confidence
- source evidence references

It should also be extensible enough to support later additions such as:

- additional component scores,
- richer setup-family detail,
- more explicit catalyst classifications,
- multiple evidence modules,
- and more granular risk or regime qualifiers,

without changing the meaning of the core object.

### 3. Canonical universe membership object

Must represent:

- ticker
- active or inactive state
- role tags such as `holding`, `core watch`, `tactical`, or `ETF`
- sector and theme metadata
- user notes
- effective date
- change history

### 4. Stock detail payload

Must be composed from persistent objects rather than ad hoc page-only assembly.

It must be possible to render stock detail from:

- latest stock decision object,
- current watchlist state,
- recent run history,
- evidence references,
- and recommendation history.

## Functional requirements

### Weekly data wiring

- The weekly page must read from stored weekly run outputs rather than sample payloads.
- Weekly records must be queryable by as-of date.
- The app must be able to identify the current published run versus older runs.

### Decision contracts

- Each stock surfaced on weekly or daily pages must map to a persistent stock decision object.
- Decision objects must preserve separate horizon judgments rather than collapsing to one score.
- Decision objects must support both `new position` and `already held` interpretations.

### Universe contracts

- The system must support a canonical set of names independent of any one weekly run.
- Universe membership changes must be historically inspectable.
- Tags must be structured rather than free-form-only.

### UI-ready mapping contracts

- The backend must expose stable UI-ready structures for:
  - weekly top actions,
  - holdings actions,
  - daily change items,
  - deep-dive current call,
  - and later focus-queue buckets.

- These structures should support additive detail sections so later strategy improvements can deepen the experience without changing page identity.

## Product decisions in this phase

- The stock decision object is the core reusable primitive for weekly, daily, and deep-dive views.
- The canonical universe is not equal to the weekly focus queue.
- The weekly focus queue is not equal to the action board.
- History begins here, even if initial history views ship later.
- Strategy sophistication should scale through richer fields and evidence modules, not through a new surface model.

## Acceptance criteria

- The weekly page can render from a real published run without sample data.
- At least one stock detail page can render from persistent recommendation data and evidence references.
- The system can represent active and inactive universe members with tags and notes.
- Engineering can add new weekly surface sections in later phases without redesigning the core data model.

## Release test

This phase is complete when the team can say:

- `We now have durable product objects, and future feature work will layer on them rather than replace them.`

## Risks to manage

- Over-modeling before any surface consumes the fields
- Under-modeling and forcing another rewrite in Phase 2 or 3
- Quietly smuggling finance doctrine into UI contracts

## Open implementation guidance

- Start with the smallest decision object that can satisfy weekly, daily, and deep-dive usage together.
- Bias toward explicit fields for action, risk, and trigger logic.
- Keep raw evidence lineage accessible even when the UI shows compressed summaries.
