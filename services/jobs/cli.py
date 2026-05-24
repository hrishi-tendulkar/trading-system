from __future__ import annotations

from datetime import date, datetime, timezone

import typer

from packages.core.config import get_settings
from packages.schemas.jobs import JobResult


app = typer.Typer(help="Trading System batch jobs and manual operator commands.")
settings = get_settings()


def _build_result(job_name: str, note: str, as_of_date: date | None = None) -> JobResult:
    started = datetime.now(timezone.utc)
    finished = datetime.now(timezone.utc)
    return JobResult(
        job_name=job_name,
        status="placeholder",
        started_at=started,
        finished_at=finished,
        as_of_date=as_of_date,
        note=note,
    )


def _print_result(result: JobResult) -> None:
    typer.echo(result.model_dump_json(indent=2))


@app.command("daily-run")
def daily_run(as_of_date: str = typer.Option("", help="Optional YYYY-MM-DD override.")) -> None:
    if not settings.daily_run_enabled:
        raise typer.Exit(code=0)
    result = _build_result(
        "daily-run",
        "Daily job scaffold is in place. Next step is wiring provider pulls, normalization, and publish gates.",
        date.fromisoformat(as_of_date) if as_of_date else None,
    )
    _print_result(result)


@app.command("weekly-run")
def weekly_run(run_date: str = typer.Option("", help="Optional YYYY-MM-DD override.")) -> None:
    if not settings.weekly_run_enabled:
        raise typer.Exit(code=0)
    result = _build_result(
        "weekly-run",
        "Weekly job scaffold is in place. Next step is score generation, published-run state, and HTML artifact persistence.",
        date.fromisoformat(run_date) if run_date else None,
    )
    _print_result(result)


@app.command("backfill-symbol")
def backfill_symbol(
    ticker: str = typer.Argument(..., help="Ticker to backfill."),
    start_date: str = typer.Option("", help="Optional YYYY-MM-DD start."),
) -> None:
    result = _build_result(
        "backfill-symbol",
        f"Backfill scaffold is ready for {ticker.upper()}. Start date: {start_date or 'default'}.",
    )
    _print_result(result)


@app.command("rebuild-features")
def rebuild_features(ticker: str = typer.Option("", help="Optional single ticker.")) -> None:
    note = "Feature rebuild scaffold is ready."
    if ticker:
        note = f"Feature rebuild scaffold is ready for {ticker.upper()}."
    _print_result(_build_result("rebuild-features", note))


@app.command("rebuild-weekly-review")
def rebuild_weekly_review(run_date: str = typer.Option("", help="Optional YYYY-MM-DD override.")) -> None:
    note = "Weekly review rebuild scaffold is ready."
    if run_date:
        note = f"Weekly review rebuild scaffold is ready for {run_date}."
    _print_result(_build_result("rebuild-weekly-review", note))


@app.command("validate-run-completeness")
def validate_run_completeness(run_kind: str = typer.Argument(..., help="daily or weekly")) -> None:
    result = _build_result(
        "validate-run-completeness",
        f"Completeness validation scaffold is ready for {run_kind}. This command should later enforce publish gates.",
    )
    _print_result(result)


if __name__ == "__main__":
    app()
