# Strategy Detail Page Content

## Purpose

Define reusable, page-ready content for canonical strategy detail pages.

This document is intended to be shared across:

- product copy
- design annotations
- engineering payload design
- research and finance review

It is written to preserve the finance meaning of each strategy without requiring readers to inspect code.

## Evidence Basis

Primary replay reference:

- `docs/research/market/sp100-canonical-strategy-replay-2026-05-25.md`

Current scope:

- universe: `S&P 100 + ETFs`
- horizon: roughly `1` to `15` trading days
- data base: daily `OHLCV`

Important interpretation rule:

- these pages should not imply equal confidence across all four strategies
- replay evidence currently supports different trust levels by strategy

## Current Trust Calibration

Use this posture unless a later promotion decision explicitly changes it:

| Strategy | Current page posture | Why |
|---|---|---|
| `Breakout Confirmation` | `Core but narrowed / sector-confirmed` | broad baseline is not enough; supportive sector-confirmed breakout cleared the promotion bar |
| `Sector-Confirmed Pullback Continuation` | `Core but narrower / still trust-calibrated` | attractive sub-buckets exist, but broad aggregate replay is weak |
| `ETF Trend / Rotation` | `Research only` | ranked weekly refinement beat exposure-aware `SPY` but still lagged `SPY` buy-and-hold too much for promotion |
| `Selective Mean Reversion` | `Research only` | evidence is too regime-specific and too inconsistent for main-board trust |

## Shared Page Structure

Each strategy page should be able to render these blocks:

1. `What this strategy is for`
2. `When it is useful`
3. `When not to trust it`
4. `What edge it is trying to capture`
5. `What can go wrong`
6. `How this week's recommendation should be read`
7. `Which backtest stats matter most`
8. `What "works best when" means`
9. `Visible rule spine`
10. `Trust-calibration note`

---

## 1. ETF Trend / Rotation

### Status

- page badge: `Research only`
- board role today: exposure appendix and candidate context only, not a promoted entry engine

### Purpose

Use ETF Trend / Rotation to express bullish market or sector exposure when trend conditions are supportive but single-name entries are less trustworthy or more event-sensitive.

### When to use

Use this strategy when:

- the market is `Risk-on` or `Selective risk-on`
- the ETF is above the `20DMA` and `50DMA`
- trend slope is supportive
- relative strength versus the benchmark is positive
- the user wants cleaner group exposure rather than idiosyncratic stock risk

### When not to use

Do not lean on this strategy when:

- the tape is defensive or unstable
- leadership is rotating too fast to trust a simple daily trend rule
- a single-name setup has a clearly stronger and more specific edge
- the ETF is technically eligible but not actually outperforming `SPY` in a durable way

### What edge it is trying to capture

This strategy is trying to capture trend persistence and sector leadership with lower company-specific event risk than a single stock.

### Main risks

- flat excess return versus `SPY` even when absolute returns are positive
- fast factor rotation that makes yesterday's leader stale quickly
- lagging badly after regime shifts
- looking "safe" while still failing to add real relative edge

### Action-label behavior

Underlying action model:

- `BUY_NOW`
- `WAIT_CONFIRMATION`
- `NO_ACTION`

Recommended user-facing wording:

- `Buy now`: "Broad or sector exposure looks actionable now."
- `Wait for confirmation`: "The trend idea is plausible, but not strong enough yet for fresh ETF exposure."
- `No action`: "This ETF does not currently earn capital."

Do not use user-facing pullback language here unless a later ETF-specific pullback rule set is formally added.

### What this week's recommendations mean

If this strategy surfaces on a weekly page today, the interpretation should be narrow:

- this is a cleaner exposure expression than forcing a weaker stock entry
- it does not mean the ETF sleeve is already the strongest proven alpha source in the system
- it means "acceptable exposure vehicle this week," not "high-conviction standalone edge"

### What backtest stats matter most

For this page, emphasize:

- excess return versus `SPY`, not just raw return
- performance split between `Broad ETF` and `Sector ETF`
- supportive-regime performance only
- sample size, because the ETF test is much smaller than the single-name sleeves

Do not over-celebrate win rate alone here. The current issue is not whether ETFs go up sometimes; it is whether this rule set adds enough edge over simply owning the benchmark.

The `2026-06-07` ranked weekly refinement did not solve this. The best tested rule, `Top 2 Sector ETFs / Supportive Strict RS`, returned `5.99%` net annualized after `20 bps` friction and beat exposure-aware `SPY` by `4.13%`, but lagged `SPY` buy-and-hold by `8.28%` annualized.

### What `works best when` means

On this page, `works best when` should mean:

- broad market posture is supportive
- sector or index leadership is already established
- the user wants immediate exposure with cleaner invalidation than a stock
- the engine prefers the ETF because single-name timing is weaker, noisier, or event-suppressed

This section should not imply that all supportive-trend ETF states are equally good. Current replay suggests that ranked sector ETF exposure can beat exposure-aware `SPY`, but not that the sleeve is validated as a standalone promoted board engine.

### Canonical rule details that should be visible without reading code

Show the rule spine in plain language:

- market posture must be supportive
- ETF should be above `20DMA` and `50DMA`
- short-term trend slope should be positive or improving
- relative strength versus `SPY` should be positive
- volatility should remain acceptable
- if a cleaner single-name edge exists, the ETF may not be the preferred expression

### Trust-calibration note

This page needs a stronger caveat than the other core pages. Current replay says the strategy idea still makes sense as an exposure tool, but neither the current daily-entry definition nor the ranked weekly rotation refinement is strong enough to present as fully promoted or equally trusted with breakout setups.

### Conditional page-content note

This page should be conditional on the mainline promotion decision session.

If the session keeps ETF Trend / Rotation as canonical but not promoted:

- keep the badge `Research only`
- keep the copy focused on exposure expression rather than alpha confidence

If the session later promotes a ranked rotation variant:

- rewrite the page around the ranked weekly rotation logic, not the current broad daily eligibility logic

---

## 2. Sector-Confirmed Pullback Continuation

### Status

- page badge: `Core, but narrower`
- board role today: trust-calibrated single-name continuation sleeve, not a broad default buy-the-dip engine

### Purpose

Use Sector-Confirmed Pullback Continuation to capture continuation in strong stocks after a controlled reset, so the system can participate in leadership without chasing an already-extended move.

### When to use

Use this strategy when:

- the stock remains above the `20DMA` and `50DMA`
- the trend structure is still intact
- relative strength versus `SPY` is positive across multiple windows
- relative strength versus the sector ETF is positive
- the sector ETF is supportive, and ideally explicitly confirmed
- the pullback is controlled rather than damaged
- extension has cooled enough to restore acceptable risk geometry

### When not to use

Do not use this strategy when:

- the move lower may actually be early technical breakdown
- the sector state is weak, unconfirmed, or unavailable and being hand-waved away
- the pullback is too deep, especially in the `10-15%` range that looked weak or noisy in replay
- the setup still requires too much forgiveness on risk geometry
- the stock is simply overextended and the page is pretending that "eventually on pullback" is the same as a live buy

### What edge it is trying to capture

This strategy is trying to capture continuation in leadership names with better entry discipline than raw momentum buying.

Important doctrine to keep explicit:

- the edge is not "stocks bounce"
- the edge is "strong stocks in supportive contexts can resume higher after a controlled reset"

### Main risks

- mistaking early breakdown for constructive pullback
- buying names whose sector support is weaker than it looks
- making the strategy too broad and losing the narrower edge that actually tested better
- underestimating how much results degrade outside supportive confirmed sub-buckets

### Action-label behavior

Underlying action model:

- `BUY_PULLBACK`
- `WAIT_CONFIRMATION`
- `DO_NOT_CHASE`
- `NO_ACTION`

Recommended user-facing wording:

- `Buy on pullback`: "The stock is attractive, but the better entry is on a controlled reset into support."
- `Wait for confirmation`: "The continuation thesis may still be valid, but the pullback quality is not clean enough yet."
- `Do not chase`: "The stock may still be strong, but the current price is too extended for a disciplined fresh entry."
- `No action`: "The setup does not currently justify capital."

Avoid translating this strategy into generic `Buy now` copy unless a live pullback zone is already active and the board layer has promoted it as actionable now.

### What this week's recommendations mean

A recommendation from this page should usually mean one of three things:

- the stock is a valid continuation candidate, but patience is part of the edge
- the setup is close, but price still needs to prove that support is holding
- the name is strategically important this week even if the ideal entry has not arrived yet

This page should teach the user that a pullback recommendation is often an entry-discipline instruction, not a weaker version of conviction.

### What backtest stats matter most

For this page, prioritize:

- supportive-regime excess return, not aggregate full-sample averages alone
- sector-confirmed versus unconfirmed splits
- pullback-depth and extension-band breakdowns
- sample size inside the stronger sub-buckets
- deterioration in defensive and weak-sector states

The core page should explicitly mention that the aggregate strategy was roughly flat to slightly negative versus `SPY` at `10D` and `15D`, and that the usable edge currently appears inside narrower confirmed bands.

### What `works best when` means

On this page, `works best when` should mean:

- the market is supportive rather than defensive
- the sector is clearly confirmed, not merely non-negative
- the pullback is mid-depth and controlled rather than deep and damaged
- the stock has real prior leadership and positive multi-window relative strength
- extension has cooled enough that invalidation is clean

This should be framed as a filter summary, not as marketing language.

### Canonical rule details that should be visible without reading code

Show the rule spine in plain language:

- stock should be above `20DMA` and `50DMA`
- `20DMA` and `50DMA` trend structure should remain intact
- relative strength versus `SPY` should be positive across multiple windows
- relative strength versus the sector ETF should be positive
- sector state should be visible as `Confirmed`, `Unconfirmed`, or `Unavailable`
- pullback depth should stay in favored bands rather than deep damage zones
- extension above support should cool enough to make risk geometry acceptable
- deep `10-15%` pullbacks should be treated with skepticism

### Trust-calibration note

This is a core strategy page, but it needs narrower claims than Breakout Confirmation. The replay supports keeping the setup family, yet does not support presenting the broad version as a universally reliable mainline engine.

### 2026-06-07 refinement note

The latest pullback replay tested narrowed v2 candidates by pullback depth, extension band, sector confirmation, regime, RS consistency, ATR burden, support proximity, and watch-only extended-strength separation.

Decision: keep `sector-confirmed-pullback-continuation.v1` active; do not promote a v2 yet.

Evidence to show:

- current v1 had `18.82%` net annualized return and `+4.54%` annualized excess versus `SPY` buy-and-hold, but weak weekly information-like quality of `0.041`
- strict support-proximity improved information-like quality to `0.232` and beat exposure-aware `SPY` by `+11.08%` annualized, but lagged `SPY` buy-and-hold by `-0.13%`
- deeper controlled pullbacks were weak, reinforcing skepticism toward damaged resets
- extended leadership names should remain `Wait for pullback` or `Do not chase`, not live `Buy on pullback`

### Conditional page-content note

The 2026-06-07 promotion decision keeps the page in the second state:

- keep the badge `Core, but narrower`
- keep stronger caveats around aggregate replay weakness
- show the current active version as `sector-confirmed-pullback-continuation.v1`
- separate live `Buy on pullback` rows from watch-only pullback candidates

---

## 3. Breakout Confirmation

### Status

- page badge: `Core but narrowed / sector-confirmed`
- board role today: strongest promoted single-name continuation sleeve, but only through supportive sector-confirmed rules

### Purpose

Use Breakout Confirmation to capture continuation in leadership names that remain technically strong but have not offered a clean pullback entry, so the system can wait for proof through price instead of buying early on hope.

### When to use

Use this strategy when:

- trend structure is intact
- the stock is close to a definable resistance or recent high
- relative strength is acceptable to strong
- the market regime is `Risk-on` or `Selective risk-on`
- the sector context is confirmed
- the system wants proof through price before allocating capital

### When not to use

Do not use this strategy when:

- the market regime is defensive
- sector confirmation is weak or absent
- the page is treating a pre-breakout watch name as if it were already an executed breakout
- the stock is too extended after the trigger and no longer offers clean risk geometry
- the broad breakout baseline is being used without the promoted regime and sector gates

### What edge it is trying to capture

This strategy is trying to capture continuation after price proves that demand is strong enough to clear resistance, rather than assuming the breakout will happen.

### Main risks

- false breakouts that reverse quickly
- crowded entries after obvious levels clear
- reduced edge when regime and sector filters are ignored
- confusion between a watch setup and a live triggered setup

### Action-label behavior

Underlying action model:

- `WAIT_CONFIRMATION`
- `BUY_NOW`
- `NO_ACTION`

Recommended user-facing wording:

- `Wait for confirmation`: "This is a valid breakout watch, but price still needs to clear the trigger."
- `Buy now`: "The breakout confirmation has triggered and is actionable now."
- `No action`: "The stock does not currently justify a breakout entry."

This is the cleanest strategy for mapping a `Wait` state into a later `Buy now` state without changing the underlying thesis.

### What this week's recommendations mean

A weekly recommendation from this page should mean one of two things:

- the stock is one of the best current watch candidates for a defined breakout trigger
- the trigger has already been satisfied and the system believes the confirmation is still early enough to act on

The page should make the distinction visually obvious.

### What backtest stats matter most

For this page, emphasize:

- overall excess return versus `SPY`
- supportive-regime splits
- sector-confirmed splits
- win rate and excess return together, not either alone
- the fact that the replay used `true triggered entries only`

The strongest visible proof point should be the `Risk-on + sector confirmed` subgroup:

- sample `1599`
- average `10D` excess return `+0.66%`
- average `15D` excess return `+0.96%`
- `10D` win rate `57.8%`
- `15D` win rate `57.9%`

The newer promotion proof point is the `Supportive + Sector-Confirmed Breakout` weekly portfolio replay:

- signal sample `1985`
- net annualized return `19.94%`
- annualized excess versus `SPY` buy-and-hold `+5.93%`
- annualized excess versus exposure-aware `SPY` `+18.50%`
- max drawdown `-18.10%`, better than `SPY` buy-and-hold at `-25.36%`

### What `works best when` means

On this page, `works best when` should mean:

- the market regime is supportive
- the sector confirms rather than fights the move
- the breakout is triggered, not merely anticipated
- the stock already showed leadership before the breakout attempt
- price is still close enough to the trigger that risk remains definable

### Canonical rule details that should be visible without reading code

Show the rule spine in plain language:

- trend should already be intact
- a definable resistance or breakout trigger must exist
- the strategy should be tested and interpreted on triggered entries only
- relative strength should be acceptable or strong
- market regime must be `Risk-on` or `Selective risk-on` for board-eligible buys
- sector context must be confirmed for board-eligible buys
- defensive-regime breakouts deserve skepticism
- if the trigger has not fired, the recommendation should remain in a watch state rather than pretending to be live

### Trust-calibration note

This is still the strongest current strategy page, but the live claim is narrower than the broad label. The promoted version is triggered breakout plus supportive regime plus sector confirmation; the broad current breakout rule remains research context only.

### Conditional page-content note

This page is the least dependent on the mainline promotion decision session.

Unless later replay materially changes the evidence, this page can ship as the benchmark example of a promoted decision-basis page only if its copy and board logic preserve the supportive sector-confirmed gates.

---

## 4. Selective Mean Reversion

### Status

- page badge: `Research only`
- board role today: not eligible for main-board fresh-cash promotion by default

### Purpose

Use Selective Mean Reversion to test whether narrowly defined oversold rebound setups can add edge in specific stress regimes without collapsing into undisciplined dip-buying.

### When to use

Use this strategy only when:

- weakness is sharp but not obviously thesis-destroying
- the move is not primarily an event gamble
- oversold conditions are measurable
- the setup is being evaluated inside a narrow regime-specific sandbox

### When not to use

Do not use this strategy when:

- the market is broadly risk-on and continuation setups are working better
- the stock is falling for a fresh event-driven reason
- the page is implying that all selloffs are buying opportunities
- sample sizes are too small to support live confidence

### What edge it is trying to capture

This strategy is trying to capture temporary dislocation and rebound, especially when selling pressure overshoots fair short-term damage.

### Main risks

- catching breakdowns instead of rebounds
- overfitting narrow historical pockets that do not transfer well live
- encouraging indiscriminate dip-buying
- falsely treating regime-specific behavior as a general strategy edge

### Action-label behavior

Underlying action model:

- `NO_ACTION`
- `SUPPRESSED`
- potentially `WAIT_CONFIRMATION` in a future refined research variant, but not as live default

Recommended user-facing wording:

- `Research watch only`: "This setup is being tracked for evidence, not promoted as a standard fresh entry."
- `No action`: "The rebound case is not strong enough to deserve capital."
- `Suppressed`: "Even if the setup is interesting, a risk rule blocks fresh action."

Avoid live-ready wording like `Buy now` or `Buy on pullback` on the main page while this remains research only.

### What this week's recommendations mean

If this strategy appears anywhere user-facing, it should usually mean:

- the setup is worth monitoring as a research case
- the engine sees a potential oversold rebound pattern
- the system is not yet asking the user to treat it like a core fresh-cash action

This content belongs more naturally in a research appendix or focus queue than the main action board.

### What backtest stats matter most

For this page, emphasize:

- regime breakdowns first, aggregate summary second
- whether defensive buckets show repeatable excess return
- sample size inside the promising oversold bands
- how weak the risk-on results were
- the inconsistency of aggregate win rates

The key evidence to show is that only certain defensive oversold buckets looked promising, while the broad strategy did not justify promotion.

### What `works best when` means

On this page, `works best when` should mean:

- the market is defensive or stressed rather than trending cleanly higher
- the oversold condition falls inside the narrower promising bands
- the setup is not being driven by an imminent earnings or thesis-break event
- the page is being read as a research result, not as standard live trade guidance

### Canonical rule details that should be visible without reading code

Show the rule spine in plain language:

- oversold state should be measurable rather than discretionary
- regime should be visible and matter explicitly
- event-driven collapses should not be treated as routine rebound candidates
- the system should distinguish research-watch output from promoted action-board output
- risk suppressors should remain visible when they block otherwise interesting cases

### Trust-calibration note

This page should carry the strongest caution label. It is useful as a research sleeve because it may uncover regime-specific edge, but current evidence does not justify presenting it as a trusted fresh-cash strategy.

### 2026-06-07 refinement note

The latest Selective Mean Reversion replay tested defensive and stress-regime-only variants with daily `OHLCV`, `20 bps` friction, `5D` / `10D` / `15D` holding windows, `SPY` buy-and-hold, and exposure-aware `SPY`.

Best result:

- `stress_v1`, `15D` hold
- `7.05%` net annualized return
- `+6.10%` annualized excess versus exposure-aware `SPY`
- `-7.22%` annualized excess versus `SPY` buy-and-hold
- `43.04%` largest-year signal share

Decision: keep `selective-mean-reversion.v1` `Research only`; do not promote to sandbox, paper-live, or main-board fresh-cash eligibility.

### Conditional page-content note

This page is only lightly dependent on the mainline promotion decision session.

Unless materially stronger replay evidence appears, it should remain `Research only` and stay off the main board.

---

## Cross-Strategy Action Interpretation Notes

Use the persisted action vocabulary underneath the product, but present the meaning in natural language:

| Persisted action | Recommended user-facing interpretation |
|---|---|
| `BUY_NOW` | Actionable now |
| `BUY_PULLBACK` | Attractive, but better on a controlled reset |
| `WAIT_CONFIRMATION` | Valid watch, but still needs price proof |
| `DO_NOT_CHASE` | Strong idea, poor current entry |
| `NO_ACTION` | Does not currently deserve capital |
| `SUPPRESSED` | Setup may exist, but a risk rule overrides fresh action |

Important product rule:

- the same underlying action should not sound equally forceful on every page
- wording should reflect both live setup quality and historical evidence quality

## Recommendation For Shipping Order

If only one page is used as the canonical first decision-basis page, it should be:

1. `Breakout Confirmation`

If a second page is shipped immediately after:

2. `Sector-Confirmed Pullback Continuation`, but only with narrowed and caveated copy

Pages that should wait for either stronger evidence or a promotion decision:

3. `ETF Trend / Rotation`
4. `Selective Mean Reversion`
