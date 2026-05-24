# QA Checklist: Published-Run Presentation Slice

## Status

- Owner: QA
- Status: Proposed
- Last updated: 2026-05-24

## Primary review questions

- Does each core page answer its intended user question clearly?
- Could the UI look confident while the underlying stored data is missing or stale?
- Are action buckets and stock-detail labels internally consistent?

## Data-loading checks

- Verify the app fails clearly if the preferred published files are missing.
- Verify the loader falls back only to supported alternate files.
- Verify benchmark rows do not accidentally dominate stock action sections.

## Weekly checks

- `This Week's Plan` appears as the main title.
- The page has a visible `start here` section.
- Top actions are clearly ranked and linked to stock pages.
- Fresh-cash buckets do not mix with holder-only guidance.
- The page still shows selectivity rather than a flat wall of names.

## Daily checks

- The page opens with a verdict, not a generic heading only.
- Action-required items are concise and behavior-changing.
- No item reads like filler commentary.

## Watchlist checks

- The page presents an active universe rather than a generic board copy.
- Recommendation context is visible where available.
- Benchmarks or ETFs are visually distinguishable from stock ideas.

## Deep-dive checks

- The current call is visible above the fold.
- Observed facts are separated from derived reasoning.
- Entry, stop, and target logic render clearly.
- Event-risk status is visible and believable.

## Regression checks

- Unauthenticated pages still redirect to login.
- Login still works with the configured shared password.
- Navigation links remain usable on mobile widths.

## Test gaps to note if still present

- no true historical daily diff
- no write-path persistence for watchlist changes
- no publish-state validation against a database-backed run table
