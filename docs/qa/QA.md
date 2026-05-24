# QA

## Purpose

QA in Trading System protects decision quality. The standard is not just "the job ran" but "the output is trustworthy enough to inform a real capital-allocation choice."

## QA Principles

- Silent failure is worse than loud failure
- Source lineage matters for any meaningful recommendation
- Historical consistency matters as much as current correctness
- Missing data, stale data, and partial runs must be visible
- Review should focus on behavior and risk before style

## High-Risk Failure Modes

- Recommendations produced from incomplete source data
- Context files not loading and agents proceeding anyway
- Historical scores changing without explainable input changes
- AI summaries implying facts that source data does not support
- Options recommendations appearing without a valid underlying equity case

## Canonical References

- `docs/engineering/requirements/high-level-technical-requirements.md`
- `docs/product/PRODUCT.md`
- `docs/agents/CONTEXT_BUGS.md`
