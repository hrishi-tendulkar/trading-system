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
    assert response.headers["location"] == "/login"


def test_weekly_renders_plan() -> None:
    response = _authenticated_client().get("/weekly")
    assert response.status_code == 200
    assert "This Week&#39;s Plan" in response.text
    assert "Top actions this week" in response.text


def test_daily_renders_verdict() -> None:
    response = _authenticated_client().get("/daily")
    assert response.status_code == 200
    assert "Daily verdict" in response.text
    assert "What needs attention before next week" in response.text


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


def test_missing_stock_returns_404() -> None:
    response = _authenticated_client().get("/stocks/notreal")
    assert response.status_code == 404
