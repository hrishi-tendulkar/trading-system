# Strategy Versioning And Revision Archive

## Purpose

Define how Trading System names, versions, archives, promotes, and reconstructs strategy rule changes.

The goal is simple:

- know which strategy version generated each weekly report,
- compare old and new versions without mutating history,
- recover cases where an older version later proves better,
- and add new strategies without losing lineage.

## Core Principle

A strategy is a stable family. A version is a specific measurable rule set inside that family.

Example:

- Strategy family: `breakout-confirmation`
- Version: `breakout-confirmation.v2`
- Human label: `Supportive + Sector-Confirmed Breakout`
- Production status: promoted

Do not create a new strategy family for every threshold change. Create a new version when the behavioral rule set changes enough that future outcomes should be evaluated separately.

## Naming Convention

### Stable Strategy Code

Use `basis_code` as the permanent external ID.

Rules:

- lowercase slug format
- never reuse a code for a different behavioral thesis
- safe for URLs, database keys, filenames, and report metadata

Examples:

- `breakout-confirmation`
- `sector-confirmed-pullback-continuation`
- `etf-trend-rotation`
- `selective-mean-reversion`

### Version Label

Use this format:

```text
{basis_code}.v{version_num}
```

Examples:

- `breakout-confirmation.v1`
- `breakout-confirmation.v2`
- `etf-trend-rotation.v3`

### Registry Version

Use a date plus sequence:

```text
YYYY-MM-DD.N
```

Example:

- `2026-06-07.1`

The registry version represents the whole active strategy set, not one strategy.

## What Requires A New Strategy Version

Create a new version when any of these change:

- board-eligible rule gates
- trigger definition
- regime requirements
- sector confirmation requirements
- holding-period assumption
- benchmark or promotion bar
- action mapping such as `Wait` becoming `Buy now`
- risk suppressors that materially change live eligibility
- data inputs required at decision time

Do not create a new version for:

- wording-only copy edits
- typo fixes
- non-functional UI presentation changes
- adding a research note without changing active rules

## Current Active Versions

As of registry version `2026-06-07.1`:

| Strategy Code | Active Version | Status | Production Role |
|---|---|---|---|
| `breakout-confirmation` | `breakout-confirmation.v2` | `core` | Board-eligible only when triggered, supportive, and sector-confirmed |
| `sector-confirmed-pullback-continuation` | `sector-confirmed-pullback-continuation.v1` | `core` | Board-eligible only through narrowed pullback rules |
| `etf-trend-rotation` | `etf-trend-rotation.v1` | `research` | Off-board until a stronger ranked rotation version is validated |
| `selective-mean-reversion` | `selective-mean-reversion.v1` | `research` | Off-board research sandbox |

## Revision Archive Grain

Every strategy revision should have these artifacts where practical:

1. Registry update
   - `config/strategy_registry.json`
   - updates `version_label`, `version_num`, `effective_from`, status, promotion text, and rule spine

2. Research evidence
   - stored under `docs/research/market/`
   - includes facts, inferences, unknowns, benchmark comparison, drawdown, risk-adjusted metrics, and decision

3. Replay outputs
   - stored under `data/processed/`
   - directory name should include strategy code, date, and version or purpose

4. Weekly run manifest
   - stored under `data/processed/weekly_runs/{run_id}/manifest.json`
   - pins `strategy_registry_version`
   - pins `active_strategy_versions`

5. Durable memory
   - finance memory records what was validated or rejected
   - tech memory records persistence or architecture implications
   - product memory records workflow implications when relevant

## Weekly Run Pinning

Every published weekly run must snapshot:

```json
{
  "strategy_registry_version": "2026-06-07.1",
  "active_strategy_versions": {
    "breakout-confirmation": "breakout-confirmation.v2",
    "sector-confirmed-pullback-continuation": "sector-confirmed-pullback-continuation.v1",
    "etf-trend-rotation": "etf-trend-rotation.v1",
    "selective-mean-reversion": "selective-mean-reversion.v1"
  }
}
```

This answers:

- which versions analyzed week `Z`,
- when version `Y` started feeding reports,
- whether a trade outcome belongs to old or new logic,
- and whether live results should be compared to the right backtest.

## Lifecycle Status

Use these statuses for strategy versions:

- `idea`: not yet encoded
- `research`: encoded or described, not board eligible
- `backtesting`: under replay evaluation
- `paper_live`: visible in shadow output, not fresh-capital eligible
- `promoted`: eligible for production weekly board
- `retired`: no longer active, but preserved for historical reconstruction

The current registry keeps coarse `status` values for compatibility, but future database tables should store version-level lifecycle status explicitly.

## Promotion Decision Template

Every promotion or rejection note should include:

- Strategy code
- Old version
- New version
- Effective date
- First weekly report expected to use it
- Rule changes
- Data inputs required
- Benchmark used
- Replay period
- Friction assumption
- SPY buy-and-hold comparison
- Exposure-aware SPY comparison
- Max drawdown comparison
- Risk-adjusted result
- Regime / sector / ticker concentration check
- Decision: promoted, paper-live, research-only, or retired
- Next research question

## File Naming

Research note:

```text
docs/research/market/{strategy_code}-refinement-{YYYY-MM-DD}.md
```

Replay output directory:

```text
data/processed/{strategy_code}_refinement_{YYYY-MM-DD}_{version_label}/
```

Strategy improvement goal prompt:

```text
docs/strategy/workstreams/strategy-improvement-goals/{NN}-{strategy_code}-goal.md
```

## Current Strategy 1 Example

`breakout-confirmation.v1`:

- Broad triggered breakout baseline.
- Useful research context.
- Did not clear the newer promotion bar versus `SPY` buy-and-hold and had worse drawdown.

`breakout-confirmation.v2`:

- Triggered breakout only.
- Market regime must be `Risk-on` or `Selective risk-on`.
- Sector must be confirmed.
- Promoted on `2026-06-07`.
- First future weekly reports should use this version after the production wiring change.

## Database Direction

The repo remains the source of truth during the file-backed phase.

The database should eventually snapshot this into:

- `ref.decision_bases`
- `ref.decision_basis_versions`
- `research.replay_runs`
- `research.replay_signal_events`
- `intelligence.strategy_candidates`
- `intelligence.board_rows`
- `intelligence.weekly_report_runs`

Do not make the database the only place a strategy definition exists until repo-based review, testing, and docs are equally strong.

## Non-Negotiables

- Historical weekly reports must never be rewritten when a strategy version changes.
- Research variants must not feed the board until promoted.
- Strategy pages must distinguish strategy family from active version.
- Weekly report generation must use the same measurable rules that were validated in replay.
- Every future strategy improvement workstream must end with either a promoted version or a clear research-only decision.
