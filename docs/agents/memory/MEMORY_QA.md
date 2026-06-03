# MEMORY_QA

## Durable Notes

- [2026-05-22] The most important QA question is whether a plausible-looking output can still be wrong because its inputs were incomplete or stale.
- [2026-05-24] When server-rendered pages are driven by dictionary payloads, QA should explicitly check template keys like `items` because Jinja attribute lookup can silently resolve built-in dict methods instead of the intended data fields.
- [2026-06-03] Weekly-run QA should include desktop and mobile checks for metadata cards. Long timestamps and run IDs can wrap badly even when backend freshness logic is correct.
