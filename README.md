# 📈 Trading System

> A weekly investing workbench I built for my own trading. Every weekend, it gives me a short list of stocks to buy, wait on, hold, or trim — with the reasoning behind each call, and an audit trail.

**Status:** Personal tool. Single-user by design (just me). Showcased here for the product structure, not as something to distribute.

> Screenshots use placeholder tickers and synthetic data. The real version uses my actual portfolio.

![Weekly summary](./screenshots/01_Main_View.png)

---

## Why I built this

I have a full-time job and limited time on weekends to make investing decisions. Today the work is scattered: market context lives in one place, stock research in another, options data in a third, watchlist notes in a fourth. Switching between them on a Sunday afternoon is slow and inconsistent, and a few weeks later I can't remember why I made a particular call.

Most consumer investing tools optimize for one of two things: showing more data (research abundance) or executing trades faster. Neither helps the actual question on a Sunday afternoon, which is: *given everything that happened this week, what should I do this weekend?*

So I built one place that compresses all of it down to a short, explainable, traceable weekly action list.

## What it does

- Produces a **weekly action report**: where the market is, what to buy now, what to wait on, what to avoid, what to hold or trim, and any covered-call or cash-secured-put overlays worth considering.
- Splits the workflow into a funnel: a broad coverage universe → an active watchlist → a weekly focus board → a sparse action board of 3–5 names. The engine can scan widely without me ever seeing a 500-name feed.
- Publishes each week as an **immutable run** — with a recommendation week, data-through date, run ID, and the strategy version used. So I can always go back and see what was being recommended and why.
- On every stock, separates **observed facts** (price, earnings result, news) from **derived interpretation** (the model's read on what those facts mean). So I'm always clear on what's a number and what's an opinion.
- Maintains a registry of **strategies** — each one a different lens (e.g. Breakout Confirmation, Pullback Continuation). Strategies are either *promoted* (feeding the main board) or *research-only*. Weak strategies don't quietly contaminate the main recommendations.

![Candidates board](./screenshots/02_Candidates_View.png)

![Stock detail — observed vs. derived](./screenshots/03_Stock_Detail_View.png)

![Strategy registry](./screenshots/04_Strategy_Detail_View.png)

> The information design principle across every screen: lead with the **call**, then show the **evidence**. The stock detail page enforces an explicit split between *observed facts* and *derived interpretation*, so I always know what's a number and what's an opinion.

## Decisions I made — and why

**A weekly decision tool — not an intraday trading app.**
*Why:* My constraint is weekend time. Intraday alerts and automated execution are explicit non-goals. The product wins or loses on whether the weekend workflow gets me to a decision.

**A funnel, not a feed.** Broad coverage → watchlist → focus board → 3–5 name action board.
*Why:* Broad scanning helps me discover candidates, but the weekly screen needs to stay short and trusted. A flat list of 500 names is the same as no list.

**Weekly recommendations are explicit published runs — not "whatever CSV is newest."**
*Why:* Once I had a stale May report sitting on top of my dashboard while I was making decisions for June. After that I made every weekly run an explicit, dated, archived publication, with staleness warnings if I'm looking at something old.

**AI summarizes evidence. Deterministic code does the math.**
*Why:* The model summarizes earnings calls, news, and filings into a useful read. But the actual price-based calculations stay deterministic. I never want to be in a position where I'm trusting a model on a number.

**Separating strategy lenses.** Each strategy has its own decision logic and either feeds the main board or doesn't.
*Why:* It's the difference between "good stock, wrong entry" and "no edge here." A single blended strength score hides that distinction. Separate strategies make each one inspectable.

## How it's built

- **Frontend:** Server-rendered Jinja2 templates with hand-authored CSS
- **Backend:** Python 3.11 with FastAPI for the app, Typer for jobs
- **Data:** CSV snapshots and JSON manifests today, with Supabase Postgres as the intended system of record (in progress)
- **Hosting:** Railway

The core architecture is candidate-first: prepare features → evaluate strategies → suppress risky candidates → promote to the action board. Each weekly run is a fixed, immutable snapshot, so historical decisions can always be traced.

## What this is not

This is human-in-the-loop decision support for one person — me. Not autonomous trading. Not investment advice. Not built for distribution.

## What I learned

A single "strength score" feels precise, but it hides what actually matters. The product became more useful — and more trustworthy — once I separated *is this a good stock* from *is this a good entry*, and made strategy provenance visible on the surface. One number invites overconfidence; a structured surface invites judgment.

---

*Source code is private. Available on request — reach out via LinkedIn.*
