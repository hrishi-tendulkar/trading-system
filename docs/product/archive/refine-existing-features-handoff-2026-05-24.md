# Refine Existing Features Handoff

## What this workstream is

This workstream is about making the current product surfaces actually useful before adding more feature breadth.

The product already has the beginnings of:

- `Weekly review`
- `Daily digest`
- `Watchlist`
- `Stock detail`

But today these are still mostly scaffolds. The main issue is not missing page count. The main issue is that the user job behind each page is still too fuzzy.

## Core conclusion

The current product should be refined around three clear jobs:

- `Weekly review` should answer: `What should I do with capital this week?`
- `Daily review` should answer: `What changed enough to matter before next week's review?`
- `Deep dive` should answer: `For this stock, should I act now, wait, or avoid it?`

If a surface cannot answer one of those questions clearly, it is not yet strong enough for `P0`.

## P0 product direction

### 1. Weekly review should become a decision session

It should not feel like a recap or dashboard.

The page should guide the user through:

- market posture,
- top actions this week,
- fresh cash deployment,
- existing positions needing action,
- and which names deserve deeper work.

The most important missing piece is a `start here` section that tells the user where to begin.

### 2. Daily digest should become exception-based

It should not become a news stream or mini dashboard.

It should only surface changes that alter behavior before the next weekly session, such as:

- broken setups,
- important post-earnings reactions,
- holdings that need reassessment,
- or watchlist names that became actionable.

If nothing material changed, the page should say that directly.

### 3. Stock detail should become a real deep-dive object

The stock page should be reframed as a decision memo, not a generic research page.

It should clearly separate:

- short-term setup quality,
- long-term quality,
- event risk,
- what makes the stock actionable now,
- and what would break the case.

## Deep-dive recommendation

Yes, deep dives should exist, but not for the whole universe every week.

Recommended `P0` rule:

- automatically refresh deep dives for top `Buy now` names,
- include the highest-priority `Wait for pullback` names,
- include holdings with event risk or thesis tension,
- allow manual deep dives later for any watchlist name.

This keeps depth focused on names that matter now.

## Why this matters for phasing

This workstream argues for strengthening the core operating loop before layering on too many new surfaces.

In practice, that means:

1. tighten the purpose of existing pages,
2. make weekly decisions clearer,
3. make daily usage more selective,
4. and only then expand feature breadth where it strengthens that loop.

This does **not** mean `no` to new features.

It means new features should be judged by whether they improve:

- weekly decision quality,
- stock-level trust,
- or exception-based daily awareness.

## Suggested sequencing lens for the next chat

When combining `new features` and `refine existing`, use this test:

- Does the feature make the weekly plan clearer?
- Does it improve the quality of a stock decision?
- Does it help the user notice a genuinely important daily change?
- Or is it adding surface area before the core loop is crisp?

Features that help one of the first three should phase earlier.
Features that mostly add breadth should phase later unless they unlock a blocked core workflow.

## Main artifact created in this workstream

- [prd-2026-05-24-review-surfaces-p0-refinement.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/requirements/archive/prd-2026-05-24-review-surfaces-p0-refinement.md)

## Useful supporting docs

- [PRODUCT.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/PRODUCT.md)
- [trading-system-product-strategy.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/trading-system-product-strategy.md)
- [weekly-equity-intelligence-prd.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/product/weekly-equity-intelligence-prd.md)
- [weekly-equity-intelligence-strategy-blueprint.md](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/strategy/weekly-equity-intelligence-strategy-blueprint.md)

## Copy-ready short summary

Refine existing features workstream summary:

The current product already has the right top-level surfaces, but they are still too scaffolded to be truly useful. The main recommendation is to sharpen the user job of each existing page before adding too much more breadth. `Weekly review` should become a clear weekly decision session with a ranked starting point, fresh-cash actions, holder actions, and a short queue of names worth deeper work. `Daily digest` should become exception-based and only surface changes that materially alter behavior before the next weekly session. `Stock detail` should become a real deep-dive object focused on whether to act now, wait, or avoid, with explicit separation between short-term setup, long-term quality, and event risk. Deep dives should exist for the week's most important names and risk-sensitive holdings, not automatically for the whole universe. The core phasing principle is to prioritize anything that improves weekly decision quality, stock-level trust, or meaningful daily awareness before adding feature breadth that expands surface area without strengthening the core loop.
