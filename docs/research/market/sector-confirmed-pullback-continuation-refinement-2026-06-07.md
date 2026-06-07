# Sector-Confirmed Pullback Continuation Refinement

## Date

2026-06-07

## Decision

Do not promote `sector-confirmed-pullback-continuation.v2`.

Keep the active version at:

- `sector-confirmed-pullback-continuation.v1`

The broad v1 rule remains the active narrowed/trust-calibrated pullback sleeve for now. The tested narrowed variants improved exposure-aware information quality, but none cleared the full promotion bar because they failed to beat `SPY` buy-and-hold by at least `3%` annualized after conservative friction.

## Scope

- Universe: `S&P 100 + ETFs`
- Price history: daily `OHLCV` from `data/raw/sp100_5y/mlp_prices.csv`
- Cadence model: weekly review
- Portfolio model: top `5` live `Buy on pullback` candidates per active review week
- Holding model: `15` trading days represented as a rolling `3`-week tranche
- Friction: `20 bps` round trip per trade
- Benchmarks:
  - `SPY` buy-and-hold over the replay period
  - exposure-aware `SPY` over the same signal windows

## Artifacts

- Script: `scripts/mlp/run_pullback_strategy2_refinement.py`
- Output directory: `data/processed/strategy2_pullback_refinement_2026-06-07_strategy2_v2/`
- Promotion table: `strategy2_promotion_decisions.csv`
- Portfolio table: `strategy2_portfolio_summary.csv`
- Signal table: `strategy2_signal_summary.csv`
- Regime, sector, ticker, depth, and extension checks:
  - `strategy2_regime_summary.csv`
  - `strategy2_sector_summary.csv`
  - `strategy2_ticker_summary.csv`
  - `strategy2_pullback_depth_summary.csv`
  - `strategy2_extension_summary.csv`

## Variant Results

| Variant | Decision | Signal Sample | Net Ann. Return | Ann. Excess vs SPY Buy-Hold | Ann. Excess vs Exposure-Aware SPY | Max Drawdown | Weekly Information-Like |
|---|---:|---:|---:|---:|---:|---:|---:|
| Current v1 Pullback | `active current` | 3707 | 18.82% | +4.54% | +3.30% | -25.16% | 0.041 |
| Strict RS + Support-Proximity Pullback | `research only` | 186 | 14.14% | -0.13% | +11.08% | -10.77% | 0.232 |
| Mid-Depth Low-Extension Pullback | `research only` | 583 | 13.60% | -0.67% | +10.23% | -16.83% | 0.148 |
| Shallow Confirmed Reset | `research only` | 2362 | 11.95% | -2.32% | +8.06% | -19.19% | 0.166 |
| Supportive + Confirmed Controlled Pullback | `research only` | 701 | 10.14% | -4.13% | +6.83% | -16.60% | 0.120 |
| Risk-On + Confirmed Controlled Pullback | `research only` | 593 | 8.19% | -6.09% | +5.63% | -15.51% | 0.112 |
| Deeper Controlled Confirmed Pullback | `research only` | 171 | 1.11% | -13.16% | -1.35% | -28.72% | -0.011 |
| Watch-Only Extended Strength | `watch only` | 1045 | N/A | N/A | N/A | N/A | N/A |

`SPY` buy-and-hold annualized return was approximately `14.27%` with max drawdown of `-25.36%`.

## Evidence Ledger

Facts:

- Current v1 had the strongest absolute annualized result at `18.82%` net and exceeded `SPY` buy-and-hold by `+4.54%` annualized.
- Current v1 had weak exposure-aware information quality at `0.041` and nearly matched `SPY` drawdown at `-25.16%`.
- The stricter narrowed variants improved exposure-aware information quality materially, led by `Strict RS + Support-Proximity Pullback` at `0.232`.
- No narrowed live-entry variant beat `SPY` buy-and-hold by the required `+3%` annualized.
- The `6-10%` deeper controlled confirmed variant was weak and had worse drawdown than `SPY`, supporting the doctrine against deeper pullback damage.
- `Watch-Only Extended Strength` produced a positive signal-level `15D` excess return, but it is not a live pullback entry because extension remained above the controlled live-entry band.

Inferences:

- Pullback narrowing improves timing quality relative to exposure-aware `SPY`, but in this replay it gives up too much market participation to justify a new active version.
- The current v1 sleeve is not elegant: it has low information quality and SPY-like drawdown. However, replacing it with a cleaner narrowed rule would currently lower absolute performance below the promotion bar.
- The next research step should focus on portfolio construction and action separation, not deeper dip-buying.

Unknowns:

- Historical point-in-time earnings and revision data remain incomplete.
- The test uses current `S&P 100` membership, so constituent-survivorship risk remains.
- Weekly top-`5` portfolio selection is a practical approximation, not a complete execution simulator.

## Concentration Check

Current v1 was broad:

- Largest sector: `Information Technology`, `22.31%` of signals.
- Largest regime: `Risk-on`, `41.38%` of signals.
- Largest ticker: `AVGO`, `1.81%` of signals.

The strict support-proximity variant was more concentrated but still not ticker-driven:

- Largest sector: `Information Technology`, `44.62%` of signals.
- Largest regime: `Risk-on`, `76.88%` of signals.
- Largest ticker: `AVGO`, `6.99%` of signals.

The stricter variant was close to the sector concentration guardrail and still failed the `SPY` buy-and-hold hurdle, so it should not be promoted.

## Live Versus Watch-Only Rule Separation

Live `Buy on pullback` candidates should remain actual controlled-reset entries, not merely strong stocks that may become attractive later.

Watch-only pullback candidates are different:

- They can be supportive, sector-confirmed leadership names.
- They can have positive RS and strong trend structure.
- But if extension is still above the controlled live-entry band, they should remain `Wait for pullback` or `Do not chase`.

This separation should remain visible in weekly reports and strategy pages.

## Final Rule Decision

No registry update.

No active-version bump.

No weekly manifest rewrite.

Keep:

- `sector-confirmed-pullback-continuation.v1`
- status `core`
- board role: narrowed/trust-calibrated only

Do not promote:

- broad dip-buying
- deep `10-15%` pullbacks
- extended leadership names as live pullback buys
- a strict v2 that looks cleaner but fails the `SPY` buy-and-hold promotion bar

## Next Research Question

Test whether portfolio construction improves v1 without changing the signal definition:

- top `3` versus top `5`
- same-sector cap per weekly board
- exclude deepest `10-15%` pullbacks only as a risk suppressor
- rank live pullbacks by support proximity, sector-relative strength, and ATR burden
- keep `Wait for pullback` candidates out of live trade-return promotion math
