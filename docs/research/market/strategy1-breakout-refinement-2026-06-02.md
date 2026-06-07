# Strategy 1 Breakout Refinement

## Date

2026-06-02

## Decision

`Strategy 1 / Breakout Confirmation` should remain promoted only as a narrowed rule set:

- `Supportive + Sector-Confirmed Breakout`

The broad current breakout baseline should remain useful research context, but it should not be treated as sufficient by itself for board-eligible `Buy now` calls.

## Scope

- Universe: `S&P 100 + ETFs`
- Price history: `2021-01-04` through `2026-05-22`
- Data type: daily `OHLCV`
- Cadence model: weekly review
- Portfolio model: top `5` breakout candidates per active review week
- Holding model: `15` trading days represented as a rolling `3`-week tranche
- Friction: `20 bps` round trip per trade
- Benchmark:
  - `SPY` buy-and-hold over the replay period
  - exposure-aware `SPY` over the same signal windows

## Artifacts

- Script: `scripts/mlp/run_breakout_strategy1_refinement.py`
- Output directory: `data/processed/strategy1_breakout_refinement_2026-06-02_strategy1_v2/`
- Promotion table: `strategy1_promotion_decisions.csv`
- Portfolio table: `strategy1_portfolio_summary.csv`
- Signal table: `strategy1_signal_summary.csv`
- Regime, sector, and ticker checks:
  - `strategy1_regime_summary.csv`
  - `strategy1_sector_summary.csv`
  - `strategy1_ticker_summary.csv`

## Variant Results

| Variant | Decision | Signal Sample | Net Ann. Return | Ann. Excess vs SPY Buy-Hold | Ann. Excess vs Exposure-Aware SPY | Max Drawdown | Weekly Information-Like |
|---|---:|---:|---:|---:|---:|---:|---:|
| Supportive + Sector-Confirmed Breakout | `promotable` | 1985 | 19.94% | +5.93% | +18.50% | -18.10% | 0.258 |
| Risk-on + Sector-Confirmed Breakout | `research only` | 1704 | 18.16% | +4.15% | +16.66% | -17.00% | 0.259 |
| Current Breakout Confirmation | `research only` | 3169 | 9.83% | -4.18% | +3.64% | -33.49% | 0.044 |
| Leadership-Quality Breakout | `research only` | 981 | 3.44% | -10.57% | +1.04% | -13.25% | 0.028 |
| Strict Entry-Quality Breakout | `research only` | 405 | -0.37% | -14.38% | -3.42% | -22.66% | -0.080 |

`SPY` buy-and-hold annualized return was `14.01%` with max drawdown of `-25.36%`.

## Why The Winning Variant Clears The Bar

Facts:

- The winning variant beat `SPY` buy-and-hold by `+5.93%` annualized after conservative friction.
- It beat exposure-aware `SPY` by `+18.50%` annualized.
- Its max drawdown was `-18.10%`, better than `SPY` buy-and-hold at `-25.36%`.
- It had `1985` signal observations and `856` weekly portfolio trades.
- Signal-level `15D` excess return was `+0.92%` with a `58.1%` `15D` win rate.

Inference:

- Strategy 1's edge is not the broad idea that any triggered breakout is enough.
- The validated edge is narrower: triggered breakout plus supportive market regime plus sector confirmation.
- Adding stricter relative-strength and entry-quality filters reduced or damaged the edge, likely because they selected later, more crowded breakouts.

Unknowns:

- Historical point-in-time earnings and revision data are still incomplete.
- The test is based on current `S&P 100` constituents, so constituent-survivorship risk remains.
- The weekly portfolio model is a realistic approximation, not a full execution simulation.

## Concentration Check

The promotable variant was not driven by one ticker, but it did lean into leadership-heavy sectors:

- Largest sector: `Information Technology`, `33.9%` of signals.
- Next largest sectors:
  - `Financials`, `21.7%`
  - `Industrials`, `18.0%`
  - `Health Care`, `13.5%`
- Largest ticker: `NVDA`, `57` signals, or about `2.9%` of the sample.

The sector mix is acceptable for a breakout strategy, but live board construction should still cap same-theme exposure.

## Final Rule Set

Promoted `Strategy 1` rule:

1. Single-name only; exclude ETFs from this sleeve.
2. Fresh triggered entry only: close must be above the prior `20` trading-day high.
3. Trend must be intact: close above `20DMA`, and `20DMA` above `50DMA`.
4. Relative strength must be positive versus `SPY` over both `20D` and `60D`.
5. ATR percent must be at or below `6%`.
6. Price must be within `15%` of its `52-week` high.
7. Market regime must be `Risk-on` or `Selective risk-on`.
8. Sector must be confirmed: sector ETF above both `20DMA` and `50DMA`.
9. Pre-breakout watch names stay `Wait for confirmation`; they do not become live `Buy now` calls.

## Tradeoffs

- This is less available than the broad baseline, active in about `68.9%` of review weeks.
- It gives up some broad signal count to avoid defensive and unconfirmed-sector breakouts.
- Risk-on-only looked strong, but it concentrates entirely in one regime and is therefore too narrow for promotion under the current doctrine.
- Stricter leadership filters looked sensible in theory but underperformed, so they should stay research-only.

## Next Research Question

Test whether board construction can improve Strategy 1 without changing the signal definition:

- cap same-sector exposure per review week,
- compare top `3` versus top `5`,
- and test whether ranking by fresh trigger proximity, sector-relative strength, or ATR burden improves the exposure-aware benchmark.
