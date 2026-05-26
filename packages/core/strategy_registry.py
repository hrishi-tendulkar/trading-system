from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from packages.schemas.strategy_engine import DecisionBasisRecord, DecisionBasisRegistry


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _registry_path() -> Path:
    return _repo_root() / "config" / "strategy_registry.json"


@lru_cache(maxsize=1)
def load_strategy_registry() -> DecisionBasisRegistry:
    payload = json.loads(_registry_path().read_text(encoding="utf-8"))
    return DecisionBasisRegistry.model_validate(payload)


@lru_cache(maxsize=1)
def get_strategy_index() -> dict[str, DecisionBasisRecord]:
    registry = load_strategy_registry()
    return {record.basis_code: record for record in registry.decision_bases}


def get_strategy_record(basis_code: str) -> DecisionBasisRecord | None:
    return get_strategy_index().get(basis_code)
