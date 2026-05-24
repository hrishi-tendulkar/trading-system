# Railway Setup

This folder records the intended Railway service topology for Trading System.

Recommended services:

- `trading-system-web`
- `trading-system-daily-job`
- `trading-system-weekly-job`
- `trading-system-manual-job`

Suggested start commands:

- web: `python -m uvicorn apps.web.main:app --host 0.0.0.0 --port $PORT`
- daily: `python -m services.jobs.cli daily-run`
- weekly: `python -m services.jobs.cli weekly-run`
- manual: `python -m services.jobs.cli --help`

Recommended cron schedules:

- daily: `30 22 * * 1-5`
- weekly: `0 14 * * 6`
