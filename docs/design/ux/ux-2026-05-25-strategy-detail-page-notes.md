# Strategy Deep Dive Page

## Page structure and UX flow

1. `Cross-page nav`
   Links back to the weekly overview, into stock detail, and across peer strategies so the page behaves like part of the weekly operating loop rather than a dead-end document.
2. `Strategy identity header`
   Shows strategy name, decision-basis type, trust level, promotion status, version, and last update. The header also carries a plain-English weekly interpretation so the operator can calibrate trust immediately.
3. `This week at a glance`
   A compact pulse strip with live matches, board-promoted count, suppressed count, dominant action mix, and one-line operating implication.
4. `Current recommendations`
   The primary decision module. Candidates are sorted `Board-promoted`, then `Strategy-only`, then `Suppressed` so the page mirrors the board-assembly doctrine.
5. `Interpretation + why this strategy exists`
   Short decision memo covering what edge the strategy is trying to capture, when it tends to work, and what a false positive looks like.
6. `Historical evidence`
   A compact replay summary with verdict, sample window, excess returns, win rates, and regime-aware interpretation.
7. `Where it works / where it fails`
   Regime and sub-bucket panels that connect replay evidence directly to live usage and non-usage.
8. `Canonical rules`
   A two-layer rules section: plain-language rule spine first, field-level exact logic second.
9. `Recent changes and lineage`
   Version history plus explicit links to board-promoted names, supporting-lineage names, stock pages, canonical docs, and replay sources.

## Information hierarchy

- The page starts with `what it is`, `how much to trust it`, and `what it is doing this week`.
- Current candidates come before backtest and rule detail because this is an active weekly tool.
- Historical evidence appears before exact canonical rules so the user sees `why this strategy deserves trust` before `how every field is wired`.
- Changelog and lineage sit low on the page because they are important for auditability, but secondary to the current week.

## Visual treatment

### Strategy summary

- Use a strong header card with two independent badges:
  - `Trust level`
  - `Promotion status`
- Trust level owns the page accent:
  - `Core`: deep green
  - `Core but narrowed / trust-calibrated`: amber with a green support accent
  - `Refine before promotion`: blue-slate
  - `Research only`: muted rust
- Promotion status stays as a separate outlined chip so it cannot be confused with trust.

### This week’s recommendations

- Present as ranked candidate cards with a persistent left-edge state bar.
- Live candidate state colors:
  - `Board-promoted`: green
  - `Strategy-only`: blue
  - `Suppressed`: red
- Each card surfaces action, setup quality, evidence tier, lineage, `why now`, `why not stronger`, and suppression reason if relevant.

### Backtest panel

- Use a verdict-first evidence panel rather than a generic stats table.
- Put the promotion verdict in a large badge, then show compact metric tiles for window, universe, sample size, forward-return stats, excess return, and win rate.
- A small trend chart and best/worst bucket callouts make the panel scannable without turning it into a research dump.

### Regime / when-it-works panel

- Split into two paired cards:
  - `Works best when`
  - `Degrades when`
- Support them with sub-bucket strips so the operator sees the filters that actually earned trust.

### Canonical rules section

- Use a stepped rule spine with numbered blocks for entry, context, exclusion, holding style, invalidation, and board eligibility.
- Put exact field logic in a secondary darker panel to signal `implementation truth` without overwhelming the main read path.

### Strategy history / changelog

- Render as a vertical timeline with explicit product impact labels such as:
  - `More selective`
  - `Higher trust`
  - `Reduced board eligibility`
  - `Moved to research`

## Navigation model

- `Overview -> Strategy`
  Each weekly board row links to its primary source strategy and any supporting strategy.
- `Strategy -> Stock detail`
  Every live candidate row links into the stock deep dive with setup-family context already established.
- `Stock detail -> Strategy`
  Stock detail should link back to the primary source strategy and supporting strategies for that name.
- `Strategy -> Strategy`
  A side rail `Canonical strategy map` lets the operator compare peer strategy trust and promotion states without leaving the strategy domain.

## Notes on trust, promotion status, and live candidate state

- Trust level is expressed at the strategy level through header accent, badge styling, and caution copy.
- Promotion status is expressed separately as a workflow badge and reinforced in the weekly interpretation sentence.
- Live candidate state is expressed at the row level through strong color, ordering, and copy. This prevents a user from mistaking `interesting` for `board-ready`.
- The `Canonical strategy map` provides one scalable place to compare all four canonical strategies without flattening them into equal peers.
