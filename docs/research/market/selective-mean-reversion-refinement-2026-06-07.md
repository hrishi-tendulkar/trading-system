# Selective Mean Reversion Refinement

## Date

2026-06-07

## Decision

`selective-mean-reversion.v1` remains `research-only` and off-board.

No main-board, sandbox, or paper-live promotion is warranted from this replay. Some stress-only variants beat exposure-aware `SPY`, but every variant materially lagged `SPY` buy-and-hold after friction, and the strongest stress buckets were too dependent on defensive tape and 2022-style selloff conditions.

## Scope

- Strategy code: `selective-mean-reversion`
- Active version tested: `selective-mean-reversion.v1`
- Replay universe: `S&P 100 + ETFs`
- Price history: `2021-01-04` through `2026-05-22`
- Data type: daily `OHLCV` only
- Benchmark: `SPY`
- Friction: `20 bps` round-trip
- Portfolio construction: weekly top `5` signals by rebound score
- Holding windows tested: `5D`, `10D`, and `15D`

## Artifacts

- Replay script: `scripts/mlp/run_selective_mean_reversion_refinement.py`
- Replay output directory: `data/processed/selective_mean_reversion_refinement_2026-06-07_selective_mean_reversion_v1_refinement/`
- Manifest: `data/processed/selective_mean_reversion_refinement_2026-06-07_selective_mean_reversion_v1_refinement/mean_reversion_refinement_manifest.json`
- Promotion decisions: `data/processed/selective_mean_reversion_refinement_2026-06-07_selective_mean_reversion_v1_refinement/mean_reversion_promotion_decisions.csv`
- Signal summary: `data/processed/selective_mean_reversion_refinement_2026-06-07_selective_mean_reversion_v1_refinement/mean_reversion_signal_summary.csv`
- Portfolio summary: `data/processed/selective_mean_reversion_refinement_2026-06-07_selective_mean_reversion_v1_refinement/mean_reversion_portfolio_summary.csv`

## Variants Tested

| Variant | Rule Intent |
|---|---|
| `v1_baseline_current` | Current v1 oversold rebound trigger across all regimes |
| `defensive_v1` | Current v1 trigger only in `Defensive` regimes |
| `stress_v1` | Current v1 trigger only in `Defensive` or `Neutral` regimes |
| `defensive_moderate_band_near_50dma` | Defensive, `-5% to -2%` oversold band, close near 50DMA, ATR capped |
| `defensive_deep_band_near_50dma` | Defensive, `-8% to -5%` oversold band, close near 50DMA, ATR capped |
| `stress_moderate_reclaim_50dma` | Stress regime plus explicit 50DMA reclaim |
| `stress_moderate_sector_confirmed` | Stress regime plus sector confirmation |
| `defensive_spy_below_ma50_reclaim_20dma` | Defensive benchmark stress plus 20DMA reclaim |

The replay also tagged signals as:

- `true_rebound_candidate`
- `ambiguous_rebound`
- `damaged_trend_or_broad_dip`

This was included to prevent broad dip-buying or damaged trend continuation from being mislabeled as mean reversion.

## Evidence Ledger

### Facts

- Best portfolio result by annualized excess versus `SPY` buy-and-hold was `stress_v1`, `15D` hold:
  - net annualized return: `7.05%`
  - annualized excess versus exposure-aware `SPY`: `+6.10%`
  - annualized excess versus `SPY` buy-and-hold: `-7.22%`
  - max drawdown: `-12.98%` versus `SPY` buy-and-hold at `-25.36%`
  - sample size: `158` signals across `67` active weeks
- `defensive_v1`, `15D` hold:
  - net annualized return: `4.97%`
  - annualized excess versus exposure-aware `SPY`: `+4.51%`
  - annualized excess versus `SPY` buy-and-hold: `-9.30%`
  - sample size: `150`
- `v1_baseline_current`, `15D` hold:
  - net annualized return: `5.16%`
  - annualized excess versus exposure-aware `SPY`: `+2.37%`
  - annualized excess versus `SPY` buy-and-hold: `-9.11%`
  - sample size: `259`
- Narrow reclaim and sector-confirmed variants had tiny samples:
  - `stress_moderate_reclaim_50dma`: `11` signals
  - `stress_moderate_sector_confirmed`: `3` signals
  - `defensive_spy_below_ma50_reclaim_20dma`: `2` signals
- `stress_v1` signal concentration:
  - largest year share: `43.04%`
  - largest sector share: `34.81%`
  - largest ticker share: `5.06%`
- `defensive_v1` signal concentration:
  - largest year share: `44.67%`
  - largest sector share: `34.67%`
  - largest ticker share: `4.67%`
- Moderate defensive band evidence was cleaner as true rebound behavior but too narrow and unstable:
  - `54` signals
  - true rebound share: `98.15%`
  - largest year share: `50.00%`
  - annualized excess versus `SPY` buy-and-hold: `-11.22%` at `15D`

### Inferences

- The only usable mean-reversion behavior remains a defensive or stress-regime rebound effect, not a general single-name long setup.
- Exposure-aware outperformance is not enough for promotion because this sleeve would still allocate capital poorly versus simply owning `SPY` over the replay window.
- The `15D` window is the only directionally interesting hold; `5D` and `10D` results are weaker and often unstable.
- Moderate oversold bands near the 50DMA are more explainable than deep oversold bands, but the evidence is too small and too concentrated to become paper-live.
- Sector confirmation and explicit reclaim behavior shrink the sample below a reliable promotion threshold.

### Unknowns

- Whether point-in-time event filters would remove enough damaged or thesis-driven selloffs to improve expectancy.
- Whether a broader `S&P 500` replay would increase sample size without reducing edge.
- Whether this is better treated as a market-regime context lens than as an independent trade setup.

## Promotion Review

| Candidate | Best Window | Main-Board Result | Paper-Live Result | Reason |
|---|---:|---|---|---|
| `stress_v1` | `15D` | Reject | Reject | Beat exposure-aware `SPY`, but lagged buy-and-hold by `7.22%` annualized and had `43.04%` of signals in one year |
| `defensive_v1` | `15D` | Reject | Reject | Lagged buy-and-hold by `9.30%` annualized and had `44.67%` of signals in one year |
| `defensive_moderate_band_near_50dma` | `15D` | Reject | Reject | Explainable rules, but only `54` signals, `50.00%` in one year, and lagged buy-and-hold by `11.22%` annualized |
| Reclaim / sector-confirmed variants | mixed | Reject | Reject | Samples of `2` to `11` signals are not stable enough |

## Final Decision

`Selective Mean Reversion` remains:

- lifecycle status: `research`
- active version: `selective-mean-reversion.v1`
- board eligibility: `false`
- production role: research appendix only, no fresh-capital board slots

No `config/strategy_registry.json` change is required because the active status and version do not change.

## Implementation And Test Plan

Implemented:

- Added a dedicated replay harness for Selective Mean Reversion refinements.
- Added variant-level signal, portfolio, regime, sector, ticker, year, oversold-band, and rebound-quality outputs.
- Added promotion decision logic requiring buy-and-hold comparison, exposure-aware comparison, drawdown, information ratio, ticker concentration, sector concentration, year concentration, and damaged-dip controls.
- Added unit tests for defensive-regime gating and rebound-quality classification.

Verification run:

```text
python3 scripts/mlp/run_selective_mean_reversion_refinement.py --version-label 2026-06-07_selective_mean_reversion_v1_refinement
python3 -m pytest tests/test_selective_mean_reversion_refinement.py tests/test_canonical_strategy_replay.py
```

Result:

- `6 passed`

## Next Research Question

Do not retest another threshold-only mean-reversion variant immediately. The next legitimate research step would be either:

- broaden the replay to `S&P 500` to test whether stress-only rebound behavior survives a larger universe, or
- add point-in-time event damage filters before revisiting live trust.
