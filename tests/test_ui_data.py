from packages.core.ui_data import (
    get_archive_index,
    get_archive_week,
    get_daily_digest,
    get_stock_detail,
    get_watchlist_view,
    get_weekly_review,
)


def test_weekly_review_has_top_actions() -> None:
    review = get_weekly_review()
    assert review["start_here"]
    assert review["title"] == "This Week's Plan"
    fact_labels = {fact["label"] for fact in review["facts"]}
    assert "Recommendation week" in fact_labels
    assert "Data through" in fact_labels
    assert review["metadata"]["recommendation_week"] == "Week of 2026-06-01"
    assert review["metadata"]["data_through"] == "2026-05-29"
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
    assert week["weekly_plan"]["start_here"]
    assert week["daily_addenda"]


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
