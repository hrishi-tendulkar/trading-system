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

## [2026-06-02] Weekly plans are immutable, weekday checks are addenda
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The weekly report is a published decision artifact. Scheduled weekday checks may append material status updates, but page refreshes must not trigger analysis and weekday updates must not silently replace the original weekly recommendation.
**Why it matters:** This preserves weekly clarity while still protecting the user from missed midweek invalidations, event changes, or trigger changes.

## [2026-06-02] Archive is a time-travel product surface
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The Archive tab must let the user reopen the full weekly product picture, including recommendations, deep dives, strategy outputs, daily addenda, source metadata, and later outcomes.
**Why it matters:** The product needs historical accountability and reviewability, not just a table of old recommendation rows.

## [2026-06-03] Weekly freshness is part of the product contract
**Decision** · Source: `docs/product/requirements/prd-2026-06-03-weekly-run-publishing-and-staleness.md`
The weekly page must render the latest successfully published weekly run and must clearly warn when the expected current-week report is missing or stale. Weekly recommendations are a publish lifecycle, not whichever recommendation CSV happens to exist.
**Why it matters:** The user plans trades for the coming week; an old report that looks current is a product failure, even when the data label is technically accurate.

## [2026-06-03] Medium-term product vision is a scaled-down strategy operating system
**Decision** · Source: `docs/strategy/medium-term-strategy-operating-system-vision.md`
Trading System should grow from a weekly report generator into a single-operator strategy operating system modeled on mature short-term trading workflows: maintain a small strategy library, improve strategy versions through research and replay, promote only validated versions into the weekly board, and review both backtest and live weekly outcomes.
**Why it matters:** The product may start with the four current canonical strategies, but the system should be built so those four can be refined, versioned, promoted, demoted, and evaluated with the same discipline that would support a larger strategy library later.

## [2026-06-07] Strategy revisions need archive-grade naming and workstream prompts
**Decision** · Source: `docs/strategy/strategy-versioning-and-revision-archive.md`
Strategy families use stable `basis_code` values, active rules use `{basis_code}.vN`, registry snapshots use date-based `registry_version`, and parallel improvement workstreams start from paste-ready `/goal` prompts.
**Why it matters:** The user needs to know which strategy versions analyzed each week and needs repeatable prompts to improve each strategy without mixing research variants into production reports.

## [2026-06-07] Weekly UX content hierarchy is now a product contract
**Decision** · Source: `docs/design/information-hierarchy.md`
Weekly summary, stock recommendation card, full candidate board, stock detail, strategy detail, and archive each have defined information hierarchy templates. Future UX and implementation work should change these templates deliberately rather than inventing page content ad hoc.
**Why it matters:** The product must standardize `what we show` before debating visual design; otherwise every redesign reopens the same content and workflow questions.

## [2026-05-22] The product stays single-user in v1
**Decision** · Source: `docs/product/weekly-equity-intelligence-prd.md`
v1 is for one technically capable investor, not a collaborative or multi-account platform.
**Why it matters:** This constrains workflow complexity, access-control needs, and feature prioritization across the repo.

## Patterns

## [2026-05-22] Actionability beats research exhaust
**Pattern** · Source: `docs/product/weekly-equity-intelligence-prd.md`
The user benefits most from a concise action list with evidence, not from a large undifferentiated stream of market information.
**Why it matters:** Product surfaces should compress information into decisions instead of rewarding output volume.

## [2026-06-07] Full board click-through should preserve the stock decision template
**Pattern** · Source: `docs/design/information-hierarchy.md`
Clicking a stock from the full candidate board should first open the standardized stock recommendation card / stock decision view for that stock; deeper stock analysis can sit below or behind that decision object.
**Why it matters:** The user should encounter one consistent stock decision template across weekly summary, full board, stock detail, and archive.

## Don'ts

## [2026-05-22] Do not turn the product into an execution engine
**Don't** · Source: `docs/product/weekly-equity-intelligence-prd.md`
Automated order execution and minute-by-minute trading workflows are out of scope for the current product.
**Why it matters:** This protects scope and keeps product, engineering, and design aligned around decision support.

## Inbox (proposed by other agents — owner reviews and promotes or discards)

- None currently.
