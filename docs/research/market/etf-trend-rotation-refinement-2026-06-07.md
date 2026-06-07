# ETF Trend / Rotation Ranked Weekly Refinement

## Date

2026-06-07

## Scope

- Strategy code: `etf-trend-rotation`
- Current version tested against: `etf-trend-rotation.v1`
- Candidate promoted version considered: `etf-trend-rotation.v2`
- Universe: `SPY`, `QQQ`, `XLK`, `XLF`, `XLV`, `XLE`, `XLI`, `XLY`
- Price history: `2021-01-04` through `2026-05-29`
- Cadence: weekly Friday selection
- Holding period: `5` trading days
- Base friction: `20 bps` round trip per weekly ETF position
- Benchmarks:
  - `SPY` buy-and-hold
  - exposure-aware `SPY`, active only in weeks when the ETF variant is active

## Artifacts

- Replay script: `scripts/mlp/run_etf_trend_rotation_refinement.py`
- Replay output directory: `data/processed/etf_trend_rotation_refinement_2026-06-07_etf_v2_research/`
- Promotion decisions: `data/processed/etf_trend_rotation_refinement_2026-06-07_etf_v2_research/etf_promotion_decisions.csv`
- Portfolio summary: `data/processed/etf_trend_rotation_refinement_2026-06-07_etf_v2_research/etf_portfolio_summary.csv`
- Friction sensitivity: `data/processed/etf_trend_rotation_refinement_2026-06-07_etf_v2_research/etf_friction_sensitivity.csv`
- Ticker concentration: `data/processed/etf_trend_rotation_refinement_2026-06-07_etf_v2_research/etf_ticker_summary.csv`

## Research Question

Can `ETF Trend / Rotation` be upgraded from broad daily ETF eligibility into a promoted ranked weekly rotation sleeve?

The target was a measurable ETF-only rule that could:

- select top `1` or top `2` ETFs weekly,
- preserve ETF sleeve identity,
- beat `SPY` buy-and-hold by at least `3%` annualized after conservative friction,
- beat exposure-aware `SPY`,
- avoid materially worse drawdown than `SPY`,
- and avoid dependence on one ETF, one sector, or one narrow regime.

## Variants Tested

| Variant | Treatment |
|---|---|
| `top1_all_supportive_balanced` | Top `1` across broad and sector ETFs in supportive regimes using balanced `10D`/`20D`/`60D` relative-strength ranking |
| `top2_all_supportive_balanced` | Same as balanced all-ETF top `1`, but equal-weight top `2` |
| `top1_all_supportive_strict_rs` | Top `1` across all ETFs; requires `20D` RS above `SPY` by at least `1%` and positive `60D` RS |
| `top2_all_supportive_strict_rs` | Same strict all-ETF rule, equal-weight top `2` |
| `top1_sector_supportive_strict_rs` | Sector ETFs only; strict RS; top `1` |
| `top2_sector_supportive_strict_rs` | Sector ETFs only; strict RS; equal-weight top `2` |
| `top1_broad_supportive_trend` | Broad ETFs only, `SPY`/`QQQ`; top `1` |
| `top1_all_risk_on_strict_rs` | All ETFs; strict RS; requires full `Risk-on` regime only |

All variants required:

- weekly Friday evaluation,
- ETF-only universe,
- close above `20DMA`,
- `20DMA` above `50DMA`,
- positive `20DMA` slope,
- ATR percent no higher than `4%`,
- and one-week forward replay with friction.

## Main Results

| Variant | Active Weeks | Net Ann. Return | Exposure-Aware SPY Ann. | Excess vs Exposure-Aware SPY | SPY Buy-Hold Ann. | Excess vs SPY Buy-Hold | Max DD | SPY Max DD | Largest Ticker Share | Largest Regime Share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `top2_sector_supportive_strict_rs` | 118 | 5.99% | 1.85% | 4.13% | 14.27% | -8.28% | -16.20% | -25.36% | 30.68% | 81.82% |
| `top1_sector_supportive_strict_rs` | 118 | 4.38% | 1.85% | 2.53% | 14.27% | -9.89% | -17.86% | -25.36% | 36.44% | 83.05% |
| `top2_all_supportive_strict_rs` | 124 | 3.34% | 0.97% | 2.37% | 14.27% | -10.93% | -16.31% | -25.36% | 24.40% | 84.69% |
| `top1_all_supportive_strict_rs` | 124 | 3.12% | 0.97% | 2.15% | 14.27% | -11.15% | -18.79% | -25.36% | 33.06% | 83.87% |
| `top2_all_supportive_balanced` | 153 | 3.10% | 0.91% | 2.19% | 14.27% | -11.17% | -16.47% | -25.36% | 26.17% | 85.23% |
| `top1_all_supportive_balanced` | 153 | 2.65% | 0.91% | 1.74% | 14.27% | -11.62% | -20.66% | -25.36% | 34.64% | 83.66% |
| `top1_broad_supportive_trend` | 133 | 2.38% | 1.00% | 1.38% | 14.27% | -11.89% | -17.69% | -25.36% | 66.92% | 90.23% |
| `top1_all_risk_on_strict_rs` | 104 | 1.62% | 1.96% | -0.34% | 14.27% | -12.65% | -18.87% | -25.36% | 39.42% | 100.00% |

## Friction Sensitivity

The best candidate, `top2_sector_supportive_strict_rs`, stayed ahead of exposure-aware `SPY` at higher friction, but it did not approach the SPY buy-and-hold hurdle.

| Variant | Friction | Net Ann. Return | Excess vs SPY Buy-Hold | Excess vs Exposure-Aware SPY | Max DD |
|---|---:|---:|---:|---:|---:|
| `top2_sector_supportive_strict_rs` | 10 bps | 8.38% | -5.89% | 4.22% | -14.58% |
| `top2_sector_supportive_strict_rs` | 20 bps | 5.99% | -8.28% | 4.13% | -16.20% |
| `top2_sector_supportive_strict_rs` | 40 bps | 1.35% | -12.92% | 3.96% | -19.36% |
| `top2_all_supportive_strict_rs` | 20 bps | 3.34% | -10.93% | 2.37% | -16.31% |
| `top2_all_supportive_balanced` | 20 bps | 3.10% | -11.17% | 2.19% | -16.47% |

## Concentration And Regime Check

The best variant was not driven by one ETF:

| Ticker | Trades | Avg 5D Net Return | Avg 5D Excess Net | Win Rate |
|---|---:|---:|---:|---:|
| `XLK` | 54 | 0.69% | 0.29% | 61.11% |
| `XLI` | 35 | -0.02% | 0.15% | 48.57% |
| `XLY` | 32 | 0.48% | 0.36% | 53.12% |
| `XLF` | 26 | 0.09% | 0.09% | 50.00% |
| `XLE` | 17 | 0.98% | 1.17% | 58.82% |
| `XLV` | 12 | -1.19% | -1.22% | 41.67% |

However, the result was still mostly a supportive-regime exposure tool:

- `81.82%` of best-variant trades occurred in `Risk-on`.
- `18.18%` occurred in `Selective risk-on`.
- The risk-on-only strict version did not beat exposure-aware `SPY`.

## Evidence Ledger

### Facts

- No tested variant cleared the `SPY` buy-and-hold hurdle.
- The best conservative-friction variant returned `5.99%` net annualized, which was `8.28%` annualized below `SPY` buy-and-hold.
- Most variants beat exposure-aware `SPY`, with the best variant ahead by `4.13%` annualized.
- Drawdown was better than `SPY` buy-and-hold for every tested variant at `20 bps` friction.
- The broad-only version was highly concentrated: `66.92%` in one ticker and `90.23%` in one regime.
- The sector top `2` strict-RS version had better diversification across ETFs, but still did not solve the absolute-return problem.

### Inferences

- Ranked ETF rotation can be useful as an exposure appendix or cash-deployment context, especially when the alternative is forcing weak single-name trades.
- It is not yet a promoted alpha sleeve because the strategy gives up too much market participation during a strong SPY buy-and-hold period.
- The apparent edge is mainly exposure timing and drawdown dampening, not enough standalone return generation.
- Top `2` sector treatment is more stable than top `1` and more credible than broad-only treatment.

### Unknowns

- Whether a longer holding window, monthly rebalance, or broader sector ETF universe would improve participation without overfitting.
- Whether adding cash-yield assumptions during inactive weeks would materially narrow the SPY buy-and-hold gap.
- Whether richer ETF universe coverage, such as equal-weight, factor, bond, or international ETFs, would make rotation more valuable.

## Decision

`etf-trend-rotation.v2` is **not promoted**.

The current active version remains:

- `etf-trend-rotation.v1`
- status: `research`
- board enabled: `false`
- production role: off-board ETF exposure context only

The best researched rule, `top2_sector_supportive_strict_rs`, may be retained as a research-only exposure appendix candidate:

- weekly sector ETF ranking,
- supportive regime required,
- close above `20DMA`,
- `20DMA` above `50DMA`,
- positive `20DMA` slope,
- ATR percent no higher than `4%`,
- `20D` RS at least `1%` above `SPY`,
- positive `60D` RS,
- equal-weight top `2`,
- one-week holding assumption.

It should not feed the main board and should not be represented as a promoted `Buy now` sleeve.

## Implementation Test Plan

Completed:

- Added `scripts/mlp/run_etf_trend_rotation_refinement.py`.
- Added focused replay tests in `tests/test_etf_trend_rotation_refinement.py`.
- Verified ETF refinement tests and canonical replay tests pass.
- Verified Ruff passes on the new ETF replay script and tests.

Commands run:

```bash
python3 scripts/mlp/run_etf_trend_rotation_refinement.py --version-label 2026-06-07_etf_v2_research
python3 -m pytest tests/test_etf_trend_rotation_refinement.py tests/test_canonical_strategy_replay.py
python3 -m ruff check scripts/mlp/run_etf_trend_rotation_refinement.py tests/test_etf_trend_rotation_refinement.py
```

## Next Research Question

If this sleeve is revisited, test whether ETF rotation should be a lower-turnover allocation tool rather than a weekly `Buy now` engine:

- monthly rebalance,
- `10D` versus `20D` versus `60D` rank-window ablations,
- cash-yield assumption for inactive weeks,
- broader ETF menu,
- and explicit "ETF appendix only" presentation rather than main-board eligibility.
