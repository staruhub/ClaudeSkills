---
name: deep-research
version: 8.0.0
description: >
  Use this skill when the user wants an evidence-based research memo, literature
  review, market/policy/technical landscape, or a multi-source decision brief
  with citations, trade-offs, and a clear conclusion. Best for tasks that need
  synthesis across multiple external sources, iterative follow-up research, or
  a reusable written artifact. Do not use for quick factual lookups,
  single-source summaries, simple Q&A, or when the user clearly wants a short
  answer instead of a report. Chinese trigger examples: "帮我调研", "深度研究",
  "综述报告", "技术选型分析", "竞品研究", "政策分析". Success = scoped plan,
  grounded notes, verified citations, explicit limitations, and a final
  brief/report that clearly separates evidence from analysis.
compatibility: Requires web search plus file read/write. Shell/scripts and subagents are optional accelerators, not hard requirements.
metadata:
  version: "8.0"
  owner: "enterprise-research"
  category: "research"
  maturity: "production-candidate"
  outputs: "workspace/research-plan.md workspace/research-notes/*.md workspace/registry.md workspace/draft.md workspace/evaluation.md workspace/run-summary.json"
---

# Deep Research V8.0

This skill is for **evidence-rich research outputs**, not for every question that happens to mention “analysis”.

The V8 shift is simple:
- **Single-agent first.** Start with one lead agent and only fan out when parallel work will clearly help.
- **Thin harness, fat skill.** Put reusable judgment and workflow here; keep deterministic checks in scripts.
- **Context organization over prompt stuffing.** Load the minimum active context bundle, then pull in references only when needed.
- **Eval and observability built in.** A good report is not enough; the run must also be diagnosable and improvable.

## What this skill should produce

Choose the lightest artifact that satisfies the task.

| Output type | Use when | Typical length | Required artifacts |
|---|---|---:|---|
| **Brief memo** | user wants a concise answer with evidence | 800-1800 words | `research-plan.md`, `registry.md`, `draft.md`, `run-summary.json` |
| **Full report** | user asks for comprehensive analysis / literature review / decision document | 2500-6000 words | all core artifacts + `evaluation.md` |
| **Delta update** | user says “continue”, “second round”, “what changed”, “deepen round 2” | 600-1800 words | prior round handoff + new notes + delta draft |

If the user did **not** ask for a long report, default to **Brief memo**.

## When NOT to use this skill

Do **not** activate for:
- quick fact lookups or simple definitions
- summarizing a single provided article/PDF/page
- short comparisons the model can answer directly from 1-2 sources
- brainstorming without evidence requirements
- tasks where the user explicitly wants a short answer, not a report

If in doubt, ask yourself: **Does this task need a reusable evidence artifact and multi-source synthesis?** If not, do something simpler.

## Org-policy boundary

This skill does **not** replace system policies, enterprise guardrails, or repo-level instructions.
Put these outside the skill:
- data handling / PII / compliance rules
- approval requirements for external access or irreversible actions
- org-wide style and review policy
- environment-specific permissions

Keep those in system prompts, AGENTS/CLAUDE/OpenAI config, or the harness. This skill owns the **workflow**, not the company’s permanent red lines.

## Active context bundle

At activation time, keep the active bundle small.

**Always load first**
1. This `SKILL.md`
2. `references/methodology.md`
3. `references/report-assembly.md`
4. `references/research-notes-format.md`

**Load on demand**
- `references/subagent-prompt.md` only if you actually dispatch subagents
- `references/evaluator-prompt.md` only if you run the evaluator
- `references/quality-gates.md` before finalization
- `references/observability.md` when emitting metrics or diagnosing regressions
- `references/tension-discovery.md` only for contested / decision-heavy topics
- `references/landscape-scan.md` only when literature or ecosystem mapping matters

**After compaction or context reset**
Reload only:
- `research-plan.md`
- active task notes
- `registry.md`
- unresolved issues list
- the one reference file for the current phase

Do **not** reload the whole skill tree unless the run drifted badly.

## Workflow

### P0 — Scope, route, and choose the lightest mode

Create `workspace/research-plan.md` with:
- research question
- intended audience
- freshness requirement
- geography / market / jurisdiction
- output type (brief / full / delta)
- stakes: low / medium / high
- why this skill is justified

Then choose the orchestration mode:

| Mode | Default choice |
|---|---|
| **Single-agent** | default for most tasks |
| **Lead + subagents** | only when there are 3+ separable research threads or obvious parallel value |
| **Delta update** | when continuing prior research |

**Do not fan out just because subagents exist.**

### P0.5 — Optional modules (not mandatory by default)

Use optional modules only when they earn their keep:
- **Tension discovery** (`references/tension-discovery.md`): use for contested, hype-heavy, or decision topics where mainstream framing may be wrong.
- **Landscape scan** (`references/landscape-scan.md`): use when the domain is unfamiliar, broad, or literature-heavy. For non-academic topics, this can be an ecosystem/standards/vendor scan rather than arXiv.
- **Reverse search**: use when costs, failure modes, counter-evidence, or operational constraints are missing.

### P1 — Plan the evidence work

Break the task into 1-5 research threads. Each thread needs:
- one crisp objective
- starting queries
- what “done” looks like
- what evidence would change the conclusion

If using subagents, each subagent gets **one** focused thread. Avoid overlapping ownership.

### P2 — Investigate, extract, and write notes

Follow `references/research-notes-format.md`.

Rules:
- search broadly first, then chase named entities, standards, datasets, products, trials, laws, or papers
- fetch and read the best supporting sources for the highest-value claims
- write notes that separate **facts**, **analysis**, **gaps**, and **unresolved conflicts**
- capture support snippets/paraphrases for the top claims so later verification is easier

The lead agent should work from notes **by default**, but may inspect raw/fetched sources again when:
- two sources materially conflict
- a claim is high-stakes or decision-critical
- a note looks suspiciously weak or over-compressed

### P3 — Build registry and verify evidence

Create `workspace/registry.md` from approved sources only.

Use `scripts/source_evaluator.py` as a **helper**, not an oracle.
Authority scores are heuristics. Final acceptance depends on claim fit, evidence type, and whether the source can actually bear the weight of the claim.

Use `scripts/verify_citations.py` before finalization.

Evidence rules:
- core claims should lean on the strongest available evidence for that claim type
- anecdotes illustrate; they do not anchor the conclusion
- conflicting evidence must be surfaced, not silently averaged away
- if the topic is high-stakes, spot-check raw support for top claims before shipping

### P4 — Synthesize the output

Follow `references/report-assembly.md`.

Always include:
- clear answer to the user’s question
- explicit limitations / trade-offs
- separation of source-backed findings vs your own synthesis
- uncertainty calibrated to evidence quality

Only include a dedicated **Decision Framework** when the user is choosing between options.
Only require a **contrarian** section when the topic actually has a mainstream narrative worth challenging. Otherwise produce a **non-obvious insight** instead of forcing fake contrarianism.

### P5 — Evaluate and gate

For full reports and medium/high-stakes briefs, run the evaluator using `references/evaluator-prompt.md`.

Before finalization, check `references/quality-gates.md`:
- routing correctness
- process completeness
- grounding / citation integrity
- output quality
- efficiency and operational health

### P6 — Publish, summarize, and learn

Emit:
- final `draft.md`
- `evaluation.md` if run
- `run-summary.json` via `scripts/emit_run_summary.py`

In the run summary, record what actually helped: single-agent, subagents, tension discovery, landscape scan, reverse search, evaluator, or manual spot-checks.
This is what makes the skill improve over time.

## Deterministic helpers

Use scripts for the parts that should be boring and repeatable:
- `scripts/source_evaluator.py` — baseline source scoring / diversity checks
- `scripts/verify_citations.py` — citation integrity and source-pool checks
- `scripts/emit_run_summary.py` — structured observability output for the run

If a deterministic check fails, fix the artifact first. Do not argue with the script unless you have a concrete reason.

## Evaluation and observability

This skill is only “good” if it performs well on:
1. **Routing** — does it trigger when it should, and stay out of the way when it should not?
2. **Process** — did it create the right artifacts and evidence trail?
3. **Outcome** — is the final brief/report genuinely useful and grounded?
4. **Efficiency** — did it get there with acceptable tool/time/token cost?
5. **Safety / governance** — did it respect policy boundaries and handle uncertainty honestly?

See:
- `evals/routing-evals.json`
- `references/quality-gates.md`
- `references/observability.md`

## Degraded mode

If subagents, shell, or a writable workspace are unavailable, keep the workflow but shrink the surface area:
- one lead agent only
- inline notes instead of files if needed
- fewer searches, but still enough to support the conclusion
- lightweight evaluator or self-check if full evaluation is impossible
- still keep limitations, uncertainty, and citation integrity

## Stop conditions

Stop and ask for help only when the blocker is real and specific, for example:
- no credible sources exist for a critical claim
- the user’s requested scope conflicts with available evidence
- policy or access restrictions block the required research

Otherwise, continue with the best justified artifact and say where the confidence drops.
