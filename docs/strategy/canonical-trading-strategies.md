# Canonical Trading Strategies

## Purpose

Define the canonical short-term trading strategy set for Trading System.

This document is the single source of truth for:

- current core trading strategies,
- their logic and intended use,
- how they differ from risk rules and context lenses,
- how they should be tested,
- how strategy history should be recorded as the system evolves,
- and where weekly board assembly rules are defined.

If a future document discusses adding, removing, or changing a trading strategy, it should either:

- update this document directly, or
- clearly reference the change here.

Weekly board assembly logic now lives in:

- `docs/strategy/weekly-board-assembly-spec.md`

## Scope

This document is about short-term, long-biased trading strategies for roughly `1` to `15` trading days using daily data.

It does not define:

- long-term conviction frameworks,
- position sizing,
- portfolio allocation,
- or options overlays as standalone alpha systems.

## Core conclusion

Trading System should not use one monolithic stock-ranking strategy.

It should operate as a small `strategy lab` with a few explicit `setup families`, each tested separately and only blended later at the weekly-board layer.

The current best working assumption is:

- `Breakout confirmation` is the strongest currently promoted single-name continuation sleeve
- `Sector-confirmed pullback continuation` belongs in the mainline only as a narrowed, trust-calibrated sleeve
- `ETF trend / rotation` remains canonical, but its current tested daily-entry rule should be refined before mainline promotion
- `Selective mean reversion` remains a research sleeve only until proven clearly additive

## Terminology

### Trade setup

A repeatable tactical pattern with:

- entry logic,
- invalidation logic,
- expected holding style,
- and a replay path.

### Risk rule

A rule that suppresses or modifies action even when a chart looks acceptable.

Example:

- `Event freeze before earnings`

### Context lens

A framing aid that helps interpret setup quality but is not itself the stock-picking edge.

Example:

- `Benchmark trend reference`

## Current canonical strategy set

### Strategy 1: ETF Trend / Rotation

Status:

- `Refine before promotion`

Type:

- `Trade setup`

Purpose:

- provide cleaner exposure when market or sector trends are attractive but single-name entries are less trustworthy

Typical vehicle:

- `SPY`, `QQQ`, sector ETFs such as `XLK`, `XLF`, `XLV`, `XLE`, `XLI`, `XLY`

Use when:

- regime is `Risk-on` or `Selective risk-on`
- ETF is above `20DMA` and `50DMA`
- relative strength vs benchmark is positive
- short-term trend slope is supportive
- volatility is acceptable

What it is really expressing:

- broad trend persistence
- sector leadership
- lower idiosyncratic event risk than single-name exposure

Why it belongs:

- the system still needs a cleaner exposure sleeve for weeks when market or sector trend is attractive but single-name timing is weaker

Current live posture:

- canonical strategy, but not currently feeding the main action board
- the present replayed daily-entry definition is too flat versus `SPY` to earn mainline promotion
- ranked weekly ETF rotation was retested on `2026-06-07` and also remains research-only:
  the best sector top `2` strict-RS version beat exposure-aware `SPY`, but missed
  `SPY` buy-and-hold by `8.28%` annualized after `20 bps` friction

Main risks:

- fast factor rotation
- leadership reversal
- lagging after a sharp regime shift

Primary action labels:

- `Wait for confirmation`
- `No action`

### Strategy 2: Sector-Confirmed Pullback Continuation

Status:

- `Core but narrowed / trust-calibrated`

Type:

- `Trade setup`

Purpose:

- capture continuation in strong stocks after a controlled reset instead of chasing raw strength

Use when:

- stock is above `20DMA` and `50DMA`
- trend structure is intact
- relative strength vs `SPY` is positive across multiple windows
- relative strength vs sector ETF is positive
- sector ETF is itself supportive
- pullback is controlled rather than damaged
- extension has cooled enough to restore acceptable risk geometry

What it is really expressing:

- continuation with better entry discipline

Important doctrine:

- `Pullback` is an entry method for continuation, not an independent edge

Why it belongs:

- controlled pullbacks in confirmed leadership names remain a valid continuation idea
- narrower supportive-regime and confirmed-sector sub-buckets are good enough to keep in the mainline

Current live posture:

- mainline-eligible only through a narrowed ruleset
- the broad aggregate version is not strong enough to be treated as the default single-name engine

Main risks:

- “pullback” may actually be early breakdown
- deep corrections can trap trend followers
- overly tight pullback definitions can make the strategy too sparse

Primary action labels:

- `Buy on pullback`
- `No action`

### Strategy 3: Breakout Confirmation

Status:

- `Core but narrowed / sector-confirmed`

Type:

- `Trade setup`

Purpose:

- capture continuation in leadership names that do not offer a clean pullback entry

Use when:

- trend is intact
- stock is close to a definable resistance or recent high
- relative strength is acceptable or strong
- market regime is `Risk-on` or `Selective risk-on`
- sector context is confirmed
- the system prefers proof through price rather than anticipatory buying

What it is really expressing:

- continuation with confirmation

Why it belongs:

- some leaders never reset enough to become attractive pullback entries
- current replay shows the supportive, sector-confirmed version is the strongest promoted continuation sleeve in the canonical set

Important doctrine:

- this strategy should be tested on `triggered entries`, not by treating every pre-breakout watchlist name as an immediate trade
- `Buy now` is earned only after the breakout trigger is live in a supportive regime with confirmed sector context
- the broad current breakout baseline remains research context, not sufficient board-promotion logic

Main risks:

- false breakouts
- crowded late entries
- weak performance if used without regime and relative-strength filters
- weak performance if sector confirmation is ignored

Primary action labels:

- `Buy now` for supportive, sector-confirmed triggered entries
- `Wait for confirmation`
- `No action`

### Strategy 4: Selective Mean Reversion

Status:

- `Research only`

Type:

- `Trade setup`

Purpose:

- test whether narrowly defined oversold rebound setups add edge outside continuation frameworks

Use only when:

- the move is non-event-based
- weakness is sharp but not structurally broken beyond repair
- oversold conditions are measurable
- the setup is defined tightly enough to avoid blanket dip-buying

What it is really expressing:

- temporary dislocation and rebound

Why it is not core yet:

- the evidence base is weaker for liquid large-cap long-only short-term use
- it is easier to overfit than continuation setups

Main risks:

- catching breakdowns instead of rebounds
- falsely assuming every selloff is temporary
- producing noisy backtests with weak live transferability

Primary action labels:

- `No action` by default unless the research sleeve proves itself

## Non-strategy components that still matter

These are important, but they are not core trading strategies.

### Risk rules

- `Event freeze before earnings`
- future event-risk suppressors

### Context lenses

- `Benchmark trend reference`
- regime posture
- sector posture

## How the engine should work

The engine should evaluate names in this order:

1. `Universe filter`
2. `Regime gate`
3. `Risk-rule suppression`
4. `Strategy-family eligibility`
5. `Entry-quality and invalidation test`
6. `Backtest-aware ranking inside each strategy`
7. `Weekly board assembly`

The weekly board should be built from strategy winners, not from one blended score that hides where the edge came from.

Detailed board assembly rules, source-strategy handling, and cross-strategy ranking logic are defined in:

- `docs/strategy/weekly-board-assembly-spec.md`

## How strategies should be tested

Each strategy should be tested separately before being blended.

For each strategy, track at minimum:

- `5D`, `10D`, `15D` forward return
- excess return vs `SPY`
- win rate
- sample size
- behavior by regime
- behavior by sector
- action-bucket quality

### Minimum testing doctrine

#### ETF Trend / Rotation

Test on:

- ETFs only
- supportive vs unsupportive regimes
- broad benchmark vs sector ETFs

#### Sector-Confirmed Pullback Continuation

Test on:

- single names only
- pullback-depth bands
- extension bands
- sector-confirmation on vs off

#### Breakout Confirmation

Test on:

- triggered breakout entries only
- not merely names that were near resistance

#### Selective Mean Reversion

Test on:

- a narrow sandbox
- only if definition is explicit enough to survive red-team scrutiny

## Current operating thesis

As of `2026-06-07`, the best working thesis is:

1. `Breakout Confirmation` should remain promoted only as the supportive, sector-confirmed triggered-breakout sleeve.
2. `Sector-Confirmed Pullback Continuation` should remain active as `sector-confirmed-pullback-continuation.v1`; the 2026-06-07 narrowed-v2 replay improved exposure-aware quality but failed the `SPY` buy-and-hold promotion hurdle.
3. `ETF Trend / Rotation` should remain canonical and research-only; both the prior daily-entry definition and the ranked weekly rotation refinement failed the `SPY` buy-and-hold promotion bar.
4. `Selective Mean Reversion` should remain exploratory; the 2026-06-07 refinement did not justify sandbox, paper-live, or main-board promotion.

## Strategy history log

Use this section to preserve changes over time.

### 2026-05-25

- Established the canonical four-strategy architecture.
- Rejected a single monolithic stock-ranking model as the primary design.
- Adopted a `setup-first strategy lab` posture:
  - separate strategies,
  - separate replays,
  - blend later only after edge is earned.
- Completed the first canonical strategy-separated replay across `S&P 100 + ETFs`.
- Promoted `Breakout Confirmation` to the strongest current mainline sleeve.
- Kept `Sector-Confirmed Pullback Continuation` in the mainline only as a narrowed, trust-calibrated sleeve.
- Kept `ETF Trend / Rotation` canonical, but out of mainline action-board promotion until a stronger ranked rotation variant is tested.
- Kept `Selective Mean Reversion` as research only.

### 2026-06-02

- Refined `Strategy 1 / Breakout Confirmation` with a weekly portfolio replay and exposure-aware `SPY` benchmark.
- Promoted only `Supportive + Sector-Confirmed Breakout`:
  - `19.94%` net annualized return,
  - `+5.93%` annualized excess versus `SPY` buy-and-hold,
  - `+18.50%` annualized excess versus exposure-aware `SPY`,
  - `-18.10%` max drawdown versus `SPY` buy-and-hold at `-25.36%`.
- Demoted the broad current breakout baseline to research context because it missed the `SPY` buy-and-hold hurdle and had worse drawdown.
- Rejected stricter leadership and entry-quality variants for promotion because they reduced risk-adjusted performance instead of improving the sleeve.

### 2026-06-07

- Refined `Sector-Confirmed Pullback Continuation` for a possible v2 using daily `OHLCV`, `20 bps` friction, weekly top-`5` live pullback portfolios, `SPY` buy-and-hold, and exposure-aware `SPY`.
- Tested explicit narrowed variants by pullback depth, extension band, sector confirmation, regime, RS consistency, ATR burden, support proximity, and watch-only extended-strength separation.
- Kept `sector-confirmed-pullback-continuation.v1` active with no registry bump:
  - current v1 net annualized return was `18.82%`,
  - annualized excess versus `SPY` buy-and-hold was `+4.54%`,
  - annualized excess versus exposure-aware `SPY` was `+3.30%`,
  - max drawdown was `-25.16%` versus `SPY` at `-25.36%`,
  - weekly information-like quality was weak at `0.041`.
- Rejected narrowed v2 promotion because cleaner variants improved exposure-aware information quality but failed the `SPY` buy-and-hold hurdle:
  - `Strict RS + Support-Proximity Pullback` information-like quality was `0.232`,
  - annualized excess versus exposure-aware `SPY` was `+11.08%`,
  - annualized excess versus `SPY` buy-and-hold was `-0.13%`.
- Conclusion: keep pullback continuation as a trust-calibrated sleeve, not broad dip-buying; extended strength remains `Wait for pullback`, not a live pullback buy.

### 2026-06-07

- Refined `ETF Trend / Rotation` as a ranked weekly ETF-only rotation sleeve.
- Tested top `1` and top `2` selection, broad ETF versus sector ETF treatment, supportive and risk-on regime gates, strict relative-strength filters, volatility caps, and `10/20/40 bps` friction sensitivity.
- Kept the sleeve research-only:
  - best `20 bps` variant was `Top 2 Sector ETFs / Supportive Strict RS`,
  - net annualized return was `5.99%`,
  - annualized excess versus exposure-aware `SPY` was `+4.13%`,
  - annualized excess versus `SPY` buy-and-hold was `-8.28%`,
  - max drawdown was `-16.20%` versus `SPY` at `-25.36%`.
- Conclusion: ETF rotation may remain useful as an exposure appendix or single-name substitute context, but it should not feed the main board as promoted `Buy now` logic.

### 2026-06-07

- Refined `Selective Mean Reversion` across defensive and stress-regime rebound variants using daily `OHLCV` only, `20 bps` friction, weekly top-`5` portfolios, `5D` / `10D` / `15D` holding windows, `SPY` buy-and-hold, and exposure-aware `SPY`.
- Rejected all tested variants for sandbox, paper-live, and main-board promotion:
  - best variant was `stress_v1` with a `15D` hold,
  - net annualized return was `7.05%`,
  - annualized excess versus exposure-aware `SPY` was `+6.10%`,
  - annualized excess versus `SPY` buy-and-hold was `-7.22%`,
  - largest year share was `43.04%`.
- Kept `selective-mean-reversion.v1` as `research` and excluded from fresh-capital board slots.

### Prior working ideas now reframed

- `Constructive pullback continuation` remains canonical, but is now explicitly framed as `Sector-Confirmed Pullback Continuation`; the 2026-06-07 v2 refinement did not beat the active v1 plus `SPY` buy-and-hold promotion bar, so it should stay trust-calibrated rather than upgraded.
- `ETF rotation` remains canonical, but neither the current daily-entry rule nor the ranked weekly rotation refinement is strong enough for mainline promotion.
- `Breakout confirmation` remains core and has now earned promotion through triggered-entry testing in supportive regimes.
- `Mean reversion` remains possible as a research appendix, but the 2026-06-07 defensive/stress replay did not justify sandbox, paper-live, or core promotion.

## Rule for future updates

Any future strategy change should answer:

1. Is this a new `trade setup`, a `risk rule`, or a `context lens`?
2. What exact edge is it claiming to capture?
3. How will it be tested separately?
4. Why does it deserve promotion into the canonical set?
5. What prior strategy state does it replace, refine, or retire?
