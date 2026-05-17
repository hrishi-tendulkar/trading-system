---
name: public-equity-intelligence
description: Build and apply rigorous public-equity research, stock-ranking, and trading-intelligence frameworks for the Trading System project and similar personal investing systems. Use when Codex is working in the Trading System workspace or designing the finance side of a public-equity intelligence product, including finance requirements, scoring models, signal frameworks, company and market data schemas, long-term quality evaluation, short-term setup analysis, or interpretation of earnings, news, and filings for medium- and short-term stock opportunity workflows.
---

# Public Equity Intelligence

## Overview

Use this skill to turn raw company, market, and event data into disciplined investment-analysis logic. Favor structured reasoning, explicit evidence, and repeatable scoring over vague opinions or generic market commentary.

## Workflow

Follow this order unless the user asks for a narrower task.

### 1. Clarify the finance problem

Determine which of these jobs is being asked for:

- Research framework design
- Signal or metric definition
- Ranking model design
- Data schema design for finance inputs
- Analysis of a company, event, or setup
- Validation of an existing investing heuristic

Identify the time horizon before doing anything else:

- Long-term: business quality, compounding potential, valuation support, thesis durability
- Short-term: setup quality, catalysts, positioning, momentum, timing risk
- Mixed: separate the two frameworks instead of blending them into one score too early

### 2. Build an evidence ledger

Separate observations into:

- Facts: sourced metrics, dates, guidance changes, price/volume behavior, event timing
- Inferences: interpretation of what those facts suggest
- Unknowns: missing data, unresolved risks, conflicting signals

Never present an inference as if it were a fact.

### 3. Use the right analysis frame

For long-term work, read [references/analysis-framework.md](references/analysis-framework.md) and use the long-term framework.

For short-term work, read [references/analysis-framework.md](references/analysis-framework.md) and use the short-term setup framework.

For detailed metric definitions, guardrails, and common pitfalls, read [references/metrics-and-signals.md](references/metrics-and-signals.md).

### 4. Convert judgment into a structured output

Prefer outputs with stable fields such as:

- Thesis
- Horizon
- Evidence for
- Evidence against
- Key risks
- Missing information
- Confidence
- Suggested next action

When designing system logic, prefer explicit component scores over a single opaque score. Example:

- Fundamental quality
- Estimate revision / earnings momentum
- Relative strength / price structure
- Catalyst quality
- Risk / crowding / valuation pressure

### 5. Raise the bar on analytical quality

Do these checks before finalizing:

- Test whether the thesis depends on one fragile assumption
- Check whether a metric is cyclical, one-time, or seasonally distorted
- Check whether price action conflicts with the narrative
- Check whether a short-term setup is actually just event gambling
- Check whether a long-term score is being inflated by recent momentum
- Check whether the proposed logic can be encoded into data fields later

## Rules

- Distinguish long-term investment merit from short-term tradeability.
- Prefer leading indicators over backward-looking summaries when the user is building a monitoring system.
- Treat earnings, guidance, analyst revisions, and market reaction as separate signals.
- Avoid unsupported claims about management quality, moats, or institutional demand unless evidence is available.
- Avoid false precision. Use score bands or ordinal ratings when the evidence does not support exact numbers.
- Design outputs so they can later be stored in tables, compared over time, and backtested.
- If a requested signal sounds appealing but is not operationalizable, say so and propose a measurable proxy.

## Default deliverables

When asked to help build the finance side of a product, bias toward producing one or more of:

- A scoring framework
- A metric dictionary
- A signal taxonomy
- A company or event analysis template
- A watchlist review rubric
- A ranking or alerting specification
- A finance data model for implementation

## Anti-patterns

Avoid:

- Mixing company quality, valuation, and technical momentum into one unexplained score
- Treating narrative summaries as sufficient evidence
- Recommending indicators without defining how they are measured
- Confusing correlation with a tradable edge
- Creating frameworks that cannot be maintained with available data sources
- Writing in the style of investment marketing instead of system design

## Resources

### references/

- `analysis-framework.md`: long-term and short-term evaluation frames, risk lens, and ranking design guidance
- `metrics-and-signals.md`: metric definitions, proxies, common pitfalls, and implementation-minded guardrails

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
