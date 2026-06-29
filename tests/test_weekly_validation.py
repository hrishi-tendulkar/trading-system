from __future__ import annotations

from datetime import date

from services.jobs.weekly_validation import expected_week_for_validation, validate_weekly_current


def test_expected_week_for_validation_targets_following_monday_on_weekend() -> None:
    assert expected_week_for_validation(date(2026, 6, 13)) == date(2026, 6, 15)
    assert expected_week_for_validation(date(2026, 6, 14)) == date(2026, 6, 15)


def test_validate_weekly_current_flags_stale_current_run() -> None:
    result = validate_weekly_current(
        as_of_date=date(2026, 7, 5),
        check_web=False,
    )

    assert not result.ok
    assert result.expected_week == "2026-07-06"
    assert any("expected 2026-07-06" in message for message in result.messages)
