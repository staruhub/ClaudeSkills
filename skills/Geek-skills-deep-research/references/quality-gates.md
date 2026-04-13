# Quality Gates V7.1

## Hard Gate vs Soft Gate (V7.1)

Not all gates are equal. In degraded mode (no subagents), Hard Gates MUST produce visible output. Soft Gates can be inlined or simplified.

| Gate | Type | Degraded Simplification |
|------|:----:|------------------------|
| Gate 0.7 (Topic Registry) | **HARD** | Inline list OK, but must_answer questions required |
| Gate W0 (Shared Ground Truth) | Soft | Implicit: just do shared searches first |
| Gate W1 (Per-Topic + Stop Conditions) | **HARD** | 5-Lens required; stop condition table required |
| Gate 2 (Registry) | Soft | Inline source list at report end |
| Gate W2 (Cross-Synthesis) | Soft | Section in report body |
| Gate 3 (Draft + Evidence Classification) | **HARD** | FACT/ANALYSIS/TREND tags required |
| Gate 4 (Evaluator) | **HARD** | Self-critique: find 3+ issues, spot-check 3 claims |
| Gate 5 (Final Report) | Soft | Executive Summary required; Harness Log optional |

**Enforcement principle:** Hard Gates correspond to features that directly improve result quality. Soft Gates are process overhead that helps in full mode but can be compressed in degraded mode without quality loss.

## Self-Heal Loop (applies to ALL gates)

```
For each gate:
  1. Run all checks
  2. Any check fails? → Apply the Fix action
  3. Re-check (Round 2)
  4. Still fails? → Apply Fix again
  5. Re-check (Round 3 — final)
  6. Still fails? → Escalate to user:
     - Which gate and check failed
     - What fixes were attempted
     - Specific ask (e.g., "Can you suggest alternative search terms for X?")
```

Max 2 fix rounds per gate. After that, escalate — don't loop forever.

---

## Gate 0.7: Topic Registry (after P0.7)

| Check | Threshold | Fix |
|-------|-----------|-----|
| All lines have stable NN + slug | 100% | Assign missing |
| Each line has >= 2 must_answer Qs | 100% | Add questions |
| No duplicate slugs | 0 | Rename |
| Registry written to workspace | Yes | Write file |

---

## Gate W0: Shared Ground Truth (after Wave 0)

| Check | Standard | Lightweight | Fix |
|-------|----------|-------------|-----|
| Total shared docs (composite >= 6) | >= WAVE0_FLOOR | >= 4 | Dispatch additional W0 task |
| Majority from official sources (Auth >= 7) | > 50% | > 50% | Targeted official search |
| At least 1 limitation/constraint source | >= 1 | >= 1 | Dedicated limitation search |
| At least 1 comparison/failure source | >= 1 | >= 1 | Dedicated failure search |

**Gate W0 must pass before Wave 1 dispatches.**

---

## Gate W1: Per-Topic Deep Dive (after Wave 1, per line)

| Check | Standard | Lightweight | Fix |
|-------|----------|-------------|-----|
| Docs per line (composite >= 6) | >= 8 | >= 4 | Additional searches |
| Primary sources per line | >= 4 | >= 2 | Targeted primary search |
| Limitation sources per line | >= 1 | >= 1 | Dedicated limitation search |
| All must_answer Qs have evidence | 100% | 100% | Targeted Q-specific search |
| 5-lens coverage | All 5 | At least 3 | Fill missing lenses |
| Stop conditions self-assessed | 100% | 100% | Subagent self-reports |
| Stop conditions met | >= 4/5 | >= 3/5 | Re-dispatch or flag |
| 4-dim scoring present | All sources | All sources | Add missing |
| Named entities chased | Required | Best effort | Re-dispatch targeted |

### Stop Condition Summary

After Gate W1, compile stop condition matrix:

```
| Line | Stable | Returns | must_answer | Counter | Cross-val | Score |
|------|:------:|:-------:|:-----------:|:-------:|:---------:|:-----:|
| 01   |  ✓     |   ✓     |     ✓       |   ✓     |    ✓      |  5/5  |
| 02   |  ✓     |   ✓     |     ✓       |   ✗     |    ✓      |  4/5  |
```

Lines with < 3/5 → re-dispatch or flag as incomplete.

---

## Gate 2: Citation Registry (after P3)

| Check | Standard | Lightweight | Fix |
|-------|----------|-------------|-----|
| Total approved sources (composite >= 5.0) | >= 12 | >= 6 | Flag thin areas |
| Unique domains | >= 5 | >= 3 | Diversify |
| Max single-source share | <= 25% | <= 30% | Find alternatives |
| Dropped sources listed | All | All | Must be explicit |
| No duplicate URLs | 0 | 0 | Merge |
| 4-dim scores present | All | All | Score missing |
| _INDEX.md generated | Yes | Yes | Generate |
| Evidence types classified | Yes | Yes | Classify |

---

## Gate W2: Cross-Topic Synthesis (after Wave 2)

| Check | Standard | Lightweight | Fix |
|-------|----------|-------------|-----|
| Every cross-topic judgment has [n] | 100% | 100% | Add references |
| Each line >= 2 cross-validated conclusions | Required | 1 | Identify connections |
| FACT/ANALYSIS/TREND distinguished | 100% | 100% | Tag missing |
| W2-cross-topic-synthesis.md written | Yes | Yes (may be brief) | Write |

**Skip Gate W2 if complexity = Low.**

---

## Gate 3: Draft Quality (after P5)

### Static Thresholds

| Check | Standard | Lightweight | Fix |
|-------|----------|-------------|-----|
| Every [n] in registry | 100% | 100% | Remove or fix |
| No dropped source cited | 0 violations | 0 | Remove immediately |
| Every section has confidence marker | 100% | 100% | Add missing |
| Conflict sections use debate format | All | All | Rewrite |
| Evidence classification tags present | >= 80% conclusions | >= 60% | Add tags |
| Classification accuracy (spot-check 5) | >= 80% correct | >= 60% | Fix tags |

### Dynamic Thresholds (by topic type)

| Check | Data-heavy | Narrative | Comparative | Exploratory |
|-------|-----------|-----------|-------------|-------------|
| Citation density | >= 1/100w | >= 1/300w | >= 1/150w | >= 1/200w |
| Total word count | 4000-8000 | 3000-6000 | 3000-7000 | 2500-5000 |
| Min sections | 5 | 4 | 4 | 4 |

Lightweight: reduce word count by 40%, density thresholds by 30%.

---

## Gate 4: Evaluator Quality (after P6-P7)

| Check | Threshold | Fix |
|-------|-----------|-----|
| All 7 dimensions scored | 100% | Re-run Evaluator |
| Spot-check completed (5 claims) | 100% | Re-run |
| Any dimension FAIL | 0 FAILs to pass | Lead fixes → resubmit (max 3 rounds) |
| Spot-check plausibility | >= 4/5 | Fix suspicious claims |
| 30-second back-reference (3 claims) | 3/3 traceable | Fix broken chains |
| Stop condition audit | All lines >= 3/5 | Re-research weak lines |
| Evidence classification | < 20% misclassified | Fix tags |

### Evaluator Escalation

If after 3 rounds any dimension still FAILs:
1. Output issues to user
2. Ask: adjust scope, accept lower quality, or provide context
3. Proceed with best-effort + disclaimer

---

## Gate 5: Final Report (after P8)

| Check | Threshold | Fix |
|-------|-----------|-----|
| Executive Summary present | Yes | Write it |
| References match registry | 100% | Sync |
| Every reference cited once | 100% | Remove uncited |
| Metadata header complete | Yes | Add missing |
| Harness Log present | Yes (Medium/High) | Write it |
| Limitations from Gaps | Yes | Cross-reference |
| _INDEX.md up to date | Yes | Update |

### Living Docs Gate (progressive mode only)

| Check | Threshold | Fix |
|-------|-----------|-----|
| Seed files updated with new evidence | All lines | Update |
| Topic Registry updated (answered Qs marked) | Yes | Update |
| round-summary.md written | Yes | Write |

---

## Readiness Check (Final Verification)

Before declaring research DONE, verify all 4:

1. **30-second back-reference**: Pick any important judgment → find local support doc in 30s
2. **Narrative coherence**: For each line, can you write "mechanism + trend + difficulty" without re-searching?
3. **Cross-topic structure**: Can you write "what's the overall picture" beyond parallel descriptions?
4. **Handoff continuity**: A new agent reading seed dir + reference dir can continue without briefing

If any fails → research is NOT complete.

---

## Anti-Hallucination Patterns

| Pattern | Where to detect | Fix |
|---------|----------------|-----|
| URL not from any subagent search | Gate 2 registry | Remove citation |
| Claim not in any task note | Gate 4 Evaluator spot-check | Remove or mark [unverified] |
| Number more precise than source | Gate 4 | Use note's precision |
| Source authority inflated | Gate 2 | Re-score |
| "Studies show..." without naming study | Gate 4 | Name or remove |
| Dropped source reappears | Gate 3 + Gate 5 | Remove immediately |
| Subagent invented a URL | Gate W1 | Remove from notes |
| FACT tag on speculation | Gate 3 + Gate 4 | Downgrade to ANALYSIS or TREND |
| TREND tag on verified fact | Gate 3 + Gate 4 | Upgrade to FACT |

## Chinese-Specific Patterns

| Pattern | Fix |
|---------|-----|
| Fake CNKI URL format | Remove, note gap |
| "某专家表示" without name/institution | Name or remove |
| "据统计" without data source | Add source or qualitative language |
| Fabricated institution report | Verify existence or remove |
| "核心期刊" claim without journal name | Verify or downgrade authority |
