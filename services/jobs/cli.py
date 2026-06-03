from __future__ import annotations

import subprocess
import sys
from datetime import date, datetime, timezone

import typer

from packages.core.config import get_settings
from packages.core.strategy_registry import load_strategy_registry
from packages.core.strategy_views import get_strategy_page_view, list_strategy_pages
from packages.schemas.jobs import JobResult

app = typer.Typer(help="Trading System batch jobs and manual operator commands.")
settings = get_settings()


def _build_result(job_name: str, note: str, as_of_date: date | None = None) -> JobResult:
    started = datetime.now(timezone.utc)  # noqa: UP017
    finished = datetime.now(timezone.utc)  # noqa: UP017
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
        (
            "Daily job scaffold is in place. Next step is wiring provider pulls, "
            "normalization, and publish gates."
        ),
        date.fromisoformat(as_of_date) if as_of_date else None,
    )
    _print_result(result)


@app.command("weekly-run")
def weekly_run(
    run_date: str = typer.Option("", help="Optional Monday YYYY-MM-DD recommendation week."),
    skip_fetch: bool = typer.Option(False, help="Use existing raw price data."),
) -> None:
    if not settings.weekly_run_enabled:
        raise typer.Exit(code=0)
    command = [sys.executable, "scripts/mlp/publish_weekly_run.py"]
    if run_date:
        command.extend(["--target-week", run_date])
    if skip_fetch:
        command.append("--skip-fetch")
    subprocess.run(command, check=True)


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
def rebuild_weekly_review(
    run_date: str = typer.Option("", help="Optional YYYY-MM-DD override.")
) -> None:
    note = "Weekly review rebuild scaffold is ready."
    if run_date:
        note = f"Weekly review rebuild scaffold is ready for {run_date}."
    _print_result(_build_result("rebuild-weekly-review", note))


@app.command("validate-run-completeness")
def validate_run_completeness(run_kind: str = typer.Argument(..., help="daily or weekly")) -> None:
    result = _build_result(
        "validate-run-completeness",
        (
            f"Completeness validation scaffold is ready for {run_kind}. "
            "This command should later enforce publish gates."
        ),
    )
    _print_result(result)


@app.command("list-decision-bases")
def list_decision_bases() -> None:
    registry = load_strategy_registry()
    for record in registry.decision_bases:
        typer.echo(
            f"{record.basis_code}: {record.display_name} | trust={record.trust_level} "
            f"| promotion={record.promotion_status}"
        )


@app.command("preview-strategy-engine")
def preview_strategy_engine(
    basis_code: str = typer.Option("", help="Optional strategy basis code.")
) -> None:
    basis_codes = (
        [basis_code]
        if basis_code
        else [page["basis_code"] for page in list_strategy_pages()]
    )
    for code in basis_codes:
        view = get_strategy_page_view(code)
        if view is None:
            typer.echo(f"{code}: not found")
            continue
        typer.echo(
            f"{code}: live={view.stats['live_matches']} board={view.stats['board_promoted']} "
            f"strategy_only={view.stats['strategy_only']} suppressed={view.stats['suppressed']}"
        )


if __name__ == "__main__":
    app()
