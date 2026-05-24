# Strategy Iteration Findings

## Date

2026-05-23

## Objective

Push past the original tiny MLP and run several higher-leverage iterations over a broader liquid-stock universe with longer history.

## Data scope used

- Universe: current `S&P 100` constituents from Wikipedia plus benchmark and sector ETFs
- Total watchlist rows: `109`
- Price history: roughly `2021-01-01` through `2026-05-23`
- Data type: daily OHLCV only
- Event data: lightweight current earnings snapshot only

## Artifacts

- Watchlist: `data/reference/sp100_watchlist.csv`
- Raw prices: `data/raw/sp100_5y/mlp_prices.csv`
- Baseline outputs: `data/processed/sp100_5y_baseline/`
- Iteration outputs: `data/processed/strategy_iterations_sp100_5y/`

## Iterations run

### 1. Baseline

Current strategy logic from `run_watchlist_analysis.py`.

### 2. Strict relative strength and entry control

Tighter `Buy now` qualification:

- stronger multi-window relative strength
- positive short-term momentum
- tighter extension range
- volatility cap

### 3. Regime-gated version

Adds a market posture filter before allowing fresh long entries:

- `SPY` above `20DMA` and `50DMA`
- `QQQ` above `20DMA` and `50DMA`
- positive short-term slope on `QQQ` `20DMA`

### 4. Reward-to-risk selective

Adds:

- regime gating
- tighter extension cap
- explicit reward-to-risk minimum

### 5. Pullback-only experiment

Tests whether an even narrower pullback-only posture improves results.

## Top portfolio results

### Top 2 actionable names each Friday

| Variant | Observations | Avg 1W | Avg 2W | Avg 3W |
|---|---:|---:|---:|---:|
| Regime-gated | 131 | 0.41% | 0.73% | 0.72% |
| Reward-to-risk selective | 129 | 0.32% | 0.58% | 0.63% |
| Strict RS entry | 259 | 0.14% | 0.26% | 0.31% |
| Baseline | 261 | 0.12% | 0.15% | 0.27% |

### Top 5 actionable names each Friday

| Variant | Observations | Avg 1W | Avg 2W | Avg 3W |
|---|---:|---:|---:|---:|
| Regime-gated | 131 | 0.48% | 0.86% | 0.96% |
| Reward-to-risk selective | 129 | 0.35% | 0.71% | 1.14% |
| Strict RS entry | 259 | 0.16% | 0.28% | 0.35% |
| Baseline | 261 | 0.13% | 0.30% | 0.39% |

## Most important findings

### 1. Broader replay improved the honesty of the project

The bigger universe made it much easier to see what is real and what is story.

The original tiny MLP did not give enough evidence to judge whether the strategy labels actually earned their confidence.

### 2. Baseline logic is too loose

In the broad replay, baseline `Buy now` signals were weak:

- average `1W` return around `0.19%`
- worse than baseline `Buy on pullback`
- worse than several more selective variants

This means the current engine is still too willing to call something actionable.

### 3. Regime gating was the highest-leverage improvement

The regime-gated variant produced the best portfolio-level results in this fast iteration loop.

Interpretation:

- the market filter is helping reduce low-quality long entries
- the system benefits from being more selective when the tape is mixed

### 4. Reward-to-risk filters helped, but less than regime gating

Adding explicit risk geometry discipline improved portfolio results versus baseline, but did not beat the simpler regime-gated version on `1W` or `2W`.

Interpretation:

- reward-to-risk matters
- but broad market posture appears to be the larger first-order filter

### 5. Pullback-only is directionally interesting but currently too sparse

The narrow pullback-only test was too selective to be operationally useful in its current form.

Interpretation:

- the idea may still be valuable
- but the rule window is too tight as currently defined

## What appears directionally true now

- More selectivity is helping.
- Regime awareness matters.
- Broad daily-data long signals should be harder to earn.
- The system should not hand out `Buy now` easily.
- A top `3-5` board in a broad universe is more useful than trying to make many names look equally actionable.

## What is still not proven

- That the current `Buy now` label is strong enough for live trust.
- That event-aware logic has meaningful historical edge with current data coverage.
- That the best action taxonomy is final.
- That the current setup families are optimally split.

## Recommended next finance move

Adopt this near-term stance:

1. Keep the broad universe replay base.
2. Promote regime gating into the main short-term logic.
3. Tighten `Buy now` eligibility further.
4. Treat `Buy on pullback` and `Wait for confirmation` as first-class outputs rather than weaker leftovers.
5. Build the next weekly review around the best `3-5` names, not around filling a larger board.

## Recommended next engineering move

Implement next:

- persistent `5D`, `10D`, and `15D` forward return evaluation
- regime-tagged replay outputs
- variant comparison harness as a reusable script
- easier expansion from `S&P 100` to curated `50-70` active names

## Bottom line

The project is moving in the right direction.

But the evidence now says something important:

the product shell is ahead of the trading edge.

That is good news if we respond correctly. It means the next frontier is now clear:

make the engine more selective, regime-aware, and trust-calibrated before treating it as live-ready.
