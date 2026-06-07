# Public Equity Investing Plugin Partnership

## Status

- Owner: Product Strategist + Public Equity Strategist
- Status: Canonical operating note
- Date: 2026-06-07
- Scope: Exactly where Trading System should use the Public Equity Investing plugin

## Core Judgment

Use Public Equity Investing where Trading System is currently weakest: not in finding technically attractive stocks, but in deciding whether a technically attractive stock should be trusted, delayed, suppressed, or reviewed again after new company/event evidence.

The plugin should not create a parallel research process. It should run narrow decision packets against names the system has already surfaced.

## Why This Matters Now

Trading System already has a working daily-data strategy spine:

- broad universe scan,
- regime and sector context,
- Strategy 1 `breakout-confirmation.v2`,
- sparse action board,
- weekly publish/archive discipline.

The known weakness is not candidate discovery. The known weakness is that daily OHLCV cannot reliably answer:

- Is a valid breakout about to run into an avoidable earnings event?
- Did the latest quarter actually improve the thesis, or did price just react well?
- Did guidance, margins, cash conversion, or commentary quietly weaken a setup?
- Is a holding deteriorating fundamentally while the chart has not broken yet?
- Which catalyst should change trigger expiry, sizing, or review urgency?

Those are the first places to use the plugin.

## Immediate Use Cases

### 1. Board Buy-Now Veto Check

Run this on every `Buy now` name before the weekly report is treated as decision-ready.

Trigger:

- candidate is on the weekly action board as `Buy now`.

Plugin workflow:

- `company-tearsheet` for baseline gaps,
- `earnings-preview` if earnings are within the next `14` calendar days,
- `earnings-deep-dive` if results occurred in the last `10` trading days,
- `catalyst-calendar` if a known catalyst is mentioned or timing is unclear.

Required output fields:

- `event_veto`: `none`, `soft`, or `hard`
- `earnings_window`: exact date or inferred window
- `post_print_quality`: `not_applicable`, `clean_supportive`, `mixed`, `low_quality`
- `thesis_damage`: `none`, `watch`, `material`
- `decision_effect`: `keep_buy_now`, `downgrade_to_wait`, `suppress_from_board`, `needs_manual_review`
- `one_sentence_reason`

Allowed decision impact:

- keep the `Buy now`,
- downgrade to `Wait for confirmation` or `Buy on pullback`,
- suppress from board because event risk or thesis damage overrides the setup.

What this improves:

- fewer technically valid but event-fragile fresh-cash calls.

### 2. Wait-List Trigger Hazard Map

Run this on the best `Wait for confirmation` and `Buy on pullback` names, especially near earnings.

Trigger:

- candidate is not buyable today but has a plausible near-term trigger.

Plugin workflow:

- `catalyst-calendar`,
- `earnings-preview` for pre-print names,
- `company-tearsheet` only when the company baseline is thin.

Required output fields:

- `trigger_expiry`: date or `until_next_weekly_run`
- `do_not_trigger_after`: date/event
- `event_hazard`: `none`, `low`, `medium`, `high`
- `required_confirmation`: price, event, guidance, or post-print hold
- `what_must_remain_true`

Allowed decision impact:

- shorten the trigger window,
- move from `Wait for confirmation` to `Avoid due to event or risk`,
- leave the candidate in the focus board but keep it off the action board.

What this improves:

- prevents stale triggers from surviving into event risk.

### 3. Post-Earnings Continuation Trial

Use this to develop the future post-earnings setup without prematurely promoting it.

Trigger:

- earnings occurred in the last `1-10` trading days,
- stock held or extended the post-print move,
- relative strength is positive versus `SPY` and sector.

Plugin workflow:

- `earnings-deep-dive`.

Required output fields:

- `headline_result`: beat, miss, mixed, or not comparable
- `guide_delta`: raised, maintained, lowered, withheld, or unclear
- `quality_of_print`: clean, mixed, low-quality, or distorted
- `market_reaction_confirmation`: held, faded, reversed, or still testing
- `revision_likelihood`: positive, neutral, negative, or unknown
- `next_falsifier`
- `setup_status`: `research_candidate`, `focus_board_only`, `eligible_for_manual_review`

Allowed decision impact:

- feed the weekly focus board,
- support a `Wait for confirmation`,
- support a manual review note,
- not feed automatic `Buy now` until replay evidence improves.

What this improves:

- creates a structured bridge from qualitative post-print analysis to a future testable strategy family.

### 4. Deteriorating Holding Review

Run this when the system flags a holding for `Hold`, `Trim`, or `Exit` ambiguity.

Trigger:

- held name has weakening price/relative strength,
- new earnings/news/filing evidence,
- or strategy output conflicts with existing ownership thesis.

Plugin workflow:

- `thesis-tracker`,
- `earnings-deep-dive` after a print,
- `scenario-sensitivity-generator` only if the decision depends on a specific assumption break.

Required output fields:

- `company_thesis_status`: strengthening, intact, watch, impaired, broken
- `security_thesis_readiness`: ready, conditional, re-underwrite, not decision-grade
- `action_threshold`: hold, add, trim, exit, or wait
- `broken_pillar`
- `next_proof_point`
- `review_deadline`

Allowed decision impact:

- move from `Hold` to `Trim / exit`,
- keep `Hold` but create a dated proof point,
- prevent adding to a technically attractive but fundamentally impaired name.

What this improves:

- separates stock action from company affection.

### 5. Disputed Candidate Tie-Break

Run this only when the system has a real conflict, not for every interesting stock.

Trigger:

- two strategies disagree on timing,
- a candidate has strong setup quality but weak business context,
- or a candidate is strategically important but fails one nonfatal filter.

Plugin workflow:

- `company-tearsheet` for factual baseline,
- `long-short-pitch` only if a true variant-view debate is needed.

Required output fields:

- `supports_strategy_signal`: yes, no, or mixed
- `contradicts_strategy_signal`: yes, no, or mixed
- `decision_blocker`
- `missing_evidence`
- `tie_break`: more aggressive, unchanged, more conservative, suppress

Allowed decision impact:

- choose the more conservative action,
- preserve the name as focus-board only,
- suppress if the contradiction is material.

What this improves:

- keeps confluence honest without inventing a master score.

## First Two Experiments

### Experiment A: Weekly Buy-Now Veto Packet

For the next published weekly run, run a plugin veto packet on every `Buy now` row.

Success standard:

- every `Buy now` has a stored `event_veto`, `thesis_damage`, and `decision_effect`,
- any downgrade has a one-sentence evidence reason,
- no candidate is upgraded by plugin prose alone.

This is the fastest immediate use because the current board is sparse. It adds little workload and protects the most consequential recommendations.

### Experiment B: Post-Print Continuation Watchlist

For the next `4` weekly runs, identify names with earnings in the last `10` trading days and positive post-print relative strength. Run `earnings-deep-dive` only on the top few by setup quality.

Success standard:

- each name is classified into `clean_supportive`, `mixed`, `low_quality`, or `distorted`,
- the classification is stored with later `5`, `10`, and `20` trading-day outcomes,
- after several runs, finance can decide whether post-print continuation deserves a real strategy spec or remains a focus-board research lens.

This is the best path from qualitative plugin work to measurable strategy improvement.

## Output Object

Plugin work should be converted into this compact object before it touches product surfaces:

```json
{
  "ticker": "",
  "as_of": "",
  "plugin_workflow": "",
  "trigger_case": "",
  "facts": [],
  "inferences": [],
  "unknowns": [],
  "event_veto": "none|soft|hard|not_applicable",
  "thesis_damage": "none|watch|material|not_applicable",
  "decision_effect": "keep|downgrade|suppress|manual_review|focus_only",
  "changed_fields": [],
  "next_proof_point": "",
  "review_deadline": ""
}
```

If a plugin result cannot be reduced to fields like these, it is not yet useful to the system. It can remain a research note, but it should not change weekly recommendations.

## What Not To Use It For Yet

Do not use the plugin to:

- rank the full S&P 100 or S&P 500,
- write deep dives for every weekly focus name,
- create a polished report for every candidate,
- upgrade a stock to `Buy now`,
- replace Strategy 1 v2 or promoted-sleeve rules,
- add valuation work to tactical trades with no ownership question,
- generate options overlays before the stock thesis is valid.

## Readiness

The plugin is available as a workflow library. Its local Public Equity Investing context is not initialized, so source routes and saved preferences are not yet configured.

Immediate usage should therefore be manual or semi-manual, using local artifacts, existing weekly outputs, and user-provided/public source material. Do not depend on recurring source-backed automation until source setup is explicit and weekly publish/archive semantics are stable.

## Canonical Recommendation

Start with two concrete integrations:

1. `Buy now` veto checks for action-board names.
2. Post-earnings continuation research packets for a small set of technically strong post-print names.

These are the cleanest because they target known Trading System blind spots, produce testable fields, and can be reviewed against later outcomes. If they do not change decisions or improve postmortems, the plugin should stay a manual research tool rather than becoming product infrastructure.
