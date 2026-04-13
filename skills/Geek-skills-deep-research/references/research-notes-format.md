# Research Notes Format V7

The research notes are the ONLY communication channel between subagents and
the lead agent. Every fact in the final report must be traceable to a line in
these notes. No exceptions.

## File Structure

```
workspace/
  topic-registry.md         Lead builds (P0.7)
  research-notes/
    task-w0-a.md            Wave 0 shared ground truth
    task-w0-b.md            Wave 0 (if needed)
    task-w1-01.md           Wave 1 line 01
    task-w1-02.md           Wave 1 line 02
    task-w1-03.md           Wave 1 line 03
    task-f1.md              Follow-up (from P2.5)
    registry.md             Lead builds (P3)
    _INDEX.md               Lead builds (P3) — quick reference
    outline.md              Lead builds (P4)
    W2-cross-topic-synthesis.md  Lead builds (Wave 2)
    handoff-1.md            Context reset after P2
    handoff-2.md            Context reset after P4
    handoff-3.md            Context reset after P5
    evaluation.md           Evaluator writes
    harness-log.md          Lead writes (P8)
```

## Wave 0 Notes Format

```markdown
---
task_id: w0-a
role: Shared Ground Truth Collector
status: complete
sources_found: 10
acceptance_met: yes
acceptance_gaps: none
---

## Sources
[1] {Title} | {URL} | Aut:{a} Rec:{r} Rel:{rl} Dep:{d} = {c} | {Date}
...

## Findings
- {Fact relevant to ALL research lines}. [1] [FACT]
- {Specification/standard}. [2] [FACT]
...

## Leads Discovered
- {Entity for Wave 1 to chase}: {why} — {query}

## Deep Read Notes
### Source [1]: {Title}
Key data: ...
Key insight: ...
Useful for: {which research lines}

## Gaps
- {What was searched but not found}
```

## Wave 1 Notes Format (per research line)

```markdown
---
task_id: w1-01
role: {role}
registry_line: 01 / {slug}
status: complete
sources_found: 8
acceptance_met: yes
acceptance_gaps: none
stop_conditions: [5/5]
stop_conditions_missing: none
---

## Sources
[1] {Title} | {URL} | Aut:{a} Rec:{r} Rel:{rl} Dep:{d} = {c} | {Date}
...

## Findings by Lens

### Evidence [FACT]
- {Specific verifiable fact}. [1]
- {Specific verifiable fact}. [2]

### Mechanism [ANALYSIS]
- {Why it works this way}. [1]
- {Underlying abstraction}. [3]

### Trend [TREND]
- {Direction + time evidence}. [2]

### Difficulty [FACT] or [ANALYSIS]
- {Adoption barrier}. [3]

### Controversy [FACT] or [ANALYSIS]
- {Community disagreement}. [4]
- {Failure mode}. [2]

## must_answer Status
- Q1: answered — {answer with [n]}
- Q2: answered — {answer with [n]}
- Q3: partial — {what's known, what's missing}

## Leads Discovered
- {Entity}: {why} — {query}

## Deep Read Notes
### Source [1]: {Title}
Key data: ...
Key insight: ...
Useful for: ...

## Stop Conditions Self-Assessment
| # | Condition | Met? | Evidence |
|---|-----------|:----:|----------|
| 1 | Object list stable | ✓ | No new major entities in last 2 searches |
| 2 | Diminishing returns | ✓ | Last 2 searches returned known facts |
| 3 | must_answer covered | ✓ | Q1,Q2 answered; Q3 partial |
| 4 | Counterevidence swept | ✓ | Searched "{slug} limitations failures" |
| 5 | Cross-validated | ✓ | Official docs vs GitHub issues compared |

## Gaps
- {What was searched but not found}
```

## Source Line Format (V7 — same 4 Dimensions as V6)

```
[n] Title | URL | Aut:{a} Rec:{r} Rel:{rl} Dep:{d} = {c} | Date
```

| Field | Format | Rules |
|-------|--------|-------|
| [n] | Local number | Starts at [1] per task. Lead reassigns global [n] in registry. |
| Title | Short descriptive | From page title or article heading |
| URL | Full URL | MUST be from actual search result. NEVER invent. |
| Aut: | 1-10 | Authority: institutional credibility |
| Rec: | 1-10 | Recency: 10=this month, 8=this year, 5=5yr, 2=10yr+ |
| Rel: | 1-10 | Relevance: direct match to task objective |
| Dep: | 1-10 | Depth: 9=original research, 4=news summary |
| = {c} | Weighted | Auth×0.3 + Rec×0.2 + Rel×0.3 + Dep×0.2 |
| Date | YYYY-MM | Use "undated" if unknown |

## Findings Format (V7)

Each finding must be:
- One sentence of specific, factual information
- End with source number(s): [1] or [1][2]
- Tagged with evidence classification: [FACT], [ANALYSIS], or [TREND]
- Organized by lens (for Wave 1 tasks)
- Max 15 findings per task

Good: `Full textile mechanization took 50-90 years (1760s-1850s). [4] [FACT]`
Bad: `The transition took a long time. [4]`
Bad: `Studies suggest it was lengthy.` (no source, vague, no classification)

## Evidence Classification Tags

| Tag | Meaning | How to verify |
|-----|---------|--------------|
| [FACT] | Directly verifiable from cited source | Source states this explicitly |
| [ANALYSIS] | Interpretive synthesis | Author's inference from evidence |
| [TREND] | Time-dependent projection | Has date/timeline evidence, may change |

## _INDEX.md Format

```markdown
# Reference Index

## By Research Line
- 00-shared: [1] [2] [4] [6]
- 01-<slug>: [3] [5] [7]
- 02-<slug>: [8] [9] [10]

## By Evidence Type
- FACT: [1] [2] [3] [5] [6] [8]
- ANALYSIS: [4] [7] [9]
- TREND: [10]
- LIMITATION: [2] [6]

## 30-Second Lookup
claim → [n] → line above → source doc in registry
```

## Registry Format (V7 — built by lead in P3)

```markdown
# Citation Registry
Built from: task-w0-a.md, task-w1-01.md, task-w1-02.md, task-f1.md
Topic Registry: workspace/topic-registry.md

## Approved Sources

[1] Title | URL | Aut:8 Rec:9 Rel:8 Dep:7 = 8.0 | From: task-w0-a | Line: 00-shared
[2] Title | URL | Aut:8 Rec:4 Rel:7 Dep:8 = 6.9 | From: task-w1-01 | Line: 01-<slug>
...

## Dropped
x Title | URL | Aut:3 Rec:5 Rel:4 Dep:2 = 3.4 | Reason: below threshold
...

## Conflicts (from P3.5)
CONFLICT-1: {topic}
  - Claim A: ... — task-w1-01, source [n]
  - Claim B: ... — task-w1-02, source [m]
  - Resolution: present as debate

## Stats
Total evaluated: {N}
Approved: {M}
Dropped: {K}
Unique domains: {D}
Max single-source share: {ratio} ({pass/fail})
Conflicts: {C}
```

Registry rules:
- [n] numbers are FINAL — appear unchanged in report
- Every [n] in report must exist in Approved list
- Dropped sources NEVER appear in report
- Same URL from two tasks → keep once with higher composite
- Each source tagged with originating research line
