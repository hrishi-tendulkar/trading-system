# Phase 2 PRD: Core Decision Surfaces

## Status

- Owner: Product
- Status: Proposed
- Last updated: 2026-05-24

## Phase objective

Turn the existing weekly, daily, and stock-detail surfaces into a credible operating loop for the user's actual cadence.

## Why this phase matters

The product wins when the user can sit down once per week and quickly understand:

- what deserves capital now,
- what deserves patience,
- what existing positions need action,
- and what changed materially between weekly sessions.

This phase gives the current surfaces strong jobs before adding more breadth.

## Goals

- Make the weekly page a clear decision session.
- Make the daily page exception-based.
- Make stock detail a true deep-dive decision memo.
- Preserve links between weekly summary and stock-level evidence.
- Preserve a front-end shape that can absorb more detailed strategy analysis later without changing the user's mental model.

## Non-goals

- Large new page count
- Full watchlist management workflow
- Universe-wide deep-dive automation
- Broad ranking boards without action buckets

## Product decisions

### 1. Weekly review becomes `This Week's Plan`

Primary question:

- `If I have one decision session this week, what should I do first?`

The page must answer in order:

1. market posture,
2. top actions this week,
3. fresh cash opportunities,
4. holder decisions,
5. names worth deeper work.

### 2. Daily review becomes `What Changed Since Yesterday`

Primary question:

- `Did anything happen that should alter my behavior before the next weekly review?`

The page should feel safe to skip on quiet days.

### 3. Stock detail becomes `Deep Dive`

Primary question:

- `For this stock, should I act now, wait, or avoid?`

The page must present the current decision before the supporting evidence.

It must also be able to expand downward into more detail over time:

- more evidence sections,
- more factor breakdowns,
- more explicit regime framing,
- and richer history,

without changing its core job.

## Weekly requirements

### Section 1. Week setup

Must show:

- as-of date
- market posture
- number of top actions
- number of holdings needing action
- one-sentence selectivity guidance

### Section 2. Start here

Must show:

- ranked top `1-3` actions
- one-line reason for rank
- preferred expression
- link to deep dive

### Section 3. Fresh cash board

Must include structured buckets:

- `Buy now`
- `Buy on pullback`
- `Wait for confirmation`
- `Do not chase`

Each row or card must show:

- ticker
- current action
- entry preference
- invalidation or reassessment logic
- next catalyst
- `why now`
- `why not stronger`

### Section 4. Existing positions

Must include holder-action buckets:

- `Hold`
- `Hold but do not add`
- `Trim / de-risk`
- `Exit / thesis broken`

Each row must show:

- what changed,
- whether the concern is setup, thesis, or event risk,
- and what would force reassessment.

### Section 5. Deep-dive queue

Must show:

- at most `3` names in `P0`
- why each made the queue
- direct links into the deep-dive page

## Daily requirements

### Section 1. Daily verdict

Must open with a direct summary such as:

- `No material change`
- `One holding needs review`
- `Two setups broke`
- `New earnings reaction entered the queue`

### Section 2. Action-required changes

Allowed categories:

- `Broken setup`
- `Earnings reaction changed the setup`
- `Holding risk increased`
- `Watchlist candidate became actionable`

Excluded categories:

- generic market commentary
- minor price movement without changed action
- repeated notes with no new decision implication

### Section 3. Carry-forward queue

Must show:

- names promoted into next weekly review,
- names demoted out of it,
- and names waiting for a specific trigger.

## Deep-dive requirements

### Section 1. Current call

Must show:

- new-position recommendation
- holder recommendation
- confidence
- why this stock matters now

### Section 2. Horizon separation

Must show separate views for:

- short-term tradeability
- medium-term setup
- long-term conviction

### Section 3. Evidence and risk

Must show:

- observed evidence
- derived inference summary
- event risk
- bear or break case
- what would change the recommendation

This section should be modular so later strategy improvements can add:

- more detailed evidence panels,
- strategy-specific diagnostics,
- and richer supporting tables or timelines,

without changing the page's primary action-first framing.

### Section 4. History and traceability

At minimum, the page must leave room for:

- prior recommendation snapshots,
- prior entry logic,
- and movement from earlier weekly states.

## Acceptance criteria

- The weekly page tells the user where to start in under `30` seconds.
- The daily page can explicitly say `nothing important changed`.
- A stock deep dive clearly separates `act now`, `wait`, and `avoid` logic.
- The same stock does not need conflicting UI language across weekly and deep-dive views.

## Release test

This phase is complete when the product feels like a useful weekly operating loop even before watchlist breadth expansion lands.

## Risks to manage

- letting weekly become a dashboard rather than a decision session
- letting daily become a feed
- letting deep dive become a research article instead of a decision memo
- coupling the UI too tightly to today's strategy fields and forcing redesign when the analysis gets better
