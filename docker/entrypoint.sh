#!/usr/bin/env sh
set -eu

ROLE="${APP_ROLE:-web}"

if [ "$ROLE" = "web" ]; then
  exec python -m uvicorn apps.web.main:app --host 0.0.0.0 --port "${PORT:-8000}"
fi

if [ "$ROLE" = "daily-job" ]; then
  exec python -m services.jobs.cli daily-run
fi

if [ "$ROLE" = "weekly-job" ]; then
  exec python -m services.jobs.cli weekly-run
fi

if [ "$ROLE" = "manual-job" ]; then
  exec python -m services.jobs.cli --help
fi

echo "Unknown APP_ROLE: $ROLE" >&2
exit 1
