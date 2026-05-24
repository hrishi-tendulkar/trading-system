# Equity Intelligence Data Provider Landscape

## Status

- Owner: Engineering
- Status: Draft research
- Last updated: 2026-05-24

## Purpose

Evaluate API-accessible data providers against the Weekly Equity Intelligence data foundation requirements.

This document is intended to help us decide:

- which providers can cover the `P0` stock engine,
- which providers are best reserved for `P1` qualitative depth or options overlays,
- where public pricing is transparent versus opaque,
- and which combinations give us the best balance of coverage, cost, and architectural safety.

This update also records how to think about `yfinance` / Yahoo Finance access as a bootstrap-only option for personal research and local validation.

## Scope

This review focuses on providers that are relevant to our current product shape:

- single-user
- batch-first
- daily refreshes and weekly synthesis
- U.S.-equity-centric
- long-only stock engine first
- covered-call and cash-secured-put overlays second

This is not a legal market-data licensing review. It is a product and architecture fit assessment based on publicly available official documentation and pricing pages as of **May 22, 2026**.

## Evaluation Lens

Each vendor is evaluated on:

- `P0 stock engine fit`
- public pricing transparency
- point-in-time and historical depth suitability
- options overlay support
- source breadth versus modularity risk
- architectural blast radius if the provider is later replaced

## Shortlist Reviewed

Primary vendors reviewed in detail:

- SEC EDGAR
- Financial Modeling Prep (`FMP`)
- Massive (formerly Polygon)
- Tradier
- ThetaData
- Finnhub
- EODHD
- Twelve Data
- Intrinio
- Benzinga
- Alpha Vantage

Secondary vendors noted but not deeply modeled:

- Tiingo
- Nasdaq Data Link / Sharadar and companion datasets

## Quick Take

If we optimize for the best trade-off between cost and breadth for a first build:

- `FMP + SEC EDGAR` is the strongest low-cost all-in-one starting point for the stock engine.
- `yfinance + SEC EDGAR` is the cheapest useful bootstrap path for personal local validation of watchlist prices and basic signal logic, but it is not the recommended durable product foundation.
- `Massive + SEC EDGAR + a fundamentals/revisions provider` is the strongest option if we care more about U.S. stock and options market structure quality than all-in-one convenience.
- `Intrinio + Benzinga + SEC EDGAR` is the most institutionally credible modular stack among publicly documented options here, but it is materially more expensive.
- `EODHD` is attractive on paper for breadth and price, but its own public pricing/terms pages require extra caution for trading use because of how some pricing is sourced and described.
- `Finnhub` looks very strong on revisions, transcripts, and filings breadth, but its publicly visible pricing appears materially higher than the self-serve all-in-one alternatives.

## Capability Legend

- `Y` = clear official support
- `P` = partial support, add-on, or support exists but is weaker or less direct for our need
- `N` = no clear official support found
- `C` = custom or contact sales required

## Bootstrap note on `yfinance` / Yahoo Finance

Observed from the current repo:

- `scripts/mlp/fetch_watchlist_prices.py` already uses `yfinance` for watchlist price pulls and a lightweight earnings-date snapshot

Observed from current public docs:

- the `yfinance` project states it is not affiliated with Yahoo, is intended for research and educational purposes, and reminds users that Yahoo Finance data is intended for personal use only

Architectural interpretation:

- `yfinance` is a valid zero-cost bootstrap source for a personal watchlist workflow
- it should be treated as a convenience adapter, not a contractual market-data provider
- it is strongest for simple historical price pulls and weakest when the workflow depends on unattended reliability, richer metadata, or broader point-in-time coverage

## Matrix 1: Core Product Data Requirements

Rows map back to the `P0/P1` data requirements in the data-foundation PRD.

| Data requirement | SEC EDGAR | FMP | Massive | Tradier | ThetaData | Finnhub | EODHD | Twelve Data | Intrinio | Benzinga | Alpha Vantage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Security master / reference data | P | Y | Y | P | P | Y | Y | Y | Y | Y | P |
| Daily EOD OHLCV | N | Y | Y | Y | Y | Y | Y | Y | Y | P | Y |
| Adjusted prices / corp actions | N | Y | Y | P | Y | P | Y | Y | Y | P | Y |
| Benchmark / sector ETF history | N | Y | Y | P | P | Y | Y | Y | P | P | Y |
| Delisted-history support | N | Y | P | N/P | P | P | Y | P | P | P | P |
| Earnings calendar | N | Y | P | N/P | N | Y | Y | Y | Y | Y | Y |
| Earnings actuals / surprises | N | Y | P | N/P | N | Y | Y | Y | Y | Y | Y |
| Analyst estimates consensus | N | Y | P | N | N | Y | P | Y | Y | P | Y |
| Estimate revision history | N | P | N | N | N | Y | P | Y | P | P | P |
| Target prices / analyst ratings | N | Y | Partner add-on | N | N | Y | P | Y | Y | Y | P |
| Core fundamentals (income, BS, CF) | Company Facts only | Y | P | N | N | Y | Y | Y | Y | Y | Y |
| Filing metadata | Y | P | N | N | N | Y | P | P | Y | Y | P |
| Filing raw text / HTML | Y | N/P | N | N | N | Y | N/P | N | Y | P | N |
| Company news | N | Y | Partner add-on | P | N | Y | Y | P | Y | Y | N/P |
| Press releases | N | P | N | N | N | P | P | Y | Y | P | N |
| Earnings call transcripts | N | Y | N | N | N | Y | N/P | N | Transcript URL only / weak | Y | N |
| Conference call calendar | N | P | N | N | N | N/P | N/P | N | N/P | Y | N |
| Current options chain / snapshots | N | N | Y | Y | Y | P/N | Y | N | Y | Unusual options, not chain engine | Premium real-time options mention |
| Historical options EOD / backtestable | N | N | Y | N/P | Y | N/P | P | N | Y | N | N |
| Breadth / market internals | N | P | P | N | N | P | P | P | P | P | P |
| Point-in-time friendliness for backtests | Y for filings | P | P | N/P | Y for options/stocks market data | P/Y by dataset | P | P | Y | P | P |

## Matrix 2: Public Pricing Snapshot

This table uses publicly visible official pricing where available.

| Vendor | Public pricing visibility | Lowest relevant public entry point | Notes |
|---|---|---:|---|
| SEC EDGAR | Transparent | `Free` | Official APIs and bulk ZIP files. |
| FMP | Transparent | `Starter $22/mo`, `Premium $59/mo`, `Ultimate $149/mo` | Public self-serve pricing for personal plans. Commercial display/redistribution needs separate agreement. |
| Massive | Transparent | Stocks `Starter $29/mo`, `Developer $79/mo`, `Advanced $199/mo`; Options `Starter $29/mo`, `Developer $79/mo`, `Advanced $199/mo` | Partner datasets such as Benzinga News / Analyst Ratings and TMX Calendar are `+$99/mo per dataset`. |
| Tradier | Partially transparent | Brokerage account required for real-time market data | Good API docs, but not a standalone self-serve data-vendor pricing model like FMP/Massive. Options Greeks/IV come via ORATS. |
| ThetaData | Transparent | Retail options `Value $40/mo`, `Standard $80/mo`, `Pro $160/mo`; commercial options from `~$1,600/mo`, stocks from `~$1,200/mo` before startup discounts | Very strong official pricing transparency for options and stocks. Requires Theta Terminal in current documented access model. |
| Finnhub | Partially transparent | `Free`; public pricing page snippet shows paid tier up to `$3,500/mo` | Official pricing is visible in search snippets, but the public page is less scrape-friendly and less clear than FMP/Massive. |
| EODHD | Transparent | EOD `19.99/mo`, EOD+Intraday `29.99/mo`, Fundamentals `59.99/mo`, All-in-One `99.99/mo` | Public self-serve prices appear to be for personal use; commercial use routes to startup/enterprise path. |
| Twelve Data | Transparent | `Grow $79/mo`, `Pro $229/mo`, `Ultra $999/mo` | Credit-based pricing rather than simple unlimited endpoint access. Fundamentals endpoints are high-weight. |
| Intrinio | Transparent but a la carte | EOD Stocks `3,100/yr`, US Fundamentals `9,600/yr`, Historical EOD Options `2,800/yr`, EquitiesEdge real-time stocks `1,250/mo` | News and some other feeds are contact-sales/custom. |
| Benzinga | Opaque / sales-led | `Contact sales` | Strong specialist datasets, but no simple public API bundle pricing found. |
| Alpha Vantage | Transparent | `49.99/mo` for `75 req/min`, then `99.99`, `149.99`, `199.99`, `249.99` tiers | Good public pricing clarity; weaker fit for full platform foundation. |

## Vendor-by-Vendor Analysis

## 1. SEC EDGAR

### Best use

- source-of-truth filings
- filing metadata
- filing timestamps
- company facts and XBRL bulk data

### Strengths

- free
- official
- real-time or near-real-time updates
- nightly bulk ZIPs for large-scale backfill
- ideal for raw filing capture and auditability

### Weaknesses

- not a complete market-data provider
- no newsfeed, transcripts, analyst revisions, or options
- structured financial facts are useful but still require normalization logic

### Fit

- mandatory secondary source in almost any architecture
- not sufficient as a standalone provider

## 2. Financial Modeling Prep (`FMP`)

### Best use

- broad low-cost all-in-one stock engine
- fundamentals
- historical prices
- calendars
- estimates
- transcripts

### Strengths

- unusually strong breadth for self-serve pricing
- public pricing is simple and affordable
- official site claims `30+ years` of prices and fundamentals, `10+ years` of analyst estimates and call transcripts
- Ultimate plan includes transcripts, holdings, and bulk delivery

### Weaknesses

- options support is not clearly surfaced in the official docs reviewed here
- point-in-time rigor for revisions and backtests should be verified before relying on it
- commercial display/redistribution requires separate agreement

### Fit

- strongest budget all-in-one starting point for the stock engine
- should be paired with SEC EDGAR for source-of-truth filings
- may still need a separate options provider

### Relevant official notes

- Starter: `300 calls/min`, `5 years`, fundamentals/news, `$22/mo`
- Premium: `750 calls/min`, `30 years`, intraday, technicals, calendars, `$59/mo`
- Ultimate: `3,000 calls/min`, transcripts, full historical access, bulk/batch, `$149/mo`

## 3. Massive (formerly Polygon)

### Best use

- high-quality U.S. market data
- stocks and options
- real-time or delayed snapshots
- strong technical and market-structure foundation

### Strengths

- best documented self-serve stock + options surface in this review
- clear stock and options plan ladders
- strong options chain, snapshot, quotes, Greeks, IV, and historical OHLC support
- partner datasets can add Benzinga news/ratings and TMX corporate calendars

### Weaknesses

- fundamentals depth appears lighter than dedicated fundamentals providers
- transcripts are not part of the core offering
- an all-in Massive stack likely still needs a second provider for richer revisions/fundamentals

### Fit

- strongest candidate for a high-quality U.S. stock/options market-data layer
- best when paired with SEC and a separate fundamentals / revisions provider

### Relevant official notes

- Stocks Advanced: `$199/mo`, `20+ years`, real-time, financials & ratios
- Options Starter / Developer / Advanced: `$29/$79/$199`
- Benzinga news and analyst ratings add-ons: `$99/mo per dataset`
- TMX corporate events add-on: `$99/mo`

## 4. Finnhub

### Best use

- revisions-heavy research
- estimates
- transcripts
- filings
- broad fundamental context

### Strengths

- official site claims `30+ years` of fundamentals and market data
- `25+ years` of estimates for many companies
- `15+ years` of transcripts with audio
- official docs/search show filings, recommendation trends, target prices, transcripts, and download paths

### Weaknesses

- public pricing is much less straightforward than FMP or Massive
- search snippet suggests a much higher-end pricing posture, with public reference to `$3,500/mo`
- options support is not clearly positioned as a core strength for our exact use case

### Fit

- potentially very strong research-data layer
- less attractive as the first self-serve foundation unless pricing is acceptable

## 4A. Tradier

### Best use

- brokerage-linked market data
- current options chains
- execution-adjacent workflows

### Strengths

- official docs clearly support quotes, historical market data, options chains, streaming, and brokerage integration
- real-time equities and options data are available to Tradier Brokerage account holders
- options chains can include Greeks and IV via ORATS

### Weaknesses

- not positioned as a broad fundamentals, filings, transcripts, or revision-history provider
- real-time data access is tied to having a Tradier Brokerage account, partner status, or advisor setup
- public pricing is not presented as a simple standalone market-data subscription comparable to FMP, Massive, or ThetaData
- historical options research depth appears weaker than dedicated options data vendors

### Fit

- relevant if we later want brokerage-adjacent tooling or Tradier-linked execution support
- not a strong primary data-foundation choice for the current batch-first research product

## 4B. ThetaData

### Best use

- high-quality U.S. options data
- historical options backtesting
- strong stock and options market microstructure data

### Strengths

- excellent official transparency around options and stocks coverage
- very strong options history, including chain snapshots, tick data, NBBO quotes, IV, and advanced Greeks
- public pricing is unusually clear for both retail and commercial use
- current docs explicitly mention free historical EOD for one year and deeper history on paid tiers

### Weaknesses

- not a fundamentals, transcripts, or revisions provider
- current docs require the Theta Terminal running as part of the access model
- architecture is strongest for market/derivatives data, not all-in-one product breadth

### Fit

- one of the strongest candidates if historical covered-call / cash-secured-put research becomes a near-term priority
- not a substitute for a broader stock-engine provider

## 5. EODHD

### Best use

- broad low-cost experimentation
- global EOD and fundamentals
- rapid prototyping

### Strengths

- broad apparent feature surface: EOD, intraday, fundamentals, news, options, screener, technicals
- public self-serve pricing is highly accessible
- all-in-one plan is cheap on paper

### Weaknesses

- public pricing/terms pages explicitly state that some prices are not exchange feeds and may be aggregated from market makers, peer-to-peer trades, and trading platforms
- commercial-use licensing is separate from personal-use self-serve plans
- this creates risk for a trading system where data provenance and backtesting credibility matter

### Fit

- good for prototypes and cost-sensitive experimentation
- should be treated cautiously for the production-grade core of a trading decision system until data-quality questions are resolved

## 6. Twelve Data

### Best use

- broad market + fundamentals + estimates under one API
- indicator-heavy workflows
- global market coverage

### Strengths

- official pricing and docs are very clear
- fundamentals page and pricing page expose earnings, earnings estimates, revenue estimates, EPS revisions, recommendations, financial statements, and press releases
- broad market coverage

### Weaknesses

- pricing is credit-based, and fundamentals endpoints are expensive in credit weight
- no clear official options-chain product surfaced in this review
- transcripts do not appear to be part of the core offering

### Fit

- viable stock-engine candidate if we prefer a credit-based API with strong breadth
- less suitable if options overlays are important early

## 7. Intrinio

### Best use

- modular institutional-quality stack
- strong U.S. fundamentals
- strong filings
- strong EOD options history

### Strengths

- unusually transparent a la carte pricing for several important feeds
- official pricing shows `15+ years` of US fundamentals from the SEC, back to `2006`
- raw filings text and metadata are well documented
- official pricing shows historical EOD options with IV and Greeks at a visible price

### Weaknesses

- total spend climbs quickly when combining stocks, fundamentals, options, and news
- transcripts are not presented as a first-class dataset in the same way as Finnhub or Benzinga
- this is a modular architecture, not a cheap all-in-one path

### Fit

- strong engineering-first choice if we want high-quality modularity and are willing to pay for it
- likely overkill for the earliest version unless data quality is prioritized far above cost

## 8. Benzinga

### Best use

- event data
- analyst ratings and target changes
- conference calls
- transcripts / summaries
- news

### Strengths

- deep specialist event surface
- official docs/pages show Analyst Ratings, Conference Calls, Conference Call Transcripts, Future Earnings Dates & Historical Results, Corporate Guidance, SEC Filings, Security Master, and Unusual Options Activity
- Benzinga’s analyst ratings history goes back to `2013` on the reviewed page

### Weaknesses

- public pricing is sales-led and opaque
- best thought of as a specialist layer, not the whole data foundation
- overlap with other providers can create duplication if we do not clearly define its role

### Fit

- best as a P1 specialist feed for analyst actions, event calendars, and market-moving news
- not the cleanest first provider for a lean v1 unless budget is flexible

## 9. Alpha Vantage

### Best use

- low-cost prototyping
- price series
- basic fundamentals and technicals

### Strengths

- very clear public pricing
- good entry point for experimentation
- official docs include earnings estimates and a broad endpoint surface

### Weaknesses

- weaker fit than FMP or Massive for our full product requirements
- transcripts, filings depth, and options-history support are not compelling enough here
- best viewed as a developer-friendly API, not the strongest core foundation

### Fit

- suitable for prototypes or narrow tools
- not a top recommendation for the long-term system core

## Secondary Vendors Worth Later Review

## Tiingo

Why note it:

- official support content clearly references EOD prices, real-time, news, and equity fundamentals
- operational status page exposes dedicated endpoints for EOD, news, and fundamentals
- Tiingo clearly supports stock prices, fundamentals, and news in official help content

Why not in the main recommendation set:

- public pricing was not easily extractable in a clean official form during this pass
- options, transcripts, and broader event/revisions fit were not as clear as the top alternatives
- for our current product, it appears more useful as a stock-data alternative than as a complete data-foundation answer

## Nasdaq Data Link / Sharadar

Why note it:

- very strong for curated U.S. equities data, especially Sharadar prices and fundamentals
- official help/docs explicitly note premium datasets for Sharadar prices, Sharadar Core Fundamentals, Zacks earnings estimates, and Zacks analyst ratings

Why not in the main recommendation set:

- pricing is dataset-by-dataset and not simple all-in-one self-serve
- this is more of a modular premium data platform than a quick v1 integration choice

## Comparative Recommendations

## Option A: Lowest-cost credible stock engine

### Stack

- `FMP Ultimate`
- `SEC EDGAR`

### Monthly cost

- roughly `~$149/mo` plus engineering time

### What it covers well

- EOD/intraday stock data
- fundamentals
- calendars
- analyst estimates
- transcripts
- basic news
- filings through SEC

### What it likely misses or weakens

- robust options-chain history
- best-in-class U.S. options overlay support
- highest-confidence point-in-time verification on revisions until tested

### Best for

- proving the stock engine quickly and cheaply

## Option B: Best balanced architecture for our roadmap

### Stack

- `Massive Stocks Advanced`
- `Massive Options Advanced`
- `FMP Premium or Ultimate`
- `SEC EDGAR`

### Monthly cost

- roughly `~$457/mo` with `FMP Ultimate`
- `199 + 199 + 59` or `149`, depending on FMP plan

### What it covers well

- high-quality U.S. stock and options market data
- technical / options overlay support
- fundamentals, transcripts, and estimates via FMP
- source-of-truth filings via SEC

### Architectural benefit

- splits core stock/options market structure from broader fundamental/event data
- avoids single-vendor lock-in for the most sensitive categories

### Best for

- the likely long-term architecture sweet spot

## Option B2: Best options-research upgrade path

### Stack

- `FMP Ultimate`
- `SEC EDGAR`
- `ThetaData Options` or `Massive Options`

### Monthly cost

- roughly `~$189/mo` to `~$348/mo` on retail/public pricing depending on options tier and whether Massive or ThetaData is chosen

### What it covers well

- credible stock engine via FMP
- direct filings via SEC
- materially stronger options-history support for overlays and research

### Best for

- a roadmap where options backtesting becomes important before we need institutional-grade specialist event data

## Option C: Institutional modular stack

### Stack

- `Intrinio` for fundamentals, filings, and optionally EOD options history
- `Benzinga` for ratings/news/events/transcripts
- `SEC EDGAR`
- optionally `Massive` for stock/options market data

### Monthly cost

- highly variable
- likely materially higher than Options A or B

### What it covers well

- modularity
- auditability
- stronger specialty datasets

### Best for

- later-stage quality upgrade if v1 proves valuable enough to justify higher spend

## Option D: Broad cheap experimentation stack with caution

### Stack

- `EODHD`
- `SEC EDGAR`

### Monthly cost

- as low as `~$99.99/mo` self-serve for broad data

### Risk

- not my recommended production foundation until we verify whether the provider’s public sourcing and disclaimers are acceptable for a trading decision system

## Architecture Implications

## 1. Do not hard-wire one vendor into canonical schemas

This research reinforces the earlier architecture principle:

- preserve raw, normalized, and derived layers separately
- isolate providers behind adapters
- allow the stock engine to run without the options layer

## 2. The cheapest all-in-one vendor is not automatically the safest foundation

Breadth alone is not enough.

We care about:

- point-in-time correctness
- stable historical backfills
- source lineage
- explainability when scores change

## 3. Options are the main forcing function for a second provider

If covered calls and cash-secured puts remain part of the roadmap, we should assume:

- `FMP` alone is probably not enough
- `Massive` or `Intrinio` become much more relevant

## 4. SEC EDGAR should be treated as infrastructure, not just a backup

For filings, risk reviews, and auditability:

- SEC should remain in the stack even if another vendor also offers filings

## Recommendation

For the current product and engineering direction, my recommendation is:

### Phase 1 recommendation

- `FMP Ultimate + SEC EDGAR`

Reason:

- fastest path to a credible stock engine
- lowest all-in cost
- broad enough to start building and testing weekly workflows

### Phase 2 recommendation

If options overlays and higher-confidence U.S. market structure become important:

- add `Massive` for stocks and options

### Phase 3 recommendation

If we later decide quality and specialist event coverage matter more than cost:

- evaluate `Benzinga` and/or `Intrinio` as modular upgrades

## Open Questions

- Is FMP’s revision history sufficiently point-in-time for our research standards?
- Is Massive’s financials layer deep enough, or would we still want FMP or Intrinio for conviction scoring?
- Are Benzinga’s transcripts and analyst datasets worth their likely custom pricing for a single-user first product?
- Do we need true historical options-chain snapshots immediately, or is forward-only overlay screening acceptable in v1?
- Is ThetaData’s terminal-based access model acceptable operationally, or do we prefer Massive’s more straightforward cloud-first integration even if the options feature set differs?
- Would Tradier only become relevant if we later want broker-linked execution, or is there any reason to include it earlier than that?

## Official Sources Used

- SEC EDGAR APIs: [sec.gov EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- FMP pricing: [FMP pricing plans](https://site.financialmodelingprep.com/pricing-plans)
- FMP docs and coverage: [FMP site overview](https://site.financialmodelingprep.com/), [FMP quickstart](https://site.financialmodelingprep.com/developer/docs/quickstart), [FMP estimates API](https://site.financialmodelingprep.com/developer/docs/analyst-estimates-api/?direct=true)
- Massive pricing and docs: [Massive pricing](https://massive.com/pricing), [Stocks docs](https://massive.com/docs/stocks/getting-started), [Options docs](https://massive.com/docs/options)
- Tradier docs: [Tradier market data](https://docs.tradier.com/docs/market-data), [Tradier options chains](https://docs.tradier.com/reference/brokerage-api-markets-get-options-chains), [Tradier getting started](https://docs.tradier.com/docs/getting-started)
- ThetaData pricing and docs: [ThetaData pricing](https://www.thetadata.net/pricing), [ThetaData options data](https://www.thetadata.net/options-data), [ThetaData stocks data](https://www.thetadata.net/stocks-data), [ThetaData subscriptions](https://docs.thetadata.us/Articles/Getting-Started/Subscriptions.html)
- Finnhub pricing and coverage: [Finnhub pricing](https://finnhub.io/pricing), [Finnhub home](https://finnhub.io/), [Finnhub docs](https://api.finnhub.io/docs/api/stock-bidask)
- EODHD pricing and coverage: [EODHD pricing](https://eodhd.com/pricing), [EODHD home](https://eodhd.com/)
- Twelve Data pricing and coverage: [Twelve Data pricing](https://twelvedata.com/pricing), [Twelve Data fundamentals](https://twelvedata.com/fundamentals), [Twelve Data market data](https://twelvedata.com/market-data)
- Intrinio pricing and docs: [Intrinio pricing](https://intrinio.com/pricing), [Intrinio access methods](https://intrinio.com/access-methods), [Intrinio filings docs](https://docs.intrinio.com/documentation/web_api/get_all_filings_v2)
- Benzinga APIs and docs: [Benzinga APIs](https://www.benzinga.com/apis/de/), [Benzinga financial data APIs](https://www.benzinga.com/apis/cloud-product/financial-data-apis/), [Benzinga SEC Filings](https://www.benzinga.com/apis/cloud-product/sec-filings-data/), [Benzinga conference calls](https://www.benzinga.com/apis/cloud-product/conference-calls/), [Benzinga analyst ratings](https://www.benzinga.com/apis/analyst-ratings-api/)
- Alpha Vantage pricing and docs: [Alpha Vantage premium](https://www.alphavantage.co/premium/), [Alpha Vantage docs](https://www.alphavantage.co/documentation/)
- Tiingo references: [Tiingo pricing page](https://app.tiingo.com/mission/pricing), [Tiingo API token/help](https://www.tiingo.com/kb/article/where-to-find-your-tiingo-api-token/), [Tiingo about](https://www.tiingo.com/blog/about-us/)
- Nasdaq Data Link docs/help: [Getting started](https://docs.data.nasdaq.com/docs/getting-started), [Data organization](https://docs.data.nasdaq.com/docs/data-organization), [Pricing help](https://help.data.nasdaq.com/article/568-how-much-does-nasdaq-data-link-data-cost-how-do-i-find-pricing)
