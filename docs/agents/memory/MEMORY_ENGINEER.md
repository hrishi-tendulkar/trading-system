# MEMORY_ENGINEER

## Durable Notes

- [2026-05-22] Implementation work should preserve source lineage and historical reproducibility, even in small scripts and early pipelines.
- [2026-05-22] Early MLP scripts should optimize for inspectability over sophistication: raw CSV inputs, derived features, recommendation snapshots, and simple replayable backtests are more valuable than hiding logic behind a premature service layer.
- [2026-05-22] Recommendation text, entry/stop/target levels, and strategy detail pages should all be derived from the same strategy payload to avoid explanation drift between analysis code and UI code.
- [2026-05-24] Hosted jobs must not publish partially built outputs over the current live weekly review or daily digest; explicit run states and publish gates are implementation requirements, not optional polish.
- [2026-05-24] SQL migrations should be treated as the schema source of truth; Python ORM metadata must be checked against the migrated database to catch drift before it reaches production.
- [2026-05-24] Even before database wiring lands, UI work should render from one normalized recommendation contract and page-specific projection functions rather than letting templates parse source files or invent their own labels.
- [2026-05-25] Strategy replay needs to preserve unavailable context states explicitly; collapsing `missing sector ETF proxy` into `unconfirmed sector` makes subgroup backtests look cleaner than the data actually supports.
