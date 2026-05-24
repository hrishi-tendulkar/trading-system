# MEMORY_TECH

## Durable Notes

- [2026-05-22] The architecture should preserve raw, normalized, and derived layers separately so later score changes can be explained instead of guessed.
- [2026-05-22] For this product, one low-cost all-in-one provider may be enough to prove the stock engine, but options overlays are likely the forcing function for a second provider; do not assume one vendor will cleanly satisfy both the core equity workflow and credible historical options support.
- [2026-05-22] SEC EDGAR should be treated as infrastructure, not just a backup source. Even if another vendor offers filings, direct SEC ingestion materially improves auditability, source traceability, and recovery from vendor gaps.
- [2026-05-22] For the budget-constrained lean v1, the technical strategy should optimize for a single broad provider plus SEC: `FMP Starter + SEC EDGAR`, daily batch jobs, weekly synthesis, deterministic stock-engine scoring, and no options pipeline in `P0`.
- [2026-05-22] Before broader API integration, a CSV-first MLP is the fastest believable validation path: small watchlist, local scripts, explicit recommendation history, and simple weekly backtests to test the signal spine before scaling infrastructure.
- [2026-05-22] Delivery surfaces should be generated from the same structured strategy outputs used for ranking; if the UI explanation, trade plan, and backtest metadata come from different logic paths, trust erodes quickly.
- [2026-05-24] `yfinance` / Yahoo Finance is acceptable as a zero-cost bootstrap source for personal local validation of EOD watchlist prices, but it should not be the assumed durable system-of-record provider because the access posture is personal-use/research-oriented and does not reliably solve the broader product data contract.
- [2026-05-24] The best hosted v1 shape is Python-first and server-rendered: `FastAPI + Jinja2` for the internal app, `Typer`-driven job services on Railway, `Supabase Postgres` plus private storage as the system of record, and a shared-password gate instead of full user auth.
- [2026-05-24] On Railway, scheduled work should be modeled as separate short-lived cron services that exit cleanly, not as one long-running worker with an in-process scheduler; overlapping active cron executions will cause later scheduled runs to be skipped.
