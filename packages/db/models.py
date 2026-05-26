from __future__ import annotations

# ruff: noqa: UP045
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class JobRun(Base):
    __tablename__ = "job_runs"
    __table_args__ = {"schema": "ops"}

    id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    as_of_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    market_session_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    input_completeness_pct: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class WeeklyReviewRun(Base):
    __tablename__ = "weekly_review_runs"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    run_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class StockScore(Base):
    __tablename__ = "stock_scores"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    weekly_review_run_id: Mapped[int] = mapped_column(
        ForeignKey("intelligence.weekly_review_runs.id")
    )
    security_id: Mapped[UUID] = mapped_column()
    action_label: Mapped[str] = mapped_column(String(80))
    tradeability_score: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), nullable=True)
    conviction_score: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), nullable=True)
    overlay_suitability_score: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), nullable=True)
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    weekly_review_run_id: Mapped[int] = mapped_column(
        ForeignKey("intelligence.weekly_review_runs.id")
    )
    security_id: Mapped[UUID] = mapped_column()
    recommendation_new_position: Mapped[str] = mapped_column(Text)
    recommendation_if_already_held: Mapped[str] = mapped_column(Text)
    re_evaluate_if: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class DecisionBasis(Base):
    __tablename__ = "decision_bases"
    __table_args__ = {"schema": "ref"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    basis_code: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    basis_type: Mapped[str] = mapped_column(String(40))
    display_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(40))
    sleeve: Mapped[str] = mapped_column(String(40))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class DecisionBasisVersion(Base):
    __tablename__ = "decision_basis_versions"
    __table_args__ = {"schema": "ref"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    decision_basis_id: Mapped[UUID] = mapped_column(ForeignKey("ref.decision_bases.id"))
    version_num: Mapped[int] = mapped_column(Integer)
    version_label: Mapped[str] = mapped_column(String(80))
    effective_from: Mapped[date] = mapped_column(Date)
    effective_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    rules_summary_json: Mapped[dict] = mapped_column(JSON)
    content_json: Mapped[dict] = mapped_column(JSON)
    change_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_doc_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class DecisionBasisRelationship(Base):
    __tablename__ = "decision_basis_relationships"
    __table_args__ = {"schema": "ref"}

    id: Mapped[int] = mapped_column(primary_key=True)
    from_basis_id: Mapped[UUID] = mapped_column(ForeignKey("ref.decision_bases.id"))
    to_basis_id: Mapped[UUID] = mapped_column(ForeignKey("ref.decision_bases.id"))
    relationship_type: Mapped[str] = mapped_column(String(80))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReplayRun(Base):
    __tablename__ = "replay_runs"
    __table_args__ = {"schema": "research"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    run_label: Mapped[str] = mapped_column(String(120), unique=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    universe: Mapped[str] = mapped_column(String(255))
    source_watchlist_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_prices_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    manifest_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReplaySignalEvent(Base):
    __tablename__ = "replay_signal_events"
    __table_args__ = {"schema": "research"}

    id: Mapped[int] = mapped_column(primary_key=True)
    replay_run_id: Mapped[UUID] = mapped_column(ForeignKey("research.replay_runs.id"))
    strategy_code: Mapped[str] = mapped_column(String(120), index=True)
    strategy_version_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("ref.decision_basis_versions.id"), nullable=True
    )
    security_id: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    signal_date: Mapped[date] = mapped_column(Date, index=True)
    signal_style: Mapped[str] = mapped_column(String(120))
    feature_snapshot_json: Mapped[dict] = mapped_column(JSON)
    forward_return_5d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    forward_return_10d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    forward_return_15d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    excess_return_5d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    excess_return_10d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    excess_return_15d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReplayStrategySummary(Base):
    __tablename__ = "replay_strategy_summaries"
    __table_args__ = {"schema": "research"}

    id: Mapped[int] = mapped_column(primary_key=True)
    replay_run_id: Mapped[UUID] = mapped_column(ForeignKey("research.replay_runs.id"))
    strategy_code: Mapped[str] = mapped_column(String(120), index=True)
    signal_style: Mapped[str] = mapped_column(String(120))
    sample_size: Mapped[int] = mapped_column(Integer)
    avg_fwd_5d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    avg_fwd_10d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    avg_fwd_15d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    avg_excess_5d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    avg_excess_10d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    avg_excess_15d_return: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    win_rate_5d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    win_rate_10d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    win_rate_15d: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    supportive_regime_share: Mapped[Optional[float]] = mapped_column(Numeric(18, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReplaySliceStat(Base):
    __tablename__ = "replay_slice_stats"
    __table_args__ = {"schema": "research"}

    id: Mapped[int] = mapped_column(primary_key=True)
    replay_run_id: Mapped[UUID] = mapped_column(ForeignKey("research.replay_runs.id"))
    strategy_code: Mapped[str] = mapped_column(String(120), index=True)
    slice_family: Mapped[str] = mapped_column(String(120))
    slice_key_json: Mapped[dict] = mapped_column(JSON)
    sample_size: Mapped[int] = mapped_column(Integer)
    summary_metrics_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class StrategyCandidate(Base):
    __tablename__ = "strategy_candidates"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    weekly_review_run_id: Mapped[int] = mapped_column(
        ForeignKey("intelligence.weekly_review_runs.id")
    )
    security_id: Mapped[UUID] = mapped_column()
    strategy_code: Mapped[str] = mapped_column(String(120), index=True)
    strategy_version_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("ref.decision_basis_versions.id"), nullable=True
    )
    strategy_status: Mapped[str] = mapped_column(String(40))
    fresh_cash_action_code: Mapped[str] = mapped_column(String(40))
    setup_quality_band: Mapped[str] = mapped_column(String(8))
    historical_evidence_tier: Mapped[str] = mapped_column(String(40))
    within_strategy_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_live_now: Mapped[bool] = mapped_column(Boolean, default=False)
    regime_fit: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    entry_preference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    invalidation_or_reassess: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_catalyst: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_now: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_not_stronger: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_band: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    board_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class CandidateSuppressor(Base):
    __tablename__ = "candidate_suppressors"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    strategy_candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("intelligence.strategy_candidates.id")
    )
    risk_rule_code: Mapped[str] = mapped_column(String(120))
    is_hard_block_for_fresh_cash: Mapped[bool] = mapped_column(Boolean, default=True)
    reason: Mapped[str] = mapped_column(Text)
    details_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class BoardRun(Base):
    __tablename__ = "board_runs"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    weekly_review_run_id: Mapped[int] = mapped_column(
        ForeignKey("intelligence.weekly_review_runs.id")
    )
    board_type: Mapped[str] = mapped_column(String(40))
    assembly_version: Mapped[str] = mapped_column(String(80))
    summary_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class BoardRow(Base):
    __tablename__ = "board_rows"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    board_run_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence.board_runs.id"))
    security_id: Mapped[UUID] = mapped_column()
    row_rank: Mapped[int] = mapped_column(Integer)
    start_here_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    primary_source_strategy_code: Mapped[str] = mapped_column(String(120))
    primary_candidate_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("intelligence.strategy_candidates.id"), nullable=True
    )
    fresh_cash_action_code: Mapped[str] = mapped_column(String(40))
    sleeve: Mapped[str] = mapped_column(String(40))
    historical_evidence_tier: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    setup_quality_band: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    entry_preference: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    invalidation_or_reassess: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_catalyst: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_now: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_not_stronger: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_band: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    confluence_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    promotion_reason_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class BoardRowSupportingStrategy(Base):
    __tablename__ = "board_row_supporting_strategies"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    board_row_id: Mapped[UUID] = mapped_column(ForeignKey("intelligence.board_rows.id"))
    supporting_strategy_code: Mapped[str] = mapped_column(String(120))
    supporting_candidate_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("intelligence.strategy_candidates.id"), nullable=True
    )
    support_type: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
