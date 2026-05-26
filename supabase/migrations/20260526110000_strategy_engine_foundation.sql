create schema if not exists research;

create table if not exists ref.decision_bases (
  id uuid primary key default gen_random_uuid(),
  basis_code text not null unique,
  basis_type text not null check (basis_type in ('trade_setup', 'risk_rule', 'context_lens')),
  display_name text not null,
  status text not null check (status in ('core', 'research', 'active', 'retired')),
  sleeve text not null check (sleeve in ('etf', 'single_name', 'context')),
  slug text not null unique,
  created_at timestamptz not null default now()
);

create table if not exists ref.decision_basis_versions (
  id uuid primary key default gen_random_uuid(),
  decision_basis_id uuid not null references ref.decision_bases(id) on delete cascade,
  version_num integer not null,
  version_label text not null,
  effective_from date not null,
  effective_to date,
  rules_summary_json jsonb not null default '{}'::jsonb,
  content_json jsonb not null default '{}'::jsonb,
  change_notes text,
  source_doc_path text,
  content_hash text,
  created_at timestamptz not null default now(),
  unique (decision_basis_id, version_num),
  unique (decision_basis_id, version_label)
);

create table if not exists ref.decision_basis_relationships (
  id bigserial primary key,
  from_basis_id uuid not null references ref.decision_bases(id) on delete cascade,
  to_basis_id uuid not null references ref.decision_bases(id) on delete cascade,
  relationship_type text not null,
  notes text,
  created_at timestamptz not null default now(),
  unique (from_basis_id, to_basis_id, relationship_type)
);

create table if not exists research.replay_runs (
  id uuid primary key default gen_random_uuid(),
  run_label text not null unique,
  generated_at timestamptz not null,
  universe text not null,
  source_watchlist_path text,
  source_prices_path text,
  manifest_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists research.replay_signal_events (
  id bigserial primary key,
  replay_run_id uuid not null references research.replay_runs(id) on delete cascade,
  strategy_code text not null,
  strategy_version_id uuid references ref.decision_basis_versions(id) on delete set null,
  security_id uuid references ref.securities(id) on delete set null,
  signal_date date not null,
  signal_style text not null,
  feature_snapshot_json jsonb not null default '{}'::jsonb,
  forward_return_5d numeric(18, 6),
  forward_return_10d numeric(18, 6),
  forward_return_15d numeric(18, 6),
  excess_return_5d numeric(18, 6),
  excess_return_10d numeric(18, 6),
  excess_return_15d numeric(18, 6),
  created_at timestamptz not null default now()
);

create index if not exists replay_signal_events_run_strategy_idx
  on research.replay_signal_events (replay_run_id, strategy_code, signal_date desc);

create table if not exists research.replay_strategy_summaries (
  id bigserial primary key,
  replay_run_id uuid not null references research.replay_runs(id) on delete cascade,
  strategy_code text not null,
  signal_style text not null,
  sample_size integer not null,
  avg_fwd_5d_return numeric(18, 6),
  avg_fwd_10d_return numeric(18, 6),
  avg_fwd_15d_return numeric(18, 6),
  avg_excess_5d_return numeric(18, 6),
  avg_excess_10d_return numeric(18, 6),
  avg_excess_15d_return numeric(18, 6),
  win_rate_5d numeric(18, 6),
  win_rate_10d numeric(18, 6),
  win_rate_15d numeric(18, 6),
  supportive_regime_share numeric(18, 6),
  created_at timestamptz not null default now(),
  unique (replay_run_id, strategy_code, signal_style)
);

create table if not exists research.replay_slice_stats (
  id bigserial primary key,
  replay_run_id uuid not null references research.replay_runs(id) on delete cascade,
  strategy_code text not null,
  slice_family text not null,
  slice_key_json jsonb not null default '{}'::jsonb,
  sample_size integer not null,
  summary_metrics_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists intelligence.strategy_candidates (
  id uuid primary key default gen_random_uuid(),
  weekly_review_run_id bigint not null references intelligence.weekly_review_runs(id) on delete cascade,
  security_id uuid not null references ref.securities(id) on delete cascade,
  strategy_code text not null,
  strategy_version_id uuid references ref.decision_basis_versions(id) on delete set null,
  strategy_status text not null,
  fresh_cash_action_code text not null,
  setup_quality_band text not null,
  historical_evidence_tier text not null,
  within_strategy_rank integer,
  is_live_now boolean not null default false,
  regime_fit text,
  entry_preference text,
  invalidation_or_reassess text,
  next_catalyst text,
  why_now text,
  why_not_stronger text,
  confidence_band text,
  board_eligible boolean not null default false,
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (weekly_review_run_id, security_id, strategy_code)
);

create index if not exists strategy_candidates_run_strategy_idx
  on intelligence.strategy_candidates (weekly_review_run_id, strategy_code, board_eligible);

create table if not exists intelligence.candidate_suppressors (
  id bigserial primary key,
  strategy_candidate_id uuid not null references intelligence.strategy_candidates(id) on delete cascade,
  risk_rule_code text not null,
  is_hard_block_for_fresh_cash boolean not null default true,
  reason text not null,
  details_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists intelligence.board_runs (
  id uuid primary key default gen_random_uuid(),
  weekly_review_run_id bigint not null references intelligence.weekly_review_runs(id) on delete cascade,
  board_type text not null check (board_type in ('fresh_cash_main', 'start_here', 'focus_queue', 'research_appendix')),
  assembly_version text not null,
  summary_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (weekly_review_run_id, board_type, assembly_version)
);

create table if not exists intelligence.board_rows (
  id uuid primary key default gen_random_uuid(),
  board_run_id uuid not null references intelligence.board_runs(id) on delete cascade,
  security_id uuid not null references ref.securities(id) on delete cascade,
  row_rank integer not null,
  start_here_rank integer,
  primary_source_strategy_code text not null,
  primary_candidate_id uuid references intelligence.strategy_candidates(id) on delete set null,
  fresh_cash_action_code text not null,
  sleeve text not null,
  historical_evidence_tier text,
  setup_quality_band text,
  entry_preference text,
  invalidation_or_reassess text,
  next_catalyst text,
  why_now text,
  why_not_stronger text,
  confidence_band text,
  confluence_note text,
  promotion_reason_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (board_run_id, security_id),
  unique (board_run_id, row_rank)
);

create table if not exists intelligence.board_row_supporting_strategies (
  id bigserial primary key,
  board_row_id uuid not null references intelligence.board_rows(id) on delete cascade,
  supporting_strategy_code text not null,
  supporting_candidate_id uuid references intelligence.strategy_candidates(id) on delete set null,
  support_type text not null,
  created_at timestamptz not null default now(),
  unique (board_row_id, supporting_strategy_code, support_type)
);
