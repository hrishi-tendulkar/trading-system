# Trading System Information Hierarchy

## Purpose

This document defines what information belongs on each page and reusable card/template.

It is not a visual design spec. The design agency should decide how to present this information clearly.

This is the canonical source of truth for Trading System page and card information hierarchy.

The goal is to separate:

- what we show,
- from how it looks.

When the product changes, this document should be updated first so page templates stay consistent.

## Core Product Object

The main product object is a weekly run.

A weekly run contains:

- one weekly summary,
- final recommendations,
- all analyzed candidates,
- stock detail records,
- strategy detail records,
- report metadata,
- archive copy of the run.

## Page Map

```text
Weekly Summary
  -> Final recommendation stock cards
  -> Full Candidate Board
  -> Stock Recommendation Card / Stock Detail
  -> Strategy Detail
  -> Archive
```

The weekly summary is the home base.

## 1. Weekly Summary Page

### Page Job

Tell the user what to do this week.

### Page Hierarchy

1. Page title
2. Weekly action summary card
3. Final recommendation stock cards
4. Full candidate board preview
5. Report details
6. Links to archive / prior weeks

### Page Title Template

Show:

- `Weekly Summary`
- recommendation week
- short status label

Example:

```text
Weekly Summary
Week of Jun 8, 2026
Current published plan
```

### Weekly Action Summary Card

This is the top decision card.

Show:

- one-line recommendation summary,
- fresh cash guidance,
- number of buys,
- number of wait-list names,
- number of sell / reduce checks,
- market risk mode,
- one-line instruction about what not to do.

Example:

```text
This week: buy QQQ and AVGO if entry levels hold; wait on NVDA; review CRM for possible reduction.
Deploy up to $35k. Take 2 new trades max. Do not chase gap-up opens.
```

### Final Recommendation Section

Show the stocks that made the final weekly recommendation list.

Each item uses the Stock Recommendation Card template.

### Full Candidate Board Preview

Show a compact count summary and link to the full board.

Show:

- included count,
- wait-listed count,
- excluded count,
- sell-check count,
- link: `See why picks passed or failed`.

Do not show a weak partial table that feels arbitrary.

### Report Details Template

Report details are supporting metadata, not the hero.

Show compactly:

- published timestamp,
- data-through date,
- universe,
- run ID,
- engine/version if needed.

Example:

```text
Published: Jun 7, 2026 6:00 PM ET
Data through: Jun 5 close
Universe: S&P 100 + ETFs
Run ID: weekly_2026_06_08
```

## 2. Stock Recommendation Card Template

### Card Job

Help the user decide whether to act on this stock this week.

### Card Hierarchy

1. Ticker and company
2. Action
3. Plain-English recommendation
4. Strategy used
5. Validity and expected hold
6. Entry / upside exit / downside exit
7. Why this week
8. Main risk
9. Links to stock detail and strategy detail

### Required Fields

Show:

- ticker,
- company,
- action,
- strategy name,
- strategy role,
- valid until,
- expected hold,
- entry level or zone,
- upside exit / target,
- downside exit / sell level,
- one-line why,
- main risk,
- link to stock detail,
- link to strategy detail.

### Example

```text
QQQ - Nasdaq 100 ETF
Action: Buy if price holds entry zone
Recommendation: Buy QQQ only if it holds above $462 after the open. If it gaps above $470, wait.
Strategy: Index Trend Follow-Through
Valid until: Friday close, Jun 12, or earlier if QQQ loses $454
Expected hold: 1-3 weeks after entry
Entry: $462-$468
Upside exit: Trim near $485
Downside exit: Sell below $454
Why this week: broad tech leadership is still the cleanest market exposure.
Main risk: if QQQ loses support, the trade reason is gone.
```

## 3. Full Candidate Board Page

### Page Job

Show what was analyzed this week and why each idea passed, waited, or failed.

### Page Hierarchy

1. Page title
2. Board summary counts
3. Candidate table/list
4. Filters or grouping, if useful
5. Links to stock detail and strategy detail

### Candidate Row Template

Show:

- ticker,
- company,
- strategy,
- strategy result,
- final result,
- action,
- simple reason,
- valid until / not valid,
- expected hold if relevant,
- link to stock detail,
- link to strategy detail.

Clicking a stock from the full candidate board should first open the standardized Stock Recommendation Card / stock decision view for that stock. Deeper stock analysis can be available from that view, but the first click should preserve the same decision-card template used on the weekly summary.

### Final Result Vocabulary

Use consistent final result labels:

- `Included`
- `Wait-listed`
- `Hold board`
- `Sell check`
- `Excluded`
- `Context only`

### Strategy Result Vocabulary

Use consistent strategy result labels:

- `Buy`
- `Possible buy`
- `Wait`
- `Hold`
- `Rejected`
- `Context`

## 4. Stock Detail Page

### Page Job

Help the user understand one stock recommendation or candidate in detail.

The top of this page should reuse the same Stock Recommendation Card / stock decision template used on the weekly summary and full candidate board. This keeps the stock decision object consistent everywhere.

### Page Hierarchy

1. Stock title and action summary
2. Stock switcher for the same weekly run
3. Trade plan
4. Strategy lineage
5. Why this is on the board
6. Why not stronger
7. Trade geometry
8. Signal breakdown
9. What changed since last week
10. Report metadata

### Stock Title Template

Show:

- ticker,
- company,
- action,
- strategy used,
- final board status.

Example:

```text
QQQ - Nasdaq 100 ETF
Action: Buy if price holds entry zone
Strategy: Index Trend Follow-Through
Final result: Included
```

### Trade Plan Template

Show:

- entry,
- upside exit / target,
- downside exit / sell level,
- valid until,
- expected hold.

### Strategy Lineage Template

Show:

- primary strategy,
- strategy role,
- strategy detail link,
- whether the strategy was the final recommendation basis or only supporting evidence.

## 5. Strategy Detail Page

### Page Job

Explain what one strategy did this week and whether its picks should be trusted.

### Page Hierarchy

1. Strategy title and plain-English purpose
2. Strategy switcher for the same weekly run
3. Strategy summary facts
4. Simple action rules
5. When this helps
6. When this hurts
7. Minimum proof before a buy
8. This week's stock outcomes
9. Trust check
10. Limits
11. Internal audit info

### Strategy Title Template

Show:

- strategy name,
- plain-English purpose,
- whether it can influence weekly recommendations.

Example:

```text
Breakout Confirmation
Purpose: stops you from buying too early by waiting for price proof.
Use in weekly picks: approved
```

### Strategy Summary Facts

Show:

- kind,
- use in weekly picks,
- number analyzed this week,
- default validity.

Use info icons for terms that need explanation.

Example:

```text
Kind: Entry finder
Use in weekly picks: Approved
This week: 4 analyzed
Default validity: This week
```

### Simple Action Rules Template

Show simple rules:

- buy rule,
- wait rule,
- reject rule,
- validity rule,
- expected hold rule.

### Strategy Weekly Outcomes Template

Show every stock analyzed by this strategy this week.

Show:

- ticker,
- strategy result,
- final result,
- simple reason,
- validity,
- stock detail link.

## 6. Archive Page

### Page Job

Let the user reopen a previous weekly run as it existed when originally published.

### Archive Index Hierarchy

1. Page title
2. List of weekly runs
3. Each run's week, publish date, data-through date, and status
4. Link to archived weekly summary

### Archived Weekly Run Hierarchy

Use the same page hierarchy as the current Weekly Summary Page, but clearly mark it as archived.

Must preserve:

- old summary,
- old final recommendations,
- old full candidate board,
- old stock details,
- old strategy details,
- original report details,
- later addenda or outcomes separately.

## 7. Navigation Rules

The user should always know:

- which weekly run they are viewing,
- whether they are on summary, board, stock detail, strategy detail, or archive,
- how to return to weekly summary,
- how to inspect why a stock passed or failed,
- how to switch to another stock or strategy from the same weekly run.

Avoid:

- duplicate confusing nav bars,
- ugly dropdowns,
- internal labels without explanation,
- making metadata visually dominant.

## 8. Language Rules

Prefer plain English.

Use:

- `Buy`
- `Wait`
- `Hold`
- `Sell / reduce`
- `Avoid`
- `Included`
- `Wait-listed`
- `Rejected`
- `Approved for weekly picks`
- `Entry finder`
- `Sell below`
- `Valid until`

Avoid:

- `promoted`,
- `trade setup` without explanation,
- `invalidated`,
- `regime supportive`,
- `suppressor`,
- vague rank-only language.
