from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class JobResult(BaseModel):
    job_name: str
    status: str
    started_at: datetime
    finished_at: datetime
    as_of_date: date | None = None
    note: str
