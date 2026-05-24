# ENGINEERING

## Purpose

The engineering system should turn market, company, event, and options inputs into traceable weekly intelligence outputs without requiring real-time infrastructure or heavy operational overhead.

## Engineering Principles

- Batch-first over real-time by default
- Source capture, normalization, features, and recommendations stay separate
- Derived scores must remain explainable and reproducible
- Schemas and transformations should be explicit and versionable
- Provider choices should be swappable where practical
- Historical state must be preserved for backtesting and audits

## v1 Shape

- Single-user internal platform
- Daily refresh cadence plus weekly synthesis
- Event-driven updates where useful, but no intraday dependency
- Supabase for relational history and storage
- Railway for scheduled jobs, workers, and lightweight delivery surfaces

## Non-Goals

- Brokerage execution
- Tick-level or HFT infrastructure
- Opaque AI-only orchestration with no deterministic spine
- Tight coupling between one data vendor and every downstream schema

## Canonical References

- `docs/engineering/requirements/high-level-technical-requirements.md`
- `docs/engineering/repository-structure.md`
- `docs/product/high-level-design.md`
