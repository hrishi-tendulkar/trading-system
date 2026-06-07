from packages.core.ui_data import (
    get_archive_index,
    get_archive_week,
    get_daily_digest,
    get_stock_detail,
    get_watchlist_view,
    get_weekly_review,
)
from packages.core.weekly_runs import WeeklyRunManifest


def test_weekly_review_has_top_actions() -> None:
    review = get_weekly_review()
    assert review["fresh_cash"]
    assert review["title"] == "Weekly summary for week of 2026-06-08"
    assert review["coverage"]["analyzed_count"] == "108"
    assert "Every analyzed name appears" in review["coverage"]["board_note"]
    assert "current holdings" in review["coverage"]["holdings_note"]
    fact_labels = {fact["label"] for fact in review["facts"]}
    assert "Recommendation week" in fact_labels
    assert "Data through" in fact_labels
    assert review["metadata"]["recommendation_week"] == "Week of 2026-06-08"
    assert review["metadata"]["data_through"] == "2026-06-05"
    assert review["metadata"]["strategy_registry_version"] == "2026-06-07.1"
    assert "breakout-confirmation.v2" in review["metadata"]["active_strategy_versions"]
    assert review["alerts"] == []


def test_archive_index_links_to_reconstructable_week() -> None:
    archive = get_archive_index()
    assert archive["weeks"]
    week_ids = {week["week_id"] for week in archive["weeks"]}
    assert any(week_id.startswith("weekly_2026-06-01_published_") for week_id in week_ids)
    assert "weekly_2026-05-22_published_2026-05-22" in week_ids
    week_id = archive["weeks"][0]["week_id"]
    week = get_archive_week(week_id)
    assert week is not None
    assert week["weekly_plan"]["fresh_cash"]
    assert week["daily_addenda"]
    assert "strategy_registry_version" in week["metadata"]


def test_archive_week_reads_saved_snapshot_not_only_current_run() -> None:
    week = get_archive_week("weekly_2026-05-22_published_2026-05-22")
    assert week is not None
    assert week["metadata"]["data_through"] == "2026-05-22"
    assert week["metadata"]["status"] == "Archived immutable plan"


def test_daily_digest_has_items() -> None:
    digest = get_daily_digest()
    assert digest["items"]
    assert digest["verdict"]


def test_stock_detail_uses_uppercase_ticker() -> None:
    stock = get_stock_detail("nvda")
    assert stock is not None
    assert stock["ticker"] == "NVDA"


def test_watchlist_has_sections() -> None:
    watchlist = get_watchlist_view()
    assert watchlist["sections"]
    fact_labels = {fact["label"] for fact in watchlist["facts"]}
    assert "Active universe" in fact_labels
    assert "Source file" in fact_labels
    assert "Recommendation coverage" in fact_labels


def test_weekly_run_manifest_round_trips_universe_metadata() -> None:
    manifest = WeeklyRunManifest.from_dict(
        {
            "run_id": "weekly_test",
            "recommendation_week_start": "2026-06-01",
            "recommendation_week_end": "2026-06-05",
            "published_at": "2026-06-06T12:00:00+00:00",
            "market_data_through": "2026-06-05",
            "source_data_through": "2026-06-05",
            "run_status": "published",
            "engine_version": "mlp-watchlist-v1",
            "strategy_registry_version": "repo-current",
            "input_snapshot_id": "input",
            "output_snapshot_id": "output",
            "recommendations_path": "recommendations.csv",
            "created_at": "2026-06-06T12:00:00+00:00",
            "universe": "sp100",
            "source_watchlist_path": "data/reference/sp100_watchlist.csv",
            "active_strategy_versions": {
                "breakout-confirmation": "breakout-confirmation.v2",
            },
        }
    )

    payload = manifest.to_dict()

    assert payload["universe"] == "sp100"
    assert payload["source_watchlist_path"] == "data/reference/sp100_watchlist.csv"
    assert payload["active_strategy_versions"]["breakout-confirmation"] == (
        "breakout-confirmation.v2"
    )
