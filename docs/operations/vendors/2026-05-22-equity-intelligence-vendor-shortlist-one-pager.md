# Equity Intelligence Vendor Shortlist One-Pager

## Purpose

Recommend the most practical vendor path for the Weekly Equity Intelligence system across:

- `v1` stock-engine launch
- `v2` options-overlay expansion
- expected monthly cost by phase
- and the exact diligence tests we should run before committing

This is a decision memo built from the broader provider landscape research.

Related source:

- [Equity Intelligence Data Provider Landscape](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/docs/engineering/integrations/2026-05-22-equity-intelligence-data-provider-landscape.md)

## Executive Recommendation

### Recommended v1 stack

- `Financial Modeling Prep Ultimate`
- `SEC EDGAR`

### Recommended v2 stack

- keep `FMP Ultimate`
- keep `SEC EDGAR`
- add either `Massive Options Advanced` or `ThetaData Options`

### Recommended default path

Start with `FMP + SEC` to prove the weekly stock engine fast and cheaply. Add a dedicated options provider only after we confirm that covered-call and cash-secured-put overlays are materially worth building into the workflow.

## Why this is the recommended path

### Why `FMP + SEC` wins for v1

- lowest-cost credible all-in-one stock-engine foundation
- broad coverage across prices, fundamentals, earnings, estimates, and transcripts
- simple public self-serve pricing
- fast implementation with low architecture overhead
- SEC keeps filings source-of-truth and auditability independent from the vendor

### Why not start with a more modular stack

- `Massive + FMP + SEC` is better architecturally for stock + options quality, but more expensive before we know the weekly engine is working
- `Intrinio + Benzinga + SEC` is stronger as a specialist stack, but too expensive and fragmented for the first version
- `Tradier` is more brokerage/execution-adjacent than data-foundation-first
- `ThetaData` is strongest where options research matters, not as the all-in-one first provider

## Recommended Vendor by Phase

| Phase | Goal | Recommended vendors | Why |
|---|---|---|---|
| `Phase 1 / v1` | Launch the weekly stock engine | `FMP Ultimate + SEC EDGAR` | Cheapest credible path with broad stock-engine coverage |
| `Phase 2 / v1.5` | Add live weekly options overlays | `FMP Ultimate + SEC EDGAR + Massive Options Advanced` or `ThetaData Options` | Dedicated options support without replacing stock engine |
| `Phase 3 / v2+` | Improve specialist event / options / institutional data quality | Consider `Benzinga`, `Intrinio`, or `Massive Stocks` upgrades | Only after we know where current data is limiting outcomes |

## Expected Monthly Cost

These are approximate public-pricing figures as of **May 22, 2026** and exclude engineering time, OpenAI usage, and any commercial licensing upgrades.

| Stack | Expected monthly cost | Notes |
|---|---:|---|
| `SEC EDGAR only` | `Free` | Not sufficient alone |
| `FMP Ultimate + SEC` | `~$149/mo` | Best v1 starting point |
| `FMP Premium + SEC` | `~$59/mo` | Cheaper, but likely too restrictive if we need transcripts and broader history |
| `FMP Ultimate + Massive Options Advanced + SEC` | `~$348/mo` | Strong v2 options path |
| `FMP Ultimate + Massive Stocks Advanced + Massive Options Advanced + SEC` | `~$547/mo` | Best balanced higher-quality stack |
| `FMP Ultimate + ThetaData retail options + SEC` | `~$189-$309/mo` | Depends on ThetaData tier: `Value $40`, `Standard $80`, `Pro $160` |
| `ThetaData commercial options + FMP + SEC` | `~$649/mo+` with startup discounts possibly lower | More relevant if commercial usage terms or deeper options backtesting matter |
| `EODHD All-in-One + SEC` | `~$99.99/mo` | Cheap, but not my recommended production core without deeper diligence |
| `Massive Stocks Advanced + Massive Options Advanced + SEC` | `~$398/mo` | Strong market-data stack, but weaker than FMP on transcripts/revisions |

## Best-Fit Vendor by Category

| Category | Best current fit | Backup / alternative |
|---|---|---|
| Stock-engine all-in-one | `FMP` | `Twelve Data`, `Finnhub` |
| Source-of-truth filings | `SEC EDGAR` | `Intrinio` as paid structured layer |
| U.S. stock market data quality | `Massive` | `ThetaData` for deeper market-data use cases |
| Historical options research | `ThetaData` | `Massive`, `Intrinio` |
| Analyst ratings / event specialist | `Benzinga` | `Finnhub`, partner datasets via Massive |
| Modular premium fundamentals | `Intrinio` | `Nasdaq Data Link / Sharadar` later |

## Decision Rules

### Choose `FMP + SEC` if:

- the immediate goal is to launch the weekly stock engine
- budget discipline matters
- we want one broad self-serve provider before splitting the stack
- options overlays are secondary for the first release

### Choose `Massive + FMP + SEC` earlier if:

- we already know options overlays will be a core differentiator
- we care a lot about U.S. market-data and options-chain quality from day one
- we are comfortable with roughly `2x-4x` higher recurring data cost than the cheapest viable stack

### Choose `ThetaData` earlier if:

- serious historical covered-call / cash-secured-put research is a near-term requirement
- we are comfortable with the current terminal-based access model
- we specifically value options history, NBBO coverage, and Greeks depth

## Vendors We Should Not Lead With

### `Tradier`

Reason:

- useful later for brokerage-linked execution or account integration
- not the best data-foundation-first provider for this product

### `EODHD`

Reason:

- attractive feature surface and price
- but we should not make it the production foundation until we are comfortable with its public sourcing and terms posture for a trading decision system

### `Alpha Vantage`

Reason:

- good prototyping API
- not the strongest end-state fit for our full weekly intelligence stack

## What We Should Test Before Committing

These tests matter more than marketing pages.

## Test 1: Point-in-time revision integrity

Vendors to test:

- `FMP`
- `Finnhub`
- `Twelve Data`

Questions:

- Can we retrieve estimate history with clear timestamps?
- Are revisions stored historically or only current consensus?
- Can we reconstruct what the system would have known before an earnings event?

Pass condition:

- we can replay revision state for prior dates without obvious look-ahead leakage

## Test 2: Earnings and event completeness

Vendors to test:

- `FMP`
- `Finnhub`
- `Benzinga`

Questions:

- Are earnings dates stable and corrected when companies move them?
- Do we get actuals, consensus, surprise, and guidance context?
- How often do events arrive late or with missing fields?

Pass condition:

- we trust the event layer enough to drive weekly catalyst logic

## Test 3: Filings capture and traceability

Vendors to test:

- `SEC EDGAR`
- `FMP`
- `Intrinio`

Questions:

- Can we capture raw filing text reliably?
- Can we link every extracted fact back to source filing and timestamp?
- Is direct SEC enough, or do we need a paid filing-normalization layer later?

Pass condition:

- direct SEC ingestion is stable enough for v1 and traceable in storage

## Test 4: Transcript usefulness

Vendors to test:

- `FMP`
- `Finnhub`
- `Benzinga`

Questions:

- What percent of our 50-70 name universe has transcript coverage?
- Are transcripts timely enough after earnings?
- Is speaker attribution present and usable?

Pass condition:

- coverage and timeliness are good enough for top names and holdings

## Test 5: Historical options support

Vendors to test:

- `ThetaData`
- `Massive`
- `Intrinio`

Questions:

- Can we retrieve historical chain snapshots cleanly?
- Do we have strikes, expiries, bid/ask, volume, OI, IV, and contract metadata?
- Are APIs usable enough for weekly overlay research without heroic engineering?

Pass condition:

- we can realistically backtest or at least forward-test covered calls and cash-secured puts

## Test 6: Operational friction

Vendors to test:

- all shortlisted vendors

Questions:

- Are rate limits manageable for daily batch jobs?
- Are bulk backfills feasible?
- Are error messages and docs good enough for a small team?
- Does the vendor force awkward local components or brittle workflows?

Pass condition:

- the integration is maintainable by a single operator / small team

## Concrete Next-Step Plan

### Week 1

- trial `FMP`
- build a small sample pipeline for `10` names plus `SPY/QQQ/sector ETFs`
- ingest prices, earnings, estimates, fundamentals, and transcripts
- ingest direct filings from `SEC EDGAR`

### Week 2

- evaluate data completeness and point-in-time behavior
- compare `FMP` revisions and earnings fields against one secondary provider if possible
- decide whether `FMP` is good enough for the stock engine

### Week 3

- if options are a near-term requirement, run a focused bake-off:
  - `Massive Options`
  - `ThetaData`
  - optionally `Intrinio EOD options`

### Week 4

- lock the `Phase 1` vendor stack
- document any vendor-specific limitations in engineering context

## Final Recommendation

If we had to choose today:

- `v1`: `FMP Ultimate + SEC EDGAR`
- `v2 options path`: add `ThetaData` if historical options research is the priority, or add `Massive Options` if we want a cleaner cloud-first options integration

That gives us the best balance of:

- speed
- cost
- stock-engine breadth
- traceability
- and future flexibility

## Official Sources Used

- FMP pricing: [FMP pricing plans](https://site.financialmodelingprep.com/pricing-plans)
- Massive pricing and options docs: [Massive pricing](https://massive.com/pricing), [Massive options docs](https://massive.com/docs/options)
- ThetaData pricing: [ThetaData pricing](https://www.thetadata.net/pricing), [ThetaData commercial use](https://www.thetadata.net/commercial-use)
- SEC EDGAR APIs: [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [Accessing EDGAR Data](https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm)
