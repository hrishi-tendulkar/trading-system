# Weekly Archive and Addenda UX

- Date: 2026-06-02
- Owner: Design
- Related product doc: `docs/product/weekly-equity-intelligence-prd.md`

## Purpose

Define the UX requirements for preserving the full weekly recommendation picture and showing weekday checks without confusing the user about whether the weekly plan changed.

## Core UX Principle

The weekly report is a published decision artifact. The daily page and archive addenda are status layers around that artifact, not silent replacements for it.

## Required Weekly Metadata

Every weekly recommendation surface must show:

- recommendation week
- published timestamp
- data-through timestamp
- last-checked timestamp
- run ID or published run label
- current status relative to the weekly plan

## Archive IA

The Archive tab should have two levels:

1. Archive index
- list prior recommendation weeks
- show publish date, data-through date, posture, count of actionable names, count of watch names, count of deep dives, and archive status
- include supporting historical research artifacts when they are not yet fully integrated into a weekly report

2. Archived week detail
- reconstruct the weekly overview as the user saw it
- show original top actions and board buckets before weekday addenda
- show deep dives and strategy outputs from that week
- show daily addenda as timestamped status changes
- show later outcomes in a separate evaluation layer
- show source and run metadata

## Visual Rules

- Use `Published`, `Data through`, and `Last checked` labels instead of a single vague `As of` label.
- Keep original plan, daily addenda, and later outcomes in separate sections.
- Label archived weekly plans as immutable.
- Avoid feed-like styling for daily updates; they are exception records, not a news stream.
- Use compact rows for archive weeks so the user can scan history quickly.

## Failure Modes To Avoid

- Do not let page refresh imply a new analysis was generated.
- Do not replace a Sunday recommendation with a Tuesday status change.
- Do not mix outcome hindsight into the original recommendation card.
- Do not require the user to search raw files to understand what the product showed in a prior week.
