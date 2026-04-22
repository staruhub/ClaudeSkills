# Evals Runbook V8

Use this folder to keep routing and output checks close to the skill.

## Minimal loop
1. Run a routing slice (`routing-evals.json`)
2. Run a few representative output cases
3. Compare with the previous skill version or a simple no-skill baseline
4. Record failures in `run-summary.json` and promote important failures into new eval cases

## What to test
- should-trigger prompts
- should-not-trigger prompts
- short brief memo tasks
- full report tasks
- delta / follow-up tasks
- high-stakes tasks that require stronger grounding

## Ground rule
Do not declare V8 better because one demo looked nicer.
Treat it like code: compare runs, check artifacts, and look for regressions.
