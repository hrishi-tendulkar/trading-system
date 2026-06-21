<!-- TAGLINE -->
A weekly investing app I built for myself to decide which stocks to buy, wait on, or trim.

<!-- BLURB -->
Trading System is a private investing app I built for my own weekend review. It scans a watchlist, shows the current weekly plan, and tells me which stocks look ready, which ones need a better entry, and which ones I should leave alone. It also keeps old weekly plans so I can see what I believed at the time instead of rewriting the past. I built it because my investing notes, market data, stock research, and trade rules were scattered across too many places.

<!-- FULL README BELOW -->
# Trading System

A weekly investing app I built for myself to decide which stocks to buy, wait on, or trim.

**Status:** Private internal app. In personal use as a weekly review tool; not a commercial product.

![Weekly plan](./screenshots/01_Main_View.png)

> Screenshots use placeholder tickers and synthetic portfolio data. The real version uses my actual portfolio.

## Why I built this

I have limited time during the week to watch markets. Most of my investing decisions happen on the weekend, after the market has closed and I can think clearly.

Before this project, the work was scattered. Prices were in one place. Stock notes were somewhere else. Earnings dates, market context, and old decisions were easy to lose track of. That made the process slower than it needed to be, and it made it hard to learn from past calls.

Most investing tools give me more charts, more news, or faster trading. I wanted something quieter: one page that tells me what deserves attention this week, what can wait, and what I should not touch.

## What it does

- Builds a weekly plan from the latest saved run: market posture, top ideas, waitlist names, and names to avoid.
- Keeps the main action list short, even when the system scans a broader watchlist.
- Shows why a stock is marked `buy now`, `buy on pullback`, `wait`, `hold`, or `no action`.
- Opens a stock detail page with price context, earnings timing, entry zone, stop, target, and the reason for the current call.
- Keeps an archive of old weekly plans so I can go back and see what the system recommended at the time.
- Shows strategy pages so I can tell which rules are trusted enough for the main board and which ones are still research only.

![Candidates board](./screenshots/02_Candidates_View.png)

![Stock detail — observed vs. derived](./screenshots/03_Stock_Detail_View.png)

![Strategy registry](./screenshots/04_Strategy_Detail_View.png)

## How I made it

**I made it weekly, not real-time.**  
The goal is to help me make better weekend decisions. Real-time alerts, broker connections, and automated trades would add cost and distraction before the basic workflow is proven.

**I kept the action board small.**  
The app can scan a larger list, but the weekly plan only promotes a handful of names. If everything looks actionable, nothing is.

**I made weekly plans explicit saved runs.**  
An old report should never look current just because it is the newest file the app can find. Each run has a week, publish time, data-through date, and strategy version.

**I separated strategy rules instead of using one big score.**  
A stock can be high quality and still be a bad entry this week. Separate rules make that easier to see.

**I used a file-backed bridge before moving everything into the database.**  
That let me ship the app surface and weekly workflow first, while keeping a path to Supabase-backed history later.

## How it's built

- **Frontend:** Server-rendered Jinja templates with custom CSS
- **Backend:** Python, FastAPI, Typer jobs, Pydantic, pandas
- **LLM:** OpenAI API is planned for summaries and classification; the current scoring is deterministic
- **Data:** CSV snapshots and JSON run manifests today; Supabase Postgres is the planned long-term store
- **Hosting:** Railway is configured for the private app and scheduled jobs

The main technical idea is simple: compute stock signals, test them against strategy rules, block risky candidates, then publish a weekly board. Published runs are saved so later changes do not rewrite old recommendations.

## What I learned

The most useful change was separating “good stock” from “good entry.” Early versions leaned too much on broad strength. That felt clean, but it hid the reason behind each call. The app got better when I made the rules more specific: a breakout has different evidence than a pullback, and a research-only rule should not quietly become a buy recommendation.

Source code is private. Available on request — reach out via LinkedIn.
