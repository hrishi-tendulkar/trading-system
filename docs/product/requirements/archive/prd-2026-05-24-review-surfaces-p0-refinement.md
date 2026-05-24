# Review Surfaces P0 Refinement

## Status

- Owner: Product
- Status: Proposed
- Last updated: 2026-05-24

## Why this exists

The current web app exposes `Weekly review`, `Daily digest`, and `Stock detail`, but the labels are still more scaffold than workflow. A user can see that pages exist without immediately understanding:

- what decision each page is for,
- what action should come out of the page,
- when to use that page,
- and how the pages relate to each other.

This refinement defines the `P0` product shape that makes those surfaces useful before broader feature expansion.

## Core product decision

Each primary surface must answer one job only:

- `Weekly review` = what should I do with capital this week?
- `Daily review` = what changed enough to force attention before the next weekly review?
- `Deep dive` = should I trust this specific stock enough to act, wait, or avoid?

If a page cannot answer its job clearly, it is not ready for `P0`.

## Problems with the current shape

### 1. `Weekly review` sounds descriptive, not actionable

The name suggests a recap, not a decision cockpit. The user still has to infer:

- whether this is for new buys, existing positions, or both,
- whether this is a once-a-week workflow or a rolling dashboard,
- and what they are supposed to leave the page with.

### 2. `Daily digest` risks becoming a low-value news stream

Without tighter rules, the page can drift into:

- summarizing activity rather than decision changes,
- repeating information that will not alter behavior,
- and training the user to check the app without a real reason.

### 3. `Deep dives` are not yet defined as a product object

The product currently has `stock detail`, but not a clear deep-dive workflow. The unresolved questions are important:

- which stocks deserve a deep dive,
- whether deep dives run automatically every week,
- whether the user can request one manually,
- and whether a deep dive is a ranked decision memo or a generic research page.

## P0 design principles

- Weekly first: the product center of gravity remains the once-a-week decision session.
- Exception-based daily use: daily usage should happen only when something materially changed.
- Stock-first clarity: every stock page must separate setup quality, conviction, and event risk.
- Fewer screens, stronger jobs: `P0` should tighten the purpose of existing surfaces before adding more categories.
- No research theater: long text is not value unless it changes a decision.

## P0 surface model

### 1. Weekly review becomes `This Week's Plan`

The page can still be routed from `/weekly`, but the on-screen framing should be more explicit than `Weekly review`.

Primary user question:

- `If I have time for one session this week, what should I do with fresh cash, open positions, and watchlist names?`

Primary outputs:

- top `1` to `3` actions for fresh capital,
- names to watch but not chase,
- names to hold, trim, or pause,
- and the small set of stocks worth deeper inspection.

The page should end with a clear weekly action list, not just a board of cards.

### 2. Daily review becomes `What Changed Since Yesterday`

This page should not be a mini weekly review.

Primary user question:

- `Did anything happen that invalidates the weekly plan or creates a new must-watch situation?`

Primary outputs:

- newly broken setups,
- major post-earnings reactions,
- names upgraded into the weekly queue,
- names downgraded out of it,
- and holdings that now require reassessment.

If nothing important changed, the page should say that clearly and confidently.

### 3. Stock detail becomes `Deep Dive`

For `P0`, deep dives should be the stock detail page with a tighter purpose and stronger structure.

Primary user question:

- `For this stock, what is the actual case for acting now, waiting, or avoiding it?`

Primary outputs:

- current action,
- setup quality,
- long-term quality,
- event risk,
- explicit bull case and break case,
- and what would change the recommendation.

## Recommended P0 weekly screen

### Section 1. Week setup

Purpose:

- orient the user in under `30` seconds.

Must show:

- as-of date,
- market posture,
- number of actionable names this week,
- number of existing holdings needing action,
- and one sentence describing how selective the user should be.

### Section 2. Start here

Purpose:

- answer `what should I look at first?`

Must show:

- `Top actions this week` as a ranked list of `1` to `3`,
- one-line reason each is in the top tier,
- preferred expression: stock, wait, hold, or later overlay,
- and a direct link into the relevant deep dive.

This is more useful than a generic hero because it converts posture into an actual starting order.

### Section 3. Fresh cash board

Purpose:

- help decide where new money should go.

Groups:

- `Buy now`
- `Wait for pullback / confirmation`
- `Do not chase`

Each card must show:

- ticker and company,
- current action,
- setup family or reason label,
- entry zone,
- invalidation or stop logic,
- next catalyst,
- `why now`,
- `why not stronger`,
- link to deep dive.

### Section 4. Existing positions

Purpose:

- separate holder decisions from new-entry decisions.

Groups:

- `Hold`
- `Hold but do not add`
- `Trim / de-risk`
- `Exit / thesis broken`

Each row must show:

- what changed since last week,
- whether the issue is timing, thesis, or event risk,
- and the specific trigger for reassessment.

This is critical because the current weekly board can blur new buys and held names.

### Section 5. Stocks worth deeper work

Purpose:

- tell the user which names deserve more attention.

Rules for `P0`:

- show at most `3` names,
- default to names in `Buy now`, `Wait for pullback`, or `Hold but event-sensitive`,
- and explain why they made the deep-dive queue.

This section answers the user's question directly: yes, deep dives should usually focus on the names most likely to matter this week.

## Recommended P0 daily screen

The daily page should be shorter than the weekly page and should feel comfortable to skip.

### Section 1. Daily verdict

One of:

- `No material change`
- `One holding needs review`
- `Two setups broke`
- `New post-earnings candidate entered the queue`

This should be the first line on the page.

### Section 2. Action-required changes

Only include items that change behavior before the next weekly session.

Allowed categories in `P0`:

- `Broken setup`
- `Earnings reaction changed the setup`
- `Holding risk increased`
- `Watchlist candidate became actionable`

Exclude for `P0`:

- generic market summaries,
- small price moves,
- repeated commentary with no changed action.

### Section 3. Carry-forward queue

Purpose:

- show which names should be reconsidered at the next weekly review.

This can be a short list of:

- promoted names,
- demoted names,
- and names awaiting a specific trigger.

## Recommended P0 deep-dive screen

The deep dive should be decision-first, not article-first.

### Section 1. Current call

Must show:

- action now,
- confidence,
- time horizon,
- event risk,
- and one-sentence thesis.

### Section 2. Decision summary

Must show:

- `Why this week`
- `Why not stronger`
- `What would make this a buy`
- `What would break the case`

This is the most important block on the page.

### Section 3. Evidence by horizon

Split into:

- `Short-term setup`
- `Long-term quality`
- `Known risks / unknowns`

This protects the system from mixing a good company with a bad entry.

### Section 4. Price and risk geometry

Must show:

- entry zone,
- invalidation,
- target zone,
- and what price condition upgrades or downgrades the name.

### Section 5. Event and catalyst path

Must show:

- next earnings date if known,
- other material event flags,
- and whether the event is a reason to act, wait, or avoid fresh entry.

## Deep-dive generation rules for P0

### Which stocks get deep dives?

Default candidates:

- all `Buy now` names,
- the highest-priority `Wait for pullback` names,
- existing holdings with event risk or thesis tension.

### Can the user request deep dives on any stock?

Yes, but with two modes:

- `Priority deep dives`: stocks already in the weekly queue
- `Manual deep dives`: on-demand lookup for any watchlist or holding name

The page should support manual request later, but the weekly review should only spotlight the names most likely to matter now.

### Do deep dives run every week?

Not for every stock.

`P0` rule:

- refresh deep dives automatically only for the week's top actionable names and risk-sensitive holdings,
- keep the rest available on demand from the stock list or watchlist.

This avoids wasting effort on low-value summaries while still supporting research depth where needed.

## P0 scope cuts

To keep the product useful and credible, `P0` should avoid:

- auto-generating deep dives for the whole universe,
- turning daily review into a news feed,
- putting options overlays in prime weekly screen real estate before the stock engine is trusted,
- or showing many cards without a ranked starting point.

## P0 navigation changes

Recommended sidebar labels:

- `This Week`
- `Daily Changes`
- `Watchlist`
- `Deep Dives`
- `Admin`

This wording is more job-oriented than the current labels.

## Acceptance criteria

The product has reached the right `P0` shape when:

- a first-time user can tell in under `1` minute what each main page is for,
- the weekly page tells the user where to start instead of merely presenting information,
- the daily page is comfortably skippable unless something changed,
- deep dives are reserved for names that matter now or are explicitly requested,
- and holder decisions are visibly separated from fresh-buy decisions.

## Recommended implementation sequence

1. Refactor the weekly page around `start here`, `fresh cash`, `existing positions`, and `deep-dive queue`.
2. Tighten the daily page into an exception-driven change log with explicit `no material change` states.
3. Reframe `stock detail` as the `deep dive` object with decision-first sections.
4. Add manual deep-dive request from watchlist after the core read surfaces are credible.
