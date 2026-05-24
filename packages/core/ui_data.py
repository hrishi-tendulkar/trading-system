from __future__ import annotations


def sample_weekly_review() -> dict[str, object]:
    return {
        "title": "Weekly review shell",
        "summary": "This scaffold is ready to switch from sample payloads to published run data once the database and jobs are wired.",
        "facts": [
            {"label": "As of", "value": "2026-05-24"},
            {"label": "Market posture", "value": "Selective risk-on"},
            {"label": "Active names", "value": "52"},
            {"label": "Published run", "value": "Placeholder"},
        ],
        "posture": {
            "title": "Selective risk-on",
            "summary": "Leadership is healthy enough for buying, but the bar stays high and broken setups should still be cut quickly.",
            "points": [
                "Fresh capital should stay concentrated in top-ranked names.",
                "Weak relative-strength laggards should not be force-owned.",
                "Event risk remains a real filter around earnings-heavy names.",
            ],
        },
        "board": [
            {
                "ticker": "NVDA",
                "company": "NVIDIA",
                "action": "Buy candidate",
                "badge_class": "buy",
                "thesis": "Leadership-quality name with strong relative strength and broad demand support.",
                "note": "Good example of a top-ranked name once real score components are connected.",
            },
            {
                "ticker": "CRM",
                "company": "Salesforce",
                "action": "Watch for entry",
                "badge_class": "wait",
                "thesis": "Constructive structure, but not yet clean enough to warrant an aggressive entry.",
                "note": "Useful example of a patient, setup-driven action label.",
            },
            {
                "ticker": "TSLA",
                "company": "Tesla",
                "action": "Hold",
                "badge_class": "hold",
                "thesis": "Name stays interesting, but the system should separate conviction from tactical cleanup.",
                "note": "Represents a case where existing holders and new buyers may need different framing.",
            },
            {
                "ticker": "SNOW",
                "company": "Snowflake",
                "action": "Avoid / no action",
                "badge_class": "avoid",
                "thesis": "Incomplete or weak setup quality should be reflected clearly rather than hidden behind optimism.",
                "note": "Represents the kind of suppressed output the publish rules should handle honestly.",
            },
        ],
    }


def sample_daily_digest() -> dict[str, object]:
    return {
        "title": "Daily digest shell",
        "summary": "This page will later render from the most recent published digest run.",
        "items": [
            {
                "category": "Post-earnings",
                "headline": "NVDA held gains after earnings",
                "detail": "Placeholder event highlighting how the digest will bubble meaningful changes, not every price move.",
            },
            {
                "category": "Broken setup",
                "headline": "One lower-quality candidate lost support",
                "detail": "The daily digest should stay small, decisive, and useful before the next weekly review.",
            },
        ],
    }


def sample_stock_detail(ticker: str) -> dict[str, object]:
    normalized = ticker.upper()
    return {
        "ticker": normalized,
        "company": "Sample Company" if normalized not in {"NVDA", "CRM", "TSLA"} else {
            "NVDA": "NVIDIA",
            "CRM": "Salesforce",
            "TSLA": "Tesla",
        }[normalized],
        "primary_thesis": "This page is wired as the stock-detail shell and will later read from published score, evidence, and history rows.",
        "observed": [
            "Observed facts should be stored and rendered separately from inferences.",
            "Recent price, benchmark context, and upcoming events belong here.",
        ],
        "derived": [
            "Derived views should explain why a setup is attractive or weak.",
            "The system should keep long-term and short-term logic separate.",
        ],
        "why_now": "Use this block for timely setup-specific reasoning.",
        "why_not_stronger": "Use this block for the best opposing evidence or missing confirmation.",
    }
