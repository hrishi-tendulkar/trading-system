# Weekly Run Automation

## Purpose

Publish the weekly recommendation run automatically after the prior trading week closes.

The job command is:

```bash
python3 -m services.jobs.cli weekly-run
```

## Schedule

Default schedule:

```text
0 22 * * 0
```

This is Sunday `22:00 UTC`, which is Sunday evening in New York during daylight-saving time.

## Railway Setup

Use a dedicated Railway cron service for this job. Do not apply this config to the web service.

Config file:

```text
infra/railway-weekly-run.toml
```

Railway cron jobs run the service start command on the configured UTC crontab schedule. The process must finish and exit; if a prior execution is still active, Railway skips the next scheduled execution.

## Expected Behavior

The weekly job:

1. snapshots the existing published report into the archive if needed,
2. refreshes phase-2 watchlist market data through the prior Friday close,
3. runs the weekly recommendation analysis,
4. validates that the output uses the expected source date,
5. writes a run snapshot under `data/processed/weekly_runs/`,
6. updates `current.json` only after validation passes.

If validation fails, the previous published run remains current.

## Local Cron Setup

The current file-backed bridge writes reports under this repo's `data/processed/weekly_runs/`
folder. Until the published-run store moves to Supabase or another shared persistent store,
local cron is the automation that updates the local app state directly.

Installed crontab block:

```cron
# Trading System weekly publish start
0 18 * * 0 cd "/Users/hrishimansi/Documents/Hrishi/Projects/Trading System" && /usr/bin/python3 -m services.jobs.cli weekly-run >> "logs/weekly-run.log" 2>&1
# Trading System weekly publish end
```

This runs Sunday at 6:00 PM local machine time. The computer must be awake and able to
reach the data provider.

To inspect it:

```bash
crontab -l | sed -n '/# Trading System weekly publish start/,/# Trading System weekly publish end/p'
```

To remove it, delete the block between those marker comments with `crontab -e`.

## Manual Run

For the current week:

```bash
python3 -m services.jobs.cli weekly-run
```

For a specific recommendation week:

```bash
python3 -m services.jobs.cli weekly-run --run-date 2026-06-01
```

For QA without provider refresh:

```bash
python3 -m services.jobs.cli weekly-run --skip-fetch
```
