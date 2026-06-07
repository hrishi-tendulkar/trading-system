from __future__ import annotations

from pathlib import Path

import pytest

import packages.core.weekly_runs as weekly_runs
from packages.core.strategy_registry import (
    get_active_strategy_versions,
    get_strategy_registry_version,
)
from packages.core.weekly_runs import WeeklyRunManifest, write_run_snapshot


def _manifest(
    *,
    strategy_registry_version: str | None = None,
    active_strategy_versions: dict[str, str] | None = None,
) -> WeeklyRunManifest:
    return WeeklyRunManifest(
        run_id="weekly_test",
        recommendation_week_start="2026-06-01",
        recommendation_week_end="2026-06-05",
        published_at="2026-06-06T12:00:00+00:00",
        timezone="America/New_York",
        market_data_through="2026-06-05",
        source_data_through="2026-06-05",
        last_checked_at="2026-06-06T12:00:00+00:00",
        run_status="published",
        engine_version="mlp-watchlist-v1",
        strategy_registry_version=strategy_registry_version or get_strategy_registry_version(),
        input_snapshot_id="input",
        output_snapshot_id="output",
        recommendations_path="recommendations.csv",
        created_at="2026-06-06T12:00:00+00:00",
        universe="sp100",
        source_watchlist_path="data/reference/sp100_watchlist.csv",
        active_strategy_versions=active_strategy_versions
        if active_strategy_versions is not None
        else get_active_strategy_versions(),
    )


def test_weekly_manifest_accepts_current_strategy_pinning() -> None:
    _manifest().validate_strategy_pinning()


def test_weekly_manifest_rejects_placeholder_registry_version() -> None:
    with pytest.raises(ValueError, match="concrete strategy_registry_version"):
        _manifest(strategy_registry_version="repo-current").validate_strategy_pinning()


def test_weekly_manifest_rejects_incomplete_active_strategy_versions() -> None:
    versions = get_active_strategy_versions()
    versions.pop("breakout-confirmation")

    with pytest.raises(ValueError, match="missing=breakout-confirmation"):
        _manifest(active_strategy_versions=versions).validate_strategy_pinning()


def test_publish_current_requires_strategy_pinning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    recommendations = tmp_path / "recommendations.csv"
    recommendations.write_text("date,ticker\n2026-06-05,NVDA\n", encoding="utf-8")
    monkeypatch.setattr(weekly_runs, "run_dir", lambda run_id: tmp_path / run_id)
    monkeypatch.setattr(weekly_runs, "current_pointer_path", lambda: tmp_path / "current.json")

    with pytest.raises(ValueError, match="concrete strategy_registry_version"):
        write_run_snapshot(
            manifest=_manifest(strategy_registry_version="repo-current"),
            recommendations_source=recommendations,
            publish_current=True,
        )

    assert not (tmp_path / "weekly_test").exists()
    assert not (tmp_path / "current.json").exists()
