from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from packages.core.auth import (
    clear_session_cookie,
    create_session_cookie_value,
    is_authenticated,
    verify_password,
)
from packages.core.config import get_settings
from packages.core.ui_data import sample_daily_digest, sample_stock_detail, sample_weekly_review


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


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    return RedirectResponse(url="/weekly", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    if is_authenticated(request, settings):
        return templates.TemplateResponse(
            name="redirect.html",
            context={"request": request, "target_url": "/weekly"},
        )
    return templates.TemplateResponse(
        name="login.html",
        context={"request": request, "error": None},
    )


@app.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, password: str = Form(...)) -> HTMLResponse | RedirectResponse:
    if not verify_password(password, settings.app_shared_password_hash):
        return templates.TemplateResponse(
            name="login.html",
            context={
                "request": request,
                "error": "Password did not match. Double-check and try again.",
            },
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


@app.post("/logout")
def logout() -> RedirectResponse:
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    clear_session_cookie(response, settings)
    return response


@app.get("/weekly", response_class=HTMLResponse)
def weekly(request: Request) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    context = {"review": sample_weekly_review(), "active_page": "weekly"}
    return templates.TemplateResponse(name="weekly.html", context={"request": request, **context})


@app.get("/daily", response_class=HTMLResponse)
def daily(request: Request) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    context = {"digest": sample_daily_digest(), "active_page": "daily"}
    return templates.TemplateResponse(name="daily.html", context={"request": request, **context})


@app.get("/watchlist", response_class=HTMLResponse)
def watchlist(request: Request) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    context = {"review": sample_weekly_review(), "active_page": "watchlist"}
    return templates.TemplateResponse(name="watchlist.html", context={"request": request, **context})


@app.get("/stocks/{ticker}", response_class=HTMLResponse)
def stock_detail(request: Request, ticker: str) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    context = {
        "stock": sample_stock_detail(ticker),
        "active_page": "stocks",
    }
    return templates.TemplateResponse(name="stock_detail.html", context={"request": request, **context})


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request) -> HTMLResponse | RedirectResponse:
    guard = _guard(request)
    if guard:
        return guard
    context = {
        "active_page": "admin",
        "jobs": [
            {"name": "daily-run", "status": "Not configured yet", "note": "Placeholder until DB wiring"},
            {"name": "weekly-run", "status": "Not configured yet", "note": "Placeholder until DB wiring"},
        ],
    }
    return templates.TemplateResponse(name="admin.html", context={"request": request, **context})
