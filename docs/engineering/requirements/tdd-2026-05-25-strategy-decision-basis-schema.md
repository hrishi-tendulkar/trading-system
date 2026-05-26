# TDD: Strategy Decision-Basis Schema

## Status

- Owner: Engineering + Product + Finance
- Status: Proposed
- Last updated: 2026-05-25

## Purpose

Define the persistence model needed to support the canonical multi-strategy architecture, weekly board assembly, strategy detail pages, and replay-backed strategy evaluation.

This design is intentionally aligned to:

- `docs/strategy/canonical-trading-strategies.md`
- `docs/strategy/weekly-board-assembly-spec.md`
- `packages/core/canonical_strategy_replay.py`
- `scripts/mlp/run_watchlist_analysis.py`
- `db/migrations/20260524110000_initial_platform_schema.sql`

## Canonical Decisions

1. The persistence model should center on per-strategy candidate evaluation first, then board promotion second.
   `board_rows` must not become the primary recommendation source.
2. A ticker can have exactly one `primary_source_strategy` on the board and zero-to-many `supporting_strategies`.
   Model this explicitly rather than inferring it from text.
3. Risk suppressors should be first-class records with a hard-block flag, not just labels on rows.
4. Strategy pages should render from versioned structured metadata plus replay summaries plus current live matches.
5. `No action` is an outcome, not a strategy.
   `benchmark-reference` and `event-risk-hold` are also not strategies; they are a context lens and a risk rule.

## Canonical Action Vocabulary

Use persisted enum codes plus display labels. Keep one field per decision dimension so holder actions and fresh-cash actions stop bleeding together.

### `fresh_cash_action_code`

- `BUY_NOW` -> `Buy now`
- `BUY_PULLBACK` -> `Buy on pullback`
- `WAIT_CONFIRMATION` -> `Wait for confirmation`
- `DO_NOT_CHASE` -> `Do not chase`
- `NO_ACTION` -> `No action`
- `SUPPRESSED` -> `Suppressed by risk rule`

### `position_action_code`

- `HOLD`
- `HOLD_ADD`
- `TRIM`
- `EXIT`
- `REVIEW_POST_EVENT`

### `expression_code`

- `STOCK_LONG`
- `ETF_LONG`
- `COVERED_CALL`
- `CASH_SECURED_PUT`
- `WAIT`

### Alias mapping to remove drift

- `Accumulate now` -> `BUY_NOW`
- `Wait for better entry` -> `BUY_PULLBACK`
- `Wait for pullback` -> `BUY_PULLBACK`
- `Hold existing long` and `Hold` -> move to `position_action_code`, never `fresh_cash_action_code`
- `Do nothing / monitor` -> `NO_ACTION`
- `Avoid due to event or risk` -> `SUPPRESSED`
- `Hold / reassess after earnings` -> `position_action_code=REVIEW_POST_EVENT` plus suppressor row
- `Benchmark reference` -> not an action; use `basis_type=CONTEXT_LENS`

## Schema / Storage Shape

Recommended core entities:

### `ref.decision_bases`

Stable registry for all named bases.

Fields:

- `id uuid`
- `basis_code text unique`
- `basis_type enum(trade_setup, risk_rule, context_lens)`
- `display_name`
- `status enum(core, research, active, retired)`
- `sleeve enum(etf, single_name, context)`
- `slug`
- `created_at`

### `ref.decision_basis_versions`

Versioned metadata and rules summary.

Fields:

- `id uuid`
- `decision_basis_id`
- `version_num int`
- `version_label text`
- `effective_from date`
- `effective_to date null`
- `rules_summary_json jsonb`
- `content_json jsonb`
- `change_notes text`
- `source_doc_path text`
- `content_hash text`

### `ref.decision_basis_relationships`

Links such as `supports`, `suppresses`, and `alternate_path`.

Fields:

- `from_basis_id`
- `to_basis_id`
- `relationship_type`
- `notes`

## Strategy Metadata Source Of Truth

Keep the repo as the source of truth and the database as a snapshot.

Recommended source layout:

- `config/decision_bases/*.yaml`
  or
- `config/strategy_registry.yaml`

Load those into:

- `ref.decision_bases`
- `ref.decision_basis_versions`

This keeps docs, replay, and app aligned while preserving historical snapshots in the database.

### Example `content_json`

```json
{
  "purpose": "Capture continuation with confirmation",
  "what_it_expresses": "Continuation with proof",
  "use_when": ["trend intact", "near resistance", "sector supportive"],
  "primary_actions": ["WAIT_CONFIRMATION", "BUY_NOW"],
  "doctrine": ["triggered entries only"],
  "main_risks": ["false breakouts", "crowded late entries"],
  "test_doctrine": ["triggered breakout entries only", "slice by regime and sector confirmation"],
  "page_sections": {
    "why_it_exists": "...",
    "known_failure_modes": ["..."],
    "interpretation_notes": ["..."]
  }
}
```

## Replay / Backtest Persistence

Align directly to the current replay artifact shape instead of inventing a different grain.

### `research.replay_runs`

One run per artifact directory.

Fields:

- `id uuid`
- `run_label`
- `generated_at`
- `universe`
- `source_watchlist_path`
- `source_prices_path`
- `manifest_json`

### `research.replay_signal_events`

Row grain = current `canonical_strategy_signals.csv`.

Fields:

- `replay_run_id`
- `strategy_code`
- `strategy_version_id null`
- `security_id`
- `signal_date`
- `signal_style`
- replay feature columns
- forward returns
- excess returns

### `research.replay_strategy_summaries`

Row grain = strategy-level summary.

Fields:

- `replay_run_id`
- `strategy_code`
- `signal_style`
- `sample_size`
- `avg_fwd_5d_return`
- `avg_excess_10d_return`
- `win_rate_15d`
- `supportive_regime_share`

### `research.replay_slice_stats`

Generic slice table instead of one table per CSV.

Fields:

- `replay_run_id`
- `strategy_code`
- `slice_family`
  - `regime`
  - `sector`
  - `pullback_band`
  - `breakout_context`
  - `mean_reversion_regime`
  - `etf_rotation`
- `slice_key_json`
- summary metrics

This preserves today’s CSV exports while giving the product a normalized query model.

## Weekly Evaluation / Board Persistence

### `intelligence.weekly_review_runs`

Keep the existing parent run table, but treat it as the top-level weekly review object.

### `intelligence.strategy_candidates`

Row grain = one ticker evaluated by one strategy for one weekly run.

Fields:

- `id uuid`
- `weekly_review_run_id`
- `security_id`
- `strategy_code`
- `strategy_version_id`
- `strategy_status`
- `fresh_cash_action_code`
- `setup_quality_band`
- `historical_evidence_tier`
- `within_strategy_rank`
- `is_live_now boolean`
- `regime_fit`
- `entry_preference`
- `invalidation_or_reassess`
- `next_catalyst`
- `why_now`
- `why_not_stronger`
- `confidence_band`
- `board_eligible boolean`
- `metadata_json`

### `intelligence.candidate_suppressors`

Fields:

- `strategy_candidate_id`
- `risk_rule_code`
- `is_hard_block_for_fresh_cash`
- `reason`
- `details_json`

### `intelligence.board_runs`

One row per weekly board assembly pass.

Fields:

- `id uuid`
- `weekly_review_run_id`
- `board_type`
  - `fresh_cash_main`
  - `start_here`
  - `focus_queue`
  - `research_appendix`
- `assembly_version`
- `summary_json`

### `intelligence.board_rows`

Row grain = one promoted ticker.

Fields:

- `id uuid`
- `board_run_id`
- `security_id`
- `row_rank`
- `start_here_rank null`
- `primary_source_strategy_code`
- `primary_candidate_id`
- `fresh_cash_action_code`
- `sleeve`
- `historical_evidence_tier`
- `setup_quality_band`
- `entry_preference`
- `invalidation_or_reassess`
- `next_catalyst`
- `why_now`
- `why_not_stronger`
- `confidence_band`
- `confluence_note`
- `promotion_reason_json`

### `intelligence.board_row_supporting_strategies`

Fields:

- `board_row_id`
- `supporting_strategy_code`
- `supporting_candidate_id`
- `support_type`

### `intelligence.board_row_suppressors`

Optional for focus or rejected views.

Fields:

- `board_row_id`
- `risk_rule_code`
- `reason`

## Links Between Overview, Stock Detail, And Strategy Detail

Use foreign keys and slugs, not hardcoded URLs.

- Overview row -> stock detail: `board_rows.security_id`
- Overview row -> strategy detail: `board_rows.primary_source_strategy_code`
- Stock detail -> strategy detail: latest `strategy_candidates` for that `security_id`, plus `board_row_supporting_strategies`
- Strategy detail -> live matches: query `strategy_candidates` where `strategy_code = ?` and `weekly_review_run_id = latest`
- Strategy detail -> replay evidence: query `research.replay_*` where `strategy_code = ?`

Recommended route keys:

- stock page: `/stocks/{ticker}`
- strategy page: `/strategies/{basis_code}`
- weekly board: `/weekly/{run_date}`

## MVP Vs Later

### MVP

- `ref.decision_bases`
- `ref.decision_basis_versions`
- `research.replay_runs`
- `research.replay_signal_events`
- `research.replay_strategy_summaries`
- `intelligence.strategy_candidates`
- `intelligence.candidate_suppressors`
- `intelligence.board_runs`
- `intelligence.board_rows`
- `intelligence.board_row_supporting_strategies`

### Later

- `research.replay_slice_stats`
- generic `decision_basis_relationships`
- dedicated focus queue or research appendix boards
- point-in-time earnings or revision suppressor evidence
- holder-action and overlay-action tables
- content-generation cache for strategy pages

## Migration Notes

- `intelligence.stock_scores` and `intelligence.recommendations` are too monolithic for the new architecture.
  Keep them for backward compatibility, but treat them as deprecated projections.
- `ui_data.py` is currently masking label drift in code.
  Replace that mapping with canonical persisted enum codes.
- `run_watchlist_analysis.py` currently uses mixed concepts as `strategy_id`.
  Re-map:
  - `etf-rotation` -> `etf-trend-rotation`
  - `strong-stock-constructive-pullback` -> `sector-confirmed-pullback-continuation`
  - `wait-for-confirmation` -> `breakout-confirmation`
  - `event-risk-hold` -> `risk_rule_code=event-freeze-before-earnings`
  - `benchmark-reference` -> `basis_type=context_lens`
  - `no-action` -> remove as a strategy id; persist as `fresh_cash_action_code=NO_ACTION`

## Naming And Versioning Conventions

- Current replay slugs in `canonical_strategy_replay.py` are good candidates for canonical external IDs.
  Keep those stable and use UUIDs only as internal primary keys.
- Use this versioning convention:
  - `basis_code`: stable forever, slug form
  - `version_num`: monotonic integer
  - `version_label`: human-readable, for example `2026-05-25.1`
- Effective dating on versions is required so historical board rows can always point to the exact rule metadata they were generated from.

## Bottom Line

The right core model is:

`decision basis registry -> versioned strategy metadata -> per-strategy weekly candidates -> suppressors -> promoted board rows`

Replay should be persisted at signal-event grain, with a strict canonical action-enum layer so docs, code, and product stop drifting apart.
