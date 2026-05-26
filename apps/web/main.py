from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from packages.core.auth import (
    clear_session_cookie,
    create_session_cookie_value,
    is_authenticated,
    verify_password,
)
from packages.core.config import get_settings
from packages.core.strategy_views import get_strategy_page_view, list_strategy_pages
from packages.core.ui_data import (
    get_daily_digest,
    get_stock_detail,
    get_watchlist_view,
    get_weekly_review,
)

settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Trading System", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def _redirect_to_login() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


def _guard(request: Request) -> RedirectResponse | None:
    if not is_authenticated(request, settings):
        return _redirect_to_login()
    return None


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse, response_model=None)
def root(request: Request) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    return RedirectResponse(url="/weekly", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login", response_class=HTMLResponse, response_model=None)
def login_page(request: Request) -> Response:
    if is_authenticated(request, settings):
        return templates.TemplateResponse(
            request,
            "redirect.html",
            {"target_url": "/weekly"},
        )
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.post("/login", response_class=HTMLResponse, response_model=None)
def login_submit(request: Request, password: str = Form(...)) -> Response:
    if not verify_password(password, settings.app_shared_password_hash):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Password did not match. Double-check and try again."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    response = RedirectResponse(url="/weekly", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=create_session_cookie_value(settings),
        httponly=True,
        secure=settings.environment != "development",
        samesite="strict",
        max_age=settings.session_ttl_seconds,
    )
    return response


@app.post("/logout", response_model=None)
def logout() -> Response:
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    clear_session_cookie(response, settings)
    return response


@app.get("/weekly", response_class=HTMLResponse, response_model=None)
def weekly(request: Request) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    context = {"review": get_weekly_review(), "active_page": "weekly"}
    return templates.TemplateResponse(request, "weekly.html", context)


@app.get("/daily", response_class=HTMLResponse, response_model=None)
def daily(request: Request) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    context = {"digest": get_daily_digest(), "active_page": "daily"}
    return templates.TemplateResponse(request, "daily.html", context)


@app.get("/watchlist", response_class=HTMLResponse, response_model=None)
def watchlist(request: Request) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    context = {"watchlist": get_watchlist_view(), "active_page": "watchlist"}
    return templates.TemplateResponse(request, "watchlist.html", context)


@app.get("/stocks/{ticker}", response_class=HTMLResponse, response_model=None)
def stock_detail(request: Request, ticker: str) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    stock = get_stock_detail(ticker)
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    context = {
        "stock": stock,
        "active_page": "stocks",
    }
    return templates.TemplateResponse(request, "stock_detail.html", context)


@app.get("/strategies/{basis_code}", response_class=HTMLResponse, response_model=None)
def strategy_detail(request: Request, basis_code: str) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    strategy = get_strategy_page_view(basis_code)
    if strategy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    context = {
        "strategy": strategy.model_dump(),
        "strategy_pages": list_strategy_pages(),
        "active_page": "strategies",
    }
    return templates.TemplateResponse(request, "strategy_detail.html", context)


@app.get("/admin", response_class=HTMLResponse, response_model=None)
def admin(request: Request) -> Response:
    guard = _guard(request)
    if guard:
        return guard
    context = {
        "active_page": "admin",
        "jobs": [
            {
                "name": "daily-run",
                "status": "Not configured yet",
                "note": "Placeholder until DB wiring",
            },
            {
                "name": "weekly-run",
                "status": "Not configured yet",
                "note": "Placeholder until DB wiring",
            },
        ],
    }
    return templates.TemplateResponse(request, "admin.html", context)
