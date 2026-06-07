from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REQUIRED_COLUMNS = {"ticker", "display_name", "sector", "is_benchmark", "is_active"}

DEFAULT_ACTIVE_UNIVERSE = "sp100"

KNOWN_UNIVERSES = {
    "phase2": Path("data/reference/phase2_watchlist.csv"),
    "mlp": Path("data/reference/mlp_watchlist.csv"),
    "sp100": Path("data/reference/sp100_watchlist.csv"),
    "sp500": Path("data/reference/sp500_watchlist.csv"),
}


@dataclass(frozen=True)
class UniverseMember:
    ticker: str
    display_name: str
    sector: str
    is_benchmark: bool
    is_active: bool


@dataclass(frozen=True)
class UniverseSource:
    slug: str
    path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _to_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def normalize_ticker(value: str) -> str:
    return value.strip().upper().replace(".", "-")


def _configured_universe() -> str:
    return os.environ.get("TRADING_SYSTEM_ACTIVE_UNIVERSE", DEFAULT_ACTIVE_UNIVERSE).strip()


def active_universe_source() -> UniverseSource:
    override_path = os.environ.get("TRADING_SYSTEM_WATCHLIST_PATH", "").strip()
    if override_path:
        path = Path(override_path)
        if not path.is_absolute():
            path = repo_root() / path
        return UniverseSource(slug="custom", path=path)

    slug = _configured_universe() or DEFAULT_ACTIVE_UNIVERSE
    try:
        relative_path = KNOWN_UNIVERSES[slug]
    except KeyError as exc:
        known = ", ".join(sorted(KNOWN_UNIVERSES))
        raise ValueError(f"Unknown active universe '{slug}'. Known universes: {known}") from exc
    return UniverseSource(slug=slug, path=repo_root() / relative_path)


def active_universe_path() -> Path:
    return active_universe_source().path


def _validate_columns(fieldnames: list[str] | None, path: Path) -> None:
    available = set(fieldnames or [])
    missing = REQUIRED_COLUMNS - available
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Universe file {path} is missing required columns: {missing_list}")


@lru_cache(maxsize=8)
def load_universe_members_from_path(path_value: str) -> dict[str, UniverseMember]:
    path = Path(path_value)
    if not path.exists():
        raise FileNotFoundError(f"Active universe file not found: {path}")

    members: dict[str, UniverseMember] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _validate_columns(reader.fieldnames, path)
        for row in reader:
            member = UniverseMember(
                ticker=normalize_ticker(row["ticker"]),
                display_name=row["display_name"].strip(),
                sector=row["sector"].strip(),
                is_benchmark=_to_bool(row["is_benchmark"]),
                is_active=_to_bool(row["is_active"]),
            )
            members[member.ticker] = member
    return members


def load_active_universe_members() -> dict[str, UniverseMember]:
    return load_universe_members_from_path(str(active_universe_path()))
