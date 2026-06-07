#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import pandas as pd
from jinja2 import Template

BASE_CSS = """
  :root {
    --bg: #f4efe6;
    --paper: rgba(255, 250, 242, 0.94);
    --paper-strong: #fffaf2;
    --ink: #17261d;
    --muted: #5f6e65;
    --line: #d8cfc1;
    --green: #1d6e4e;
    --green-soft: #dff1e8;
    --blue: #285d87;
    --blue-soft: #e2eef8;
    --amber: #a7641d;
    --amber-soft: #fff0dd;
    --red: #9d3d31;
    --red-soft: #f8e4df;
    --purple: #5d4aa8;
    --purple-soft: #eee8ff;
    --shadow: 0 18px 44px rgba(23, 38, 29, 0.09);
    --radius-xl: 28px;
    --radius-lg: 22px;
    --radius-md: 18px;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    font-family: "IBM Plex Sans", sans-serif;
    color: var(--ink);
    background:
      radial-gradient(circle at top left, rgba(40,93,135,0.10), transparent 22%),
      radial-gradient(circle at top right, rgba(29,110,78,0.10), transparent 22%),
      linear-gradient(180deg, #f5ecde 0%, var(--bg) 46%, #eee5d9 100%);
  }
  .page {
    max-width: 1380px;
    margin: 0 auto;
    padding: 28px 22px 52px;
  }
  .card {
    background: var(--paper);
    border: 1px solid rgba(216, 207, 193, 0.86);
    box-shadow: var(--shadow);
    border-radius: var(--radius-xl);
    backdrop-filter: blur(6px);
  }
  .panel {
    padding: 22px 24px;
  }
  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
    color: var(--muted);
    font-weight: 700;
    margin-bottom: 10px;
  }
  h1, h2, h3, h4 {
    margin: 0;
    font-family: "Space Grotesk", sans-serif;
    line-height: 1.06;
  }
  h1 { font-size: 42px; }
  h2 { font-size: 28px; }
  h3 { font-size: 20px; }
  h4 { font-size: 16px; }
  .copy, .copy p, .copy li {
    font-size: 15px;
    line-height: 1.64;
    color: #314339;
  }
  .copy p { margin: 0 0 10px; }
  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 18px;
  }
  .chip {
    padding: 9px 13px;
    border-radius: 999px;
    border: 1px solid #e1d7c8;
    background: #f1e9db;
    color: #415046;
    font-size: 13px;
    font-weight: 600;
  }
  .hero {
    display: grid;
    grid-template-columns: 1.2fr 0.95fr;
    gap: 18px;
    margin-bottom: 18px;
  }
  .hero-main, .hero-side {
    padding: 26px 28px;
  }
  .hero-side {
    background: linear-gradient(180deg, rgba(29,110,78,0.98), rgba(22,70,51,0.98));
    color: #f3fff8;
  }
  .posture-card {
    padding: 20px 22px;
    min-height: 0;
  }
  .hero-side .copy, .hero-side .copy p, .hero-side .copy li {
    color: rgba(243,255,248,0.90);
  }
  .two-col {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 18px;
    align-items: start;
  }
  .three-col {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    align-items: start;
  }
  .facts {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
  }
  .fact {
    border-radius: 16px;
    padding: 12px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.72);
  }
  .fact-label {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .fact-value {
    font-size: 18px;
    font-weight: 700;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
  }
  .buy { background: var(--green-soft); color: var(--green); }
  .wait { background: var(--blue-soft); color: var(--blue); }
  .hold { background: var(--amber-soft); color: var(--amber); }
  .avoid { background: var(--red-soft); color: var(--red); }
  .context { background: var(--purple-soft); color: var(--purple); }
  .item-list { display: grid; gap: 12px; margin-top: 14px; }
  .item {
    border-radius: 18px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.62);
    padding: 14px 15px;
  }
  .item strong { display: block; margin-bottom: 6px; }
  .amount {
    margin-top: 8px;
    font-family: "Space Grotesk", sans-serif;
    font-size: 28px;
  }
  .ticker-card {
    padding: 20px;
    display: grid;
    grid-template-columns: 1.14fr 0.86fr;
    gap: 18px;
  }
  .ticker-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    gap: 14px;
    margin-bottom: 12px;
  }
  .ticker-name { font-size: 30px; margin-bottom: 4px; }
  .ticker-meta { color: var(--muted); font-size: 14px; }
  .links, a {
    color: var(--blue);
    text-decoration: none;
    font-weight: 700;
  }
  a:hover { text-decoration: underline; }
  .small-link {
    font-size: 13px;
    font-weight: 700;
  }
  .trade-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin-top: 14px;
  }
  .trade-box {
    border-radius: 16px;
    padding: 12px;
    border: 1px solid var(--line);
    background: rgba(241,233,219,0.75);
  }
  .trade-box span {
    display: block;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .trade-box strong {
    font-family: "Space Grotesk", sans-serif;
    font-size: 20px;
  }
  .chart-shell {
    border-radius: 20px;
    padding: 14px;
    border: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(244,240,232,0.88));
  }
  .chart-caption {
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 13px;
    margin-top: 10px;
  }
  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 10px;
    font-size: 13px;
    color: var(--muted);
  }
  .legend-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .legend-line {
    width: 22px;
    height: 0;
    border-top: 3px solid currentColor;
    display: inline-block;
  }
  .legend-dash {
    width: 22px;
    height: 0;
    border-top: 2px dashed currentColor;
    display: inline-block;
  }
  .axis-text {
    font-size: 11px;
    fill: #7c8a82;
    font-family: "IBM Plex Sans", sans-serif;
  }
  .chart-label {
    font-size: 11px;
    font-weight: 700;
    fill: #425147;
    font-family: "IBM Plex Sans", sans-serif;
  }
  .analysis-block {
    border-radius: 20px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.62);
    padding: 16px;
  }
  .analysis-block h3 { margin-bottom: 10px; }
  .analysis-findings {
    margin: 0 0 10px;
    padding-left: 18px;
  }
  .analysis-findings li { margin-bottom: 6px; }
  .insight-band {
    border-radius: 16px;
    padding: 12px 14px;
    background: #eef4f8;
    border: 1px solid #d4e2ee;
    color: #28425a;
    font-size: 14px;
    line-height: 1.56;
  }
  .notes {
    margin-top: 18px;
    border-radius: 22px;
    padding: 18px 20px;
    background: #1f2d26;
    color: #eef7f1;
  }
  .notes .copy, .notes .copy p, .notes .copy li { color: rgba(238,247,241,0.90); }
  .glossary-entry {
    padding: 18px 0;
    border-bottom: 1px solid var(--line);
  }
  .glossary-entry:target {
    background: #fff6dd;
    border-radius: 14px;
    padding: 18px 16px;
    border: 1px solid #f1dfac;
  }
  .back {
    margin-bottom: 14px;
    display: inline-block;
  }
  .term {
    text-decoration: underline;
    text-decoration-style: dotted;
    text-underline-offset: 3px;
  }
  .hero-title-wrap { max-width: 17ch; }
  .status-line {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
  }
  .kpis {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 14px;
  }
  .kpi {
    border-radius: 18px;
    padding: 16px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.72);
  }
  .kpi-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 30px;
    margin: 6px 0;
  }
  @media (max-width: 1120px) {
    .hero, .two-col, .ticker-card, .grid-2, .three-col { grid-template-columns: 1fr; }
    .facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 720px) {
    .page { padding: 18px 12px 34px; }
    h1 { font-size: 34px; }
    .facts, .trade-strip, .kpis { grid-template-columns: 1fr; }
  }
"""


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <style>{{ css }}</style>
</head>
<body>
  <div class="page">
    {{ body | safe }}
  </div>
</body>
</html>
"""


GLOSSARY = [
    {
        "id": "selective-risk-on",
        "term": "Selective Risk-On",
        "definition": "A market posture where the broad tape is constructive enough to take risk, but not strong enough to buy every apparent breakout without extra discipline.",
        "why": "This affects how aggressive the weekly action list should be. In a selective risk-on tape, patience and entry quality matter more than volume of trades.",
    },
    {
        "id": "refined-score",
        "term": "Refined Score",
        "definition": "A compact ranking helper built from trend, momentum, relative strength, proximity to highs, and penalties for excess volatility or overextension.",
        "why": "It is a supporting ranking signal, not a standalone recommendation. A higher score helps a stock surface, but the final call should still come from the decision basis and entry-quality checks.",
    },
    {
        "id": "decision-basis",
        "term": "Decision Basis",
        "definition": "The named logic behind the recommendation. In this prototype, a decision basis can be a setup family, a risk guardrail, or a context lens.",
        "why": "This prevents us from calling everything a 'strategy' when some rows are really just contextual or risk-management rules.",
    },
    {
        "id": "trade-setup",
        "term": "Trade Setup",
        "definition": "A repeatable short-term trading pattern with entry rules, invalidation logic, time horizon, and a path to historical replay.",
        "why": "This is closer to standard trading language than an invented category label. Examples include constructive pullback continuation or breakout confirmation.",
    },
    {
        "id": "risk-rule",
        "term": "Risk Rule",
        "definition": "A rule that suppresses or modifies action even if a chart looks acceptable.",
        "why": "The clearest example in this MLP is avoiding fresh entries right before earnings. This is not alpha generation by itself; it is damage control.",
    },
    {
        "id": "context-lens",
        "term": "Context Lens",
        "definition": "A row or rule used to interpret the market rather than directly recommend a stock purchase.",
        "why": "The SPY row is a context lens. It helps explain posture and relative strength, but it is not competing with every other stock idea.",
    },
    {
        "id": "relative-strength-vs-spy",
        "term": "Relative Strength vs SPY",
        "definition": "The stock’s 20-day return minus SPY’s 20-day return.",
        "why": "This tells us whether the stock is merely going up with the market or actually acting stronger than the benchmark.",
    },
    {
        "id": "event-risk",
        "term": "Event Risk",
        "definition": "The risk that a scheduled catalyst, most often earnings, dominates the next move and overwhelms the chart setup.",
        "why": "A decent chart can still be a weak weekly entry if a major event is only a few days away.",
    },
    {
        "id": "support",
        "term": "Support",
        "definition": "A price area where the stock has recently found demand or where a key moving average offers structural support.",
        "why": "Support helps anchor entry zones and invalidation levels.",
    },
    {
        "id": "resistance",
        "term": "Resistance",
        "definition": "A price area where the stock previously struggled to move higher or where a breakout trigger sits.",
        "why": "Resistance matters because some setups need confirmation through that level before they deserve capital.",
    },
    {
        "id": "invalidation",
        "term": "Invalidation",
        "definition": "The price condition that tells us the current setup no longer holds.",
        "why": "This is more useful than a vague stop concept because it ties risk management directly to why the trade exists.",
    },
    {
        "id": "atr",
        "term": "ATR",
        "definition": "Average True Range, a volatility proxy based on recent trading ranges and gaps.",
        "why": "ATR helps size targets and buffers so the model does not pretend every stock moves the same way.",
    },
]


NOTES_COPY = [
    "This prototype uses daily OHLCV data and a lightweight earnings snapshot only. It does not yet include point-in-time analyst revisions, transcript deltas, or full filing-change analysis.",
    "The pages are designed to look like product surfaces, but the data coverage is still lean MLP coverage. In production we would keep the same structure and swap in richer evidence modules where data exists.",
]


STRATEGY_META = {
    "constructive-pullback-continuation": {
        "type": "Trade setup",
        "objective": "Buy a leading stock after it cools enough to offer defined risk without losing the uptrend.",
        "challenge_rounds": [
            {
                "pushback": "This could just be disguised momentum chasing.",
                "refinement": "Add an overextension filter so names too far above the 20-day average do not qualify as immediate buys.",
            },
            {
                "pushback": "A pullback can look constructive right before a deeper breakdown.",
                "refinement": "Require price to remain above the 20-day and 50-day averages so the pattern stays trend-following rather than bottom-fishing.",
            },
            {
                "pushback": "A strong chart before earnings can still be a coin flip next week.",
                "refinement": "Let the event-risk guardrail override the setup when earnings are too close.",
            },
            {
                "pushback": "Even good entries can fail in a sloppy market.",
                "refinement": "Condition the setup on market posture so selective tapes demand more patience than broad risk-on tapes.",
            },
        ],
        "decision_rules": [
            "Price above the 20-day and 50-day averages",
            "Positive 20-day relative strength vs SPY",
            "Only modestly extended above the 20-day average",
            "Defined support and a practical invalidation",
        ],
    },
    "breakout-confirmation": {
        "type": "Trade setup",
        "objective": "Wait until a stock proves demand through a trigger level rather than buying a flat or indecisive chart.",
        "challenge_rounds": [
            {
                "pushback": "This can buy too late and sacrifice upside.",
                "refinement": "Accept a slightly higher entry in exchange for fewer false starts.",
            },
            {
                "pushback": "A single breakout day can be noise.",
                "refinement": "Tie the trigger to recent resistance and keep the invalidation near the 20-day average.",
            },
            {
                "pushback": "Confirmation logic can underperform in weak tapes.",
                "refinement": "Treat it more conservatively when market posture is only selective risk-on.",
            },
        ],
        "decision_rules": [
            "Trend still intact",
            "Need price through a breakout trigger",
            "Cancel if the stock loses near-term support before the trigger",
        ],
    },
    "index-trend-follow-through": {
        "type": "Trade setup",
        "objective": "Use a broad-market ETF when the tape is healthy and single-name idiosyncratic risk is unnecessary.",
        "challenge_rounds": [
            {
                "pushback": "This is too generic to be a real strategy.",
                "refinement": "Frame it as an explicit expression choice for market exposure, not as a substitute for all stock selection logic.",
            },
            {
                "pushback": "It may just clone SPY with no edge.",
                "refinement": "Use it as the cleaner alternative when single-name setups are less attractive but broad exposure is still warranted.",
            },
        ],
        "decision_rules": [
            "Broad market ETF above the 20-day and 50-day averages",
            "Controlled volatility",
            "Reasonable entry near trend support",
        ],
    },
    "event-freeze-before-earnings": {
        "type": "Risk rule",
        "objective": "Stop the system from confusing a technically acceptable chart with a good weekly entry right before earnings.",
        "challenge_rounds": [
            {
                "pushback": "This may skip some strong post-earnings winners before the move starts.",
                "refinement": "Accept that missed upside is preferable to turning a weekly process into event gambling by default.",
            },
            {
                "pushback": "Not every earnings event is equally risky.",
                "refinement": "Later versions can add nuance with revision history and prior reaction patterns, but the MLP should use a blunt guardrail first.",
            },
        ],
        "decision_rules": [
            "If earnings are within 7 calendar days, suppress fresh swing entries by default",
            "Allow hold/reassess language instead of forcing a new buy or sell",
        ],
    },
    "benchmark-trend-reference": {
        "type": "Context lens",
        "objective": "Explain the tape so individual stock recommendations feel coherent rather than isolated.",
        "challenge_rounds": [
            {
                "pushback": "Why show SPY at all if the product is about stock picks?",
                "refinement": "Because relative strength, posture, and selectivity decisions need a common benchmark anchor.",
            },
            {
                "pushback": "A benchmark row can distract from actual actions.",
                "refinement": "Keep it explicitly labeled as context, not as a trade recommendation.",
            },
        ],
        "decision_rules": [
            "Benchmark above or below key moving averages sets posture context",
            "Benchmark return anchors relative-strength comparisons",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate product-like HTML pages from MLP outputs.")
    parser.add_argument("--watchlist", default="data/reference/mlp_watchlist.csv")
    parser.add_argument("--prices", default="data/raw/mlp/mlp_prices.csv")
    parser.add_argument("--current", default="data/processed/mlp/mlp_current_recommendations.csv")
    parser.add_argument("--portfolio", default="data/processed/mlp/mlp_backtest_portfolio.csv")
    parser.add_argument("--strategies", default="data/processed/mlp/mlp_backtest_strategies.csv")
    parser.add_argument("--stock_signals", default="data/processed/mlp/mlp_backtest_stock_signals.csv")
    parser.add_argument("--overview", default="docs/design/ux/ux-2026-05-22-weekly-review-mock.html")
    parser.add_argument("--output_dir", default="docs/design/ux")
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def format_pct(value: float, decimals: int = 1) -> str:
    return f"{value * 100:+.{decimals}f}%"


def money(value: float, decimals: int = 0) -> str:
    return f"${value:,.{decimals}f}"


def detail_page_name(prefix: str, slug: str) -> str:
    return f"ux-2026-05-22-{prefix}-{slug}.html"


def overview_link() -> str:
    return "ux-2026-05-22-weekly-review-mock.html"


def glossary_link(term_id: str) -> str:
    return f"{detail_page_name('glossary', 'terms')}#{term_id}"


def market_posture_link() -> str:
    return detail_page_name("market-posture", "selective-risk-on")


def classify_badge(action: str) -> str:
    if action == "Buy now":
        return "buy"
    if action in {"Buy on pullback", "Wait for confirmation"}:
        return "wait"
    if action in {"Hold", "Hold / reassess after earnings"}:
        return "hold"
    if action == "Benchmark reference":
        return "context"
    return "avoid"


def term_link(label: str, term_id: str) -> str:
    return f'<a class="term" href="{glossary_link(term_id)}">{html.escape(label)}</a>'


def basis_slug(row: pd.Series) -> str:
    mapping = {
        "Constructive pullback continuation": "constructive-pullback-continuation",
        "Breakout confirmation": "breakout-confirmation",
        "Index trend follow-through": "index-trend-follow-through",
        "Event freeze before earnings": "event-freeze-before-earnings",
        "Benchmark trend reference": "benchmark-trend-reference",
    }
    return mapping.get(row["strategy_name"], slugify(str(row["strategy_name"])))


def make_chart_geometry(series_values: list[float], width: int, height: int, extra_levels: list[float] | None = None) -> tuple[float, float]:
    extra_levels = extra_levels or []
    values = [v for v in series_values + extra_levels if pd.notna(v)]
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        maximum += 1.0
    pad = (maximum - minimum) * 0.1
    return minimum - pad, maximum + pad


def y_scale(value: float, y_min: float, y_max: float, height: int) -> float:
    return 12 + (height - 24) * (1 - ((value - y_min) / max(y_max - y_min, 1e-9)))


def series_path(values: list[float], y_min: float, y_max: float, width: int, height: int) -> str:
    if len(values) < 2:
        return ""
    pts = []
    for idx, value in enumerate(values):
        x = 42 + idx / (len(values) - 1) * (width - 62)
        y = y_scale(value, y_min, y_max, height)
        pts.append((x, y))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def area_path(line_path: str, width: int, height: int) -> str:
    if not line_path:
        return ""
    return f"{line_path} L {width - 20} {height - 16} L 42 {height - 16} Z"


def chart_svg(price_series: pd.Series, ma_series: pd.Series, annotations: list[dict[str, object]], stroke: str) -> str:
    width, height = 360, 168
    prices = price_series.tolist()
    mas = ma_series.bfill().tolist()
    levels = [a["value"] for a in annotations if a.get("value") is not None]
    y_min, y_max = make_chart_geometry(prices + mas, width, height, levels)
    price_path = series_path(prices, y_min, y_max, width, height)
    ma_path = series_path(mas, y_min, y_max, width, height)
    area = area_path(price_path, width, height)
    left = 42
    right = width - 20
    bottom = height - 16
    top = 12
    y_ticks = [y_max, (y_max + y_min) / 2, y_min]
    x_labels = [
        price_series.index[0].strftime("%b %d"),
        price_series.index[len(price_series) // 2].strftime("%b %d"),
        price_series.index[-1].strftime("%b %d"),
    ]
    x_positions = [left, (left + right) / 2, right]
    annotation_lines = []
    for ann in annotations:
        y = y_scale(float(ann["value"]), y_min, y_max, height)
        annotation_lines.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{ann["color"]}" stroke-dasharray="5 5" stroke-width="1.3" opacity="0.85"></line>'
            f'<text x="{right - 4}" y="{max(top + 10, y - 4):.1f}" text-anchor="end" class="chart-label">{html.escape(str(ann["label"]))}</text>'
        )
    y_tick_html = "".join(
        f'<line x1="{left}" y1="{y_scale(val, y_min, y_max, height):.1f}" x2="{right}" y2="{y_scale(val, y_min, y_max, height):.1f}" stroke="#e2dbcf" stroke-width="1"></line>'
        f'<text x="0" y="{y_scale(val, y_min, y_max, height) + 4:.1f}" class="axis-text">{money(val, 0)}</text>'
        for val in y_ticks
    )
    x_tick_html = "".join(
        f'<text x="{x:.1f}" y="{height - 2}" text-anchor="middle" class="axis-text">{label}</text>'
        for x, label in zip(x_positions, x_labels)
    )
    return f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="{height}" preserveAspectRatio="none" aria-label="Annotated price chart">
      {y_tick_html}
      <line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#d8d0c2" stroke-width="1.2"></line>
      <line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#d8d0c2" stroke-width="1.2"></line>
      <path d="{area}" fill="{stroke}" opacity="0.08"></path>
      <path d="{ma_path}" fill="none" stroke="#c29141" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"></path>
      <path d="{price_path}" fill="none" stroke="{stroke}" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"></path>
      {''.join(annotation_lines)}
      <text x="{right}" y="{top + 10}" text-anchor="end" class="chart-label">Price</text>
      <text x="{right}" y="{top + 26}" text-anchor="end" class="chart-label" fill="#c29141">20D MA</text>
      {x_tick_html}
    </svg>
    """


def regime_from_spy(spy_row: pd.Series, portfolio: pd.DataFrame) -> tuple[str, str, list[tuple[str, str]]]:
    excess_mean = portfolio["excess_return_1w"].mean() if not portfolio.empty else 0.0
    findings = []
    if spy_row["close"] > spy_row["ma_20"] > spy_row["ma_50"]:
        findings.append(("Benchmark trend", "SPY is above both the 20-day and 50-day averages."))
    else:
        findings.append(("Benchmark trend", "SPY is not fully above the short and intermediate trend lines."))
    findings.append(("20-day benchmark return", f"SPY is up {format_pct(spy_row['ret_20d'])} over the last 4 weeks."))
    findings.append(("Replay quality", f"The tiny replay is still only {format_pct(excess_mean, 2)} vs SPY, which argues for selectivity instead of broad aggression."))
    label = "Selective Risk-On" if spy_row["close"] > spy_row["ma_20"] > spy_row["ma_50"] else "Neutral"
    note = (
        "The broad tape is constructive, but the system has not earned the right to act aggressively on every strong chart. We should still favor defined entries, event awareness, and patience."
        if label == "Selective Risk-On"
        else "The market is not strong enough to make stock selection easy, so the system should lean toward waiting and protecting entry quality."
    )
    return label, note, findings


def build_annotations(row: pd.Series) -> list[dict[str, object]]:
    items = [{"label": "Support", "value": row["ma_20"], "color": "#c29141"}]
    if row["action_label"] == "Wait for confirmation":
        items.append({"label": "Trigger", "value": row["high_10"], "color": "#285d87"})
    if row["action_label"] == "Buy now":
        items.append({"label": "Current", "value": row["close"], "color": "#1d6e4e"})
    if row["distance_from_52w_high"] <= 0.18:
        items.append({"label": "52W High", "value": row["high_252"], "color": "#7f6cb6"})
    return items


def card_insight(row: pd.Series) -> str:
    if row["strategy_name"] == "Constructive pullback continuation":
        return (
            f"Trend is intact, the stock beat SPY by {format_pct(row['rs_20d'])} over the last 4 weeks, and price is only {row['extension_vs_ma20'] * 100:.1f}% above the 20-day average. "
            "That makes the entry usable instead of obviously stretched."
        )
    if row["strategy_name"] == "Breakout confirmation":
        return (
            f"The stock is holding trend support, but 4-week relative strength is only {format_pct(row['rs_20d'])}. "
            "This is why the system wants proof through a trigger instead of assuming strength will resume."
        )
    if row["strategy_name"] == "Event freeze before earnings":
        return "The chart is secondary this week because the next scheduled earnings report can dominate the move and invalidate a normal swing setup."
    if row["strategy_name"] == "Index trend follow-through":
        return "This is the cleaner broad-market expression: constructive tape, calmer volatility, and less single-name earnings or narrative risk."
    return "This row is used to interpret the tape rather than to generate a fresh stock trade."


def stock_page_title(row: pd.Series) -> str:
    return f"{row['ticker']} - {row['display_name']}"


def stock_page_file(row: pd.Series) -> str:
    return detail_page_name("stock-detail", row["ticker"].lower())


def strategy_page_file(row: pd.Series) -> str:
    return detail_page_name("strategy-detail", basis_slug(row))


def build_card(row: pd.Series, prices: pd.DataFrame) -> dict[str, object]:
    history = prices[prices["ticker"] == row["ticker"]].sort_values("date").tail(60).copy()
    history["ma_20"] = history["close"].rolling(20).mean().bfill()
    history = history.set_index("date")
    stroke = "#1d6e4e" if row["action_label"] == "Buy now" else "#285d87" if row["action_label"] in {"Buy on pullback", "Wait for confirmation"} else "#a7641d"
    basis_label = (
        "Trade setup" if row["basis_type"] == "Setup family"
        else "Risk rule" if row["basis_type"] == "Risk guardrail"
        else "Context lens"
    )
    if row["strategy_name"] == "Constructive pullback continuation":
        why_now = "Leadership is positive, the uptrend is intact, and the entry is still close enough to support to define risk."
        why_not_stronger = "This is still a single-stock swing idea. If it loses the invalidation level, the edge disappears quickly."
    elif row["strategy_name"] == "Breakout confirmation":
        why_now = "The stock is still on the list because the broader trend has not broken."
        why_not_stronger = "It is not a buy yet because price still needs to clear resistance and prove demand."
    elif row["strategy_name"] == "Event freeze before earnings":
        why_now = "The stock remains relevant because it could become actionable after the event."
        why_not_stronger = "Fresh capital is paused because earnings are close enough to dominate the next move."
    elif row["strategy_name"] == "Index trend follow-through":
        why_now = "This is the calmer way to express a constructive market tape."
        why_not_stronger = "It is broad exposure, not a high-conviction single-name edge."
    else:
        why_now = "This row helps frame the tape for the rest of the watchlist."
        why_not_stronger = "It should not be treated as a primary stock pick."
    return {
        "ticker": row["ticker"],
        "company": row["display_name"],
        "badge_class": classify_badge(row["action_label"]),
        "action": row["action_label"],
        "last_close": money(row["close"], 2),
        "horizon": row["horizon"],
        "event_risk": row["event_risk"],
        "refined_score": int(row["refined_score"]),
        "basis_type": row["basis_type"],
        "basis_label": basis_label,
        "strategy_name": row["strategy_name"],
        "stock_href": stock_page_file(row),
        "strategy_href": strategy_page_file(row),
        "rs_20d": "In line" if abs(row["rs_20d"]) < 0.001 else format_pct(row["rs_20d"]),
        "insight": card_insight(row),
        "why_now": why_now,
        "why_not_stronger": why_not_stronger,
        "entry_label": row["entry_label"],
        "entry_value": row["entry_value"],
        "stop_label": row["stop_label"],
        "stop_value": row["stop_value"],
        "target_label": row["target_label"],
        "target_value": row["target_value"],
        "stroke": stroke,
        "chart": chart_svg(history["close"], history["ma_20"], build_annotations(row), stroke),
        "chart_caption_left": f"Support near {money(row['ma_20'], 0)}",
        "chart_caption_right": f"20D vs SPY {('In line' if abs(row['rs_20d']) < 0.001 else format_pct(row['rs_20d']))}",
    }


def deployment_items(cards: list[dict[str, object]]) -> list[dict[str, str]]:
    buys = [c for c in cards if c["action"] == "Buy now" and c["basis_type"] == "Setup family"]
    waits = [c for c in cards if c["action"] in {"Buy on pullback", "Wait for confirmation"}]
    items = []
    for idx, card in enumerate(buys[:2]):
        items.append(
            {
                "title": f"Start with {card['ticker']}",
                "body": f"{card['ticker']} is a live setup-family match with a defined entry box, invalidation, and horizon. This is where fresh cash deserves attention first.",
                "amount": "25%" if idx == 0 else "20%",
            }
        )
    if waits:
        items.append(
            {
                "title": f"Keep a watch order on {waits[0]['ticker']}",
                "body": f"{waits[0]['ticker']} is interesting but has not earned immediate action. The product should make patience feel explicit rather than vague.",
                "amount": "15%",
            }
        )
    items.append(
        {
            "title": "Keep unforced cash",
            "body": "The product should normalize leaving capital undeployed when the market posture is only selective risk-on and not every chart has a trustworthy entry.",
            "amount": "40%",
        }
    )
    return items[:4]


def backtest_items(strategies: pd.DataFrame, portfolio: pd.DataFrame) -> list[dict[str, str]]:
    items = []
    excess = portfolio["excess_return_1w"].mean() if not portfolio.empty else 0.0
    items.append(
        {
            "title": "The replay still demands humility",
            "body": f"The top-two portfolio is only {format_pct(excess, 2)} vs SPY on average, so the product should surface conviction carefully rather than implying the model is already proven.",
        }
    )
    cp = strategies[strategies["strategy_name"] == "Constructive pullback continuation"]
    if not cp.empty:
        row = cp.iloc[0]
        items.append(
            {
                "title": "A clean idea can still be weak historically",
                "body": f"`Constructive pullback continuation` is conceptually strong, but in this tiny replay it only delivered {row['avg_fwd_1w_return']:.2%} with a {row['win_rate']:.0%} win rate. That is exactly why the strategy detail page needs to show both logic and evidence.",
            }
        )
    items.append(
        {
            "title": "Backtests are still technical-only",
            "body": "The current replay does not yet include historical revision data, transcript changes, or point-in-time filing deltas. Strategy pages should say that clearly instead of overclaiming edge.",
        }
    )
    return items


def render_overview(
    merged: pd.DataFrame,
    prices: pd.DataFrame,
    watchlist: pd.DataFrame,
    portfolio: pd.DataFrame,
    strategies: pd.DataFrame,
) -> str:
    cards = [build_card(row, prices) for _, row in merged.iterrows()]
    regime_label, regime_note, _ = regime_from_spy(merged[merged["ticker"] == "SPY"].iloc[0], portfolio)
    right_cards = []
    for card in cards:
        right_cards.append(
            f"""
            <article class="card ticker-card">
              <div>
                <div class="ticker-header">
                  <div>
                    <div class="ticker-name"><a href="{card['stock_href']}">{card['ticker']}</a></div>
                    <div class="ticker-meta">{html.escape(card['company'])}</div>
                  </div>
                  <div class="badge {card['badge_class']}">{html.escape(card['action'])}</div>
                </div>
                <div class="facts">
                  <div class="fact"><div class="fact-label">Last Close</div><div class="fact-value">{card['last_close']}</div></div>
                  <div class="fact"><div class="fact-label">{term_link('4W vs SPY', 'relative-strength-vs-spy')}</div><div class="fact-value">{card['rs_20d']}</div></div>
                  <div class="fact"><div class="fact-label">{term_link('Event Risk', 'event-risk')}</div><div class="fact-value">{html.escape(card['event_risk'])}</div></div>
                  <div class="fact"><div class="fact-label">Time Horizon</div><div class="fact-value">{html.escape(card['horizon'])}</div></div>
                  <div class="fact"><div class="fact-label">{term_link('Refined Score', 'refined-score')}</div><div class="fact-value">{card['refined_score']}</div></div>
                </div>
                <div class="copy"><strong>{card['basis_label']}:</strong> <a href="{card['strategy_href']}">{html.escape(card['strategy_name'])}</a></div>
                <div class="copy"><a class="small-link" href="{glossary_link('decision-basis')}">What is a decision basis?</a></div>
                <div class="copy" style="margin-top:10px;">
                  <p><strong>Why this week:</strong> {html.escape(card['why_now'])}</p>
                  <p><strong>Why not stronger:</strong> {html.escape(card['why_not_stronger'])}</p>
                </div>
                <div class="trade-strip">
                  <div class="trade-box"><span>{html.escape(card['entry_label'])}</span><strong>{html.escape(card['entry_value'])}</strong></div>
                  <div class="trade-box"><span>{html.escape(card['stop_label'])}</span><strong>{html.escape(card['stop_value'])}</strong></div>
                  <div class="trade-box"><span>{html.escape(card['target_label'])}</span><strong>{html.escape(card['target_value'])}</strong></div>
                </div>
              </div>
              <div class="chart-shell">
                {card['chart']}
                <div class="legend">
                  <div class="legend-item" style="color:{card['stroke']};"><span class="legend-line"></span><span>Price</span></div>
                  <div class="legend-item" style="color:#c29141;"><span class="legend-line"></span><span>20D average</span></div>
                  <div class="legend-item" style="color:#7c8a82;"><span class="legend-dash"></span><span>Annotated levels</span></div>
                </div>
                <div class="chart-caption">
                  <div>{html.escape(card['chart_caption_left'])}</div>
                  <div>{html.escape(card['chart_caption_right'])}</div>
                </div>
              </div>
            </article>
            """
        )

    body = f"""
    <section class="card panel" style="margin-bottom:18px;">
      <div class="eyebrow">Weekly Equity Intelligence</div>
      <div style="display:flex;justify-content:space-between;gap:16px;align-items:end;flex-wrap:wrap;">
        <div>
          <h1>Weekly Review</h1>
          <div class="copy"><p>Week of {merged['date'].max().date().isoformat()}</p></div>
        </div>
        <div class="chips" style="margin-top:0;">
          <div class="chip">Universe: {html.escape(', '.join(watchlist['ticker'].tolist()))}</div>
          <div class="chip">Mode: Lean MLP</div>
        </div>
      </div>
    </section>

    <section class="grid-2" style="margin-bottom:18px;">
      <div class="card hero-side posture-card">
        <div class="eyebrow">Market Posture</div>
        <div class="status-line">
          <div class="badge context"><a style="color:inherit;text-decoration:none;" href="{market_posture_link()}">{html.escape(regime_label)}</a></div>
          <a class="small-link" style="color:#f3fff8;" href="{market_posture_link()}">View posture analysis</a>
        </div>
        <div class="copy" style="margin-top:12px;"><p>{html.escape(regime_note)}</p></div>
      </div>
      <div class="card panel">
        <div class="eyebrow">If Fresh Cash Arrived</div>
        <h2>How the week should be broken down</h2>
        <div class="copy"><p>Start from market posture, then allocate only to the names with clean enough entries. Cash discipline is part of the system, not an afterthought.</p></div>
        <div class="item-list">
          {''.join(f'<div class="item"><strong>{html.escape(item["title"])}</strong><div class="copy">{html.escape(item["body"])}</div><div class="amount">{html.escape(item["amount"])}</div></div>' for item in deployment_items(cards))}
        </div>
      </div>
    </section>

    <section class="card panel" style="margin-bottom:18px;">
      <div class="eyebrow">Weekly Stock Decisions</div>
      <h2>Why each stock is recommended, watched, or paused</h2>
      <div class="copy"><p>This is the main decision board. Read it as: why act now, why wait, and what exactly would need to happen next.</p></div>
    </section>

    <section style="display:grid;gap:16px;">
      {''.join(right_cards)}
    </section>

    <section class="card panel" style="margin-top:18px;">
      <div class="eyebrow">Backtest Learnings</div>
      <h2>What the replay is telling us about the logic</h2>
      <div class="copy"><p>Backtests belong after the weekly board, not before it. Their role is to calibrate trust in the logic that generated the actions above.</p></div>
      <div class="item-list">
        {''.join(f'<div class="item"><strong>{html.escape(item["title"])}</strong><div class="copy">{html.escape(item["body"])}</div></div>' for item in backtest_items(strategies, portfolio))}
      </div>
    </section>

    <section class="notes">
      <div class="eyebrow" style="color:rgba(238,247,241,0.72);">Notes (won't show in Prod)</div>
      <div class="copy">
        <ul>
          {''.join(f'<li>{html.escape(note)}</li>' for note in NOTES_COPY)}
        </ul>
      </div>
    </section>
    """
    return Template(PAGE_TEMPLATE).render(title="Weekly Equity Intelligence", css=BASE_CSS, body=body)


def render_market_posture_page(spy_row: pd.Series, portfolio: pd.DataFrame) -> str:
    label, note, findings = regime_from_spy(spy_row, portfolio)
    kpis = [
        ("SPY vs 20D MA", money(spy_row["close"] - spy_row["ma_20"], 1)),
        ("SPY vs 50D MA", money(spy_row["close"] - spy_row["ma_50"], 1)),
        ("4W SPY Return", format_pct(spy_row["ret_20d"])),
    ]
    body = f"""
    <a class="back" href="{overview_link()}">&#8592; Back to weekly overview</a>
    <section class="card panel">
      <div class="eyebrow">Market Posture Detail</div>
      <div class="badge context">{html.escape(label)}</div>
      <h1>{html.escape(label)}</h1>
      <div class="copy" style="margin-top:12px;"><p>{html.escape(note)}</p></div>
      <div class="kpis">
        {''.join(f'<div class="kpi"><div class="fact-label">{html.escape(k)}</div><div class="kpi-value">{html.escape(v)}</div></div>' for k, v in kpis)}
      </div>
    </section>
    <section class="grid-2">
      <div class="card panel">
        <div class="eyebrow">Observed Findings</div>
        <h2>Why the posture is not fully aggressive</h2>
        <div class="item-list">
          {''.join(f'<div class="item"><strong>{html.escape(k)}</strong><div class="copy">{html.escape(v)}</div></div>' for k, v in findings)}
        </div>
      </div>
      <div class="card panel">
        <div class="eyebrow">Decision Consequence</div>
        <h2>How this changes weekly actions</h2>
        <div class="copy">
          <ul>
            <li>Prefer defined entries over chasing raw strength.</li>
            <li>Allow cash to remain undeployed when charts are merely acceptable rather than compelling.</li>
            <li>Give more weight to event risk and invalidation clarity than you would in a fully risk-on tape.</li>
          </ul>
        </div>
      </div>
    </section>
    <section class="notes">
      <div class="eyebrow" style="color:rgba(238,247,241,0.72);">Notes (won't show in Prod)</div>
      <div class="copy">
        <ul>
          <li>This posture call is currently based on benchmark trend plus replay quality. In production, breadth and sector leadership should also feed into it.</li>
        </ul>
      </div>
    </section>
    """
    return Template(PAGE_TEMPLATE).render(title="Market posture detail", css=BASE_CSS, body=body)


def render_glossary_page() -> str:
    entries = []
    for entry in GLOSSARY:
        entries.append(
            f"""
            <div class="glossary-entry" id="{entry['id']}">
              <div class="eyebrow">Glossary</div>
              <h2>{html.escape(entry['term'])}</h2>
              <div class="copy" style="margin-top:10px;">
                <p><strong>Definition:</strong> {html.escape(entry['definition'])}</p>
                <p><strong>Why it matters here:</strong> {html.escape(entry['why'])}</p>
              </div>
            </div>
            """
        )
    body = f"""
    <a class="back" href="{overview_link()}">&#8592; Back to weekly overview</a>
    <section class="card panel">
      <div class="eyebrow">Glossary</div>
      <h1>Terms used on the page</h1>
      <div class="copy"><p>The production product should never force you to guess what a label means. Every important term on the weekly overview can link here.</p></div>
      {''.join(entries)}
    </section>
    """
    return Template(PAGE_TEMPLATE).render(title="Glossary", css=BASE_CSS, body=body)


def analysis_block(title: str, findings: list[str], insight: str) -> str:
    return f"""
    <div class="analysis-block">
      <h3>{html.escape(title)}</h3>
      <ul class="analysis-findings">
        {''.join(f'<li>{html.escape(item)}</li>' for item in findings)}
      </ul>
      <div class="insight-band"><strong>Insight:</strong> {html.escape(insight)}</div>
    </div>
    """


def stock_analysis_sections(row: pd.Series) -> list[str]:
    close = row["close"]
    trend_findings = [
        f"Price is {money(close, 2)} versus a 20-day average of {money(row['ma_20'], 2)} and a 50-day average of {money(row['ma_50'], 2)}.",
        "Trend alignment is positive." if close > row["ma_20"] > row["ma_50"] else "Trend alignment is mixed or weakening.",
        f"Price is {row['distance_from_52w_high'] * 100:.1f}% below the 52-week high.",
    ]
    trend_insight = (
        "The stock still has a live uptrend structure." if close > row["ma_20"] > row["ma_50"] else "The chart no longer gives the clean structure we want for a fresh long."
    )
    rs_findings = [
        f"20-day return is {format_pct(row['ret_20d'])}.",
        f"20-day relative strength versus SPY is {'In line' if abs(row['rs_20d']) < 0.001 else format_pct(row['rs_20d'])}.",
        f"5-day return is {format_pct(row['ret_5d'])}.",
    ]
    rs_insight = (
        "The stock is acting like a near-term leader." if row["rs_20d"] > 0.03 else
        "The stock is not showing enough leadership yet to justify a blind entry."
    )
    geometry_findings = [
        f"Price is {row['extension_vs_ma20'] * 100:.1f}% above the 20-day average.",
        f"Recent support sits near {money(max(row['ma_20'], row['low_10']), 0)}.",
        f"Recent resistance / trigger sits near {money(row['high_10'], 0)}.",
    ]
    geometry_insight = (
        "The entry is close enough to support to define risk cleanly."
        if row["strategy_name"] == "Constructive pullback continuation"
        else "The geometry says wait: either price needs a reset or it needs to prove itself through resistance."
    )
    risk_findings = [
        f"ATR is about {row['atr_pct'] * 100:.1f}% of price.",
        f"Event risk is marked {row['event_risk']}.",
        f"Current invalidation on the page is {row['stop_value']}.",
    ]
    risk_insight = (
        "Risk is manageable for a 1-3 week swing." if row["event_risk"] == "Low" and row["atr_pct"] < 0.05 else
        "The risk profile argues for either patience or smaller confidence."
    )
    event_findings = [
        "No near-term scheduled earnings event is constraining the setup." if row["event_risk"] == "Low" else f"Upcoming earnings are only {int(row['days_to_earnings'])} days away.",
        "This MLP does not yet include transcripts, estimate revisions, or filing deltas.",
    ]
    event_insight = (
        "Without event pressure, the chart can drive the call." if row["event_risk"] == "Low" else
        "The event calendar matters more than the chart for the next few sessions."
    )
    return [
        analysis_block("Trend structure analysis", trend_findings, trend_insight),
        analysis_block("Relative strength analysis", rs_findings, rs_insight),
        analysis_block("Entry geometry analysis", geometry_findings, geometry_insight),
        analysis_block("Risk and volatility analysis", risk_findings, risk_insight),
        analysis_block("Event and data coverage analysis", event_findings, event_insight),
    ]


def synthesis_points(row: pd.Series) -> list[str]:
    if row["strategy_name"] == "Constructive pullback continuation":
        return [
            "Multiple findings agree that the stock is strong without being obviously overheated: trend is intact, relative strength is positive, and support is still nearby.",
            "That combination is why the page says `Buy now` rather than `Wait for confirmation`.",
            "The entry zone sits near current price because the edge depends on continuing strength from support, not on a deep reset.",
        ]
    if row["strategy_name"] == "Breakout confirmation":
        return [
            "Trend is intact, but the stock is not proving leadership strongly enough yet.",
            "That is why the system gives you a trigger price instead of a discretionary interpretation.",
            "The target is only relevant if the breakout trigger is reclaimed first.",
        ]
    if row["strategy_name"] == "Event freeze before earnings":
        return [
            "The chart is not the primary driver of the next move because earnings are too close.",
            "That is why the page suppresses a new buy and instead tells you when to revisit the name.",
        ]
    if row["strategy_name"] == "Index trend follow-through":
        return [
            "The ETF gives you constructive exposure without forcing a single-stock narrative.",
            "This is useful when broad conditions are fine but individual stock edges are mixed.",
        ]
    return [
        "This row is designed to explain the tape, not to create a fresh stock action by itself."
    ]


def render_stock_detail(row: pd.Series, prices: pd.DataFrame, stock_signals: pd.DataFrame) -> str:
    history = prices[prices["ticker"] == row["ticker"]].sort_values("date").tail(60).copy()
    history["ma_20"] = history["close"].rolling(20).mean().bfill()
    history = history.set_index("date")
    stroke = "#1d6e4e" if row["action_label"] == "Buy now" else "#285d87" if row["action_label"] in {"Buy on pullback", "Wait for confirmation"} else "#a7641d"
    chart = chart_svg(history["close"], history["ma_20"], build_annotations(row), stroke)
    sections = "".join(stock_analysis_sections(row))
    synthesis = "".join(f"<li>{html.escape(point)}</li>" for point in synthesis_points(row))
    ticker_replay = stock_signals[
        (stock_signals["ticker"] == row["ticker"]) & (stock_signals["strategy_name"] == row["strategy_name"])
    ].copy()
    if not ticker_replay.empty:
        replay_obs = int(ticker_replay["fwd_1w_return"].count())
        replay_avg = ticker_replay["fwd_1w_return"].mean()
        replay_win = (ticker_replay["fwd_1w_return"] > 0).mean()
        replay_line = (
            f"This same decision basis appeared {replay_obs} times for {row['ticker']} in the replay window, with an average 1-week return of "
            f"{replay_avg:.2%} and a win rate of {replay_win:.0%}."
        )
    else:
        replay_line = "This exact stock-plus-basis combination did not appear enough times in the replay window to summarize responsibly."
    basis_label = (
        "Trade setup" if row["basis_type"] == "Setup family"
        else "Risk rule" if row["basis_type"] == "Risk guardrail"
        else "Context lens"
    )
    body = f"""
    <a class="back" href="{overview_link()}">&#8592; Back to weekly overview</a>
    <section class="card panel">
      <div class="eyebrow">Stock Detail</div>
      <div class="status-line">
        <div class="badge {classify_badge(row['action_label'])}">{html.escape(row['action_label'])}</div>
        <a class="small-link" href="{strategy_page_file(row)}">{html.escape(basis_label)}: {html.escape(row['strategy_name'])}</a>
      </div>
      <h1>{html.escape(stock_page_title(row))}</h1>
      <div class="copy" style="margin-top:12px;">
        <p>{html.escape(card_insight(row))}</p>
      </div>
      <div class="facts" style="margin-top:16px;">
        <div class="fact"><div class="fact-label">{term_link('Refined Score', 'refined-score')}</div><div class="fact-value">{int(row['refined_score'])}</div></div>
        <div class="fact"><div class="fact-label">{term_link('Relative Strength vs SPY', 'relative-strength-vs-spy')}</div><div class="fact-value">{'In line' if abs(row['rs_20d']) < 0.001 else format_pct(row['rs_20d'])}</div></div>
        <div class="fact"><div class="fact-label">{term_link('Event Risk', 'event-risk')}</div><div class="fact-value">{html.escape(row['event_risk'])}</div></div>
        <div class="fact"><div class="fact-label">Time Horizon</div><div class="fact-value">{html.escape(row['horizon'])}</div></div>
        <div class="fact"><div class="fact-label">{term_link('Decision Basis', 'decision-basis')}</div><div class="fact-value">{html.escape(basis_label)}</div></div>
      </div>
      <div class="trade-strip">
        <div class="trade-box"><span>{html.escape(row['entry_label'])}</span><strong>{html.escape(row['entry_value'])}</strong></div>
        <div class="trade-box"><span>{html.escape(row['stop_label'])}</span><strong>{html.escape(row['stop_value'])}</strong></div>
        <div class="trade-box"><span>{html.escape(row['target_label'])}</span><strong>{html.escape(row['target_value'])}</strong></div>
      </div>
    </section>

    <section class="card panel">
      <div class="eyebrow">Annotated Chart</div>
      <h2>What the chart is actually saying</h2>
      <div class="copy"><p>This chart is here because the page is making a timing call. The annotations highlight the specific price areas driving that call instead of leaving you to infer them from a generic sparkline.</p></div>
      <div class="chart-shell" style="margin-top:14px;">
        {chart}
        <div class="legend">
          <div class="legend-item" style="color:{stroke};"><span class="legend-line"></span><span>Price</span></div>
          <div class="legend-item" style="color:#c29141;"><span class="legend-line"></span><span>20D average</span></div>
          <div class="legend-item" style="color:#7c8a82;"><span class="legend-dash"></span><span>Support / resistance / 52W high markers</span></div>
        </div>
      </div>
    </section>

    <section class="card panel">
      <div class="eyebrow">Analysis Stack</div>
      <h2>Findings, then insight</h2>
      <div class="three-col" style="margin-top:14px;">{sections}</div>
    </section>

    <section class="grid-2">
      <div class="card panel">
        <div class="eyebrow">Cross-Signal Synthesis</div>
        <h2>Insights from multiple findings</h2>
        <div class="copy"><ul>{synthesis}</ul></div>
      </div>
      <div class="card panel">
        <div class="eyebrow">Recommendation Logic</div>
        <h2>Why this page lands on {html.escape(row['action_label'])}</h2>
        <div class="copy">
          <p><strong>Why this action:</strong> {html.escape(row['observed_reason'])}</p>
          <p><strong>Why these prices:</strong> the entry box is tied to the current decision basis, the invalidation is tied to where that basis breaks, and the target is a first review zone based on recent volatility rather than a claim about the ultimate top.</p>
          <p><strong>What would change the call:</strong> a loss of the invalidation level, a meaningful deterioration in relative strength, or a new event that changes the next one to three weeks.</p>
        </div>
      </div>
    </section>

    <section class="card panel">
      <div class="eyebrow">Single-Stock Replay</div>
      <h2>What a {html.escape(row['ticker'])}-only backtest validates</h2>
      <div class="copy">
        <p>{html.escape(replay_line)}</p>
        <p>A single-stock replay does not prove universal edge. What it validates is whether this specific trade setup tends to work on this specific name, which matters because some setups are stock-dependent. That is useful for sizing trust in names like TSLA that have their own behavioral profile.</p>
      </div>
    </section>

    <section class="notes">
      <div class="eyebrow" style="color:rgba(238,247,241,0.72);">Notes (won't show in Prod)</div>
      <div class="copy">
        <ul>
          <li>This page is showing the current lean-MLP analysis stack honestly. Fundamental trend, revision history, and transcript sections will be richer only after those datasets are wired in.</li>
          <li>The production page should keep the same structure: findings by analysis module, then cross-signal insight, then recommendation logic.</li>
        </ul>
      </div>
    </section>
    """
    return Template(PAGE_TEMPLATE).render(title=stock_page_title(row), css=BASE_CSS, body=body)


def render_strategy_detail(strategy_row: pd.Series, merged: pd.DataFrame) -> str:
    slug = slugify(strategy_row["strategy_name"])
    key_map = {
        "constructive-pullback-continuation": "constructive-pullback-continuation",
        "breakout-confirmation": "breakout-confirmation",
        "index-trend-follow-through": "index-trend-follow-through",
        "event-freeze-before-earnings": "event-freeze-before-earnings",
        "benchmark-trend-reference": "benchmark-trend-reference",
    }
    meta = STRATEGY_META.get(key_map.get(slug, slug), {"type": "Decision basis", "objective": "Explain the logic behind this basis.", "challenge_rounds": [], "decision_rules": []})
    matches = merged[merged["strategy_name"] == strategy_row["strategy_name"]][["ticker", "action_label", "entry_value"]]
    challenge_html = "".join(
        f'<div class="item"><strong>Challenge {idx + 1}</strong><div class="copy"><p><strong>Pushback:</strong> {html.escape(round_data["pushback"])}</p><p><strong>Refinement:</strong> {html.escape(round_data["refinement"])}</p></div></div>'
        for idx, round_data in enumerate(meta["challenge_rounds"])
    )
    matches_html = "".join(
        f"<li><a href=\"{detail_page_name('stock-detail', m.ticker.lower())}\">{html.escape(m.ticker)}</a>: {html.escape(m.action_label)} with trigger {html.escape(str(m.entry_value))}</li>"
        for m in matches.itertuples(index=False)
    ) or "<li>No current live matches this week.</li>"
    body = f"""
    <a class="back" href="{overview_link()}">&#8592; Back to weekly overview</a>
    <section class="card panel">
      <div class="eyebrow">Decision Basis Detail</div>
      <div class="badge context">{html.escape(meta['type'])}</div>
      <h1>{html.escape(strategy_row['strategy_name'])}</h1>
      <div class="copy" style="margin-top:12px;">
        <p><strong>Objective:</strong> {html.escape(meta['objective'])}</p>
      </div>
      <div class="kpis">
        <div class="kpi"><div class="fact-label">Observations</div><div class="kpi-value">{int(strategy_row.get('observations', 0) if pd.notna(strategy_row.get('observations', 0)) else 0)}</div></div>
        <div class="kpi"><div class="fact-label">Avg 1W Return</div><div class="kpi-value">{('N/A' if pd.isna(strategy_row.get('avg_fwd_1w_return')) else f"{strategy_row['avg_fwd_1w_return']:.2%}")}</div></div>
        <div class="kpi"><div class="fact-label">Win Rate</div><div class="kpi-value">{('N/A' if pd.isna(strategy_row.get('win_rate')) else f"{strategy_row['win_rate']:.0%}")}</div></div>
      </div>
    </section>

    <section class="grid-2">
      <div class="card panel">
        <div class="eyebrow">What We Challenged</div>
        <h2>Adversarial refinement</h2>
        <div class="item-list">{challenge_html}</div>
      </div>
      <div class="card panel">
        <div class="eyebrow">Current Rule Spine</div>
        <h2>What survives after that debate</h2>
        <div class="copy">
          <ul>
            {''.join(f'<li>{html.escape(rule)}</li>' for rule in meta['decision_rules'])}
          </ul>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <div class="card panel">
        <div class="eyebrow">Current Live Matches</div>
        <h2>Where this basis is firing now</h2>
        <div class="copy"><ul>{matches_html}</ul></div>
      </div>
      <div class="card panel">
        <div class="eyebrow">How to Read the Replay</div>
        <h2>Backtest interpretation</h2>
        <div class="copy">
          <p>The replay is a measurement aid, not a seal of approval. If the basis has poor historical outcomes, that should reduce trust even if the logic sounds appealing. If it has decent outcomes, that still does not eliminate the need for broader data coverage.</p>
          <p>This page exists so you can challenge both the idea and the evidence before you act on real money.</p>
        </div>
      </div>
    </section>

    <section class="notes">
      <div class="eyebrow" style="color:rgba(238,247,241,0.72);">Notes (won't show in Prod)</div>
      <div class="copy">
        <ul>
          <li>The weakest part of the earlier version was pretending every label was a strategy. This page now distinguishes setup families, risk guardrails, and context lenses explicitly.</li>
          <li>Production should keep this adversarial section in spirit, even if the wording becomes tighter.</li>
        </ul>
      </div>
    </section>
    """
    return Template(PAGE_TEMPLATE).render(title=strategy_row["strategy_name"], css=BASE_CSS, body=body)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    watchlist = pd.read_csv(args.watchlist)
    prices = pd.read_csv(args.prices, parse_dates=["date"])
    current = pd.read_csv(args.current, parse_dates=["date", "next_earnings_date"])
    portfolio = pd.read_csv(args.portfolio)
    strategies = pd.read_csv(args.strategies)
    stock_signals = pd.read_csv(args.stock_signals, parse_dates=["date"])

    merged = current.merge(watchlist[["ticker", "display_name"]], on="ticker", how="left")
    merged = merged.sort_values(["action_rank", "refined_score"], ascending=[True, False])

    for pattern in ["ux-2026-05-22-stock-detail-*.html", "ux-2026-05-22-strategy-detail-*.html", "ux-2026-05-22-market-posture-*.html", "ux-2026-05-22-glossary-*.html"]:
        for existing in output_dir.glob(pattern):
            existing.unlink()

    overview_html = render_overview(merged, prices, watchlist, portfolio, strategies)
    Path(args.overview).write_text(overview_html)

    market_html = render_market_posture_page(merged[merged["ticker"] == "SPY"].iloc[0], portfolio)
    (output_dir / detail_page_name("market-posture", "selective-risk-on")).write_text(market_html)

    glossary_html = render_glossary_page()
    (output_dir / detail_page_name("glossary", "terms")).write_text(glossary_html)

    for _, row in merged.iterrows():
        (output_dir / stock_page_file(row)).write_text(render_stock_detail(row, prices, stock_signals))

    strategy_stats = {row["strategy_name"]: row for _, row in strategies.iterrows()}
    seen = set()
    for _, sample in merged.iterrows():
        name = sample["strategy_name"]
        if name in seen:
            continue
        seen.add(name)
        stats_row = strategy_stats.get(name)
        if stats_row is not None:
            payload = pd.Series({**sample.to_dict(), **stats_row.to_dict()})
        else:
            payload = pd.Series({**sample.to_dict(), "observations": 0, "avg_fwd_1w_return": float("nan"), "win_rate": float("nan")})
        (output_dir / strategy_page_file(sample)).write_text(render_strategy_detail(payload, merged))

    print(f"Wrote overview page to {args.overview}")
    print(f"Wrote glossary page to {output_dir / detail_page_name('glossary', 'terms')}")
    print(f"Wrote market posture page to {output_dir / detail_page_name('market-posture', 'selective-risk-on')}")
    print(f"Wrote stock detail pages to {output_dir}")
    print(f"Wrote decision-basis detail pages to {output_dir}")


if __name__ == "__main__":
    main()
