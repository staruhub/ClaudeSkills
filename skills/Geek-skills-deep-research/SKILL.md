---
name: deep-research
version: 7.1.0
description: >
  Subagent-powered research pipeline producing cited, verified long-form reports.
  Lead agent plans and synthesizes. Subagents investigate in parallel, writing
  structured notes to shared workspace. Independent Evaluator agent validates.
  Lead reads only notes, never raw search results.
  Use this skill for deep research, literature review, comprehensive analysis,
  investigation, topic survey, or any task requiring multi-source synthesis.
  Trigger phrases: "帮我调研一下", "深度研究", "综述报告", "深入分析",
  "research this topic", "write a report on", "survey the literature on",
  "competitive analysis of", "技术选型分析", "竞品研究", "政策分析", "行业报告".
  Trigger even without explicit keywords when the query requires 5+ sources
  or a structured evidence-based report.
  Also triggers for progressive/multi-round research: "继续深挖", "第二轮调研",
  "based on last round", "progressive research", "逐轮递进".
compatibility: "Requires web_search and web_fetch. Optimal with subagent dispatch (Claude Code, Cowork, DeerFlow). Degrades gracefully to single-thread on Claude.ai."
---

# Deep Research V7.1

Lead agent plans. Subagents investigate. Evaluator validates. Notes bridge the gap.

## Additional Resources

- For the phase-by-phase execution model and gating rules, read [references/methodology.md](references/methodology.md).
- For multi-round continuation and seed-directory updates, read [references/progressive-protocol.md](references/progressive-protocol.md).
- For subagent dispatch format and note-taking contracts, read [references/subagent-prompt.md](references/subagent-prompt.md) and [references/research-notes-format.md](references/research-notes-format.md).
- For evaluator checks and arbitration criteria, read [references/evaluator-prompt.md](references/evaluator-prompt.md) and [references/quality-gates.md](references/quality-gates.md).
- For final report structure, use [assets/report_template.md](assets/report_template.md).
- For citation and source verification helpers, use [scripts/source_evaluator.py](scripts/source_evaluator.py) and [scripts/verify_citations.py](scripts/verify_citations.py).

## What's New in V7.1 (from V7)

- **Degraded Mode Playbook** — explicit Hard/Soft Gate table for Claude.ai single-thread execution
- **Hard Gate enforcement** — 5 phases that MUST execute regardless of environment
- **Soft Gate simplification** — 4 phases that can be inlined in degraded mode
- **Progress Reporting lite format** — `[W0→W1→W2 inline]` allowed in degraded mode

## V7 Features (from V6)

- **Topic Registry** — mandatory structured research-line registration before dispatch
- **Wave 0 / 1 / 2 Architecture** — shared ground truth first, then per-topic deep dive, then cross-topic synthesis
- **Explicit Stop Conditions** — 5-point checklist replaces "feels done enough"
- **30-Second Back-Reference Check** — Readiness gate: any claim traceable in 30s
- **Evidence Classification** — every conclusion tagged: FACT / ANALYSIS / TREND
- **Living Docs Protocol** — multi-round progressive research with seed directory growth
- **_INDEX.md** — quick-reference entry point for citation registry
- *Retained from V6:* Evaluator Agent, Sprint Contract, Context Reset, 4-Dim Source Scoring, Self-Heal Loop, Harness Log

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │  P0: Environment Detection            │
                    │  P0.5: Complexity Assessment           │
                    └──────────────┬──────────────────────┘
                                   │
  [Session 1]       ┌──────────────▼──────────────────────┐
                    │  P0.7: Topic Registry                  │ ← NEW: stable IDs
                    │  P1: Sprint Contract per research line  │
                    │  (user checkpoint if interactive mode)  │
                    └──────────────┬──────────────────────┘
                                   │
              ┌─── Wave 0: Shared Ground Truth ────────────┐
              │  Subagent-00-shared (official docs, specs)   │
              │  → writes 00-shared-*.md to references/      │
              │  Gate W0: >= WAVE0_FLOOR shared docs          │
              └──────────────┬─────────────────────────────┘
                             │ (only after W0 gate passes)
              ┌─── Wave 1: Per-Topic Deep Dive ────────────┐
  [Parallel]  │  Subagent NN-<slug> per research line        │
              │  5 lenses: evidence / mechanism / trend /     │
              │            difficulty / controversy            │
              │  → writes NN-<slug>-*.md to references/       │
              │  Gate W1: per-line doc floors met              │
              └──────────────┬─────────────────────────────┘
                             │
                    ── context reset + handoff-1.md ──
                             │
  [Session 2]       ┌────────▼────────────────────────────┐
                    │  P2.5: Gap-Filling (chase leads)       │
                    │  P3: Citation Registry + _INDEX.md      │
                    │  P3.5: Conflict Arbitration              │
                    │  Wave 2: Cross-Topic Synthesis           │ ← NEW
                    │  P4: Evidence-mapped Outline              │
                    └──────────────┬──────────────────────┘
                                   │
                    ── context reset + handoff-2.md ──
                                   │
  [Session 3]       ┌──────────────▼──────────────────────┐
                    │  P5: Draft (from notes + registry)      │
                    │  Every conclusion tagged FACT/ANALYSIS/  │
                    │  TREND                                    │
                    └──────────────┬──────────────────────┘
                                   │
                    ── context reset + handoff-3.md ──
                                   │
  [Session 4]       ┌──────────────▼──────────────────────┐
                    │  Evaluator Agent (GAN-style)             │
                    │  + Stop Condition Audit                   │ ← NEW
                    │  + 30-Second Back-Reference Check         │ ← NEW
                    │  + Evidence Classification Audit          │ ← NEW
                    └──────────────┬──────────────────────┘
                              pass │  fail (max 3 rounds)
                                   │     │
  [Session 5]       ┌──────────────▼─────▼────────────────┐
                    │  P8: Polish + Harness Log               │
                    │  + Living Docs update (if progressive)   │ ← NEW
                    └─────────────────────────────────────┘
```

## Degraded Mode Playbook (V7.1 — Claude.ai / single-thread)

When running without subagents (Claude.ai, single conversation turn), use this table to decide what to execute vs simplify.

**Iron Rule:** Every Hard Gate MUST execute. No exceptions. Soft Gates can be inlined.

### Hard Gates (MUST execute, even in degraded mode)

| Phase | What to do | Minimum output |
|-------|-----------|----------------|
| **P0.7 Topic Registry** | List research lines with NN/slug/must_answer | Inline in response, no file needed |
| **Wave 1: 5-Lens Protocol** | Every research line investigated through all 5 lenses | Findings organized by lens in report |
| **Stop Conditions** | Self-assess 5 conditions per line after research | Table at end of each line's section |
| **P5: Evidence Classification** | Tag conclusions FACT/ANALYSIS/TREND | Tags in report body |
| **P6: Self-Critique** | In degraded mode: re-read draft, find 3+ issues, spot-check 3 claims | Issues section in report |

**Why these 5:** They directly improve result quality. Skipping them degrades the output, not just the process.

### Soft Gates (can be inlined/simplified in degraded mode)

| Phase | Full mode | Degraded simplification |
|-------|----------|------------------------|
| **P0/P0.5** | Explicit status lines | One-line: `[Degraded, Medium complexity, N lines]` |
| **P1 Sprint Contract** | Written task board with acceptance criteria per task | Implicit: just follow Topic Registry must_answer as criteria |
| **P3 Registry + _INDEX** | Separate files with 4-dim scoring | Inline: list sources at end of report with brief quality note |
| **Wave 2 Cross-Synthesis** | Separate W2 file | Inline: "Cross-Topic Synthesis" section in report |
| **P8 Harness Log** | Separate file | Optional: 2-3 lines at report end noting which phases contributed |

### Degraded Mode Progress Reporting (lite format)

Instead of per-phase status lines, output a single summary block:

```
[DR V7.1 degraded] Lines: 3 | Complexity: Medium
[W0 inline] 2 searches, shared ground truth established
[W1 inline] 3 lines × 5 lenses, stop conditions: 01=5/5, 02=4/5, 03=5/5
[W2 inline] Cross-synthesis in report body
[Self-critique] 3 issues found, 3 claims spot-checked
[DONE] ~2000 words, 8 sources cited, FACT:12 ANALYSIS:8 TREND:4
```

### The克谦 Test (V7.1 self-check)

> "每个 action 必须对应一个 eval。" — 胥克谦

Before declaring research DONE in degraded mode, verify:
- [ ] Every Hard Gate has visible output in the response
- [ ] Every must_answer question has an evidence-backed answer
- [ ] Every conclusion has a FACT/ANALYSIS/TREND tag
- [ ] Stop conditions are self-assessed per line (even if brief)
- [ ] At least 3 claims have been spot-checked against sources

If any checkbox fails, the research is NOT done.

## P0: Environment Detection

Same as V6 (see `references/methodology.md`), plus:

**Progressive Mode Detection:** If user provides a seed directory, references a prior round, or uses trigger phrases ("继续深挖", "第二轮", "based on last round"), set `progressive: true`. Read `references/progressive-protocol.md` Round Initialization Checklist before P0.7.

## P0.5: Complexity Assessment

Same as V6. See `references/methodology.md`.

## P0.7: Topic Registry (NEW)

**Before P1, mandatory.** The lead agent reads the research question (or seed directory for progressive mode) and builds a Topic Registry.

### Topic Registry Format

```
# Topic Registry

## Research Question
{verbatim question}

## Research Lines

- 01 / <topic-slug-1> / <topic-title-1>
  - seed_files: {if progressive mode, list input files}
  - current_hypothesis: {what we currently believe}
  - why_it_matters: {why this line is worth investigating}
  - must_answer:
    - Q1: {specific question}
    - Q2: {specific question}
    - Q3: {specific question}

- 02 / <topic-slug-2> / <topic-title-2>
  - seed_files:
  - current_hypothesis:
  - why_it_matters:
  - must_answer:
    - Q1:
    - Q2:
```

### Rules

1. Every research line gets a stable **NN** (2-digit number) and **slug** — these persist across rounds
2. `must_answer` questions are the Sprint Contract's acceptance criteria seed
3. The registry is written to `workspace/topic-registry.md` and referenced in all handoffs
4. For progressive rounds: import prior round's registry, mark which questions are already answered, add new ones

Status: `[P0.7 complete] {N} research lines registered.`

## P1: Sprint Contract

**Read `references/methodology.md` for full rules.**

V7 change: Sprint Contracts now reference Topic Registry line numbers. Each task maps to one or more registry lines. The contract includes Wave assignment:

```
Task W0-A: [Shared Ground Truth Collector]
  Registry lines: ALL (shared foundation)
  Wave: 0
  Acceptance Criteria:
  - [ ] >= WAVE0_FLOOR shared ground truth docs
  - [ ] Majority from official/authoritative sources
  - [ ] >= 1 limitation/constraint source
  - [ ] >= 1 comparison/failure-analysis source

Task W1-01: [Research Line 01 Specialist]
  Registry line: 01 / <slug>
  Wave: 1
  Acceptance Criteria:
  - [ ] >= WAVE1_DOC_FLOOR docs for this line
  - [ ] All must_answer questions have evidence
  - [ ] 5-lens coverage: evidence, mechanism, trend, difficulty, controversy
  - [ ] Named entities chased
```

### Wave Doc Floors (defaults)

| Parameter | Formula | Standard | Lightweight |
|-----------|---------|----------|-------------|
| WAVE0_FLOOR | max(8, TOPIC_COUNT × 2) | 8+ | 4+ |
| WAVE1_DOC_FLOOR | per line | 8 | 4 |
| PRIMARY_SOURCE_FLOOR | per line | 4 | 2 |
| LIMITATION_SOURCE_FLOOR | per line | 1 | 1 |

Authority-first rule: **when authoritative primary sources already suffice, do NOT pad with weak secondary sources to meet floors. Floors are minimums against shallow research, not quotas to fill.**

## P2: Wave 0 → Wave 1 Dispatch

### Wave 0: Shared Ground Truth

Dispatch first. All subagents in Wave 1 depend on Wave 0 output.

Wave 0 subagent targets:
- Official documentation, specifications, RFCs
- Official repositories, README, release notes
- Security analyses, protocol specifications
- High-authority comparison/review articles
- Known limitation/constraint documentation

**Gate W0:** Wave 0 must meet WAVE0_FLOOR before ANY Wave 1 task dispatches.

### Wave 1: Per-Topic Deep Dive

Each research line gets its own subagent (or sequential task in degraded mode).

Every Wave 1 subagent investigates through **5 lenses** (embedded in subagent prompt):

1. **Evidence** — key facts with primary source support
2. **Mechanism** — why it works this way, underlying abstractions
3. **Trend** — where it's evolving, with time-stamped evidence
4. **Difficulty** — adoption/migration/maintenance barriers
5. **Controversy** — community disagreement, failure modes, limitations

**Read `references/subagent-prompt.md` for V7 prompt template with 5-lens protocol.**
**Read `references/research-notes-format.md` for V7 notes format.**

### Stop Conditions (per research line — MANDATORY)

A research line is NOT done until ALL 5 conditions are met:

1. **Object list stable** — core entities no longer growing structurally
2. **Diminishing returns** — new searches mostly repeat known facts
3. **must_answer covered** — every registry question has evidence support
4. **Counterevidence sweep done** — at least 1 dedicated search for failures/limitations/controversies
5. **Cross-validation done** — at least 1 "official claim vs community practice" check

If any condition is unmet, subagent must continue or mark `status: partial` with specifics.

## P3-P8: Synthesis Pipeline

### P2.5 Gap-Filling

Same as V6, plus: check Wave 0 shared docs against Wave 1 findings for consistency.

### P3 Registry + _INDEX.md (NEW)

Same 4-dim scoring as V6. Additionally:

**_INDEX.md**: After building the registry, generate a quick-reference index:

```markdown
# Reference Index

## By Research Line
- 01-<slug>: [1] [3] [7] [12]
- 02-<slug>: [2] [5] [8] [13]
- 00-shared: [4] [6] [9] [10] [11]

## By Evidence Type
- FACT (hard, verifiable): [1] [4] [6] [9]
- ANALYSIS (interpretation): [3] [7] [8]
- TREND (time-dependent): [2] [5] [12] [13]
- LIMITATION (constraints/failures): [10] [11]

## 30-Second Lookup
For any claim → find its [n] → look up research line above → read the source doc
```

### P3.5 Conflict Arbitration

Same as V6.

### Wave 2: Cross-Topic Synthesis (NEW)

After all Wave 1 lines complete and registry is built, do cross-topic synthesis:

1. **Shared foundations** — which facts are true across all lines?
2. **Surface vs structural differences** — what looks different but shares a mechanism?
3. **Cross-line validation** — do conclusions from line 01 contradict line 02?
4. **Tracking priorities** — which entities deserve long-term monitoring?

Output: `workspace/W2-cross-topic-synthesis.md`

Gate W2:
- Every cross-topic judgment has registry back-reference
- Each line has >= 2 cross-validated conclusions with other lines
- Clearly distinguished: FACT / ANALYSIS / TREND

### P4 Outline

Same as V6, plus: each section's claims tagged with evidence classification.

### P5 Draft

Same as V6. **New requirement:** every conclusion paragraph ends with evidence classification:

```markdown
The protocol achieves consensus through three-phase commit. [4][6]
**[FACT]**

This design choice likely reflects the influence of Paxos-family algorithms,
though the authors don't cite it directly. [4][7]
**[ANALYSIS]**

Given the trend toward Byzantine-tolerant designs in 2025-2026, this approach
may face pressure to add BFT guarantees within 2 years. [5][12]
**[TREND]**
```

### P6-P7 Evaluator Agent (V7 Enhanced)

**Read `references/evaluator-prompt.md` for V7 Evaluator prompt.**

V7 adds 3 new audit dimensions to the Evaluator:

| New Dimension | What it checks | Hard Fail |
|---------------|---------------|-----------|
| Stop Condition Audit | All 5 stop conditions met per line | Any line with < 3/5 conditions met |
| 30-Second Back-Reference | Evaluator picks 3 claims, tries to trace to registry → source doc | Any claim untraceable |
| Evidence Classification | FACT/ANALYSIS/TREND tags present and accurate | > 20% of tagged conclusions have wrong classification |

### P8 Polish + Living Docs

Same as V6, plus:

**Living Docs Protocol** (for progressive/multi-round research):

If this research is part of a progressive series, after final report:

1. Update seed files with new evidence (see `references/progressive-protocol.md`)
2. Update Topic Registry with answered questions and new questions
3. Write `workspace/round-summary.md` for next-round handoff
4. Update `_INDEX.md` with new references

**Read `references/progressive-protocol.md` for Living Docs update format.**

## Anti-Hallucination Rules

Same as V6, plus:
7. Evidence classifications (FACT/ANALYSIS/TREND) must be honest — a trend speculation tagged as FACT is a hallucination of certainty

## Self-Heal Loop

Same as V6. Max 2 fix rounds per gate, then escalate.

## Progress Reporting

```
[P0 complete] Subagent: yes. Standard mode.
[P0.5 complete] Complexity: medium. Pipeline: full.
[P0.7 complete] 4 research lines registered.
[P1 complete] 1 W0 task + 4 W1 tasks. Sprint contracts set.
[W0 complete] 10 shared ground truth docs. Gate W0: PASS.
[W1 01-<slug> complete] 8 docs, 12 findings. Stop conditions: 5/5.
[W1 02-<slug> complete] 6 docs, 9 findings. Stop conditions: 4/5 (counterevidence partial).
[P2.5 complete] 2 leads chased, 1 counterevidence gap filled.
[P3 complete] Registry: 18 approved, 5 dropped. _INDEX.md written.
[P3.5 complete] 1 conflict detected.
[W2 complete] Cross-synthesis: 3 shared foundations, 2 cross-validated.
── context reset → handoff-2.md ──
[P5 complete] ~6000 words, 18 sources, 48 citations. FACT:24 ANALYSIS:16 TREND:8.
── context reset → handoff-3.md ──
[Evaluator R1] Evidence=PASS Depth=PASS Coherence=FAIL StopAudit=PASS BackRef=PASS ClassAudit=PASS
[Evaluator R2] All PASS.
[P8 complete] Harness log written. Living docs updated (if progressive).
[DONE] ~6200 words, 18 sources, 50 citations.
```
