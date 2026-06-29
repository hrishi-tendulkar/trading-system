from __future__ import annotations

import subprocess
import sys
from datetime import date, datetime, timezone

import typer

from packages.core.config import get_settings
from packages.core.strategy_registry import load_strategy_registry
from packages.core.strategy_views import get_strategy_page_view, list_strategy_pages
from packages.core.weekly_runs import (
    LocalWeeklyRunRepository,
    SupabaseWeeklyRunRepository,
    load_current_manifest,
)
from packages.schemas.jobs import JobResult
from services.jobs.notifications import send_email
from services.jobs.weekly_validation import notify_weekly_result, validate_weekly_current

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
    watchlist: str = typer.Option(
        "data/reference/sp100_watchlist.csv",
        help="Reference watchlist CSV to use for the weekly run.",
    ),
    raw_outdir: str = typer.Option(
        "data/raw/sp100_5y",
        help="Directory for raw price and earnings CSVs.",
    ),
    processed_outdir: str = typer.Option(
        "data/processed/sp100_current",
        help="Directory for processed weekly outputs before publishing.",
    ),
    notify: bool = typer.Option(
        settings.environment != "development",
        help="Send success/failure email notification.",
    ),
) -> None:
    if not settings.weekly_run_enabled:
        raise typer.Exit(code=0)
    command = [sys.executable, "scripts/mlp/publish_weekly_run.py"]
    if run_date:
        command.extend(["--target-week", run_date])
    if skip_fetch:
        command.append("--skip-fetch")
    command.extend(
        [
            "--watchlist",
            watchlist,
            "--raw-outdir",
            raw_outdir,
            "--processed-outdir",
            processed_outdir,
        ]
    )
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        if notify:
            _send_job_email(
                subject="[Trading System] Weekly publish failed",
                body=(
                    "Weekly publish failed.\n\n"
                    f"Command: {' '.join(command)}\n"
                    f"Exit code: {exc.returncode}\n\n"
                    f"STDOUT:\n{exc.stdout or ''}\n\n"
                    f"STDERR:\n{exc.stderr or ''}\n"
                ),
            )
        typer.echo(exc.stdout or "", nl=False)
        typer.echo(exc.stderr or "", err=True, nl=False)
        raise typer.Exit(code=exc.returncode) from exc

    typer.echo(completed.stdout or "", nl=False)
    typer.echo(completed.stderr or "", err=True, nl=False)
    if notify:
        manifest = load_current_manifest()
        _send_job_email(
            subject="[Trading System] Weekly publish succeeded",
            body=(
                "Weekly publish succeeded.\n\n"
                f"Run ID: {manifest.run_id if manifest else 'unknown'}\n"
                f"Recommendation week: "
                f"{manifest.recommendation_week_start if manifest else 'unknown'}\n"
                f"Source data through: {manifest.source_data_through if manifest else 'unknown'}\n"
            ),
        )


@app.command("backfill-weekly-runs-to-supabase")
def backfill_weekly_runs_to_supabase(
    dry_run: bool = typer.Option(False, help="Print planned imports without writing."),
) -> None:
    local_repo = LocalWeeklyRunRepository()
    target_repo = SupabaseWeeklyRunRepository()
    manifests = list(reversed(local_repo.list_manifests()))
    current = local_repo.load_current_manifest()
    for manifest in manifests:
        recommendations_path = local_repo.run_dir(manifest.run_id) / manifest.recommendations_path
        if not recommendations_path.exists():
            typer.echo(f"Skipping {manifest.run_id}: missing {recommendations_path}")
            continue
        publish_current = bool(current and current.run_id == manifest.run_id)
        typer.echo(
            f"{'Would import' if dry_run else 'Importing'} {manifest.run_id}"
            f"{' as current' if publish_current else ''}"
        )
        if dry_run:
            continue
        target_repo.write_run_snapshot(
            manifest=manifest,
            recommendations_source=recommendations_path,
            publish_current=publish_current,
        )
    typer.echo("Backfill complete." if not dry_run else "Dry run complete.")


@app.command("validate-weekly-current")
def validate_weekly_current_command(
    as_of_date: str = typer.Option("", help="Optional YYYY-MM-DD validation date."),
    base_url: str = typer.Option("", help="Production app base URL to check."),
    check_web: bool = typer.Option(True, help="Check the deployed /weekly page."),
    notify: bool = typer.Option(
        settings.environment != "development",
        help="Send success/failure email notification.",
    ),
) -> None:
    result = validate_weekly_current(
        as_of_date=date.fromisoformat(as_of_date) if as_of_date else date.today(),
        base_url=base_url or settings.app_base_url,
        check_web=check_web,
    )
    typer.echo(
        {
            "ok": result.ok,
            "expected_week": result.expected_week,
            "expected_source_through": result.expected_source_through,
            "run_id": result.run_id,
            "messages": result.messages,
        }
    )
    if notify:
        try:
            notify_weekly_result(
                subject="[Trading System] Weekly validation "
                + ("succeeded" if result.ok else "failed"),
                result=result,
            )
        except RuntimeError as exc:
            typer.echo(f"Email notification failed: {exc}", err=True)
    if not result.ok:
        raise typer.Exit(code=1)


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


def _send_job_email(*, subject: str, body: str) -> None:
    try:
        send_email(settings, subject=subject, body=body)
    except RuntimeError as exc:
        typer.echo(f"Email notification failed: {exc}", err=True)


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
