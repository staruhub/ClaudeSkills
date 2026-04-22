# Context Reset + Handoff Protocol

## Why Context Reset

Long research pipelines (5+ tasks, 30+ searches) accumulate context that
degrades output quality in later phases. The lead agent's P5 draft quality
suffers when its context is full of P2 search results and P3 registry building.

Context reset means: write a structured handoff file, start a fresh session
that reads ONLY the handoff + referenced artifacts.

## Session Boundaries

```
Session 1: P0 → P1 → dispatch P2 → wait for subagents
  Output: task-board.md, subagent prompts dispatched
  
  ── handoff-1.md ──

Session 2: Read notes → P2.5 → P3 → P3.5 → P4
  Input: handoff-1.md + task-*.md files
  Output: registry.md, outline.md, conflicts.md (if any)
  
  ── handoff-2.md ──

Session 3: P5 draft
  Input: handoff-2.md + registry.md + outline.md
  Output: draft.md
  
  ── handoff-3.md ──

Session 4: Evaluator Agent
  Input: handoff-3.md + draft.md + registry.md
  Output: evaluation.md
  
  ── handoff-4.md (if fix needed) ──

Session 5: P8 polish (or fix → resubmit)
  Input: handoff-3.md or handoff-4.md + draft.md + evaluation.md + registry.md
  Output: final-report.md + harness-log.md
```

## Handoff File Format

Each handoff file follows this structure:

```markdown
# Handoff — Session {N} → Session {N+1}

## Research Question
{original question, verbatim — never paraphrase}

## Current Phase
Completed: {list of completed phases}
Next: {next phase to execute}

## Mode & Complexity
Mode: {Standard/Lightweight}
Complexity: {Low/Medium/High}
Topic Type: {Data-heavy/Narrative/Comparative/Exploratory}

## Artifacts (read these files)
- workspace/research-notes/task-a.md
- workspace/research-notes/task-b.md
- workspace/registry.md
- workspace/outline.md

## Key Decisions Made
- {decision 1, e.g., "Dropped 4 sources below threshold 5.0"}
- {decision 2, e.g., "Classified as Comparative topic type"}
- {decision 3, e.g., "Chased 2 leads in P2.5: Glean™, FUTURE trial"}

## Known Issues
- {issue 1, e.g., "task-c gap: no Chinese-language sources found"}
- {issue 2, e.g., "1 conflict detected: AI displacement 30% vs 80%"}

## Acceptance Status
- task-a: met
- task-b: met
- task-c: partial (only 2 sources, below threshold)
- task-d: met
- task-f1: met (follow-up for Glean™)

## Quality Baselines (for Evaluator)
- Citation density: 1 per 150 words
- Expected confidence: mostly Medium
- Expectation: "Reads like a balanced comparison with evidence for each position"
```

## Rules

1. The research question is ALWAYS copied verbatim — never summarized or reworded
2. Artifact paths must be exact — the next session reads only these files
3. Key decisions provide context the next session needs to understand WHY
   certain sources were dropped or phases were skipped
4. Known issues prevent the next session from re-discovering known gaps
5. Acceptance status lets the next session know which tasks are reliable

## Degraded Mode (no filesystem)

If context reset via files isn't possible (Claude.ai), use a visible block:

```
═══════════════════════════════════════════
CONTEXT RESET — Treat everything above as discarded.
From here forward, reference ONLY the information below.
═══════════════════════════════════════════

Research Question: {verbatim}
Completed: P0, P1, P2, P2.5, P3, P3.5, P4
Next: P5

Registry: [inline registry from P3]
Outline: [inline outline from P4]
Conflicts: [inline from P3.5]
Known Issues: {list}
```

The lead agent mentally discards everything above this block.
Less effective than true session reset but better than nothing.

## When to Skip Context Reset

For Low complexity research (2-3 tasks, < 15 searches), context reset
may be unnecessary overhead. Skip if total context is estimated < 50%
of window capacity.

Always do context reset for Medium and High complexity.
