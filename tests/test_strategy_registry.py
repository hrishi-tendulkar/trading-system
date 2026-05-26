from packages.core.strategy_registry import get_strategy_record, load_strategy_registry
from packages.core.strategy_views import get_strategy_page_view


def test_registry_loads_four_canonical_decision_bases() -> None:
    registry = load_strategy_registry()
    assert len(registry.decision_bases) == 4


def test_breakout_strategy_is_board_enabled() -> None:
    record = get_strategy_record("breakout-confirmation")
    assert record is not None
    assert record.board_enabled is True
    assert record.trust_level == "Core"


def test_strategy_page_view_uses_replay_and_live_rows() -> None:
    page = get_strategy_page_view("breakout-confirmation")
    assert page is not None
    assert page.replay_summary is not None
    assert page.stats["live_matches"] >= 0


def test_pullback_page_normalizes_legacy_buy_now_into_buy_on_pullback() -> None:
    page = get_strategy_page_view("sector-confirmed-pullback-continuation")
    assert page is not None
    assert page.current_rows
    assert all(row.current_action_label != "Buy now" for row in page.current_rows)
