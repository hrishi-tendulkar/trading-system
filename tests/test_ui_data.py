from packages.core.ui_data import (
    get_daily_digest,
    get_stock_detail,
    get_watchlist_view,
    get_weekly_review,
)


def test_weekly_review_has_top_actions() -> None:
    review = get_weekly_review()
    assert review["start_here"]
    assert review["title"] == "This Week's Plan"


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
