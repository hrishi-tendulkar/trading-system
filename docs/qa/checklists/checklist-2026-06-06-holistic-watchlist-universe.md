# QA Checklist: Holistic Watchlist And Universe Expansion

## Status

- Owner: QA Reviewer
- Date: 2026-06-06
- Result: Pass for first CSV-backed implementation slice

## Scope Reviewed

- Product PRD for universe tiers and sparse-board product behavior
- Engineering TDD for CSV-backed universe bridge
- Active universe loader and override behavior
- S&P 500 reference watchlist builder
- Watchlist page coverage metadata
- Weekly manifest universe metadata

## Checks Performed

- Confirmed default active universe is now `sp100`.
- Confirmed Phase 2 remains selectable through the active-universe override.
- Confirmed `TRADING_SYSTEM_ACTIVE_UNIVERSE=sp100` selects `data/reference/sp100_watchlist.csv`.
- Confirmed explicit custom watchlist path override works.
- Confirmed universe CSV contract fails loudly when required columns are missing.
- Confirmed weekly run manifest round-trips `universe` and `source_watchlist_path`.
- Confirmed watchlist route renders recommendation coverage.
- Confirmed S&P 500 builder generated `data/reference/sp500_watchlist.csv`.

## Verification Commands

```bash
python3 -m pytest
python3 -m ruff check packages/core/universes.py packages/core/ui_data.py packages/core/weekly_runs.py services/jobs/cli.py scripts/mlp/build_sp100_watchlist.py scripts/mlp/build_sp500_watchlist.py scripts/mlp/publish_weekly_run.py tests/test_universes.py tests/test_ui_data.py tests/test_web_routes.py
python3 scripts/mlp/publish_weekly_run.py --target-week 2026-06-01 --watchlist data/reference/sp100_watchlist.csv --raw-outdir data/raw/sp100_5y --processed-outdir data/processed/sp100_current --skip-fetch
TRADING_SYSTEM_ACTIVE_UNIVERSE=sp100 python3 - <<'PY'
from packages.core.ui_data import get_watchlist_view
view = get_watchlist_view()
print({fact["label"]: fact["value"] for fact in view["facts"]})
PY
python3 scripts/mlp/build_sp100_watchlist.py
python3 scripts/mlp/build_sp500_watchlist.py
```

## Observed Results

- Full test suite: `34 passed`
- Ruff: `All checks passed`
- S&P 100 publish succeeded for `weekly_2026-06-01_published_2026-06-06`.
- Published S&P 100 manifest records:
  - `universe`: `sp100`
  - `source_watchlist_path`: `data/reference/sp100_watchlist.csv`
  - `input_snapshot_id`: `sp100-prices-through-2026-05-29`
- S&P 100 override facts included:
  - `Active names`: `109`
  - `Recommendation coverage`: `109 / 109`
  - `Active universe`: `sp100`
- Browser verification confirmed the Watchlist page renders `sp100`, `109 / 109`, and `weekly_2026-06-01_published_2026-06-06`.
- Browser verification confirmed the Weekly page renders `Week of 2026-06-01`, data through `2026-05-29`, and the same published run ID.
- S&P 500 builder wrote `515` CSV rows including benchmark and ETF context.

## Residual Risks

- The active universe now defaults to `sp100`; Phase 2 remains available as an explicit universe slug.
- The S&P 500 builder depends on Wikipedia table structure and should be treated as a bootstrap source, not a permanent source of record.
- Published runs still do not write a frozen universe snapshot artifact; they only record the source path and universe slug in this slice.
- Recommendation coverage can be low after switching universes unless a fresh weekly run is published against the same source watchlist.
