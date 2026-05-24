# Short-Term Equity And ETF Strategies Research

## Date

2026-05-23

## Objective

Research what short-term traders with a roughly `1-2 week` holding horizon actually do in `equities` and `ETFs`, and separate:

- practitioner playbooks,
- documented research support,
- weakly supported folklore,
- and ideas that look strong enough to later encode into Trading System signals and backtests.

The requested scope excludes `earnings trades` and other discrete `event-driven` setups. A narrow section on `covered calls` is included as an overlay, not as a primary alpha source.

## Core question

What non-event-based short-term trading approaches in equities and ETFs appear both:

1. common in real practitioner behavior, and
2. supported enough by research or transparent practitioner testing to deserve consideration in this repo?

## Scope

Included:

- U.S. equities
- U.S.-listed ETFs
- Holding periods from roughly `1` to `10` trading days and up to `2` weeks
- Long-biased tactical strategies
- Covered calls only as a subordinate overlay

Excluded:

- Earnings trades
- Discrete news and catalyst trades
- Intraday-only setups
- Pure options income systems
- Portfolio allocation recommendations

## Method

The research used three evidence tiers:

1. `Academic / formal research`
   Papers from journals, NBER, SSRN, and institutionally credible research outlets.

2. `Transparent practitioner research`
   Quant and systematic investing research from firms or blogs that explain the mechanics clearly enough to assess whether the claimed edge is testable.

3. `Practitioner playbooks`
   Trading education and discretionary setup writeups used only to understand what traders do in practice, not to establish proof of edge.

The working standard was:

- `Observed`: directly supported by cited source
- `Derived`: inference made by combining multiple sources
- `Unknown`: plausible but not adequately documented

## Key conclusion

The best-supported non-event short-term strategies in equities and ETFs are not a large set of independent edges. Most practical setups reduce to a few repeatable families:

1. `Continuation / momentum`
2. `Pullback within trend`
3. `Breakout / range expansion`
4. `Sector or industry leadership and ETF rotation`
5. `Selective short-term mean reversion`

The most important overall finding is that many named chart setups only become credible when reframed as expressions of a more basic edge:

- continuation in strong names,
- trend-aligned entry timing,
- leadership persistence,
- or liquidity-driven overshoot and reversion.

In other words, the highest-confidence view is not that there are many unrelated 1-2 week edges. It is that short-term traders mostly try to `join existing strength more intelligently` or `fade temporary dislocations selectively`.

## Executive summary

### What short-term traders appear to do

Observed from practitioner material:

- buy stocks and ETFs already showing `relative strength`
- prefer entries near highs, on breakout, or after controlled pullback
- rotate toward `strong sectors` and away from weak ones
- use ETFs for cleaner expression of sector or broad-trend views
- attempt mean reversion only after sharp non-event weakness, washed-out conditions, or liquidity-driven overshoot

### What the research most strongly supports

- `Momentum / continuation` has the strongest evidence base.
- `Industry and sector leadership` are important and explain part of individual-stock momentum.
- `Nearness to the 52-week high` is a particularly useful continuation lens.
- `Time-series momentum / trend following` is more robust at the asset or basket level than as a naive stock-by-stock chart heuristic.
- `Short-term reversal` exists, but the cleanest evidence is conditional and often stronger in less liquid or stressed segments.

### What is weaker than traders often assume

- Standalone chart-pattern claims without broader context
- Generic "breakout works" statements with no regime filter
- Blind mean reversion in liquid large-cap names
- Covered calls as a primary short-term edge for a `1-2 week` directional trader

## Strategy taxonomy

| Strategy family | What traders do | Evidence strength | Best fit | Main warning |
|---|---|---|---|---|
| Relative-strength continuation | Buy recent leaders, often near highs | High | Strong tape, strong sectors | Momentum crashes and crowding |
| Pullback within trend | Buy controlled weakness in strong names | Medium | Selective risk-on regimes | Often just an entry tactic, not a standalone edge |
| Breakout / expansion | Buy range resolution and strength confirmation | Medium | Leadership names leaving consolidation | Weak without RS and regime context |
| Industry / sector leadership | Favor strong industries or rotate via ETFs | High | ETF rotation and stock filtering | Can lag sharply during rotations |
| Short-term mean reversion | Buy stretched weakness for bounce | Medium-Low | Stress, panic, oversold or illiquid dislocations | Weak as a blanket strategy in liquid large caps |
| Covered calls overlay | Sell short-dated calls against owned stock/ETF | Low as core trading strategy | Mildly bullish or neutral hold | Caps upside over the exact horizon trader is targeting |

## Detailed findings by strategy

## 1. Relative-strength continuation

### What traders do

Short-term traders often begin with names already outperforming:

- the broad market,
- the relevant sector,
- and their own recent range.

They usually look for:

- price near recent highs,
- strong moving-average structure,
- constructive pullbacks rather than breakdowns,
- and some confirmation that leadership is not just a one-day spike.

### Research support

This is the strongest strategy family in the study set.

- `Chan, Jegadeesh, and Lakonishok` document that momentum strategies earn profits and find little evidence that intermediate-horizon winners quickly reverse. Source: [NBER - Momentum Strategies](https://www.nber.org/papers/w5375)
- `George and Hwang` show that `nearness to the 52-week high` explains a large part of momentum profits and improves on simple past-return signals. Source: [SSRN - The 52-Week High and Momentum Investing](https://ssrn.com/abstract=1104491)
- `D'Souza, Jacob, and others` find evidence of `time-series momentum` in individual stocks, showing own-past-return persistence can matter even after accounting for known factors. Source: [SSRN - The Enduring Effect of Time-Series Momentum on Stock Returns](https://ssrn.com/abstract=2720600)
- `Zakamulin and Giner` argue there is compelling evidence of short-term momentum in the U.S. stock market index context. Source: [SSRN - Time Series Momentum in the US Stock Market](https://ssrn.com/abstract=3585714)

### Interpretation

Derived:

- For a `1-2 week` horizon, the cleanest long setup is often not "cheap" or "oversold."
- It is a `leader` that has already demonstrated demand and is still behaving constructively.
- Near-high status is not merely cosmetic. It appears to capture useful persistence.

### Regime fit

Best in:

- `Risk-on`
- `Selective risk-on`
- strong sector rotation with broad participation

More fragile in:

- sharp factor rotations
- rebound crashes where previous losers rip higher
- regime transitions after crowded leadership breaks

### Confidence

`High`

## 2. Pullback within trend

### What traders do

This is one of the most common practical tactics in swing trading. Traders identify a strong stock or ETF and wait for:

- a pullback toward a short moving average,
- a retest of breakout support,
- a brief oversold reading inside an intact uptrend,
- or a low-volume pause after expansion.

Practitioner examples describe buying pullbacks into support, especially in leaders and uptrends. Source: [New Trader U - Pullback Trading Strategies](https://www.newtraderu.com/2020/11/04/pullback-trading-strategies/) and [New Trader U - Trend Trading 101](https://www.newtraderu.com/2017/09/28/trend-trading-101/)

### Research support

Direct academic support for "pullback" as a named edge is weaker than for momentum itself.

What is better supported is the underlying structure:

- momentum persists,
- leaders continue to lead,
- and better entry timing may improve realized reward-to-risk.

There is not strong evidence in the source set that a generic moving-average pullback works in isolation across equities.

### Interpretation

Derived:

- `Pullback` should be treated as an `entry method` for continuation, not a separate factor.
- It becomes most plausible when paired with:
  - relative strength,
  - sector leadership,
  - trend integrity,
  - and muted damage during the pullback.

### Regime fit

Best in:

- steady uptrends
- selective tapes where leaders hold structure while the average stock chops

Poor in:

- broad breakdown environments
- deep corrective phases where "pullbacks" become trend failures

### Confidence

`Medium`

## 3. Breakout and range expansion

### What traders do

Breakout traders buy when price exits:

- a base,
- consolidation,
- flag,
- inside-day cluster,
- or volatility compression zone.

They often want:

- price near highs before the move,
- some volume expansion,
- clean support beneath entry,
- and alignment with a strong group or ETF.

### Research support

The direct literature is mixed.

- `Lo, Mamaysky, and Wang` found that some technical patterns contain incremental information, but the evidence does not justify treating chart labels as magical standalone predictors. Source: [SSRN - Foundations of Technical Analysis](https://ssrn.com/abstract=228099)
- The stronger support comes indirectly from momentum, near-high effects, and trend continuation rather than from pattern names themselves.

### Interpretation

Derived:

- Breakouts appear most credible when they are really `continuation entries on existing leaders`.
- The core edge is less likely to be "rectangle breakout" and more likely to be:
  - persistent demand,
  - leadership,
  - compression before expansion,
  - and manageable invalidation.

### Regime fit

Best in:

- broad or selective momentum regimes
- low-friction, trend-friendly tapes

Poor in:

- choppy, headline-driven, mean-reverting environments
- late-stage crowded leadership where breakout failure rates rise

### Confidence

`Medium`

## 4. Industry and sector leadership

### What traders do

Short-term traders often care less about a stock in isolation than about whether:

- its industry group is leading,
- its sector ETF is trending,
- and money is rotating into that part of the market.

ETF traders frequently implement this directly through sector rotation.

### Research support

This is well supported.

- `Moskowitz and Grinblatt` show that a large component of momentum is tied to `industry momentum`, and industry effects explain an important part of stock-level continuation. Source: [PDF - Do Industries Explain Momentum?](https://andreisimonov.com/Microstr_PhD/MSU_09/MoskowitzGrinblatt99.pdf)
- Broader momentum reviews continue to treat industry and sector leadership as a durable part of the anomaly complex. Source: [Review - Momentum: What Do We Know 30 Years After Jegadeesh and Titman?](https://link.springer.com/article/10.1007/s11408-022-00417-8)
- Practitioner ETF rotation discussions often frame sector rotation as a momentum extension rather than a separate idea. Source: [Morningstar - Tactical Investment Strategies That Bolster Performance](https://www.morningstar.com/funds/tactical-investment-strategies-that-bolster-performance) and [Newfound - Two Centuries of Momentum](https://blog.thinknewfound.com/2018/03/two-centuries-of-momentum/)

### Interpretation

Derived:

- For `ETFs`, sector rotation may be one of the cleanest ways to express short-term momentum without single-name event risk.
- For `stocks`, group strength should be a filter, not background decoration.
- A mediocre stock in a powerful group may outperform a good-looking chart in a weak group.

### Regime fit

Best in:

- rotating but trending markets
- selective risk-on conditions

Weaker in:

- chaotic macro reversal phases
- broad de-risking where correlations rise sharply

### Confidence

`High`

## 5. Short-term mean reversion

### What traders do

This playbook buys sharp weakness expecting a bounce, typically after:

- oversold conditions,
- panic selling,
- a washout away from moving averages,
- or abrupt downside extension without a fresh event.

Practitioner literature treats this as common, but often without strong distinction between:

- structural overshoot,
- justified repricing,
- and outright trend failure.

### Research support

There is real support for short-horizon reversal, but the context matters a lot.

- `Jegadeesh` and `Lehmann` documented short-term reversal effects at short horizons. Sources: [Ideas/RePEc summary - Jegadeesh 1990](https://ideas.repec.org/a/bla/jfinan/v45y1990i3p881-98.html) and [NBER - Fads, Martingales, and Market Efficiency](https://www.nber.org/papers/w2533)
- `Nagel` argues that short-term reversal is connected to `liquidity provision` and is strongest when market volatility is high. Source: [NBER - Evaporating Liquidity](https://www.nber.org/papers/w17653)
- `Stivers and Sun` find that one-month reversal weakened after discovery and remains more meaningful in smaller stocks. Source: [SSRN - Short-Term Reversals and the Efficiency of Liquidity Provision](https://ssrn.com/abstract=1911506)
- More recent practitioner summaries highlight that reversal and momentum can coexist: low-turnover names often reverse while high-turnover names can continue. Source: [Alpha Architect - Short-term Momentum](https://alphaarchitect.com/short-term-momentum/) and [Alpha Architect - Alpha from Short-Term Signals](https://alphaarchitect.com/2022/08/alpha-from-short-term-signals/)

### Interpretation

Derived:

- A blanket "buy the dip" strategy in liquid large-cap stocks is not strongly supported.
- Mean reversion is more credible when:
  - volatility is elevated,
  - liquidity temporarily disappears,
  - the move is statistically stretched,
  - and there is evidence of overshoot rather than structural damage.

### Regime fit

Best in:

- stressed but not collapsing markets
- panic flushes
- high-volatility overshoot conditions

Poor in:

- orderly downtrends
- fundamental repricing
- weak tapes where every bounce is sold

### Confidence

`Medium-Low`

## 6. ETF trend following and rotation

### What traders do

ETF traders often simplify the problem:

- rank sector ETFs by relative strength,
- apply an absolute momentum or trend filter,
- hold only leaders,
- and rotate as leadership changes.

This is common in practitioner tactical investing circles because ETFs reduce single-name gap risk and cleanly express group behavior.

### Research support

The direct academic evidence base is stronger for momentum and trend following broadly than for every specific sector-ETF implementation. Still, the logic is well aligned with the literature:

- relative momentum seeks the strongest assets in the cross-section
- absolute momentum avoids owning assets in negative trend
- time-series momentum supports the idea that an asset's own trend contains information

Useful practitioner framing:

- [Newfound - Two Centuries of Momentum](https://blog.thinknewfound.com/2018/03/two-centuries-of-momentum/)
- [Morningstar - Tactical Investment Strategies That Bolster Performance](https://www.morningstar.com/funds/tactical-investment-strategies-that-bolster-performance)
- [Alpha Architect - Sector momentum replication discussion](https://alphaarchitect.com/can-investors-easily-replicate-the-dorsey-wright-focus-5-momentum-etf/)

### Interpretation

Derived:

- ETF rotation looks like one of the most system-friendly places to start because:
  - definitions are clearer,
  - sector leadership can be measured directly,
  - and event risk is diluted compared with single stocks.

### Regime fit

Best in:

- persistent leadership regimes
- broad market recoveries with clear group winners

Weaker in:

- violent style reversals
- macro whipsaw environments

### Confidence

`High` for the broad concept, `Medium` for any one narrow implementation

## 7. Covered calls over a 1-2 week horizon

### What traders do

Some traders sell short-dated covered calls against stock or ETF positions when they expect:

- mild upside,
- sideways action,
- or elevated implied volatility relative to expected realized move.

### Research support

The evidence suggests covered calls are an `overlay`, not a primary short-term alpha engine.

- CBOE buy-write research shows buy-write strategies can reduce volatility and monetize option premium, but they cap upside. Source: [CBOE / Callan - BuyWrite Strategy Review](https://cdn.cboe.com/resources/education/research_publications/Callan_CBOE.pdf)
- `Israelov, Klein, and Tummala` show that covered call returns are better understood as equity exposure plus a short-volatility / variance-risk-premium component. Source: [SSRN - Covering the World: Global Evidence on Covered Calls](https://ssrn.com/abstract=2990522)

### Interpretation

Derived:

- Covered calls do not appear attractive as a core tactic for a trader explicitly seeking `1-2 week` upside participation.
- They make more sense when the underlying is already a valid hold and the trader prefers slightly lower variance and is willing to sell away part of the upside.

### Practical recommendation for this repo

- Keep covered calls under `options overlay suitability`
- Require a valid underlying stock or ETF thesis first
- Do not treat them as a substitute for finding strong short-term setups

### Confidence

`High` that they are secondary, `Low` that they are a primary edge for this horizon

## What the literature does not fully prove

The research leaves several things unresolved:

- exactly which `weekly` breakout or pullback rule set is best
- whether daily-price-only implementations can retain enough edge after costs in all universes
- whether stock-level continuation beats ETF-level rotation after simple risk controls in this specific system
- whether the best risk filter is broad market trend, sector trend, volatility regime, or a combination

Much of the academic literature studies:

- monthly ranking windows,
- longer holding periods,
- or long-short settings.

So there is some unavoidable translation from research result to a long-only `1-2 week` tactical engine.

## Practical implications for Trading System

This research points toward a short-term engine built around a small number of setup families rather than a generic score soup.

Most promising candidates:

1. `Relative-strength continuation`
2. `Near-52-week-high continuation`
3. `Sector or industry leadership filter`
4. `Constructive pullback in strong trend`
5. `ETF rotation with absolute momentum gate`
6. `Selective oversold reversion only in specific stress regimes`

Less promising as primary engines:

- generic chart-pattern taxonomies without broader context
- unconditional mean reversion
- covered-call-first thinking

## Suggested next backtests

The highest-value next tests appear to be:

1. `Leader continuation`
   Long-only top-ranked names by `20D`, `60D`, and `126D` relative strength with extension and regime filters.

2. `Near-high continuation`
   Compare `distance to 52-week high` against simple return-based momentum as a ranking or gating feature.

3. `Trend pullback entry`
   Restrict continuation candidates to those pulling back a controlled amount while remaining above key structure.

4. `Sector-filtered stocks`
   Only allow stock longs when the stock's sector ETF also passes trend and RS filters.

5. `ETF rotation`
   Rank sector ETFs and test top `1-3` holdings under absolute momentum and regime gates.

6. `Stress-only reversion`
   Test oversold bounce logic only when volatility and downside extension exceed a threshold.

## Bottom line

The strongest research-backed answer to the original question is:

short-term traders in equities and ETFs mostly trade `continuation`, `leadership`, and `trend-aligned entries`, with `mean reversion` as a narrower special case.

If the goal is a daily-data Trading System, the most defensible path is not to collect many discretionary chart labels. It is to build a small number of strategy families around:

- relative strength persistence,
- trend structure,
- sector confirmation,
- regime gating,
- and disciplined entry quality.

## Bibliography

### Academic and formal research

- Chan, Jegadeesh, Lakonishok. [Momentum Strategies](https://www.nber.org/papers/w5375)
- Jegadeesh. [Evidence of Predictable Behavior of Security Returns](https://ideas.repec.org/a/bla/jfinan/v45y1990i3p881-98.html)
- Lehmann. [Fads, Martingales, and Market Efficiency](https://www.nber.org/papers/w2533)
- George and Hwang. [The 52-Week High and Momentum Investing](https://ssrn.com/abstract=1104491)
- Moskowitz and Grinblatt. [Do Industries Explain Momentum?](https://andreisimonov.com/Microstr_PhD/MSU_09/MoskowitzGrinblatt99.pdf)
- Lo, Mamaysky, Wang. [Foundations of Technical Analysis](https://ssrn.com/abstract=228099)
- Nagel. [Evaporating Liquidity](https://www.nber.org/papers/w17653)
- Stivers and Sun. [Short-Term Reversals and the Efficiency of Liquidity Provision](https://ssrn.com/abstract=1911506)
- D'Souza et al. [The Enduring Effect of Time-Series Momentum on Stock Returns](https://ssrn.com/abstract=2720600)
- Zakamulin and Giner. [Time Series Momentum in the US Stock Market](https://ssrn.com/abstract=3585714)
- Israelov, Klein, Tummala. [Covering the World: Global Evidence on Covered Calls](https://ssrn.com/abstract=2990522)
- Swinkels. [Momentum: What Do We Know 30 Years After Jegadeesh and Titman?](https://link.springer.com/article/10.1007/s11408-022-00417-8)

### Practitioner and implementation-oriented sources

- Alpha Architect. [The 52 Week High and the Q-Factor Investment Model](https://alphaarchitect.com/52-week-high-q-factor-investment-model/)
- Alpha Architect. [The Secret to Momentum is the 52-Week High???](https://alphaarchitect.com/the-secret-to-momentum-is-the-52-week-high/)
- Alpha Architect. [Short-term Momentum](https://alphaarchitect.com/short-term-momentum/)
- Alpha Architect. [Alpha from Short-Term Signals](https://alphaarchitect.com/2022/08/alpha-from-short-term-signals/)
- Alpha Architect. [Can Investors Easily Replicate the Dorsey Wright Focus 5 Momentum ETF?](https://alphaarchitect.com/can-investors-easily-replicate-the-dorsey-wright-focus-5-momentum-etf/)
- Newfound Research. [Two Centuries of Momentum](https://blog.thinknewfound.com/2018/03/two-centuries-of-momentum/)
- Morningstar. [Tactical Investment Strategies That Bolster Performance](https://www.morningstar.com/funds/tactical-investment-strategies-that-bolster-performance)
- CBOE / Callan. [The CBOE S&P 500 BuyWrite Index Strategy Benchmark](https://cdn.cboe.com/resources/education/research_publications/Callan_CBOE.pdf)

### Practitioner playbook examples

- New Trader U. [Pullback Trading Strategies](https://www.newtraderu.com/2020/11/04/pullback-trading-strategies/)
- New Trader U. [Trend Trading 101](https://www.newtraderu.com/2017/09/28/trend-trading-101/)
- New Trader U. [What is Relative Strength?](https://www.newtraderu.com/2021/05/06/what-is-relative-strength/)
