# Frontend Design Brief: Trading System

## 1. What We Are Building

Trading System is a single-user weekly trading decision app.

It helps one investor answer:

> What should I buy, wait on, hold, sell, or avoid this week?

This is not a brokerage app and does not place trades. It is a decision-support product.

The user has limited weekday time and needs a clear weekly plan before placing trades manually.

## 2. Design Goal

Redesign the frontend so the product feels like a clear weekly decision workspace, not a technical report.

The user should be able to quickly understand:

- what to trade this week,
- why those names were recommended,
- entry level,
- upside exit / target,
- downside exit / sell level,
- how long the idea is valid,
- which strategy produced the idea,
- what other candidates were considered and rejected.

## 3. Scope

Please redesign the UX and visual presentation for these surfaces:

- Weekly Summary
- Full Candidate Board
- Stock Detail
- Strategy Detail
- Archive
- Shared navigation between those pages

The output can be Figma, high-fidelity wireframes, or implementation-ready frontend designs depending on engagement scope.

## 4. Hard Boundary

Do not invent new product functionality.

Do not invent:

- new trading strategies,
- new scores,
- new recommendation logic,
- new data fields,
- brokerage/execution flows,
- AI chat,
- portfolio optimization,
- alerts,
- new workflows outside the pages listed above.

Your job is to make the existing decision workflow much clearer and more usable.

## 5. Core Workflow

The product revolves around a weekly run.

A weekly run contains:

- final recommendations,
- all candidates considered,
- strategy outputs,
- stock-level details,
- reasons picks passed or failed,
- archive metadata.

Primary flow:

```text
Weekly Summary
  -> Full Candidate Board
  -> Stock Detail
  -> Strategy Detail
  -> Archive
```

The weekly summary is the home base. The user should always know how to get back to it.

## 6. Page Jobs

### Weekly Summary

Job:

> Tell me what to do this week.

It should show the most important recommendations first. Metadata should be secondary.

Must make clear:

- top buys,
- wait-list names,
- sell / reduce checks,
- risk posture,
- link to the full board for why picks passed or failed.

### Full Candidate Board

Job:

> Show me everything considered this week and why each idea passed, waited, or failed.

This page should answer:

- What made the final recommendations?
- What did not?
- Why not?
- Which strategy produced the idea?
- Is this a buy, wait, hold, sell check, or reject?

### Stock Detail

Job:

> Help me decide whether I trust this stock recommendation.

Must show:

- ticker and company,
- action,
- strategy used,
- entry,
- upside exit / target,
- downside exit / sell level,
- valid-until date or condition,
- expected holding period,
- why this week,
- why not stronger,
- what changed,
- link to strategy detail,
- way to switch to another stock from the same weekly run.

### Strategy Detail

Job:

> Explain what this strategy did this week and why we should or should not trust its picks.

Must show:

- strategy name,
- plain-English purpose,
- whether it can influence weekly recommendations,
- what stocks it analyzed this week,
- what the strategy said for each stock,
- whether each stock made the final recommendation board,
- simple reason for inclusion or exclusion,
- limits / when the strategy is not reliable,
- way to switch to another strategy from the same weekly run.

### Archive

Job:

> Let me reopen an old weekly run exactly as it was originally published.

Archive should preserve:

- old weekly summary,
- old final recommendations,
- old full board,
- old stock detail,
- old strategy detail,
- original publish date and data-through date,
- later addenda or outcomes separately from the original recommendation.

Archive should feel like time travel, not just a table of old rows.

## 7. Language Direction

Use plain investor language. Avoid internal system labels.

Examples:

| Avoid | Prefer |
| --- | --- |
| Promoted | Approved for weekly picks |
| Trade setup | Entry finder / entry strategy, with an info tooltip |
| Invalidated | Sell below / avoid below |
| Regime supportive | Market conditions allow selective buys |
| Suppressor | Reason this did not make the final list |
| Final board | Final recommendations |

Some concepts may need info icons or hover/click explanations. The UI should not assume the user knows internal trading-system vocabulary.

## 8. Navigation Direction

The current prototype navigation is functional but not good enough.

Please rethink navigation from first principles.

Requirements:

- global nav should be clear,
- weekly summary should feel like the home base,
- back path should be obvious,
- stock and strategy pages should allow switching to another stock or strategy from the same weekly run,
- full board should be easy to reach when the user asks "why not this stock?",
- avoid confusing duplicate nav bars,
- avoid ugly dropdowns unless there is a strong UX reason.

## 9. Design Quality Bar

This should feel like a professional internal investing tool:

- calm,
- dense but readable,
- decision-first,
- not decorative,
- not consumer-trading-app flashy,
- not a technical dashboard,
- not a marketing page.

The first screen should make the user's next decision clearer.

## 10. Available Example Data Fields

The design should assume the product can provide fields like:

- recommendation week,
- published date,
- data-through date,
- ticker,
- company,
- action,
- strategy name,
- strategy result,
- final recommendation status,
- entry,
- target / upside exit,
- sell / downside exit,
- valid until,
- expected hold,
- confidence,
- reason,
- exclusion reason,
- market posture,
- universe name,
- archive run ID.

Do not require new data fields without explicitly marking them as design assumptions.

## 11. Prototype

A rough HTML prototype is included.

Use it to understand workflow and data relationships. Do not copy its visual design.

The source of truth for what belongs on each page/card is:

`docs/design/information-hierarchy.md`

Primary file:

`docs/design/prototypes/weekly-decision-redesign/weekly-trade-plan.html`

Supporting files:

- `full-candidate-board.html`
- `stock-analysis-card.html`
- `strategy-detail-card.html`

## 12. What We Want From The Agency

We want a redesigned UX system for these pages, including:

- information architecture,
- desktop layouts,
- mobile layouts,
- navigation model,
- reusable components,
- card patterns,
- table/list patterns,
- plain-English terminology recommendations,
- empty/loading/error state recommendations,
- implementation handoff notes.

The best outcome is not "prettier screens." The best outcome is that the investor can make better weekly trading decisions faster and with less confusion.
