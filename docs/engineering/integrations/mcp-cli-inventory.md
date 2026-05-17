# MCP And CLI Inventory

## Goal

Identify the connections and local tooling needed to build and operate the Trading System over time.

## 1. Core Codex-side connections

These help us build and operate the project from Codex.

### Required

- GitHub MCP
  - Use for repository workflows, PR review, issue tracking, and CI visibility
- Shell / local command execution
  - Use for running code, tests, scripts, and local data jobs

### Strongly recommended

- Browser Use plugin / in-app browser
  - Use for testing any future local dashboard or web UI
- OpenAI docs skill
  - Use for up-to-date OpenAI platform and model guidance when we build AI features

## 2. External product integrations

These are not Codex MCPs by default; they are system integrations the product will need.

### Market and fundamentals

- Market data provider
  - Examples: Polygon, Tiingo, Alpha Vantage, IEX Cloud alternative, Twelve Data
  - Use for OHLCV, benchmark context, and potentially fundamentals

### Company fundamentals and estimates

- Financial statement / estimates provider
  - Examples: Financial Modeling Prep, FactSet-class provider later, Alpha Vantage supplements
  - Use for revenue, margins, EPS, guidance context, estimates, and revisions

### SEC filings

- SEC EDGAR access
  - Use for 10-K, 10-Q, 8-K, proxy, and filing delta extraction

### Earnings call transcripts

- Transcript provider
  - Examples: Financial Modeling Prep, AlphaSense-class provider later, other transcript APIs
  - Use for management commentary, Q&A, and narrative change analysis

### News

- News provider
  - Examples: NewsAPI, Finnhub news, Benzinga-class provider later
  - Use for company-, sector-, and market-level event ingestion

### Calendar and corporate events

- Earnings calendar / corporate actions source
  - Use for timing-sensitive catalysts and event-driven workflows

### AI models

- OpenAI API
  - Use for summarization, classification, synthesis, and structured extraction

## 3. Engineering and operations CLI tools

### Required early

- `git`
  - Source control
- `gh`
  - GitHub workflow and CI convenience
- `python3`
  - Strong default for ingestion, feature engineering, and automation

### Recommended early

- `uv` or `poetry`
  - Python dependency and environment management
- `duckdb`
  - Excellent local analytical store for early versions
- `jq`
  - JSON inspection and API debugging

### Likely later

- `psql`
  - If we move from local analytical storage to Postgres
- `docker`
  - For environment consistency and service packaging
- Cloud CLI
  - `aws`, `gcloud`, or `vercel` depending on hosting choice

## 4. Suggested minimum day-one stack

If we want a pragmatic first build, the minimum useful connection set is:

1. GitHub MCP plus `git` and `gh`
2. OpenAI API
3. One market data provider
4. SEC EDGAR access
5. One transcript provider
6. One news provider
7. Python plus `uv`
8. DuckDB for local storage

## 5. Open questions before locking vendors

- Do we want to optimize for low cost, best transcript quality, or best historical coverage?
- Do we need analyst estimate revisions in v1, or can that wait?
- Should local-first infrastructure remain the default through the first scoring engine?
- Do we want one broad provider or several narrow best-of-breed providers?
