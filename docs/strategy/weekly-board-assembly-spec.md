# Weekly Board Assembly Spec

## Status

- Owner: Strategy + Product
- Status: Proposed
- Last updated: 2026-05-25

## Purpose

Define how independently tested strategy outputs become one unified weekly action board without collapsing back into one opaque ranking model.

This spec exists to preserve three things at once:

- separate testing by strategy,
- one small weekly board for the user,
- and clear source-strategy lineage on every recommendation.

## Scope

This spec applies to the weekly `fresh cash` action board and its `Start here` ranking.

It does not redefine:

- how each strategy is tested,
- holder-action logic for existing positions,
- or options-overlay selection.

Those can reference this spec, but they should not be silently folded into it.

## Core board doctrine

### 1. The board is assembled after strategy evaluation, not instead of it

Each canonical strategy should run and be judged on its own logic first.

Only after that should the system build the weekly board.

### 2. The board is a promotion layer, not a full dump of strategy outputs

The user should not see every strategy candidate on the overview page.

The overview board should promote only the best current weekly actions.

### 3. Board rows must preserve source lineage

Every board row must show:

- the `primary source strategy`,
- any `supporting strategies`,
- and enough setup-family context to explain why the row exists.

### 4. No opaque cross-strategy master score

The system may use structured bands and explicit tie-breakers, but it should not compress all strategy logic into one unexplained number.

### 5. Selectivity is a feature

The board should be allowed to be sparse.

The system must not weaken quality thresholds just to fill slots.

## Board size

### Weekly overview action board

- target size: `3-5` names
- preferred default: `5` only when quality clearly supports it
- allowed minimum: `0`

Interpretation:

- `3-5` is the normal operating range
- `1-2` is acceptable in a weak tape
- `0` is acceptable if nothing deserves action

### Start-here ranking

Within the board, the weekly overview should still highlight the top `1-3` rows as the `Start here` set.

Those are not extra names.

They are the highest-priority subset of the same unified board.

## Input contract for each strategy

Before the board can be assembled, each strategy should emit a standardized `strategy candidate` object for every board-eligible name.

Required fields:

- `ticker`
- `source_strategy`
- `strategy_status`
  - `Core`
  - `Research`
- `sleeve`
  - `ETF`
  - `Single-name`
- `current_action`
  - `Buy now`
  - `Buy on pullback`
  - `Wait for confirmation`
  - `Do not chase`
  - `No action`
- `within_strategy_rank`
- `setup_quality_band`
  - `A`
  - `B`
  - `C`
- `historical_evidence_tier`
  - `Strong`
  - `Moderate`
  - `Exploratory`
- `regime_fit`
- `entry_preference`
- `invalidation_or_reassess`
- `next_catalyst`
- `why_now`
- `why_not_stronger`
- `confidence`
- `suppressed_by_risk_rule`
- `suppression_reason`

Important rule:

The strategy object may include internal component scores, but the board layer should consume them through visible bands and decision fields rather than a hidden composite.

## Board assembly pipeline

### Step 1. Run shared gates first

All names should first pass the shared system gates:

- universe inclusion
- regime gating where required
- risk-rule suppression
- minimum trade-plan completeness

If a name is suppressed by a risk rule, it is not eligible for fresh-cash promotion even if a strategy likes it.

Example:

- `Event freeze before earnings` overrides a would-be breakout candidate.

### Step 2. Build each strategy's winner list

Each strategy should produce its own ranked weekly output.

Promotion limits before cross-strategy blending:

- `ETF Trend / Rotation`: up to top `2`
- `Sector-Confirmed Pullback Continuation`: up to top `2`
- `Breakout Confirmation`: up to top `2`, only through supportive sector-confirmed rules
- `Selective Mean Reversion`: `0` main-board slots by default while it remains `Research`

Research-only strategies may still feed:

- the weekly focus queue,
- a research appendix,
- or later promotion if their status changes to `Core`.

Why this rule exists:

- it keeps the main board trust-calibrated,
- prevents one strategy from monopolizing the board,
- and avoids treating experimental logic as live-ready.

### Step 3. Filter to board-eligible actions

Only candidates with these actions should normally be eligible for the main board:

- `Buy now`
- `Buy on pullback`
- `Wait for confirmation`

`Do not chase` can appear on the main board only if all of the following are true:

- the name is strategically important,
- the system wants the user actively aware of it this week,
- and the board would still remain within the `3-5` name discipline.

Otherwise `Do not chase` belongs in the focus queue, not the action board.

`No action` never belongs on the action board.

### Step 4. Dedupe by ticker, but preserve confluence

The unified weekly board should show one row per ticker.

The same stock may be recommended by multiple strategies, but it should not appear multiple times on the overview board.

When multiple strategies surface the same ticker:

- keep one board row,
- choose one `primary source strategy`,
- store the others as `supporting strategies`,
- and show a short `confluence` note if it helps.

### Step 5. Choose the primary source strategy

Use this precedence order:

1. The strategy whose entry condition is live now
2. The strategy with the stronger `historical_evidence_tier`
3. The better `within_strategy_rank`
4. `Core` over `Research`

Practical interpretation:

- If a stock is currently in a valid pullback buy zone, the pullback strategy should usually be primary even if breakout confirmation is also a plausible later path.
- If two strategies only describe future contingencies and neither is live now, prefer the more conservative current action at the board layer.

### Step 6. Resolve same-ticker conflicts conservatively

There are three conflict types.

#### A. Same direction, same current action

Example:

- two strategies both point to `Wait for confirmation`

Rule:

- keep one row
- show one primary source strategy
- add the other as supporting context

#### B. Same direction, different timing expression

Example:

- `Buy on pullback` from pullback continuation
- `Wait for confirmation` from breakout confirmation

Rule:

- if one setup is live now, use that strategy as primary
- if neither is live now, use the less aggressive current action on the board
- preserve the alternate path in supporting strategy context

#### C. Strategy signal versus suppressor conflict

Example:

- a breakout candidate qualifies technically
- but earnings are too close

Rule:

- the suppressor wins
- the name stays off the fresh-cash board
- it may still appear in focus queue or holdings review with the suppression reason shown

## Cross-strategy ranking without a master score

The board should be ordered with a transparent decision ladder, not one blended number.

### Primary ordering

1. `Current action` priority
2. `Historical evidence tier` of the primary source strategy
3. `Setup quality band`
4. `Risk cleanliness`
5. `Within-strategy rank`
6. `Multi-strategy confluence`
7. `Exposure overlap` tie-break

### Ordering details

#### 1. Current action priority

Default order:

1. `Buy now`
2. `Buy on pullback`
3. `Wait for confirmation`

This ensures the board still answers `what deserves capital first?`

#### 2. Historical evidence tier

Prefer strategies and rows backed by stronger replay evidence.

Current intent:

- `Core` strategies with better evidence should outrank weaker or exploratory logic
- but evidence tier should not rescue a poor current setup

#### 3. Setup quality band

Use the strategy's own setup-quality judgment.

This preserves local strategy nuance rather than forcing false comparability.

#### 4. Risk cleanliness

Prefer names with:

- cleaner invalidation
- lower immediate event risk
- and less ambiguity about what would break the setup

#### 5. Within-strategy rank

If two rows are otherwise similar, the top-ranked name inside its own strategy should win.

#### 6. Multi-strategy confluence

Confluence is a tie-breaker, not a rescue mechanism.

It can improve rank among already-strong candidates.

It should not pull a weak candidate onto the board by itself.

#### 7. Exposure overlap tie-break

If two near-tied rows express highly similar exposure, prefer:

- the cleaner expression,
- the clearer invalidation,
- or the broader ETF expression when single-name edge is not clearly better.

This is not portfolio allocation.

It is a clarity rule to avoid cluttering a tiny board with redundant rows.

## Strategy contribution rules

### Hard rules

- no more than `2` rows from one strategy on the main board
- no more than `1` row per ticker
- no `Research` strategy rows on the main board by default
- no backfilling just to hit `5`

### Soft rules

- prefer at least `2` contributing strategies when quality supports it
- avoid redundant same-theme rows when the difference in board value is trivial
- prefer ETF expressions when immediate exposure is attractive but single-name timing is weak

These soft rules should only break near-ties.

They should not override clearly better setups.

## What the overview page should show for source-strategy context

### Page-level summary

The weekly overview should show a small strategy-source summary above or near the board:

- `ETF Trend / Rotation: 2`
- `Sector-Confirmed Pullback Continuation: 1`
- `Breakout Confirmation: 2`
- `Selective Mean Reversion: 0 (Research)`

This helps the user understand what is driving the week without opening deep dives.

### Row-level required fields

Each board row should show:

- `ticker`
- `current action`
- `primary source strategy`
- `supporting strategies` if any
- `sleeve`
- `entry preference`
- `invalidation or reassess level`
- `next catalyst`
- `why now`
- `why not stronger`
- `confidence`

### Row-level optional but recommended fields

- `within-strategy rank label`
  - example: `Top ETF trend candidate`
- `historical evidence tier`
- `confluence note`
  - example: `Also fits breakout watch if resistance clears`

## Behavior when one strategy has no valid names

The system should not force representation.

If a strategy has no valid names this week:

- contribute `0` rows from that strategy
- show the zero count in the strategy-source summary
- do not lower thresholds to manufacture coverage
- allow other valid strategies to carry the board
- allow the total board count to shrink if needed

Example:

- `Sector-Confirmed Pullback Continuation: 0`
- `ETF Trend / Rotation: 2`
- `Breakout Confirmation: 1`

The resulting board can legitimately have only `3` names.

If every core strategy has `0` valid names, the board should explicitly say:

- `No fresh-cash action this week`

That is a valid output, not a system failure.

## Decision rules

1. `Risk rules override promotion.`
2. `One ticker gets one board row.`
3. `Every row must show a primary source strategy.`
4. `Supporting strategies add context, not duplicate rows.`
5. `Research-only strategies do not occupy main-board slots by default.`
6. `Board size is a cap, not a quota.`
7. `Cross-strategy ordering uses a visible decision ladder, not a hidden master score.`
8. `Confluence can break ties, but it cannot rescue weak setups.`
9. `When two near-tied rows express the same exposure, prefer the cleaner expression.`
10. `If no strategy earns promotion, the board should say so directly.`

## Example 1. Normal mixed week

Illustrative only.

### Strategy-source summary

- `ETF Trend / Rotation: 2`
- `Sector-Confirmed Pullback Continuation: 2`
- `Breakout Confirmation: 1`
- `Selective Mean Reversion: 0 (Research)`

### Unified weekly board

| Rank | Ticker | Action | Primary source strategy | Supporting strategies | Entry preference | Why now | Why not stronger |
|---|---|---|---|---|---|---|---|
| 1 | XLK | Buy now | ETF Trend / Rotation |  | Above key moving averages with supportive sector trend | Cleaner immediate exposure than most single names | Broad trend can still reverse quickly |
| 2 | QQQ | Buy now | ETF Trend / Rotation |  | Buy against recent support | Regime and benchmark trend are supportive | More extended than ideal versus recent base |
| 3 | MSFT | Buy on pullback | Sector-Confirmed Pullback Continuation |  | Buy only in pullback zone near support | Strong relative strength with controlled reset | Pullback has not fully completed yet |
| 4 | CRM | Buy on pullback | Sector-Confirmed Pullback Continuation | Breakout Confirmation | Preferred on controlled weakness; alternate trigger on breakout | Leadership remains intact and multiple strategy lenses agree | Entry is not live unless price revisits support or clears resistance |
| 5 | NVDA | Wait for confirmation | Breakout Confirmation |  | Trigger only on resistance break | Strong leadership candidate if price proves itself | Current entry is too extended to chase |

## Example 2. Same stock recommended by multiple strategies

Illustrative only.

### Raw strategy outputs

- `AVGO` from `Sector-Confirmed Pullback Continuation`: `Buy on pullback`
- `AVGO` from `Breakout Confirmation`: `Wait for confirmation`

### Board treatment

Show one row only:

| Ticker | Action | Primary source strategy | Supporting strategies | Board note |
|---|---|---|---|---|
| AVGO | Buy on pullback | Sector-Confirmed Pullback Continuation | Breakout Confirmation | Pullback entry is live now; breakout path remains valid if price re-expands later |

Why:

- the ticker appears once
- the current live setup becomes primary
- alternate strategy context is preserved without duplicating the row

## Example 3. Sparse week with one empty strategy

Illustrative only.

### Strategy-source summary

- `ETF Trend / Rotation: 1`
- `Sector-Confirmed Pullback Continuation: 0`
- `Breakout Confirmation: 2`
- `Selective Mean Reversion: 0 (Research)`

### Unified weekly board

| Rank | Ticker | Action | Primary source strategy | Why now |
|---|---|---|---|---|
| 1 | QQQ | Buy now | ETF Trend / Rotation | Benchmark trend remains the cleanest immediate expression |
| 2 | AMZN | Wait for confirmation | Breakout Confirmation | Leadership is present but the trigger is not live yet |
| 3 | META | Wait for confirmation | Breakout Confirmation | Setup is promising, but proof through price is still required |

Important interpretation:

- the board stays at `3` names
- pullback gets `0`
- the system does not invent weaker pullback names just to maintain symmetry

## Recommended implementation consequence

The persistent weekly decision object should support:

- one `primary_source_strategy`
- zero-to-many `supporting_strategies`
- one board-level `current_action`
- one board-level `rank_reason`
- and strategy-summary counts for the weekly run

That gives product and engineering enough structure to render one unified board while preserving strategy separation underneath.
