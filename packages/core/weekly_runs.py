from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

RUNS_DIR = Path("data/processed/weekly_runs")
LEGACY_RECOMMENDATIONS_PATH = Path("data/processed/phase2/mlp_current_recommendations.csv")
LEGACY_WATCHLIST_PATH = Path("data/reference/phase2_watchlist.csv")
UNPINNED_REGISTRY_VERSION = "repo-current"


@dataclass(frozen=True)
class WeeklyRunManifest:
    run_id: str
    recommendation_week_start: str
    recommendation_week_end: str
    published_at: str
    timezone: str
    market_data_through: str
    source_data_through: str
    last_checked_at: str
    run_status: str
    engine_version: str
    strategy_registry_version: str
    input_snapshot_id: str
    output_snapshot_id: str
    recommendations_path: str
    created_at: str
    universe: str = "phase2"
    source_watchlist_path: str = "data/reference/phase2_watchlist.csv"
    active_strategy_versions: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> WeeklyRunManifest:
        return cls(
            run_id=str(payload["run_id"]),
            recommendation_week_start=str(payload["recommendation_week_start"]),
            recommendation_week_end=str(payload["recommendation_week_end"]),
            published_at=str(payload["published_at"]),
            timezone=str(payload.get("timezone", "America/New_York")),
            market_data_through=str(payload["market_data_through"]),
            source_data_through=str(payload["source_data_through"]),
            last_checked_at=str(payload.get("last_checked_at", payload["published_at"])),
            run_status=str(payload.get("run_status", "published")),
            engine_version=str(payload.get("engine_version", "mlp-watchlist-v1")),
            strategy_registry_version=str(payload.get("strategy_registry_version", "repo-current")),
            input_snapshot_id=str(payload.get("input_snapshot_id", "")),
            output_snapshot_id=str(payload.get("output_snapshot_id", "")),
            recommendations_path=str(payload.get("recommendations_path", "recommendations.csv")),
            created_at=str(payload.get("created_at", payload["published_at"])),
            universe=str(payload.get("universe", "phase2")),
            source_watchlist_path=str(
                payload.get("source_watchlist_path", "data/reference/phase2_watchlist.csv")
            ),
            active_strategy_versions={
                str(key): str(value)
                for key, value in dict(payload.get("active_strategy_versions", {})).items()
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "recommendation_week_start": self.recommendation_week_start,
            "recommendation_week_end": self.recommendation_week_end,
            "published_at": self.published_at,
            "timezone": self.timezone,
            "market_data_through": self.market_data_through,
            "source_data_through": self.source_data_through,
            "last_checked_at": self.last_checked_at,
            "run_status": self.run_status,
            "engine_version": self.engine_version,
            "strategy_registry_version": self.strategy_registry_version,
            "input_snapshot_id": self.input_snapshot_id,
            "output_snapshot_id": self.output_snapshot_id,
            "recommendations_path": self.recommendations_path,
            "created_at": self.created_at,
            "universe": self.universe,
            "source_watchlist_path": self.source_watchlist_path,
            "active_strategy_versions": self.active_strategy_versions,
        }

    def validate_strategy_pinning(self) -> None:
        from packages.core.strategy_registry import (  # noqa: PLC0415
            get_active_strategy_versions,
            get_strategy_registry_version,
        )

        expected_registry_version = get_strategy_registry_version()
        expected_versions = get_active_strategy_versions()
        if not self.strategy_registry_version:
            raise ValueError("Weekly run manifest is missing strategy_registry_version")
        if self.strategy_registry_version == UNPINNED_REGISTRY_VERSION:
            raise ValueError(
                "Weekly run manifest must pin a concrete strategy_registry_version"
            )
        if self.strategy_registry_version != expected_registry_version:
            raise ValueError(
                "Weekly run manifest strategy_registry_version does not match "
                f"the active registry: {self.strategy_registry_version} != "
                f"{expected_registry_version}"
            )
        if not self.active_strategy_versions:
            raise ValueError("Weekly run manifest is missing active_strategy_versions")

        missing = sorted(set(expected_versions) - set(self.active_strategy_versions))
        extra = sorted(set(self.active_strategy_versions) - set(expected_versions))
        mismatched = sorted(
            key
            for key, expected in expected_versions.items()
            if self.active_strategy_versions.get(key) != expected
        )
        problems = []
        if missing:
            problems.append(f"missing={','.join(missing)}")
        if extra:
            problems.append(f"extra={','.join(extra)}")
        if mismatched:
            problems.append(f"mismatched={','.join(mismatched)}")
        if problems:
            raise ValueError(
                "Weekly run manifest active_strategy_versions does not match "
                f"the active registry ({'; '.join(problems)})"
            )


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def weekly_runs_dir() -> Path:
    return repo_root() / RUNS_DIR


def current_pointer_path() -> Path:
    return weekly_runs_dir() / "current.json"


def run_dir(run_id: str) -> Path:
    return weekly_runs_dir() / run_id


def current_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")  # noqa: UP017


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def manifest_path_for_run(run_id: str) -> Path:
    return run_dir(run_id) / "manifest.json"


def load_manifest(run_id: str) -> WeeklyRunManifest | None:
    path = manifest_path_for_run(run_id)
    if not path.exists():
        return None
    return WeeklyRunManifest.from_dict(read_json(path))


def load_current_pointer() -> dict[str, Any] | None:
    path = current_pointer_path()
    if not path.exists():
        return None
    return read_json(path)


def load_current_manifest() -> WeeklyRunManifest | None:
    pointer = load_current_pointer()
    if not pointer:
        return None
    return load_manifest(str(pointer["run_id"]))


def current_recommendations_path() -> Path:
    manifest = load_current_manifest()
    if manifest:
        path = run_dir(manifest.run_id) / manifest.recommendations_path
        if path.exists():
            return path
    return repo_root() / LEGACY_RECOMMENDATIONS_PATH


def legacy_recommendations_path() -> Path:
    return repo_root() / LEGACY_RECOMMENDATIONS_PATH


def legacy_watchlist_path() -> Path:
    return repo_root() / LEGACY_WATCHLIST_PATH


def list_manifests() -> list[WeeklyRunManifest]:
    root = weekly_runs_dir()
    if not root.exists():
        return []
    manifests: list[WeeklyRunManifest] = []
    for path in root.glob("*/manifest.json"):
        try:
            manifests.append(WeeklyRunManifest.from_dict(read_json(path)))
        except (KeyError, json.JSONDecodeError):
            continue
    return sorted(
        manifests,
        key=lambda item: (item.recommendation_week_start, item.published_at, item.run_id),
        reverse=True,
    )


def write_run_snapshot(
    *,
    manifest: WeeklyRunManifest,
    recommendations_source: Path,
    publish_current: bool,
) -> None:
    if publish_current:
        manifest.validate_strategy_pinning()
    target_dir = run_dir(manifest.run_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(recommendations_source, target_dir / manifest.recommendations_path)
    write_json_atomic(target_dir / "manifest.json", manifest.to_dict())
    if publish_current:
        write_json_atomic(
            current_pointer_path(),
            {
                "run_id": manifest.run_id,
                "published_at": manifest.published_at,
                "updated_at": current_utc_timestamp(),
            },
        )


def update_manifest_status(run_id: str, status: str) -> None:
    manifest = load_manifest(run_id)
    if manifest is None:
        return
    payload = manifest.to_dict()
    payload["run_status"] = status
    write_json_atomic(manifest_path_for_run(run_id), payload)


def current_week_start(today: date) -> date:
    return today - timedelta(days=today.weekday())


def week_end(week_start: date) -> date:
    return week_start + timedelta(days=4)


def prior_friday_for_week(week_start: date) -> date:
    return week_start - timedelta(days=3)


def run_id_for_week(week_start: date, published_date: date) -> str:
    return f"weekly_{week_start.isoformat()}_published_{published_date.isoformat()}"
