# Report Assembly V8

## Core rule

Write the final artifact from:
- the research plan
- the notes
- the approved registry
- raw/fetched sources only when you need to resolve a critical conflict or verify a high-stakes claim

The goal is **notes-first synthesis**, not blind copy-paste from search results.

---

## Pick the right artifact shape

### A. Brief memo
Use when the user wants a compact but defensible answer.

Suggested structure:
1. Direct answer / recommendation
2. Key evidence
3. Trade-offs / limitations
4. Optional next step

### B. Full report
Use when the user asked for comprehensive analysis.

Suggested structure:
1. Executive summary
2. Background / framing
3. Main analysis sections
4. Limitations & trade-offs
5. Decision framework (if needed)
6. References

### C. Delta update
Use when continuing a prior round.

Suggested structure:
1. What changed
2. New evidence
3. Impact on prior conclusion
4. Remaining uncertainty

---

## Mandatory sections / elements

Every final artifact must contain:
- a clear answer to the question
- source-backed findings
- limitations / trade-offs
- calibrated uncertainty
- references or inline source mapping

### Decision framework
Include only when the user is making a choice.
Do not force it into descriptive overviews.

### Non-obvious insight
Every good artifact should surface at least one useful nuance.
For contested or hype-heavy topics, this may be an assumption the evidence challenged.
For stable topics, this can simply be the most decision-relevant nuance the user might otherwise miss.

---

## Writing order

1. Body / main analysis
2. Limitations & trade-offs
3. Decision framework (if needed)
4. Executive summary / opening answer
5. References

Do **not** write the summary first.

---

## Evidence and wording rules

- Every important factual claim should be cited
- Every important number should be cited
- If the evidence is mixed, say it is mixed
- Do not turn thin evidence into precise certainty
- If you infer, label it as your analysis

### Good phrasing
- “The evidence reviewed suggests ...”
- “Based on these sources, the most likely interpretation is ...”
- “This appears stronger in X than in Y because ...”

### Bad phrasing
- “It is proven that ...” (when the evidence is actually mixed)
- “Experts agree ...” (without named support)
- “Clearly / obviously ...” (when it is not)

---

## Limitations & trade-offs

This section is mandatory.

Include:
- where the evidence is thin, dated, indirect, or conflicting
- what important conditions could flip the conclusion
- operational costs / risks / failure modes when relevant
- what the report did not establish

A report without limitations is not production-ready.

---

## Brief template

```markdown
# {Title}

## Answer
{Direct answer with citations.}

## Key evidence
- ... [1][2]
- ... [3]

## Limitations / trade-offs
- ... [4]
- ... [5]

## Non-obvious insight
{One useful nuance or challenged assumption.}

## References
[1] ...
```

---

## Full report template skeleton

```markdown
# {Title}

> Date: YYYY-MM-DD | Output: Brief / Full / Delta | Sources: N
> Stakes: Low / Medium / High | Evaluation: Passed / Not run / Needs review

## Executive Summary
- Direct answer
- Why it matters
- Main trade-off
- Confidence / boundary

## Main Analysis
...

## Limitations & Trade-offs
...

## Decision Framework
... (only if needed)

## References
...
```
