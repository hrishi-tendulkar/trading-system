from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
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
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    as_of_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    market_session_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    input_completeness_pct: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class WeeklyReviewRun(Base):
    __tablename__ = "weekly_review_runs"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    run_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    job_run_id: Mapped[int | None] = mapped_column(ForeignKey("ops.job_runs.id"), nullable=True)


class StockScore(Base):
    __tablename__ = "stock_scores"
    __table_args__ = {"schema": "intelligence"}

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("intelligence.weekly_review_runs.id"))
    action_label: Mapped[str] = mapped_column(String(80))
    tradeability_score: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    conviction_score: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
