from fastapi.testclient import TestClient

from apps.web.main import app
from packages.core.auth import create_session_cookie_value
from packages.core.config import get_settings

client = TestClient(app)


def _authenticated_client() -> TestClient:
    settings = get_settings()
    client.cookies.set(settings.session_cookie_name, create_session_cookie_value(settings))
    return client


def test_weekly_requires_login() -> None:
    response = TestClient(app).get("/weekly", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login?next=/weekly"


def test_archive_requires_login() -> None:
    response = TestClient(app).get("/archive", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login?next=/archive"


def test_strategy_detail_redirects_to_login_with_next_target() -> None:
    response = TestClient(app).get(
        "/strategies/breakout-confirmation",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/login?next=/strategies/breakout-confirmation"


def test_weekly_renders_plan() -> None:
    response = _authenticated_client().get("/weekly")
    assert response.status_code == 200
    assert "This Week&#39;s Plan" in response.text
    assert "Top actions this week" in response.text
    assert "Strategy:" in response.text


def test_strategy_index_renders_strategy_library() -> None:
    response = _authenticated_client().get("/strategies")
    assert response.status_code == 200
    assert "How the engine makes decisions" in response.text
    assert "Breakout Confirmation" in response.text
    assert "Sector-Confirmed Pullback Continuation" in response.text


def test_daily_renders_verdict() -> None:
    response = _authenticated_client().get("/daily")
    assert response.status_code == 200
    assert "Daily verdict" in response.text
    assert "What needs attention before next week" in response.text


def test_archive_renders_weekly_reports() -> None:
    response = _authenticated_client().get("/archive")
    assert response.status_code == 200
    assert "Reopen the full weekly picture" in response.text
    assert "Open archived week" in response.text


def test_archive_week_renders_reconstructed_plan() -> None:
    response = _authenticated_client().get("/archive")
    week_path = response.text.split('href="/archive/', 1)[1].split('"', 1)[0]
    detail_response = _authenticated_client().get(f"/archive/{week_path}")
    assert detail_response.status_code == 200
    assert "Archived Weekly Report" in detail_response.text
    assert "Original Weekly Plan" in detail_response.text
    assert "Daily Addenda" in detail_response.text


def test_missing_archive_week_returns_404() -> None:
    response = _authenticated_client().get("/archive/not-a-real-week")
    assert response.status_code == 404


def test_watchlist_renders_active_universe() -> None:
    response = _authenticated_client().get("/watchlist")
    assert response.status_code == 200
    assert "Active universe" in response.text
    assert "Watchlist workspace" in response.text


def test_stock_detail_renders_deep_dive() -> None:
    response = _authenticated_client().get("/stocks/nvda")
    assert response.status_code == 200
    assert "Deep Dive" in response.text
    assert "Observed Evidence" in response.text


def test_strategy_detail_renders_strategy_surface() -> None:
    response = _authenticated_client().get("/strategies/breakout-confirmation")
    assert response.status_code == 200
    assert "Strategy Deep Dive" in response.text
    assert "Breakout Confirmation" in response.text
    assert "Backtest Verdict" in response.text
    assert "What the strategy is finding right now" in response.text


def test_login_page_preserves_target_url() -> None:
    response = TestClient(app).get("/login?next=/strategies/breakout-confirmation")
    assert response.status_code == 200
    assert 'name="target_url"' in response.text
    assert 'value="/strategies/breakout-confirmation"' in response.text


def test_missing_stock_returns_404() -> None:
    response = _authenticated_client().get("/stocks/notreal")
    assert response.status_code == 404
