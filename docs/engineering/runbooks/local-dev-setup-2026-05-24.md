# Local Dev Setup

## Purpose

Document the fastest path to run the current Trading System scaffold locally.

## 1. Install dependencies

```bash
cd "/Users/hrishimansi/Documents/Hrishi/Projects/Trading System"
make install
```

## 2. Copy environment template

```bash
cp .env.example .env
```

Replace dummy values when available.

## 3. Run the web app

```bash
make run-web
```

Expected local URL:

- `http://localhost:8000/login`

## 4. Run the batch jobs

```bash
make daily
make weekly
```

## Notes

- The current scaffold uses sample UI payloads until database-backed published runs are wired.
- The first real database step is applying the migration under `supabase/migrations/`.
- The first real provider step is replacing `FMP_API_KEY` with a live value.
