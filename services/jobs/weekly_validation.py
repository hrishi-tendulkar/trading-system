from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import httpx

from packages.core.auth import create_session_cookie_value
from packages.core.config import get_settings
from packages.core.weekly_runs import (
    WeeklyRunManifest,
    default_publish_week_start,
    load_current_manifest,
    prior_market_close_for_week,
)
from services.jobs.notifications import send_email


@dataclass(frozen=True)
class WeeklyValidationResult:
    ok: bool
    expected_week: str
    expected_source_through: str
    run_id: str | None
    messages: list[str]


def expected_week_for_validation(today: date) -> date:
    return default_publish_week_start(today)


def validate_weekly_current(
    *,
    as_of_date: date,
    base_url: str | None = None,
    check_web: bool = True,
) -> WeeklyValidationResult:
    expected_week = expected_week_for_validation(as_of_date)
    expected_source_through = prior_market_close_for_week(expected_week)
    messages: list[str] = []

    manifest = load_current_manifest()
    if manifest is None:
        messages.append("No current weekly run is published.")
        return WeeklyValidationResult(
            ok=False,
            expected_week=expected_week.isoformat(),
            expected_source_through=expected_source_through.isoformat(),
            run_id=None,
            messages=messages,
        )

    _validate_manifest(
        manifest,
        expected_week=expected_week,
        expected_source_through=expected_source_through,
        messages=messages,
    )

    if check_web and base_url:
        _validate_web_page(
            manifest,
            base_url=base_url,
            expected_week=expected_week,
            expected_source_through=expected_source_through,
            messages=messages,
        )

    return WeeklyValidationResult(
        ok=not messages,
        expected_week=expected_week.isoformat(),
        expected_source_through=expected_source_through.isoformat(),
        run_id=manifest.run_id,
        messages=messages,
    )


def _validate_manifest(
    manifest: WeeklyRunManifest,
    *,
    expected_week: date,
    expected_source_through: date,
    messages: list[str],
) -> None:
    if manifest.run_status != "published":
        messages.append(f"Current run status is {manifest.run_status}, expected published.")
    if manifest.recommendation_week_start != expected_week.isoformat():
        messages.append(
            "Current run recommendation week is "
            f"{manifest.recommendation_week_start}, expected {expected_week.isoformat()}."
        )
    if manifest.source_data_through != expected_source_through.isoformat():
        messages.append(
            "Current run source-through date is "
            f"{manifest.source_data_through}, expected {expected_source_through.isoformat()}."
        )


def _validate_web_page(
    manifest: WeeklyRunManifest,
    *,
    base_url: str,
    expected_week: date,
    expected_source_through: date,
    messages: list[str],
) -> None:
    settings = get_settings()
    cookies = {
        settings.session_cookie_name: create_session_cookie_value(settings),
    }
    try:
        response = httpx.get(
            f"{base_url.rstrip('/')}/weekly",
            cookies=cookies,
            timeout=90,
            follow_redirects=True,
        )
    except httpx.HTTPError as exc:
        messages.append(f"Production /weekly request failed: {exc}")
        return

    if response.status_code != 200:
        messages.append(f"Production /weekly returned HTTP {response.status_code}.")
        return
    checks = {
        f"Week of {expected_week.isoformat()}": "expected recommendation week",
        expected_source_through.isoformat(): "expected source-through date",
        manifest.run_id: "current run ID",
    }
    for needle, label in checks.items():
        if needle not in response.text:
            messages.append(f"Production /weekly is missing {label}: {needle}.")
    if "Current-week report missing" in response.text:
        messages.append("Production /weekly still shows current-week missing warning.")


def notify_weekly_result(
    *,
    subject: str,
    result: WeeklyValidationResult,
) -> None:
    settings = get_settings()
    body = "\n".join(
        [
            f"Status: {'success' if result.ok else 'failure'}",
            f"Expected week: {result.expected_week}",
            f"Expected source through: {result.expected_source_through}",
            f"Run ID: {result.run_id or 'none'}",
            "",
            "Messages:",
            *(result.messages or ["No validation issues."]),
        ]
    )
    send_email(settings, subject=subject, body=body)
