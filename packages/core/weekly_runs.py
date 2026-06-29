from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Protocol

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from packages.core.config import get_settings

RUNS_DIR = Path("data/processed/weekly_runs")
LEGACY_RECOMMENDATIONS_PATH = Path("data/processed/phase2/mlp_current_recommendations.csv")
LEGACY_WATCHLIST_PATH = Path("data/reference/phase2_watchlist.csv")
UNPINNED_REGISTRY_VERSION = "repo-current"
CURRENT_POINTER_ID = 1


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


class WeeklyRunRepository(Protocol):
    def load_manifest(self, run_id: str) -> WeeklyRunManifest | None: ...

    def load_current_pointer(self) -> dict[str, Any] | None: ...

    def load_current_manifest(self) -> WeeklyRunManifest | None: ...

    def current_recommendations_path(self) -> Path: ...

    def load_recommendation_rows(self, run_id: str) -> list[dict[str, str]]: ...

    def load_current_recommendation_rows(self) -> list[dict[str, str]]: ...

    def list_manifests(self) -> list[WeeklyRunManifest]: ...

    def write_run_snapshot(
        self,
        *,
        manifest: WeeklyRunManifest,
        recommendations_source: Path,
        publish_current: bool,
    ) -> None: ...

    def update_manifest_status(self, run_id: str, status: str) -> None: ...


def _csv_rows(path: Path) -> list[dict[str, str]]:
    import csv

    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


class LocalWeeklyRunRepository:
    def weekly_runs_dir(self) -> Path:
        return weekly_runs_dir()

    def current_pointer_path(self) -> Path:
        return current_pointer_path()

    def run_dir(self, run_id: str) -> Path:
        return run_dir(run_id)

    def manifest_path_for_run(self, run_id: str) -> Path:
        return manifest_path_for_run(run_id)

    def load_manifest(self, run_id: str) -> WeeklyRunManifest | None:
        path = self.manifest_path_for_run(run_id)
        if not path.exists():
            return None
        return WeeklyRunManifest.from_dict(read_json(path))

    def load_current_pointer(self) -> dict[str, Any] | None:
        path = self.current_pointer_path()
        if not path.exists():
            return None
        return read_json(path)

    def load_current_manifest(self) -> WeeklyRunManifest | None:
        pointer = self.load_current_pointer()
        if not pointer:
            return None
        return self.load_manifest(str(pointer["run_id"]))

    def current_recommendations_path(self) -> Path:
        manifest = self.load_current_manifest()
        if manifest:
            path = self.run_dir(manifest.run_id) / manifest.recommendations_path
            if path.exists():
                return path
        return repo_root() / LEGACY_RECOMMENDATIONS_PATH

    def load_recommendation_rows(self, run_id: str) -> list[dict[str, str]]:
        manifest = self.load_manifest(run_id)
        if manifest is None:
            return []
        path = self.run_dir(manifest.run_id) / manifest.recommendations_path
        if not path.exists():
            return []
        return _csv_rows(path)

    def load_current_recommendation_rows(self) -> list[dict[str, str]]:
        return _csv_rows(self.current_recommendations_path())

    def list_manifests(self) -> list[WeeklyRunManifest]:
        root = self.weekly_runs_dir()
        if not root.exists():
            return []
        manifests: list[WeeklyRunManifest] = []
        for path in root.glob("*/manifest.json"):
            try:
                manifests.append(WeeklyRunManifest.from_dict(read_json(path)))
            except (KeyError, json.JSONDecodeError):
                continue
        return _sort_manifests(manifests)

    def write_run_snapshot(
        self,
        *,
        manifest: WeeklyRunManifest,
        recommendations_source: Path,
        publish_current: bool,
    ) -> None:
        if publish_current:
            manifest.validate_strategy_pinning()
        target_dir = self.run_dir(manifest.run_id)
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(recommendations_source, target_dir / manifest.recommendations_path)
        write_json_atomic(target_dir / "manifest.json", manifest.to_dict())
        if publish_current:
            write_json_atomic(
                self.current_pointer_path(),
                {
                    "run_id": manifest.run_id,
                    "published_at": manifest.published_at,
                    "updated_at": current_utc_timestamp(),
                },
            )

    def update_manifest_status(self, run_id: str, status: str) -> None:
        manifest = self.load_manifest(run_id)
        if manifest is None:
            return
        payload = manifest.to_dict()
        payload["run_status"] = status
        write_json_atomic(self.manifest_path_for_run(run_id), payload)


class SupabaseWeeklyRunRepository:
    def __init__(self, engine: Engine | None = None) -> None:
        settings = get_settings()
        self.engine = engine or create_engine(
            settings.supabase_db_url,
            future=True,
            pool_pre_ping=True,
        )

    def load_manifest(self, run_id: str) -> WeeklyRunManifest | None:
        with self.engine.connect() as conn:
            row = (
                conn.execute(
                    text(
                        """
                        select manifest_json
                        from intelligence.weekly_review_runs
                        where run_id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return WeeklyRunManifest.from_dict(dict(row["manifest_json"]))

    def load_current_pointer(self) -> dict[str, Any] | None:
        with self.engine.connect() as conn:
            row = (
                conn.execute(
                    text(
                        """
                        select run_id, published_at, updated_at
                        from intelligence.weekly_current_run
                        where id = :id
                        """
                    ),
                    {"id": CURRENT_POINTER_ID},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return {
            "run_id": str(row["run_id"]),
            "published_at": row["published_at"].isoformat()
            if hasattr(row["published_at"], "isoformat")
            else str(row["published_at"]),
            "updated_at": row["updated_at"].isoformat()
            if hasattr(row["updated_at"], "isoformat")
            else str(row["updated_at"]),
        }

    def load_current_manifest(self) -> WeeklyRunManifest | None:
        pointer = self.load_current_pointer()
        if not pointer:
            return None
        return self.load_manifest(str(pointer["run_id"]))

    def current_recommendations_path(self) -> Path:
        return repo_root() / LEGACY_RECOMMENDATIONS_PATH

    def load_recommendation_rows(self, run_id: str) -> list[dict[str, str]]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        """
                        select raw_record_json
                        from intelligence.weekly_recommendation_records
                        where run_id = :run_id
                        order by action_rank, ticker
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .all()
            )
        return [dict(row["raw_record_json"]) for row in rows]

    def load_current_recommendation_rows(self) -> list[dict[str, str]]:
        manifest = self.load_current_manifest()
        if manifest is None:
            return _csv_rows(repo_root() / LEGACY_RECOMMENDATIONS_PATH)
        rows = self.load_recommendation_rows(manifest.run_id)
        if rows:
            return rows
        return _csv_rows(repo_root() / LEGACY_RECOMMENDATIONS_PATH)

    def list_manifests(self) -> list[WeeklyRunManifest]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        """
                        select manifest_json
                        from intelligence.weekly_review_runs
                        where status in ('published', 'superseded')
                        order by recommendation_week_start desc, published_at desc, run_id desc
                        """
                    )
                )
                .mappings()
                .all()
            )
        return _sort_manifests(
            [WeeklyRunManifest.from_dict(dict(row["manifest_json"])) for row in rows]
        )

    def write_run_snapshot(
        self,
        *,
        manifest: WeeklyRunManifest,
        recommendations_source: Path,
        publish_current: bool,
    ) -> None:
        if publish_current:
            manifest.validate_strategy_pinning()
        rows = _csv_rows(recommendations_source)
        payload = manifest.to_dict()
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    insert into intelligence.weekly_review_runs (
                      run_date, title, summary, run_id, recommendation_week_start,
                      recommendation_week_end, published_at, timezone, market_data_through,
                      source_data_through, last_checked_at, status, engine_version,
                      strategy_registry_version, input_snapshot_id, output_snapshot_id,
                      universe, source_watchlist_path, active_strategy_versions_json,
                      manifest_json, created_at, updated_at
                    )
                    values (
                      :run_date, :title, :summary, :run_id, :recommendation_week_start,
                      :recommendation_week_end, cast(:published_at as timestamptz), :timezone,
                      :market_data_through, :source_data_through,
                      cast(:last_checked_at as timestamptz), :status, :engine_version,
                      :strategy_registry_version, :input_snapshot_id, :output_snapshot_id,
                      :universe, :source_watchlist_path,
                      cast(:active_strategy_versions_json as jsonb),
                      cast(:manifest_json as jsonb), cast(:created_at as timestamptz), now()
                    )
                    on conflict (run_id) do update set
                      recommendation_week_start = excluded.recommendation_week_start,
                      recommendation_week_end = excluded.recommendation_week_end,
                      published_at = excluded.published_at,
                      timezone = excluded.timezone,
                      market_data_through = excluded.market_data_through,
                      source_data_through = excluded.source_data_through,
                      last_checked_at = excluded.last_checked_at,
                      status = excluded.status,
                      engine_version = excluded.engine_version,
                      strategy_registry_version = excluded.strategy_registry_version,
                      input_snapshot_id = excluded.input_snapshot_id,
                      output_snapshot_id = excluded.output_snapshot_id,
                      universe = excluded.universe,
                      source_watchlist_path = excluded.source_watchlist_path,
                      active_strategy_versions_json = excluded.active_strategy_versions_json,
                      manifest_json = excluded.manifest_json,
                      updated_at = now()
                    """
                ),
                {
                    "run_date": manifest.recommendation_week_start,
                    "title": f"Week of {manifest.recommendation_week_start}",
                    "summary": f"Published weekly run {manifest.run_id}",
                    "run_id": manifest.run_id,
                    "recommendation_week_start": manifest.recommendation_week_start,
                    "recommendation_week_end": manifest.recommendation_week_end,
                    "published_at": manifest.published_at,
                    "timezone": manifest.timezone,
                    "market_data_through": manifest.market_data_through,
                    "source_data_through": manifest.source_data_through,
                    "last_checked_at": manifest.last_checked_at,
                    "status": manifest.run_status,
                    "engine_version": manifest.engine_version,
                    "strategy_registry_version": manifest.strategy_registry_version,
                    "input_snapshot_id": manifest.input_snapshot_id,
                    "output_snapshot_id": manifest.output_snapshot_id,
                    "universe": manifest.universe,
                    "source_watchlist_path": manifest.source_watchlist_path,
                    "active_strategy_versions_json": json.dumps(
                        manifest.active_strategy_versions
                    ),
                    "manifest_json": json.dumps(payload),
                    "created_at": manifest.created_at,
                },
            )
            conn.execute(
                text(
                    """
                    delete from intelligence.weekly_recommendation_records
                    where run_id = :run_id
                    """
                ),
                {"run_id": manifest.run_id},
            )
            for row in rows:
                conn.execute(
                    text(
                        """
                        insert into intelligence.weekly_recommendation_records (
                          run_id, ticker, company, as_of_date, action_label, holder_bucket,
                          strategy_name, observed_reason, event_risk, stop_label,
                          stop_value, action_rank, raw_record_json
                        )
                        values (
                          :run_id, :ticker, :company, :as_of_date, :action_label,
                          :holder_bucket, :strategy_name, :observed_reason, :event_risk,
                          :stop_label, :stop_value, :action_rank,
                          cast(:raw_record_json as jsonb)
                        )
                        """
                    ),
                    {
                        "run_id": manifest.run_id,
                        "ticker": row.get("ticker", "").upper(),
                        "company": row.get("company", row.get("ticker", "")).strip(),
                        "as_of_date": row.get("date") or row.get("as_of_date"),
                        "action_label": row.get("action_label", ""),
                        "holder_bucket": row.get("holder_bucket", ""),
                        "strategy_name": row.get("strategy_name", ""),
                        "observed_reason": row.get("observed_reason", ""),
                        "event_risk": row.get("event_risk", ""),
                        "stop_label": row.get("stop_label", ""),
                        "stop_value": row.get("stop_value", ""),
                        "action_rank": int(float(row.get("action_rank") or 0)),
                        "raw_record_json": json.dumps(row),
                    },
                )
            if publish_current:
                self._publish_current(conn, manifest)

    def _publish_current(self, conn: Any, manifest: WeeklyRunManifest) -> None:
        current = self.load_current_pointer()
        if current and current["run_id"] != manifest.run_id:
            conn.execute(
                text(
                    """
                    update intelligence.weekly_review_runs
                    set status = 'superseded',
                        manifest_json = jsonb_set(manifest_json, '{run_status}', '"superseded"'),
                        updated_at = now()
                    where run_id = :run_id
                    """
                ),
                {"run_id": current["run_id"]},
            )
        conn.execute(
            text(
                """
                update intelligence.weekly_review_runs
                set status = 'published',
                    manifest_json = jsonb_set(manifest_json, '{run_status}', '"published"'),
                    updated_at = now()
                where run_id = :run_id
                """
            ),
            {"run_id": manifest.run_id},
        )
        conn.execute(
            text(
                """
                insert into intelligence.weekly_current_run (id, run_id, published_at, updated_at)
                values (:id, :run_id, cast(:published_at as timestamptz), now())
                on conflict (id) do update set
                  run_id = excluded.run_id,
                  published_at = excluded.published_at,
                  updated_at = now()
                """
            ),
            {
                "id": CURRENT_POINTER_ID,
                "run_id": manifest.run_id,
                "published_at": manifest.published_at,
            },
        )

    def update_manifest_status(self, run_id: str, status: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    update intelligence.weekly_review_runs
                    set status = :status,
                        manifest_json = jsonb_set(
                          manifest_json,
                          '{run_status}',
                          to_jsonb(cast(:status as text))
                        ),
                        updated_at = now()
                    where run_id = :run_id
                    """
                ),
                {"run_id": run_id, "status": status},
            )


def _sort_manifests(manifests: list[WeeklyRunManifest]) -> list[WeeklyRunManifest]:
    return sorted(
        manifests,
        key=lambda item: (item.recommendation_week_start, item.published_at, item.run_id),
        reverse=True,
    )


@lru_cache(maxsize=1)
def get_weekly_run_repository() -> WeeklyRunRepository:
    settings = get_settings()
    mode = settings.weekly_run_repository.strip().lower()
    if mode == "supabase":
        return SupabaseWeeklyRunRepository()
    if mode == "auto" and settings.environment != "development":
        return SupabaseWeeklyRunRepository()
    return LocalWeeklyRunRepository()


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
    return get_weekly_run_repository().load_manifest(run_id)


def load_current_pointer() -> dict[str, Any] | None:
    return get_weekly_run_repository().load_current_pointer()


def load_current_manifest() -> WeeklyRunManifest | None:
    return get_weekly_run_repository().load_current_manifest()


def current_recommendations_path() -> Path:
    return get_weekly_run_repository().current_recommendations_path()


def load_recommendation_rows(run_id: str) -> list[dict[str, str]]:
    return get_weekly_run_repository().load_recommendation_rows(run_id)


def load_current_recommendation_rows() -> list[dict[str, str]]:
    return get_weekly_run_repository().load_current_recommendation_rows()


def legacy_recommendations_path() -> Path:
    return repo_root() / LEGACY_RECOMMENDATIONS_PATH


def legacy_watchlist_path() -> Path:
    return repo_root() / LEGACY_WATCHLIST_PATH


def list_manifests() -> list[WeeklyRunManifest]:
    return get_weekly_run_repository().list_manifests()


def write_run_snapshot(
    *,
    manifest: WeeklyRunManifest,
    recommendations_source: Path,
    publish_current: bool,
) -> None:
    get_weekly_run_repository().write_run_snapshot(
        manifest=manifest,
        recommendations_source=recommendations_source,
        publish_current=publish_current,
    )


def update_manifest_status(run_id: str, status: str) -> None:
    get_weekly_run_repository().update_manifest_status(run_id, status)


def current_week_start(today: date) -> date:
    return today - timedelta(days=today.weekday())


def default_publish_week_start(today: date) -> date:
    week_start = current_week_start(today)
    if today.weekday() >= 5:
        return week_start + timedelta(days=7)
    return week_start


def week_end(week_start: date) -> date:
    return week_start + timedelta(days=4)


def prior_friday_for_week(week_start: date) -> date:
    return week_start - timedelta(days=3)


def _observed_fixed_holiday(year: int, month: int, day: int) -> date:
    holiday = date(year, month, day)
    if holiday.weekday() == 5:
        return holiday - timedelta(days=1)
    if holiday.weekday() == 6:
        return holiday + timedelta(days=1)
    return holiday


def _nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    current = date(year, month, 1)
    while current.weekday() != weekday:
        current += timedelta(days=1)
    return current + timedelta(days=7 * (occurrence - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    if month == 12:
        current = date(year, 12, 31)
    else:
        current = date(year, month + 1, 1) - timedelta(days=1)
    while current.weekday() != weekday:
        current -= timedelta(days=1)
    return current


def _easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    correction = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * correction) // 451
    month = (h + correction - 7 * m + 114) // 31
    day = ((h + correction - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def market_holidays(year: int) -> set[date]:
    holidays = {
        _observed_fixed_holiday(year, 1, 1),
        _nth_weekday(year, 1, 0, 3),
        _nth_weekday(year, 2, 0, 3),
        _easter_sunday(year) - timedelta(days=2),
        _last_weekday(year, 5, 0),
        _observed_fixed_holiday(year, 7, 4),
        _nth_weekday(year, 9, 0, 1),
        _nth_weekday(year, 11, 3, 4),
        _observed_fixed_holiday(year, 12, 25),
    }
    if year >= 2022:
        holidays.add(_observed_fixed_holiday(year, 6, 19))
    return holidays


def is_market_session(day: date) -> bool:
    return day.weekday() < 5 and day not in market_holidays(day.year)


def prior_market_close_for_week(week_start: date) -> date:
    current = week_start - timedelta(days=1)
    while not is_market_session(current):
        current -= timedelta(days=1)
    return current


def run_id_for_week(week_start: date, published_date: date) -> str:
    return f"weekly_{week_start.isoformat()}_published_{published_date.isoformat()}"
