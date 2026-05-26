# CONTEXT_PRODUCT

## Decisions

## [2026-05-22] The master product direction is now explicit
**Decision** · Source: `docs/product/trading-system-product-strategy.md`
The product's top-level direction is to become a single-user weekly decision cockpit for equity intelligence, with daily monitoring as support and options overlays sequenced behind a credible stock-first engine.
**Why it matters:** Future product work should be evaluated against whether it strengthens the weekly decision workflow, preserves explainability, and avoids execution-platform sprawl.

## [2026-05-22] Weekly review is the core operating loop
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The product is centered on a weekly review workflow, with daily monitoring acting as a supporting change digest rather than the primary experience.
**Why it matters:** Future product work should optimize for weekly decision quality first and avoid introducing intraday dependencies by accident.

## [2026-05-23] Weekly page order should mirror the user’s decision flow
**Decision** · Source: `docs/product/trading-system-product-strategy.md`
The weekly overview should lead with market posture, then fresh cash deployment, then the stock decision board, with glossary/help content available on demand rather than occupying primary screen space.
**Why it matters:** This keeps the product aligned to the user’s actual decision sequence instead of making them parse meta-explanations before the actions.

## [2026-05-25] Strategy pages are active weekly decision surfaces
**Decision** · Source: `docs/product/requirements/prd-2026-05-25-strategy-detail-page.md`
Strategy detail pages should lead with this week's live output, promotion state, and trust calibration before replay evidence or canonical rules.
**Why it matters:** This keeps strategy pages tied to the weekly operating loop instead of drifting into passive documentation.

## [2026-05-25] The overview board should currently be fed by only two promoted sleeves
**Decision** · Source: `docs/research/market/sp100-canonical-strategy-replay-2026-05-25.md`
The current action board should be sourced only from `Breakout Confirmation` and the narrowed `Sector-Confirmed Pullback Continuation` sleeve, while `ETF Trend / Rotation` and `Selective Mean Reversion` remain off-board for now.
**Why it matters:** This preserves sparse-board trust and keeps the product from presenting exploratory sleeves as if they deserve fresh capital today.

## [2026-05-22] The product stays single-user in v1
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
v1 is for one technically capable investor, not a collaborative or multi-account platform.
**Why it matters:** This constrains workflow complexity, access-control needs, and feature prioritization across the repo.

## Patterns

## [2026-05-22] Actionability beats research exhaust
**Pattern** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The user benefits most from a concise action list with evidence, not from a large undifferentiated stream of market information.
**Why it matters:** Product surfaces should compress information into decisions instead of rewarding output volume.

## Don'ts

## [2026-05-22] Do not turn the product into an execution engine
**Don't** · Source: `docs/product/weekly-equity-intelligence-prd.md`
Automated order execution and minute-by-minute trading workflows are out of scope for the current product.
**Why it matters:** This protects scope and keeps product, engineering, and design aligned around decision support.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
