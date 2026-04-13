# Deep Research Methodology V7 — Wave Architecture + Topic Registry

## P0: Environment Detection

| Check | Result | Impact |
|-------|--------|--------|
| Subagent dispatch available? | Yes → full architecture | No → degraded sequential mode |
| web_search? | Required | Stop if absent |
| web_fetch? | Required for DEEP tasks | SCAN-only if absent |
| Filesystem writable? | Notes to files | Notes to conversation context |

Mode selection (first matching rule):
- Lightweight: query < 30 words AND single entity/concept
- Standard: multi-entity comparison, historical analysis, or user says "深入"/"comprehensive"
- Default: Standard

Status: `[P0 complete] Subagent: {yes/no}. Mode: {standard/lightweight}.`

---

## P0.5: Complexity Assessment

Run AFTER P0.7 Topic Registry is generated. Determines pipeline depth.

### Assessment Criteria

| Signal | Low | Medium | High |
|--------|-----|--------|------|
| Research lines | 1-2 | 3-4 | 5+ |
| Domains | Single | Multi | Cross-disciplinary |
| Controversy | None | Some debate | Highly contested |
| Data type | Factual | Mixed | Conflicting quantitative |

### Pipeline Adaptation

**Low complexity:**
- Wave 0 may be minimal (WAVE0_FLOOR = 4)
- Skip: P3.5 (conflict arbitration), Wave 2 cross-synthesis
- Skip: Evaluator Agent (P6 self-critique sufficient)
- 2-3 subagents, Lightweight mode

**Medium complexity:**
- Full Wave 0 / 1 / 2 pipeline
- Evaluator Agent recommended
- Single evaluation round

**High complexity:**
- Full pipeline + extra P2.5 round
- Evaluator Agent mandatory, 2-round eval
- Consider dedicated Chinese-language subagent
- Wave 2 cross-synthesis mandatory

### Phase Skip Justification

When skipping a phase, always output:
```
[{phase} skipped] Reason: {why}.
  Load-bearing assumption: {what we're betting is unnecessary}.
```

### Dynamic Upgrade/Downgrade

After Wave 0 completes, reassess:
- If Wave 0 yields rich leads across many domains → upgrade complexity
- If Wave 0 finds very narrow source landscape → downgrade or flag scarcity

Status: `[P0.5 complete] Complexity: {low/medium/high}. Pipeline: {phases to run}.`

---

## P0.7: Topic Registry

**Mandatory.** Before any dispatch, the lead agent builds a Topic Registry from the research question (or seed directory for progressive rounds).

### Process

1. Parse the research question into distinct investigation lines
2. Assign each line: NN (2-digit), slug, title
3. For each line: write hypothesis, importance, must_answer questions
4. For progressive rounds: import prior registry, mark answered Qs, add new Qs
5. Write to `workspace/topic-registry.md`

### Registry Structure

```markdown
# Topic Registry

## Research Question
{verbatim — never paraphrase}

## Mode
Progressive Round: {1 / 2 / 3 / ...} (or "Single" if one-shot)
Prior Registry: {path or "none"}

## Research Lines

- 01 / <slug> / <title>
  - seed_files: {list or "none"}
  - current_hypothesis: {what we currently think}
  - why_it_matters: {1 sentence}
  - must_answer:
    - Q1: {specific, answerable question}
    - Q2: {specific, answerable question}
    - Q3: {specific, answerable question}
  - answered_from_prior: {list of Qs already answered, if progressive}

- 02 / <slug> / <title>
  ...
```

### Rules

1. Stable numbering: NN and slug never change across rounds
2. must_answer questions must be specific enough to have a verifiable answer
3. Minimum 2 must_answer questions per line
4. Maximum 8 research lines (if more, group into themes first)

Status: `[P0.7 complete] {N} research lines registered.`

---

## P1: Research Task Board + Sprint Contract (V7)

The lead agent creates tasks, each mapped to Topic Registry lines.

### Task Board Format (V7)

```
# Research Task Board
Topic: {research question}
Mode: Standard
Complexity: Medium
Subagent: Yes
Topic Registry: workspace/topic-registry.md

## Wave 0 — Shared Ground Truth

### Task W0-A: [Shared Ground Truth Collector]
Registry lines: ALL
Objective: Build shared authoritative foundation
Queries:
  - "{official docs query}"
  - "{specification query}"
  - "{limitation/constraint query}"
Depth: DEEP
Output: workspace/research-notes/task-w0-a.md
Acceptance Criteria:
  - [ ] >= WAVE0_FLOOR docs with composite >= 6
  - [ ] Majority from official/authoritative sources (Auth >= 7)
  - [ ] >= 1 source on limitations/constraints
  - [ ] >= 1 source on comparison/failure analysis

## Wave 1 — Per-Topic Deep Dive (dispatch ONLY after W0 gate passes)

### Task W1-01: [Research Line 01 — <slug> Specialist]
Registry line: 01 / <slug>
Objective: {from topic registry must_answer}
Queries:
  - "{query_1}"
  - "{query_2}"
  - "{query_3}"
Depth: DEEP
Output: workspace/research-notes/task-w1-01.md
Acceptance Criteria:
  - [ ] >= WAVE1_DOC_FLOOR sources with composite >= 6
  - [ ] All must_answer questions from registry have evidence
  - [ ] 5-lens coverage (evidence, mechanism, trend, difficulty, controversy)
  - [ ] Named entities chased with dedicated searches
  - [ ] All 5 stop conditions self-assessed (see Stop Conditions)
```

### Default Acceptance Criteria by Mode

| Criteria | Standard | Lightweight |
|----------|----------|-------------|
| WAVE0_FLOOR | max(8, lines×2) | max(4, lines×1) |
| WAVE1_DOC_FLOOR per line | 8 | 4 |
| PRIMARY_SOURCE_FLOOR per line | 4 | 2 |
| LIMITATION_SOURCE_FLOOR per line | 1 | 1 |
| Min findings per line | 5 | 3 |
| Deep Read Notes (DEEP) | 2+ sources | 1+ source |
| Named entity chase | Required | Best effort |

### Authority-First Rule (HIGHEST PRIORITY)

When authoritative primary sources already suffice for a judgment, do NOT pad with weak secondary sources to hit floors. Floors prevent shallow research; they are not quotas. Quality > quantity.

### Task Decomposition Rules

1. Wave 0: 1-2 tasks for shared foundation
2. Wave 1: 1 task per research line (max 6 parallel)
3. For bilingual topics: at least 1 Chinese-language search per Wave 1 task
4. Every task gets 2-3 pre-planned queries + the 5-lens protocol
5. Wave 1 tasks may read Wave 0 output for shared context

### User Checkpoint (interactive mode)

If requested, pause after Topic Registry (P0.7) and after Task Board (P1).

Status: `[P1 complete] {N_W0} W0 tasks + {N_W1} W1 tasks. Sprint contracts set.`

---

## P2: Wave 0 → Wave 1 Dispatch

### Wave 0 Execution

1. Dispatch Wave 0 tasks
2. Each writes to `workspace/research-notes/task-w0-*.md`
3. **Gate W0 check:**
   - Total shared docs >= WAVE0_FLOOR? If no → dispatch additional W0 task
   - Majority from official sources (Auth >= 7)? If no → flag
   - At least 1 limitation source? If no → targeted search

**Gate W0 must pass before Wave 1 dispatches.** This prevents parallel lines from building on unstable foundations.

### Wave 1 Execution

After Gate W0 passes:

1. Dispatch all Wave 1 tasks in parallel (max 6 concurrent)
2. Each subagent follows the **5-Lens Protocol**:
   - EVIDENCE: What are the key facts? Primary source support?
   - MECHANISM: Why does it work this way? What's the underlying abstraction?
   - TREND: Where is it evolving? Time-stamped evidence?
   - DIFFICULTY: What are the adoption/migration/maintenance barriers?
   - CONTROVERSY: What do critics say? Failure modes? Community disagreement?
3. Each subagent self-assesses against **5 Stop Conditions**

### 5 Stop Conditions (per research line)

A line is NOT done until ALL are met:

| # | Condition | How to check |
|---|-----------|-------------|
| 1 | Object list stable | Core entities not growing structurally |
| 2 | Diminishing returns | Last 2 searches mostly repeated known facts |
| 3 | must_answer covered | Every Q in registry has evidence support |
| 4 | Counterevidence swept | >= 1 dedicated failure/limitation search |
| 5 | Cross-validated | >= 1 "official vs community" comparison |

Subagent self-reports: `stop_conditions: [5/5]` or `stop_conditions: [3/5, missing: counterevidence, cross-validation]`

### Quality-Directed Stop (from V6)

Also still applies:
- 4+ quality sources (composite >= 6) → can stop on that sub-question
- 2 consecutive duplicate searches → stop for that query
- Tool budget exhausted → mark partial

### Context Reset After P2

After ALL P2 tasks complete:
1. Write `workspace/handoff-1.md` (see `reference/handoff-format.md`)
2. Include Topic Registry path and all task note paths
3. Next session reads handoff + task notes + registry only

---

## P2.5: Gap-Filling Dispatch

Same as V6, plus:
- Cross-check Wave 0 shared facts against Wave 1 findings
- If Wave 1 finding contradicts Wave 0 shared doc → flag for P3.5

---

## P3: Citation Registry + _INDEX.md

Same 4-dim scoring and registry process as V6.

### _INDEX.md (NEW)

After registry is built, generate `workspace/_INDEX.md`:

```markdown
# Reference Index

## By Research Line
- 00-shared: [n1] [n2] ...
- 01-<slug>: [n3] [n4] ...
- 02-<slug>: [n5] [n6] ...

## By Evidence Type
- FACT: [n1] [n3] [n5] — hard, verifiable claims
- ANALYSIS: [n2] [n4] — interpretive claims
- TREND: [n6] [n7] — time-dependent projections
- LIMITATION: [n8] — constraints, failures, risks

## Quick Lookup
claim → [n] → research line → source doc
```

Status: `[P3 complete] Registry: {approved}/{total}. _INDEX.md written.`

---

## P3.5: Conflict Arbitration

Same as V6.

---

## Wave 2: Cross-Topic Synthesis (NEW)

After registry is built and conflicts flagged, do cross-topic analysis.

### Process

1. Read all Wave 1 notes + registry + conflicts
2. Answer 4 questions:
   - **Shared foundations:** Which facts hold across ALL lines?
   - **Surface vs structural:** What appears different but shares underlying mechanism?
   - **Cross-line contradictions:** Do lines 01 and 02 conflict?
   - **Tracking priorities:** Which entities deserve long-term monitoring?
3. Write `workspace/W2-cross-topic-synthesis.md`

### Gate W2

| Check | Threshold |
|-------|-----------|
| Every cross-topic judgment has [n] back-reference | 100% |
| Each line has >= 2 cross-validated conclusions | Required |
| FACT / ANALYSIS / TREND distinguished | 100% |

Status: `[W2 complete] {N} shared foundations, {M} cross-validated conclusions.`

---

## P4: Outline

Same as V6, plus:
- Each section's key claims tagged with evidence classification (FACT/ANALYSIS/TREND)
- Wave 2 synthesis feeds the cross-cutting sections

---

## P5: Draft

Same rules as V6 (write from notes, every claim cited, no new sources).

### Evidence Classification (NEW)

Every conclusion paragraph ends with a classification tag:

- **[FACT]** — directly supported by primary evidence, verifiable
- **[ANALYSIS]** — interpretive synthesis by the author, evidence-informed but not directly stated in sources
- **[TREND]** — time-dependent projection, may become outdated

Mixed paragraphs: tag the dominant type, note if mixed.

### Context Reset

Write `workspace/handoff-2.md` before P5. Start fresh reading only handoff + registry + outline.
Write `workspace/handoff-3.md` after P5. Evaluator starts fresh.

---

## P6-P7: Evaluator Agent (V7 Enhanced)

**Read `reference/evaluator-prompt.md` for V7 Evaluator prompt.**

V7 Evaluator scores 7 dimensions (4 original + 3 new):

| Dimension | Weight | Hard Fail |
|-----------|--------|-----------|
| Evidence Quality | 25% | >3 uncited factual claims |
| Analytical Depth | 20% | >50% sections pure paraphrase |
| Coherence | 20% | Unresolved contradictions |
| Completeness | 15% | Any major aspect has 0 coverage |
| **Stop Condition Audit** | 8% | Any line with < 3/5 conditions met |
| **30-Second Back-Reference** | 7% | Any of 3 sampled claims untraceable |
| **Evidence Classification** | 5% | >20% of tags are wrong classification |

### 30-Second Back-Reference Protocol

Evaluator picks 3 claims from different sections:
1. Find the [n] citation
2. Look up [n] in _INDEX.md → research line → source
3. Can you trace the full chain in < 30 seconds reading time?
4. If any chain is broken → FAIL

---

## P8: Polish + Living Docs

Same as V6 (Executive Summary, references, metadata, harness log).

### Living Docs Protocol (progressive mode only)

**Read `reference/progressive-protocol.md` for full format.**

If progressive round, additionally:
1. Update each seed file with new evidence (structured append, never delete history)
2. Update Topic Registry: mark answered Qs, add new Qs
3. Write `workspace/round-summary.md` for next-round handoff
4. Update `_INDEX.md`

---

## Anti-Hallucination Patterns

Same as V6 (see `reference/quality-gates.md`), plus:
- FACT tag on a trend speculation = hallucination of certainty
- TREND tag on a verified fact = false hedging
