# MEMORY_ENGINEER

## Durable Notes

- [2026-05-22] Implementation work should preserve source lineage and historical reproducibility, even in small scripts and early pipelines.
- [2026-05-22] Early MLP scripts should optimize for inspectability over sophistication: raw CSV inputs, derived features, recommendation snapshots, and simple replayable backtests are more valuable than hiding logic behind a premature service layer.
- [2026-05-22] Recommendation text, entry/stop/target levels, and strategy detail pages should all be derived from the same strategy payload to avoid explanation drift between analysis code and UI code.
- [2026-05-24] Hosted jobs must not publish partially built outputs over the current live weekly review or daily digest; explicit run states and publish gates are implementation requirements, not optional polish.
- [2026-05-24] SQL migrations should be treated as the schema source of truth; Python ORM metadata must be checked against the migrated database to catch drift before it reaches production.
- [2026-05-24] Even before database wiring lands, UI work should render from one normalized recommendation contract and page-specific projection functions rather than letting templates parse source files or invent their own labels.
- [2026-05-25] Strategy replay needs to preserve unavailable context states explicitly; collapsing `missing sector ETF proxy` into `unconfirmed sector` makes subgroup backtests look cleaner than the data actually supports.
- [2026-06-03] Weekly publishing now has a file-backed bridge: `scripts/mlp/publish_weekly_run.py` snapshots the previous CSV-backed report, validates source data through the expected prior Friday, writes `data/processed/weekly_runs/`, and updates `current.json` only after validation passes. Future cron work should test `python3 -m services.jobs.cli weekly-run` directly, not only the script.
- [2026-06-06] Watchlist expansion code should expose recommendation coverage whenever the active universe can be larger than the latest published recommendation set; otherwise broad-universe UI can look more complete than the underlying run actually is.
- [2026-06-06] `publish_weekly_run.py` must derive both `input_snapshot_id` and generated report path from the selected universe. A hard-coded `phase2` label caused misleading metadata/report placement during the S&P 100 promotion and was fixed.
- [2026-06-07] Treat strategy-version pinning as a write-time contract for published weekly snapshots: `write_run_snapshot(..., publish_current=True)` validates concrete registry/version metadata before copying recommendations or updating the current pointer.
- [2026-06-15] Cron jobs need wrapper-level smoke coverage: verify log redirection paths exist and calendar defaults match the scheduled run time. Testing `services.jobs.cli weekly-run` manually is not enough if cron can fail before Python starts.
