# Railway Setup

This folder records the intended Railway service topology for Trading System.

CLI troubleshooting:

- Prefer `./scripts/railway_safe.sh <command>` over raw `railway <command>` in this repo.
- See `docs/operations/railway-cli-troubleshooting.md` for the stale-`RAILWAY_TOKEN` and expired-OAuth decision tree.

Recommended services:

- `trading-system-web`
- `trading-system-daily-job`
- `trading-system-weekly-job`
- `trading-system-manual-job`

Suggested start commands:

- web: `python -m uvicorn apps.web.main:app --host 0.0.0.0 --port $PORT`
- daily: `python -m services.jobs.cli daily-run`
- weekly: `python -m services.jobs.cli weekly-run`
- weekly validation: `python -m services.jobs.cli validate-weekly-current`
- manual: `python -m services.jobs.cli --help`

Recommended cron schedules:

- daily: `30 22 * * 1-5`
- weekly publish: `0 7 * * 0`
- weekly validation: `0 8 * * 0`

The weekly schedules are UTC cron expressions. During Eastern daylight time,
`0 7 * * 0` is Sunday 03:00 ET and `0 8 * * 0` is Sunday 04:00 ET.

Required durable weekly publishing variables:

- `WEEKLY_RUN_REPOSITORY=supabase`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`
- `APP_BASE_URL`
- `EMAIL_ALERT_TO=hrishi00@gmail.com`
- `EMAIL_ALERT_FROM`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_USE_TLS`
