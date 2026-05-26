from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class DecisionBasisRecord(BaseModel):
    basis_code: str
    basis_type: str
    display_name: str
    status: str
    sleeve: str
    slug: str
    trust_level: str
    promotion_status: str
    board_enabled: bool = False
    primary_actions: list[str] = Field(default_factory=list)
    page_summary: str
    rule_spine: list[str] = Field(default_factory=list)


class DecisionBasisRegistry(BaseModel):
    decision_bases: list[DecisionBasisRecord]


class StrategyCandidateRow(BaseModel):
    ticker: str
    company: str
    strategy_code: str
    strategy_name: str
    current_action_code: str
    current_action_label: str
    setup_quality_band: str
    historical_evidence_tier: str
    live_state: str
    why_now: str
    why_not_stronger: str
    entry_value: str
    invalidation_value: str
    next_catalyst: str
    confidence: str
    board_promoted: bool = False
    suppressed: bool = False
    suppression_reason: Optional[str] = None  # noqa: UP045


class StrategyReplaySummary(BaseModel):
    strategy_code: str
    strategy_name: str
    sample_size: int
    avg_5d: float
    avg_10d: float
    avg_15d: float
    avg_excess_5d: float
    avg_excess_10d: float
    avg_excess_15d: float
    win_rate_5d: float
    win_rate_10d: float
    win_rate_15d: float


class StrategyPageView(BaseModel):
    basis_code: str
    strategy_name: str
    trust_level: str
    promotion_status: str
    board_enabled: bool
    page_summary: str
    rule_spine: list[str]
    as_of_date: Optional[date] = None  # noqa: UP045
    stats: dict[str, int]
    headline_note: str
    replay_summary: Optional[StrategyReplaySummary] = None  # noqa: UP045
    current_rows: list[StrategyCandidateRow] = Field(default_factory=list)
