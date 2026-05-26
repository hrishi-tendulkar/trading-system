# S&P 100 Canonical Strategy Replay

## Date

2026-05-25

## Scope

- Universe: `S&P 100 + ETFs`
- Price history: `2021-01-04` through `2026-05-22`
- Data type: daily `OHLCV`
- Benchmark for excess-return math: `SPY`
- Canonical strategies tested separately:
  - `ETF Trend / Rotation`
  - `Sector-Confirmed Pullback Continuation`
  - `Breakout Confirmation`
  - `Selective Mean Reversion`

## Artifacts

- Versioned replay output directory: `data/processed/canonical_strategy_replay_2026-05-25_v1/`
- Core comparison table: `data/processed/canonical_strategy_replay_2026-05-25_v1/canonical_strategy_comparison.csv`
- Full signal log: `data/processed/canonical_strategy_replay_2026-05-25_v1/canonical_strategy_signals.csv`
- Pullback band breakdown: `data/processed/canonical_strategy_replay_2026-05-25_v1/canonical_pullback_band_summary.csv`
- Breakout context breakdown: `data/processed/canonical_strategy_replay_2026-05-25_v1/canonical_breakout_context_summary.csv`
- Mean-reversion regime breakdown: `data/processed/canonical_strategy_replay_2026-05-25_v1/canonical_mean_reversion_regime_summary.csv`

## Overall Comparison

| Strategy | Sample Size | Avg 5D | Avg 10D | Avg 15D | Avg 5D Excess vs SPY | Avg 10D Excess vs SPY | Avg 15D Excess vs SPY | 5D Win Rate | 10D Win Rate | 15D Win Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Breakout Confirmation | 3169 | 0.27% | 0.73% | 1.08% | 0.15% | 0.39% | 0.53% | 52.9% | 55.8% | 56.4% |
| ETF Trend / Rotation | 239 | 0.14% | 0.44% | 0.47% | -0.02% | 0.01% | -0.03% | 56.9% | 56.9% | 58.2% |
| Selective Mean Reversion | 253 | 0.30% | -0.08% | 0.90% | -0.01% | 0.00% | 0.63% | 50.6% | 48.6% | 50.2% |
| Sector-Confirmed Pullback Continuation | 3664 | 0.23% | 0.37% | 0.59% | 0.04% | -0.04% | -0.01% | 53.1% | 52.2% | 52.3% |

## Strategy Readout

### 1. Breakout Confirmation

What looks strong:

- This is the cleanest all-around replay result in the canonical set.
- The test used `true triggered entries only`, not pre-breakout watch names.
- In supportive regimes, the edge improved further.
- `Risk-on + sector confirmed` was especially strong:
  - sample size `1599`
  - average `10D` excess return `+0.66%`
  - average `15D` excess return `+0.96%`
  - `10D` win rate `57.8%`
  - `15D` win rate `57.9%`

What still matters:

- Defensive-regime breakouts were weak.
- Selective-risk-on breakouts with `Unconfirmed` sectors turned negative by `15D`.

Verdict:

- `Promote now`
- Best current use: secondary core single-name sleeve, but keep the doctrine strict:
  - triggered entry only
  - supportive regime preferred
  - sector confirmation still matters

### 2. Sector-Confirmed Pullback Continuation

What looks strong:

- The broad version is not strong enough on its own.
- The better edge lives inside narrower sub-buckets instead of the aggregate.
- `Risk-on + Confirmed` improved materially:
  - sample size `1081`
  - average `10D` excess return `+0.34%`
  - average `15D` excess return `+0.41%`
- Some pullback-depth / extension combinations looked healthy with usable sample:
  - `Confirmed`, `3-6%` pullback depth, `2-4%` extension: sample `206`, `10D` excess `+0.57%`
  - `Confirmed`, `0-3%` pullback depth, `4-6%` extension: sample `273`, `10D` excess `+0.41%`
  - `Confirmed`, `6-10%` pullback depth, `4-6%` extension: sample `56`, `10D` excess `+0.72%`

What still looks weak:

- The aggregate strategy was roughly flat to slightly negative versus `SPY` at `10D` and `15D`.
- `Defensive + Confirmed` was clearly weak.
- `Neutral + Unconfirmed` was poor.
- Deep pullbacks (`10-15%`) were noisy to outright bad.

Verdict:

- `Promote cautiously, but only as a narrowed rule set`
- Keep it in the core research lane, but tighten before treating it as the primary single-name engine:
  - prefer supportive regimes
  - separate `Confirmed` from `Unavailable` sector states
  - avoid deep `10-15%` pullbacks
  - likely focus on mid-depth pullbacks and controlled extension bands

### 3. ETF Trend / Rotation

What looks okay:

- Absolute returns were positive.
- Risk-on `Broad ETF` entries were directionally better:
  - sample size `38`
  - average `10D` excess return `+0.15%`
  - average `15D` excess return `+0.29%`

What still looks weak:

- The overall replay was essentially flat versus `SPY`.
- Risk-on `Sector ETF` entries faded by `10D` and `15D`.
- Selective-risk-on `Sector ETF` entries were also weak on an excess-return basis.

Verdict:

- `Do not fully promote this entry definition yet`
- The idea still makes sense as an exposure sleeve, but the current daily-entry rule is not strong enough as the canonical implementation.
- Best next refinement: test a ranked rotation form instead of a broad daily eligibility form.

### 4. Selective Mean Reversion

What looks interesting:

- The aggregate result was too mixed for promotion.
- The strategy behaved very differently by regime.
- Defensive buckets were the only clearly promising area:
  - `Defensive`, oversold band `-5% to -2%`: sample `94`, `10D` excess `+0.78%`, `15D` excess `+1.81%`
  - `Defensive`, oversold band `-8% to -5%`: sample `48`, `10D` excess `+0.56%`, `15D` excess `+1.03%`

What still looks weak:

- Risk-on mean reversion was bad.
- Sample sizes in the most extreme buckets were too small for promotion confidence.
- Overall win rates were not strong enough for a core sleeve.

Verdict:

- `Research only`
- Keep this as a regime-specific sandbox, not a promoted canonical sleeve.

## Promotion Recommendation

| Strategy | Recommendation | Why |
|---|---|---|
| Breakout Confirmation | `Promote now` | Strongest overall and subgroup evidence; triggered-entry test passed |
| Sector-Confirmed Pullback Continuation | `Promote with tighter filters` | Aggregate replay is weak, but supportive confirmed sub-buckets are usable |
| ETF Trend / Rotation | `Refine before promotion` | Concept is still valid, but the current entry definition is too flat vs `SPY` |
| Selective Mean Reversion | `Keep research only` | Too regime-dependent and not consistent enough in aggregate |

## What Still Needs Refinement

1. `ETF Trend / Rotation`
   Test a ranked weekly `top 1` or `top 2` ETF rotation variant rather than broad daily eligibility.

2. `Sector-Confirmed Pullback Continuation`
   Split `Confirmed`, `Unconfirmed`, and `Unavailable` sector states explicitly in decision logic instead of collapsing them.

3. `Sector-Confirmed Pullback Continuation`
   Convert the stronger bands into explicit candidate production rules and retest them separately.

4. `Breakout Confirmation`
   Add a stricter `relative-strength` tier test inside supportive regimes to see whether the already-strong sleeve can improve further.

5. `Selective Mean Reversion`
   Narrow the sandbox to defensive or neutral stress regimes only and retest with stricter oversold definitions.

6. All strategies
   Historical event-aware filters are still incomplete because the replay remains mostly technical and does not yet have point-in-time earnings, revision, or transcript history.

## Bottom Line

The canonical four-strategy architecture is directionally correct.

But the replay does **not** support promoting all four sleeves equally.

The clearest immediate promotion candidate is `Breakout Confirmation`.
`Sector-Confirmed Pullback Continuation` still deserves a place, but only after tighter band and context control.
`ETF Trend / Rotation` remains plausible as a design direction, yet the current entry definition needs another iteration.
`Selective Mean Reversion` stays in research mode.
