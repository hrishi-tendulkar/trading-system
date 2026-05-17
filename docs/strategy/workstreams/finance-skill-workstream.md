# Finance Skill Workstream

## Objective

Create a bar-raising Codex skill that acts as the finance brain for the Trading System project. The skill should help future agents design, critique, and implement the investing logic behind the platform, not just write generic market commentary.

## Outcome

The workstream succeeds when we have a reusable skill that consistently helps with:

- Investment-analysis framework design
- Metric and signal definitions
- Ranking model design
- Event and catalyst interpretation
- Translation of finance concepts into implementable data models and product requirements

## Scope

In scope:

- Public-equity long-term and short-term analysis frameworks
- Metric dictionary and signal taxonomy
- Evidence standards and reasoning guardrails
- Output templates that make future scoring and backtesting easier

Out of scope for v1:

- Autonomous trade recommendations
- Portfolio optimization
- Options strategies
- Real-time execution logic
- Highly quantitative factor research requiring a separate research stack

## Deliverables

1. A local Codex skill at [skills/public-equity-intelligence](/Users/hrishimansi/Documents/Hrishi/Projects/Trading%20System/skills/public-equity-intelligence)
2. Reference docs that define the analytical framework and signal language
3. A forward-testing plan using real project tasks after the wider architecture exists
4. Iterative upgrades as we learn which finance tasks recur in the build

## Quality Bar

The skill should:

- Separate facts, inference, and uncertainty
- Keep long-term and short-term logic distinct
- Favor measurable proxies over abstract investing language
- Produce outputs that can be encoded into schemas and scoring systems
- Challenge weak heuristics rather than merely echoing them

## Next Iterations

1. Add a canonical stock scoring template with explicit fields and scoring bands
2. Add a finance ontology for sectors, catalysts, risks, and signal classes
3. Add example prompts and expected output shapes once the product architecture is more concrete
4. Forward-test the skill on real design tasks for watchlist scoring, earnings analysis, and catalyst detection
