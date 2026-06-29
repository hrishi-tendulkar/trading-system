alter table intelligence.weekly_review_runs
  add column if not exists run_id text,
  add column if not exists recommendation_week_start date,
  add column if not exists recommendation_week_end date,
  add column if not exists timezone text not null default 'America/New_York',
  add column if not exists market_data_through date,
  add column if not exists source_data_through date,
  add column if not exists last_checked_at timestamptz,
  add column if not exists engine_version text,
  add column if not exists strategy_registry_version text,
  add column if not exists input_snapshot_id text,
  add column if not exists output_snapshot_id text,
  add column if not exists universe text,
  add column if not exists source_watchlist_path text,
  add column if not exists active_strategy_versions_json jsonb not null default '{}'::jsonb,
  add column if not exists manifest_json jsonb not null default '{}'::jsonb,
  add column if not exists failure_reason text,
  add column if not exists updated_at timestamptz not null default now();

do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'weekly_review_runs_run_id_key'
  ) then
    alter table intelligence.weekly_review_runs
      add constraint weekly_review_runs_run_id_key unique (run_id);
  end if;
end $$;

do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'weekly_review_runs_status_check'
  ) then
    alter table intelligence.weekly_review_runs
      add constraint weekly_review_runs_status_check
      check (status in ('building', 'validation_failed', 'failed', 'published', 'superseded'));
  end if;
end $$;

create table if not exists intelligence.weekly_current_run (
  id integer primary key default 1,
  run_id text not null references intelligence.weekly_review_runs(run_id) on delete restrict,
  published_at timestamptz not null,
  updated_at timestamptz not null default now(),
  constraint weekly_current_run_singleton check (id = 1)
);

create table if not exists intelligence.weekly_recommendation_records (
  id bigserial primary key,
  run_id text not null references intelligence.weekly_review_runs(run_id) on delete cascade,
  ticker text not null,
  company text,
  as_of_date date,
  action_label text,
  holder_bucket text,
  strategy_name text,
  observed_reason text,
  event_risk text,
  stop_label text,
  stop_value text,
  action_rank integer not null default 0,
  raw_record_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists weekly_recommendation_records_run_rank_idx
  on intelligence.weekly_recommendation_records (run_id, action_rank, ticker);

create table if not exists intelligence.weekly_run_payloads (
  id bigserial primary key,
  run_id text not null references intelligence.weekly_review_runs(run_id) on delete cascade,
  payload_name text not null,
  payload_json jsonb not null default '{}'::jsonb,
  content_hash text,
  created_at timestamptz not null default now(),
  unique (run_id, payload_name)
);

create index if not exists weekly_review_runs_current_lookup_idx
  on intelligence.weekly_review_runs (recommendation_week_start desc, published_at desc)
  where status in ('published', 'superseded');
