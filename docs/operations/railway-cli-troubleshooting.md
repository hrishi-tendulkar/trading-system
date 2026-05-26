# Railway CLI Troubleshooting

## Why this exists

This workspace repeatedly hits a misleading Railway CLI failure mode. The first error often looks like:

- `Unauthorized. Please run railway login again.`

That message is sometimes correct, but often it is not the real first problem.

## The two actual failure modes

### 1. Stale shell `RAILWAY_TOKEN` overrides the local Railway session

Symptom:

- `railway whoami`
- `railway status`
- `railway up`

fail even though the project is linked locally.

In this workspace, the shell currently exports:

- `RAILWAY_TOKEN=...`

from `~/.zshrc`.

That token is stale and overrides the Railway CLI's linked local session.

Quick fix:

```bash
env -u RAILWAY_TOKEN railway whoami
env -u RAILWAY_TOKEN railway status
env -u RAILWAY_TOKEN railway up
```

Safer repo-local wrapper:

```bash
./scripts/railway_safe.sh whoami
./scripts/railway_safe.sh status
./scripts/railway_safe.sh up
```

Permanent local fix:

- Remove the `export RAILWAY_TOKEN=...` line from `~/.zshrc`
- Open a new shell
- Prefer the linked local Railway session over a manually exported token

### 2. The linked local Railway OAuth session is actually expired

Symptom:

- Even after unsetting `RAILWAY_TOKEN`, Railway still fails with:

```text
Warning: failed to refresh OAuth token: Token refresh failed: invalid_grant: grant request is invalid.
Unauthorized. Please run `railway login` again.
```

What this means:

- The problem is no longer the shell env var
- The local Railway refresh token in `~/.railway/config.json` is stale or invalid

Observed local signal:

- `~/.railway/config.json` contains a linked project entry for `Trading System`
- but the `user.tokenExpiresAt` value is already expired
- and refresh attempts return `invalid_grant`

Actual fix:

```bash
env -u RAILWAY_TOKEN railway login
```

After that, validate with:

```bash
./scripts/railway_safe.sh whoami
./scripts/railway_safe.sh status
```

## Recommended debug order

When Railway CLI fails in this repo, do this in order:

1. Check whether the shell is exporting a token:

```bash
env | rg '^RAILWAY_TOKEN'
```

2. If present, retry with the env var removed:

```bash
./scripts/railway_safe.sh whoami
```

3. If that works:

- the problem was the stale shell token
- remove the `RAILWAY_TOKEN` export from `~/.zshrc`

4. If it still fails with `invalid_grant`:

- the local Railway session is genuinely expired
- run:

```bash
env -u RAILWAY_TOKEN railway login
```

## Trading System specifics

Current linked Railway project:

- Project: `Trading System`
- Project id: `7666b997-8ace-4284-b807-b4047b62cf1c`
- Dashboard: `https://railway.com/project/7666b997-8ace-4284-b807-b4047b62cf1c`

Current production app:

- `https://trading-system-web-production.up.railway.app`

## Practical rule

For this repo, do **not** start with `railway login`.

Start with:

```bash
./scripts/railway_safe.sh <command>
```

Only use `railway login` if the safe wrapper still fails with `invalid_grant`.
