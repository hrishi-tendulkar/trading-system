#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from packages.core.strategy_registry import (  # noqa: E402
    get_active_strategy_versions,
    get_strategy_registry_version,
)
from packages.core.universes import KNOWN_UNIVERSES  # noqa: E402
from packages.core.weekly_runs import (  # noqa: E402
    WeeklyRunManifest,
    current_utc_timestamp,
    default_publish_week_start,
    legacy_recommendations_path,
    load_current_manifest,
    prior_market_close_for_week,
    repo_root,
    run_id_for_week,
    update_manifest_status,
    week_end,
    write_run_snapshot,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a validated weekly recommendation run.")
    parser.add_argument(
        "--target-week",
        default="",
        help="Monday YYYY-MM-DD for the recommendation week. Defaults to current week.",
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Use existing raw price CSV instead of refreshing provider data first.",
    )
    parser.add_argument("--watchlist", default="data/reference/phase2_watchlist.csv")
    parser.add_argument("--raw-outdir", default="data/raw/phase2")
    parser.add_argument("--processed-outdir", default="data/processed/phase2")
    parser.add_argument("--start", default="", help="Optional inclusive raw price start date.")
    return parser.parse_args()


def universe_slug_for_watchlist(path_value: str) -> str:
    normalized = Path(path_value).as_posix()
    for slug, path in KNOWN_UNIVERSES.items():
        if path.as_posix() == normalized:
            return slug
    return "custom"


def read_first_date(path: Path) -> date:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        first = next(reader)
    return date.fromisoformat(first["date"])


def read_latest_date(path: Path) -> date:
    latest: date | None = None
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row_date = date.fromisoformat(row["date"])
            if latest is None or row_date > latest:
                latest = row_date
    if latest is None:
        raise RuntimeError(f"No rows found in {path}")
    return latest


def ensure_existing_archive() -> None:
    source = legacy_recommendations_path()
    if not source.exists():
        return
    existing_date = read_first_date(source)
    run_id = run_id_for_week(existing_date, existing_date)
    manifest_path = repo_root() / "data" / "processed" / "weekly_runs" / run_id / "manifest.json"
    if manifest_path.exists():
        return
    timestamp = f"{existing_date.isoformat()}T21:00:00+00:00"
    manifest = WeeklyRunManifest(
        run_id=run_id,
        recommendation_week_start=existing_date.isoformat(),
        recommendation_week_end=existing_date.isoformat(),
        published_at=timestamp,
        timezone="America/New_York",
        market_data_through=existing_date.isoformat(),
        source_data_through=existing_date.isoformat(),
        last_checked_at=timestamp,
        run_status="superseded",
        engine_version="mlp-watchlist-v1",
        strategy_registry_version=get_strategy_registry_version(),
        input_snapshot_id=f"legacy-phase2-{existing_date.isoformat()}",
        output_snapshot_id=run_id,
        recommendations_path="recommendations.csv",
        created_at=timestamp,
        universe="phase2",
        source_watchlist_path="data/reference/phase2_watchlist.csv",
        active_strategy_versions=get_active_strategy_versions(),
    )
    write_run_snapshot(manifest=manifest, recommendations_source=source, publish_current=False)


def run_command(command: list[str]) -> None:
    subprocess.run(command, cwd=repo_root(), check=True)


def publish_weekly_run(args: argparse.Namespace) -> WeeklyRunManifest:
    target_week = (
        date.fromisoformat(args.target_week)
        if args.target_week
        else default_publish_week_start(date.today())
    )
    if target_week.weekday() != 0:
        raise RuntimeError(f"Target week must be a Monday, got {target_week.isoformat()}")

    universe = universe_slug_for_watchlist(args.watchlist)
    source_through = prior_market_close_for_week(target_week)
    fetch_end = source_through + timedelta(days=1)
    raw_prices = repo_root() / args.raw_outdir / "mlp_prices.csv"
    existing_start = args.start or (
        read_first_date(raw_prices).isoformat() if raw_prices.exists() else "2023-05-01"
    )

    ensure_existing_archive()

    if not args.skip_fetch:
        run_command(
            [
                sys.executable,
                "scripts/mlp/fetch_watchlist_prices.py",
                "--watchlist",
                args.watchlist,
                "--start",
                existing_start,
                "--end",
                fetch_end.isoformat(),
                "--outdir",
                args.raw_outdir,
            ]
        )

    latest_raw_date = read_latest_date(raw_prices)
    if latest_raw_date < source_through:
        raise RuntimeError(
            f"Source data is stale: expected through {source_through.isoformat()}, "
            f"got {latest_raw_date.isoformat()}"
        )

    report_path = f"docs/research/market/{universe}-weekly-report-{target_week.isoformat()}.md"
    run_command(
        [
            sys.executable,
            "scripts/mlp/run_watchlist_analysis.py",
            "--watchlist",
            args.watchlist,
            "--prices",
            f"{args.raw_outdir}/mlp_prices.csv",
            "--earnings",
            f"{args.raw_outdir}/mlp_earnings_snapshot.csv",
            "--outdir",
            args.processed_outdir,
            "--report",
            report_path,
        ]
    )

    recommendations = repo_root() / args.processed_outdir / "mlp_current_recommendations.csv"
    latest_recommendation_date = read_latest_date(recommendations)
    if latest_recommendation_date != source_through:
        raise RuntimeError(
            f"Weekly analysis output date mismatch: expected {source_through.isoformat()}, "
            f"got {latest_recommendation_date.isoformat()}"
        )

    published_at = current_utc_timestamp()
    run_id = run_id_for_week(target_week, date.fromisoformat(published_at[:10]))
    previous_current = load_current_manifest()
    manifest = WeeklyRunManifest(
        run_id=run_id,
        recommendation_week_start=target_week.isoformat(),
        recommendation_week_end=week_end(target_week).isoformat(),
        published_at=published_at,
        timezone="America/New_York",
        market_data_through=source_through.isoformat(),
        source_data_through=source_through.isoformat(),
        last_checked_at=published_at,
        run_status="published",
        engine_version="mlp-watchlist-v1",
        strategy_registry_version=get_strategy_registry_version(),
        input_snapshot_id=f"{universe}-prices-through-{source_through.isoformat()}",
        output_snapshot_id=run_id,
        recommendations_path="recommendations.csv",
        created_at=published_at,
        universe=universe,
        source_watchlist_path=args.watchlist,
        active_strategy_versions=get_active_strategy_versions(),
    )
    write_run_snapshot(
        manifest=manifest,
        recommendations_source=recommendations,
        publish_current=True,
    )
    if previous_current and previous_current.run_id != manifest.run_id:
        update_manifest_status(previous_current.run_id, "superseded")
    return manifest


def main() -> None:
    manifest = publish_weekly_run(parse_args())
    print(f"Published weekly run {manifest.run_id}")
    print(f"Recommendation week: {manifest.recommendation_week_start}")
    print(f"Data through: {manifest.source_data_through}")


if __name__ == "__main__":
    main()
