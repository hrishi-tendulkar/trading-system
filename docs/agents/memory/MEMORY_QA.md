# MEMORY_QA

## Durable Notes

- [2026-05-22] The most important QA question is whether a plausible-looking output can still be wrong because its inputs were incomplete or stale.
- [2026-05-24] When server-rendered pages are driven by dictionary payloads, QA should explicitly check template keys like `items` because Jinja attribute lookup can silently resolve built-in dict methods instead of the intended data fields.
