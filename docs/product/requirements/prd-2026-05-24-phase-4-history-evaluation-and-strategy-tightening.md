# Phase 4 PRD: History, Evaluation, And Strategy Tightening

## Status

- Owner: Product + Finance + Engineering
- Status: Proposed
- Last updated: 2026-05-24

## Phase objective

Turn the product into a reviewable system that can learn from its own prior recommendations and support better strategy refinement over time.

## Why this phase matters

The product doctrine across this repo is explicit:

- preserve history,
- make recommendations explainable,
- and improve through review rather than narrative confidence.

This phase makes that discipline real.

## Goals

- Preserve inspectable recommendation history.
- Preserve watchlist and focus-queue movement history.
- Support outcome review of prior weekly calls.
- Create product hooks for improving signal discrimination over time.

## Non-goals

- full backtesting platform before core review views exist
- large analytics dashboards with weak product relevance
- portfolio optimization workflows

## Product decisions

### 1. History is a first-class product surface

The user should be able to answer:

- what the system believed,
- why it believed it,
- what changed,
- and whether that judgment later looked right.

### 2. Evaluation should improve selectivity

The point of broader coverage is not more output.

The point is to learn:

- which queue states are useful,
- which top-action patterns hold up,
- and where the product is overconfident or too noisy.

### 3. Finance refinement runs alongside product evidence

Product history should help the finance layer tighten:

- signal discrimination,
- setup gating,
- event-risk handling,
- and bucket assignment quality.

## Required history views

### Recommendation history

Must support:

- prior weekly recommendations by ticker
- prior bucket states
- prior `why now` and `why not stronger` summaries
- prior triggers and invalidations

### Watchlist history

Must support:

- add and remove history
- tag changes
- active and inactive changes
- holding-state changes

### Focus-queue movement history

Must support:

- entered queue
- promoted to action board
- demoted to watch only
- frozen for event risk
- removed from queue

## Evaluation requirements

### Outcome review

Must allow later inspection of:

- what happened after a recommendation,
- whether the trigger or invalidation logic held,
- whether the call was directionally useful,
- and whether the name belonged in the action board, focus queue, or neither.

### Product-quality review

Must support review questions such as:

- Are too many names being marked actionable?
- Are `Wait for confirmation` names graduating too late?
- Are event-risk freezes preventing obvious mistakes?
- Are holder decisions clearer week over week?

## Acceptance criteria

- The user can inspect prior weekly views for a stock without hunting through raw records.
- Queue movement and recommendation changes are understandable over time.
- The team can use stored history to refine product and finance logic with evidence rather than memory.

## Release test

This phase is complete when the system can challenge and improve its own weekly judgments.

## Risks to manage

- collecting history without a usable review surface
- evaluating outcomes with hindsight but no saved context
- drifting into analytics sprawl disconnected from the weekly decision job
