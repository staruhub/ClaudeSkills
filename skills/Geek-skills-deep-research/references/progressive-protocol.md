# Progressive Research Protocol V7 — Living Docs

## Purpose

This protocol supports multi-round research where each round builds on
the previous round's output. The seed directory grows with each round
rather than producing disposable reports.

## When to Use

- User says "继续深挖", "第二轮", "based on last round", "progressive"
- A prior round's output exists in a seed directory
- The research question is too large for a single round

## Core Principle

Each round's output is the next round's input. The seed directory is a
living document, not a read-only archive.

## Seed File Update Format

After each round, update each research line's seed file:

```markdown
# <Research Line Title>

## Historical Summary (PRESERVED — never modify)
{content from prior rounds, untouched}

## Round {N} New Evidence
<!-- Every new fact has reference/ back-pointer -->
- {new fact} → ref: {NN}-{slug}-{source-slug}.md
- {new fact} → ref: 00-shared-{source-slug}.md

## Round {N} New Mechanism Understanding
<!-- From description to "why it's designed this way" -->
- {mechanism insight} → ref: {source}.md

## Round {N} New Trends & Difficulties
<!-- Time-stamped trends + practical pain points -->
- {trend with date evidence} → ref: {source}.md [TREND]
- {difficulty / failure mode} → ref: {source}.md [FACT]

## Current Judgment (synthesized after Round {N})
<!-- Integrates all rounds. Each judgment has back-pointer. -->
- {judgment 1} → ref: {source}.md [FACT/ANALYSIS/TREND]
- {judgment 2} → ref: {source}.md [FACT/ANALYSIS/TREND]

### Overturned or Revised (if any)
- {old judgment from Round M}: REVISED because {reason} → new ref: {source}.md
```

### Rules

1. Historical Summary is append-only — never delete, never rewrite
2. Each round gets its own clearly labeled sections
3. Every new judgment has a local back-pointer to reference/
4. If a prior judgment is overturned, note it in "Overturned" — don't silently change
5. Evidence classification (FACT/ANALYSIS/TREND) required on all Current Judgments

## Topic Registry Update

After each round, update `workspace/topic-registry.md`:

```markdown
- 01 / <slug> / <title>
  - must_answer:
    - Q1: {question} — ANSWERED in Round 1 → ref: {source}
    - Q2: {question} — PARTIAL in Round 1, continued Round 2
    - Q3: {question} — NEW (added Round 2)
    - Q4: {question} — NEW (added Round 2)
  - round_1_summary: {1-2 sentences}
  - round_2_summary: {1-2 sentences}
```

## Round Summary File

After each round, write `workspace/round-{N}-summary.md`:

```markdown
# Round {N} Summary

## What Was Done
- Wave 0: {N} shared docs added
- Wave 1: {list of lines investigated}
- Wave 2: {cross-topic synthesis results}

## Key New Findings
- {finding 1} [FACT]
- {finding 2} [ANALYSIS]
- {finding 3} [TREND]

## What Changed from Prior Rounds
- {judgment revised or overturned}
- {new research line added}

## Remaining Gaps (feeds Round {N+1})
- {gap 1}: {what's missing, why it matters}
- {gap 2}: {what's missing, why it matters}

## Recommended Next Round Focus
- {suggestion 1}: "补机制" / "补趋势" / "补限制" / "扩事实"
- {suggestion 2}

## Reference Directory State
- Total docs: {N}
- New this round: {M}
- _INDEX.md updated: yes/no
```

## Directory Structure (progressive mode)

```
seed-dir/
  01-<slug>.md          ← living seed file, updated each round
  02-<slug>.md
  topic-registry.md     ← updated each round
  _artifacts/
    round-1-summary.md
    round-2-summary.md
    W2-cross-topic-synthesis.md
  reference/
    _INDEX.md           ← quick lookup, updated each round
    00-shared-*.md      ← shared ground truth
    01-<slug>-*.md      ← per-line evidence
    02-<slug>-*.md
```

## Naming Convention

- Shared: `00-shared-{source-slug}.md`
- Per-line: `{NN}-{slug}-{source-slug}.md`
- NN and slug come from Topic Registry — stable across rounds

## Round Initialization Checklist

When starting a new progressive round:

1. Read prior round summary
2. Read current topic registry (note answered/unanswered Qs)
3. Read current seed files (note "Current Judgment" sections)
4. Read _INDEX.md to know what evidence already exists
5. Identify this round's focus: "扩事实" / "补机制" / "补趋势" / "补限制"
6. Update topic registry with new must_answer questions
7. Proceed to P0 → P0.7 → P1 as normal

## Quality Threshold for Progressive Rounds

Each round should demonstrably advance the knowledge base:
- At least 30% new evidence (not duplicating prior rounds)
- At least 1 must_answer question newly answered per line
- At least 1 judgment refined or strengthened per line
- If a round produces < 20% new information, consider stopping

## When to Stop Iterating

The progressive research series is complete when:
1. All must_answer questions across all lines are answered
2. New rounds produce < 20% new information (diminishing returns)
3. The Readiness Check passes (see quality-gates.md)
4. A domain expert reading seed dir + reference dir could continue independently
