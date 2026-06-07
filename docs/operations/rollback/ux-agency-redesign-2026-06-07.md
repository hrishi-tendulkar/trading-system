# UX Agency Redesign Rollback

## Purpose

This note records how to back out the June 7, 2026 agency-aligned UX redesign if the desktop experience needs to return to the prior implementation.

## Baseline Before UX Commit

- Branch at implementation time: `codex/weekly-archive-addenda`
- Pre-UX baseline commit: `fd8cf3bbae72515d36728d9af19c98b9b70bd446`

## UX Scope

The UX commit is intended to include only presentation and projection support:

- `apps/web/static/app.css`
- `apps/web/templates/_shell.html`
- `apps/web/templates/archive.html`
- `apps/web/templates/archive_week.html`
- `apps/web/templates/base.html`
- `apps/web/templates/stock_detail.html`
- `apps/web/templates/strategy_detail.html`
- `apps/web/templates/strategy_index.html`
- `apps/web/templates/watchlist.html`
- `apps/web/templates/weekly.html`
- `packages/core/ui_data.py`
- `tests/test_web_routes.py`

Generated market data, weekly-run snapshots, screenshots, and agency handoff source files were intentionally excluded from the UX commit.

## Rollback Options

Preferred rollback after the UX commit is deployed:

```bash
git revert --no-edit <ux_commit_sha>
git push
./scripts/railway_safe.sh up
```

File-scoped rollback to restore only the UX files to the pre-change baseline:

```bash
git checkout fd8cf3bbae72515d36728d9af19c98b9b70bd446 -- \
  apps/web/static/app.css \
  apps/web/templates/_shell.html \
  apps/web/templates/archive.html \
  apps/web/templates/archive_week.html \
  apps/web/templates/base.html \
  apps/web/templates/stock_detail.html \
  apps/web/templates/strategy_detail.html \
  apps/web/templates/strategy_index.html \
  apps/web/templates/watchlist.html \
  apps/web/templates/weekly.html \
  packages/core/ui_data.py \
  tests/test_web_routes.py

python3 -m pytest
git commit -m "Rollback agency UX redesign"
git push
./scripts/railway_safe.sh up
```

## Validation Used Before Deploy

```bash
python3 -m pytest
```
