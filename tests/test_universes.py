from pathlib import Path

import pytest

from packages.core.universes import (
    active_universe_source,
    load_universe_members_from_path,
    normalize_ticker,
)


def test_default_active_universe_is_sp100(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRADING_SYSTEM_ACTIVE_UNIVERSE", raising=False)
    monkeypatch.delenv("TRADING_SYSTEM_WATCHLIST_PATH", raising=False)

    source = active_universe_source()

    assert source.slug == "sp100"
    assert source.path.name == "sp100_watchlist.csv"


def test_active_universe_can_select_sp100(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRADING_SYSTEM_ACTIVE_UNIVERSE", "sp100")
    monkeypatch.delenv("TRADING_SYSTEM_WATCHLIST_PATH", raising=False)

    source = active_universe_source()

    assert source.slug == "sp100"
    assert source.path.name == "sp100_watchlist.csv"


def test_custom_watchlist_path_override_wins(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    custom = tmp_path / "custom_watchlist.csv"
    custom.write_text(
        "ticker,display_name,sector,is_benchmark,is_active\n"
        "BRK.B,Berkshire Hathaway,Financials,false,true\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TRADING_SYSTEM_ACTIVE_UNIVERSE", "sp100")
    monkeypatch.setenv("TRADING_SYSTEM_WATCHLIST_PATH", str(custom))

    source = active_universe_source()
    members = load_universe_members_from_path(str(source.path))

    assert source.slug == "custom"
    assert set(members) == {"BRK-B"}


def test_universe_loader_requires_contract_columns(tmp_path: Path) -> None:
    bad_path = tmp_path / "bad.csv"
    bad_path.write_text("ticker,display_name\nAAPL,Apple\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_universe_members_from_path(str(bad_path))


def test_normalize_ticker_uses_provider_safe_hyphen() -> None:
    assert normalize_ticker("brk.b") == "BRK-B"
