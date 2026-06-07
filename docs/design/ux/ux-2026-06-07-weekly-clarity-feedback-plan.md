# Weekly Clarity Feedback Plan

Date: 2026-06-07

## Feedback Categories

1. Global navigation
   - Keep the nav visible while scrolling.
   - Treat this as a shared-shell requirement, not a one-page fix.

2. Weekly action clarity
   - Use a plain dated title: "Weekly summary for Week of YYYY-MM-DD."
   - Primary copy must say what to do this week, why, or what data is missing.
   - Remove vague phrases such as cleaner setup, deck, deep-dive queue, discipline, and mental model.

3. Explainability
   - Add info affordances for compact labels such as market posture.
   - Use plain-language descriptions for market and risk labels.

4. Candidate interaction
   - Summary-only candidate cards must expand and collapse on click.
   - Every recommendation card should expose entry, invalidation, catalyst, strategy, and rationale.

5. Candidate coverage
   - If the page says "full candidate board," it must include every analyzed non-benchmark candidate.
   - The page should state the analyzed count and distinguish benchmark references from candidates.

6. Holdings truthfulness
   - Do not show holder/portfolio guidance unless the user's holdings are provided.
   - Until holdings exist, label portfolio guidance as unavailable and specify the missing input.

7. Record layout
   - Current-week details belong before archive navigation.
   - Archive should remain accessible but secondary.

8. Visual simplification
   - Do not use decorative bullets in single-line pills.
   - Avoid extra markers unless they encode a meaningful state.

## Implementation Plan

1. Patch shared app shell so navigation remains fixed while page content scrolls independently.
2. Rewrite weekly hero, summary, posture, and board copy into direct investor language.
3. Convert weekly recommendation cards to accessible expandable/collapsible cards.
4. Remove the board item cap so all analyzed non-benchmark candidates render.
5. Add analyzed-count and holdings-unavailable notices.
6. Move current-week record details to the left and archive link to the right.
7. Apply the same language and pill-marker cleanup to adjacent archive, daily, watchlist, and stock-detail surfaces.
8. Update designer, product-strategist, and public-equity-strategist agent instructions so future work inherits these rules.
9. Verify with tests and browser screenshots at desktop and constrained viewport widths.
