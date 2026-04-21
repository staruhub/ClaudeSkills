# Research Notes Format V8

Research notes are the bridge between investigation and synthesis.
They must be compact enough to merge, but strong enough to defend the final claims.

## Workspace structure

```text
workspace/
  research-plan.md
  research-notes/
    task-a.md
    task-b.md
    task-c.md
    task-f1.md
  registry.md
  outline.md
  draft.md
  evaluation.md
  run-summary.json
  handoff-1.md
  handoff-2.md
```

## Required note structure

Each `task-*.md` should follow this structure.

```markdown
---
task_id: a
role: Policy Analyst
objective: Compare policy approaches to X
status: complete
confidence: medium
sources_found: 5
acceptance_met: yes
---

## Sources
[1] Title | URL | Aut:8 Rec:9 Rel:9 Dep:8 = 8.5 | META_ANALYSIS | 2025-11
[2] Title | URL | Aut:9 Rec:8 Rel:8 Dep:9 = 8.5 | OFFICIAL / PRIMARY | 2024-06
...

## Findings (facts only)
- Specific fact with source number. [1]
- Specific fact with source number. [2]

## Analysis (your synthesis)
- What these findings mean for the thread objective. [1][2]
- What appears overstated / understated / uncertain. [2][3]

## Support snippets / paraphrases for top claims
- Claim: {important claim}
  Source: [2]
  Support: {1-2 sentence paraphrase or short excerpt-level summary of what the source says}
- Claim: {important claim}
  Source: [1]
  Support: {support}

## Conflicts / unresolved issues
- Source [1] and [3] disagree on ...
- Still unresolved because ...

## Leads discovered
- Entity / document / standard / vendor / paper / law worth follow-up

## Gaps
- What you searched for but could not establish confidently
- What evidence would most reduce uncertainty
```

## Rules

### In Findings
- keep them factual
- one claim per bullet when possible
- include source numbers
- avoid vague filler like “many experts believe”

### In Analysis
- separate your synthesis from the source facts
- it is fine to infer, but make it obvious that it is your inference

### In Support snippets / paraphrases
- keep them short
- include only the few claims most likely to matter later
- use paraphrase when copyright or quoting constraints are a concern

### In Gaps
- be honest
- gaps are not failure; hidden gaps are failure
