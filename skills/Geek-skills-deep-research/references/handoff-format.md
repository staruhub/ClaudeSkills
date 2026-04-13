# Context Reset + Handoff Protocol V7

## Why Context Reset

Long research pipelines accumulate context that degrades later phases.
Context reset means: write a structured handoff file, start a fresh session
that reads ONLY the handoff + referenced artifacts.

## Session Boundaries (V7)

```
Session 1: P0 → P0.7 (Topic Registry) → P1 → Wave 0 → Gate W0 → Wave 1
  Output: topic-registry.md, task-w0-*.md, task-w1-*.md
  
  ── handoff-1.md ──

Session 2: Read notes → P2.5 → P3 + _INDEX.md → P3.5 → Wave 2 → P4
  Input: handoff-1.md + all task-*.md + topic-registry.md
  Output: registry.md, _INDEX.md, W2-cross-topic-synthesis.md, outline.md
  
  ── handoff-2.md ──

Session 3: P5 draft
  Input: handoff-2.md + registry.md + _INDEX.md + outline.md + W2 synthesis
  Output: draft.md
  
  ── handoff-3.md ──

Session 4: Evaluator Agent
  Input: handoff-3.md + draft.md + registry.md + _INDEX.md + topic-registry.md
  Output: evaluation.md
  
  ── handoff-4.md (if fix needed) ──

Session 5: P8 polish (or fix → resubmit)
  Input: handoff + draft.md + evaluation.md + registry.md
  Output: final-report.md + harness-log.md (+ living docs if progressive)
```

## Handoff File Format (V7)

```markdown
# Handoff — Session {N} → Session {N+1}

## Research Question
{original question, verbatim — never paraphrase}

## Current Phase
Completed: {list of completed phases including Wave 0, Wave 1, Wave 2}
Next: {next phase}

## Mode & Complexity
Mode: {Standard/Lightweight}
Complexity: {Low/Medium/High}
Topic Type: {Data-heavy/Narrative/Comparative/Exploratory}
Progressive Round: {N or "Single"}

## Topic Registry
Path: workspace/topic-registry.md
Lines: {N} research lines
  - 01 / {slug}: must_answer {answered/total}
  - 02 / {slug}: must_answer {answered/total}

## Wave Status
- Wave 0: {complete/partial} — {N} shared docs, Gate W0: {PASS/FAIL}
- Wave 1:
  - 01-{slug}: {complete/partial} — stop conditions: {n}/5
  - 02-{slug}: {complete/partial} — stop conditions: {n}/5
- Wave 2: {complete/skipped} — {N} shared foundations, {M} cross-validated

## Artifacts (read these files)
- workspace/topic-registry.md
- workspace/research-notes/task-w0-a.md
- workspace/research-notes/task-w1-01.md
- workspace/research-notes/task-w1-02.md
- workspace/registry.md
- workspace/_INDEX.md
- workspace/outline.md
- workspace/W2-cross-topic-synthesis.md

## Key Decisions Made
- {decision 1}
- {decision 2}

## Known Issues
- {issue 1}
- {issue 2}

## Quality Baselines (for Evaluator)
- Citation density: {target}
- Expected confidence: {profile}
- Expectation: "{one-line}"
```

## Rules

1. Research question ALWAYS copied verbatim
2. Artifact paths must be exact
3. Topic Registry path always included
4. Wave status with stop condition scores included
5. Known issues prevent re-discovering gaps

## Degraded Mode (no filesystem)

```
═══════════════════════════════════════════
CONTEXT RESET — Treat everything above as discarded.
From here forward, reference ONLY the information below.
═══════════════════════════════════════════

Research Question: {verbatim}
Topic Registry: {inline}
Completed: P0, P0.7, P1, W0, W1, P2.5, P3, P3.5, W2, P4
Next: P5

Registry: [inline]
_INDEX: [inline]
Outline: [inline]
W2 Synthesis: [inline]
Known Issues: {list}
```

## When to Skip Context Reset

For Low complexity (2-3 tasks, < 15 searches), skip if total context < 50% window.
Always reset for Medium and High complexity.
