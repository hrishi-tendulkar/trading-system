# Platform Projects

## Purpose

Record the platform resources created for the Trading System workspace so future setup and development work can reference a single source of truth.

## Canonical project name

- Human-readable project name: `Trading System`
- GitHub repository slug: `trading-system`

## GitHub

- Owner: `hrishi-tendulkar`
- Repository: `trading-system`
- URL: `https://github.com/hrishi-tendulkar/trading-system`
- Default branch: `main`

## Supabase

- Project name: `Trading System`
- Project ref: `pyijnabhkkwjoslycaqf`
- Organization id: `qdhiuivpqhjzwhlkwrji`
- Region: `us-east-1`
- Dashboard: `https://supabase.com/dashboard/project/pyijnabhkkwjoslycaqf`
- Local workspace status: linked

## Railway

- Project name: `Trading System`
- Project id: `7666b997-8ace-4284-b807-b4047b62cf1c`
- Workspace id: `d035d7d1-697f-4ed5-a939-6d47d9a52c01`
- Dashboard: `https://railway.com/project/7666b997-8ace-4284-b807-b4047b62cf1c`
- Local workspace status: linked

## Notes

- The current shell environment contains a stale `RAILWAY_TOKEN` that causes Railway CLI auth failures.
- Railway CLI access works when commands are run with `env -u RAILWAY_TOKEN ...`, which uses the valid local Railway session instead.
- Use [`docs/operations/railway-cli-troubleshooting.md`](./railway-cli-troubleshooting.md) for the full decision tree. The short version is: try `./scripts/railway_safe.sh <command>` first, and only fall back to `railway login` if the safe path still fails with `invalid_grant`.
- The Supabase project was linked locally, which created `supabase/.temp/` metadata. That path is ignored in git because it is machine-local state.
- The database password used at project creation time is not stored in this repository.
