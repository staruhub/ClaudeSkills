# Quality Gates V8

V8 gates are organized by the same five questions you should use in production:
**Did it trigger correctly? Did it execute the right process? Is the output good? Was it efficient enough? Can we explain what happened?**

---

## Gate 0 — Routing correctness

Before celebrating the output, confirm the skill should have been used at all.

### Pass when
- the task truly needed multi-source synthesis or a reusable research artifact
- the user wanted a brief/report, not just a quick answer
- the selected output type (brief/full/delta) fits the request

### Fail when
- the task was a simple lookup or short answer
- the skill produced a giant report where a paragraph would do
- the skill was triggered by generic words like “分析” without real research need

### Fix
- narrow the description
- add more should-not-trigger cases to `evals/routing-evals.json`
- make the brief mode more attractive so the model stops over-escalating

---

## Gate 1 — Process completeness

Check the evidence trail.

### Required artifacts by mode

| Artifact | Brief | Full | Delta |
|---|---|---|---|
| `research-plan.md` | Yes | Yes | Yes |
| task notes | Optional (single-agent inline ok) | Yes | Yes |
| `registry.md` | Yes | Yes | Yes |
| `draft.md` | Yes | Yes | Yes |
| `evaluation.md` | Optional | Recommended / Required for higher stakes | Optional |
| `run-summary.json` | Yes | Yes | Yes |

### Pass when
- objectives and scope are written down
- key notes exist and are traceable
- gaps and conflicts are explicit
- top claims have enough support to defend them later

### Fail when
- the run jumps straight to drafting without a visible evidence trail
- notes contain conclusions but not the supporting facts
- no limitations/counter-evidence search was done when clearly needed

### Fix
- backfill notes from the actual sources used
- run reverse search for missing trade-offs or counter-evidence
- add support snippets/paraphrases for top claims

---

## Gate 2 — Grounding and citation integrity

### Hard fail triggers
- any cited source is invented or not present in the approved pool
- more than 3 uncited factual claims in a full report
- the report cites dropped sources
- legal / financial / safety-critical wording is unsupported or obviously over-compressed

### Pass when
- every core claim has a fitting source type
- reference numbers resolve cleanly
- conflicts are surfaced instead of hidden
- evidence strength matches claim strength

### Use scripts
- `scripts/verify_citations.py`
- `scripts/source_evaluator.py` as a helper

### Fix
- remove weak or dangling citations
- downgrade confidence where support is thin
- re-open raw support for the most important disputed claims

---

## Gate 3 — Output quality

Judge the artifact the user actually sees.

### Required for every output
- direct answer to the question
- explicit limitations / trade-offs
- source-backed findings separated from synthesis
- uncertainty calibrated to the evidence

### Additional requirements by output type

**Brief memo**
- gets to the point fast
- no unnecessary ceremony
- still grounded and reusable

**Full report**
- coverage is broad enough for the stated scope
- sections build logically
- references and evidence quality are strong enough to survive scrutiny

**Delta update**
- clearly states what changed since the prior round
- avoids repeating the whole old report unless needed

### V8 nuance on “contrarian” thinking
Do not force a contrarian stance for stable descriptive topics.
Instead ask:
- Did the report surface at least one **decision-relevant non-obvious insight**?
- If the topic was contested, did it test at least one important assumption?

### Fix
- cut generic filler
- add missing trade-offs
- replace forced hot takes with useful nuance
- add a decision framework only when a decision is being made

---

## Gate 4 — Efficiency and operational health

A good artifact that wastes 10x the work is still a problem.

Track:
- total searches / fetches
- number of subagents
- draft length vs requested output type
- evaluation loops
- time or token cost if available

### Warning signs
- subagents used for a task that one lead agent could handle
- long report produced when brief was enough
- many duplicate searches
- repeated fetches of already-resolved sources
- evaluation run even when the task stakes were trivial

### Fix
- tighten mode selection
- default to brief memo more often
- reduce subagent count
- move repetitive checks into scripts

---

## Gate 5 — Observability and learning

A production skill should leave behind enough structure to debug regressions.

### Pass when
- `run-summary.json` exists
- the summary captures route, mode, artifacts, sources, and evaluation status
- the run explains which optional modules were used and whether they helped
- failures can become future tests

### Fail when
- only a narrative harness log exists
- you cannot tell why the skill triggered or why it got expensive
- a regression happens and there is no comparable structured record

### Fix
- emit `run-summary.json`
- add the failure as a routing or output eval case
- compare against previous version or a no-skill baseline

---

## Release checklist

Before shipping or publishing a new skill version:
1. Run routing evals (`evals/routing-evals.json`)
2. Run at least a few representative output cases
3. Compare against the previous skill version or a simple baseline
4. Check citation integrity with the script
5. Confirm observability output is present and readable
6. Record what changed in the skill version
