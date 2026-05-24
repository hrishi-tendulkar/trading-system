create extension if not exists pgcrypto;

create schema if not exists app;
create schema if not exists ref;
create schema if not exists raw;
create schema if not exists market;
create schema if not exists fundamentals;
create schema if not exists intelligence;
create schema if not exists ops;

create table if not exists ref.securities (
  id uuid primary key default gen_random_uuid(),
  ticker text not null,
  company_name text not null,
  primary_exchange text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (ticker)
);

create table if not exists ref.sectors (
  id uuid primary key default gen_random_uuid(),
  code text not null unique,
  name text not null
);

create table if not exists ref.benchmarks (
  id uuid primary key default gen_random_uuid(),
  code text not null unique,
  name text not null,
  ticker text not null
);

create table if not exists ref.sector_etf_map (
  sector_id uuid not null references ref.sectors(id) on delete cascade,
  benchmark_id uuid not null references ref.benchmarks(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (sector_id, benchmark_id)
);

create table if not exists ref.provider_symbols (
  id uuid primary key default gen_random_uuid(),
  security_id uuid not null references ref.securities(id) on delete cascade,
  provider text not null,
  provider_symbol text not null,
  created_at timestamptz not null default now(),
  unique (provider, provider_symbol),
  unique (security_id, provider)
);

create table if not exists app.watchlists (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name text not null,
  description text,
  is_default boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists app.watchlist_entries (
  id uuid primary key default gen_random_uuid(),
  watchlist_id uuid not null references app.watchlists(id) on delete cascade,
  security_id uuid not null references ref.securities(id) on delete cascade,
  position_status text not null default 'candidate',
  strategy_notes text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (watchlist_id, security_id)
);

create table if not exists app.watchlist_entry_history (
  id bigserial primary key,
  watchlist_entry_id uuid not null references app.watchlist_entries(id) on delete cascade,
  changed_at timestamptz not null default now(),
  change_type text not null,
  prior_value jsonb,
  new_value jsonb
);

create table if not exists raw.provider_payloads (
  id bigserial primary key,
  provider text not null,
  endpoint text not null,
  symbol text,
  request_params_json jsonb not null default '{}'::jsonb,
  payload_json jsonb not null,
  content_hash text,
  idempotency_key text,
  ingestion_run_id bigint,
  http_status integer,
  fetched_at timestamptz not null default now()
);

create index if not exists raw_provider_payloads_provider_endpoint_idx
  on raw.provider_payloads (provider, endpoint, fetched_at desc);

create table if not exists market.daily_prices (
  id bigserial primary key,
  security_id uuid not null references ref.securities(id) on delete cascade,
  as_of_date date not null,
  open numeric(18,6),
  high numeric(18,6),
  low numeric(18,6),
  close numeric(18,6),
  adjusted_close numeric(18,6),
  volume bigint,
  source_provider text not null,
  source_fetched_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (security_id, as_of_date, source_provider)
);

create index if not exists market_daily_prices_security_date_idx
  on market.daily_prices (security_id, as_of_date desc);

create table if not exists market.benchmark_prices (
  id bigserial primary key,
  benchmark_id uuid not null references ref.benchmarks(id) on delete cascade,
  as_of_date date not null,
  close numeric(18,6),
  volume bigint,
  source_provider text not null,
  source_fetched_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (benchmark_id, as_of_date, source_provider)
);

create table if not exists market.earnings_events (
  id bigserial primary key,
  security_id uuid not null references ref.securities(id) on delete cascade,
  earnings_date date not null,
  event_timing text,
  fiscal_period text,
  fiscal_year integer,
  estimate_eps numeric(18,6),
  actual_eps numeric(18,6),
  source_provider text not null,
  source_fetched_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (security_id, earnings_date, source_provider)
);

create table if not exists fundamentals.periods (
  id bigserial primary key,
  security_id uuid not null references ref.securities(id) on delete cascade,
  period_type text not null,
  fiscal_year integer not null,
  fiscal_period text not null,
  period_end_date date not null,
  source_provider text not null,
  source_fetched_at timestamptz not null,
  unique (security_id, period_type, fiscal_year, fiscal_period, source_provider)
);

create table if not exists fundamentals.income_statements (
  id bigserial primary key,
  period_id bigint not null references fundamentals.periods(id) on delete cascade,
  revenue numeric(20,2),
  gross_profit numeric(20,2),
  operating_income numeric(20,2),
  net_income numeric(20,2),
  eps_diluted numeric(18,6)
);

create table if not exists fundamentals.balance_sheets (
  id bigserial primary key,
  period_id bigint not null references fundamentals.periods(id) on delete cascade,
  cash_and_equivalents numeric(20,2),
  total_debt numeric(20,2),
  total_assets numeric(20,2),
  total_liabilities numeric(20,2)
);

create table if not exists fundamentals.cash_flow_statements (
  id bigserial primary key,
  period_id bigint not null references fundamentals.periods(id) on delete cascade,
  operating_cash_flow numeric(20,2),
  capital_expenditure numeric(20,2),
  free_cash_flow numeric(20,2)
);

create table if not exists intelligence.daily_digest_runs (
  id bigserial primary key,
  run_date date not null,
  status text not null,
  title text not null,
  summary text,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  unique (run_date, status)
);

create table if not exists intelligence.daily_digest_items (
  id bigserial primary key,
  digest_run_id bigint not null references intelligence.daily_digest_runs(id) on delete cascade,
  category text not null,
  headline text not null,
  detail text not null,
  sort_order integer not null default 0
);

create table if not exists intelligence.weekly_review_runs (
  id bigserial primary key,
  run_date date not null,
  status text not null,
  title text not null,
  summary text,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  unique (run_date, status)
);

create table if not exists intelligence.stock_scores (
  id bigserial primary key,
  weekly_review_run_id bigint not null references intelligence.weekly_review_runs(id) on delete cascade,
  security_id uuid not null references ref.securities(id) on delete cascade,
  action_label text not null,
  tradeability_score numeric(8,2),
  conviction_score numeric(8,2),
  overlay_suitability_score numeric(8,2),
  evidence_summary text,
  created_at timestamptz not null default now()
);

create table if not exists intelligence.stock_score_components (
  id bigserial primary key,
  stock_score_id bigint not null references intelligence.stock_scores(id) on delete cascade,
  component_name text not null,
  component_score numeric(8,2),
  notes text
);

create table if not exists intelligence.recommendations (
  id bigserial primary key,
  weekly_review_run_id bigint not null references intelligence.weekly_review_runs(id) on delete cascade,
  security_id uuid not null references ref.securities(id) on delete cascade,
  recommendation_new_position text not null,
  recommendation_if_already_held text not null,
  re_evaluate_if text,
  confidence text,
  created_at timestamptz not null default now()
);

create table if not exists ops.job_runs (
  id bigserial primary key,
  job_name text not null,
  status text not null,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  as_of_date date,
  market_session_date date,
  input_completeness_pct numeric(5,2),
  error_summary text
);

create table if not exists ops.job_run_steps (
  id bigserial primary key,
  job_run_id bigint not null references ops.job_runs(id) on delete cascade,
  step_name text not null,
  status text not null,
  detail text,
  created_at timestamptz not null default now()
);

create table if not exists ops.data_freshness (
  id bigserial primary key,
  domain_name text not null unique,
  last_successful_as_of_date date,
  last_successful_run_at timestamptz,
  notes text
);

create table if not exists ops.manual_actions (
  id bigserial primary key,
  action_name text not null,
  requested_by text not null default 'operator',
  requested_at timestamptz not null default now(),
  payload jsonb not null default '{}'::jsonb
);
