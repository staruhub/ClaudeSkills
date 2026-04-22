# Observability and Optimization V8

A good research skill should leave a structured trace behind.
Narrative logs are nice; structured summaries are what let you debug regressions.

## Emit `run-summary.json`

Use `scripts/emit_run_summary.py` after drafting/evaluation.

### Minimum fields
- `skill_version`
- `timestamp`
- `output_type`
- `stakes`
- `orchestration_mode`
- `used_subagents`
- `used_tension_discovery`
- `used_landscape_scan`
- `used_reverse_search`
- `search_count` / `fetch_count` (if known)
- `source_count`
- `citation_count`
- `word_count`
- `evaluation_run`
- `evaluation_verdict`
- `issues`

### Recommended fields
- `estimated_effort`
- `latency_seconds`
- `token_in` / `token_out` (if your harness can provide them)
- `manual_spotcheck_run`
- `accepted_without_major_edits`
- `failure_class`

---

## What to observe in traces

If your platform supports tracing, capture these events:
- skill activated / not activated
- output type chosen
- single-agent vs subagents
- each search / fetch
- each script call
- compaction / context reset
- evaluation run and result
- publish / stop / escalate

This makes it easier to answer:
- Why did the skill trigger?
- Why did it get expensive?
- Where did the run lose grounding?
- Which optional module actually helped?

---

## Core KPIs

### Routing KPIs
- trigger precision
- trigger recall
- over-trigger rate
- under-trigger rate

### Process KPIs
- notes completeness
- registry completeness
- citation integrity pass rate
- evaluation pass rate

### Outcome KPIs
- user accept / minimal-edit rate
- groundedness score
- coverage score
- usefulness / actionability score

### Efficiency KPIs
- median time per run
- median tool calls per run
- median tokens per run
- cost per accepted artifact

---

## Failure taxonomy

When a run fails, classify it before editing the skill.

### 1. Routing failure
Examples:
- skill should not have triggered
- full report chosen where brief memo was enough

### 2. Process failure
Examples:
- missing notes
- no counter-evidence search
- subagents duplicated work

### 3. Grounding failure
Examples:
- weak support for key claims
- citation mismatch
- wrong source type for the claim

### 4. Output failure
Examples:
- did not answer the actual question
- too generic
- forced contrarianism

### 5. Efficiency failure
Examples:
- too many searches
- unnecessary subagents
- evaluation run not worth the cost

### 6. Governance failure
Examples:
- violated data handling boundary
- missing required human review

Fix the **smallest layer** that caused the failure.
Do not rewrite the whole skill when the real bug is just the description or one quality gate.

---

## Optimization loop

1. Collect failed or expensive runs
2. Classify each failure
3. Add or update a routing or output eval case
4. Change one thing only
5. Re-run the affected eval slice
6. Compare against the previous version
7. Keep the change only if the metrics improve or at least do not regress badly

This is how a skill becomes more reliable instead of just longer.
