# MEMORY_QA

## Durable Notes

- [2026-05-22] The most important QA question is whether a plausible-looking output can still be wrong because its inputs were incomplete or stale.
- [2026-05-24] When server-rendered pages are driven by dictionary payloads, QA should explicitly check template keys like `items` because Jinja attribute lookup can silently resolve built-in dict methods instead of the intended data fields.
- [2026-06-03] Weekly-run QA should include desktop and mobile checks for metadata cards. Long timestamps and run IDs can wrap badly even when backend freshness logic is correct.
- [2026-06-06] Universe expansion QA must check active-universe size against recommendation coverage. A successful render is not enough when a new universe may have many names awaiting projection.
- [2026-06-06] For universe promotion, QA should inspect manifest labels as well as page output. The S&P 100 run initially had correct recommendations but a stale `phase2` input snapshot label, which would have compromised traceability.
- [2026-06-07] Weekly-run QA should include negative tests for unpinned strategy manifests: placeholder `repo-current`, missing active strategy maps, and incomplete version maps must fail before publication updates the current pointer.
