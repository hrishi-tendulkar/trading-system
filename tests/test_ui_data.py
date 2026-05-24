from packages.core.ui_data import sample_daily_digest, sample_stock_detail, sample_weekly_review


def test_weekly_review_has_board() -> None:
    review = sample_weekly_review()
    assert review["board"]


def test_daily_digest_has_items() -> None:
    digest = sample_daily_digest()
    assert digest["items"]


def test_stock_detail_uses_uppercase_ticker() -> None:
    stock = sample_stock_detail("nvda")
    assert stock["ticker"] == "NVDA"
