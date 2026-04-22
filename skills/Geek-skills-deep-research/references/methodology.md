# Deep Research Methodology V8

V8 is built around one idea: **use the lightest workflow that still produces a trustworthy evidence artifact**.

## 1) First decide whether deep research is justified

Deep research is justified when at least one of these is true:
- the user wants a written artifact they can reuse or share
- the task needs synthesis across multiple sources
- the task is decision-oriented and trade-offs matter
- the user wants a second round / deeper follow-up
- the topic is broad, fast-moving, contested, or cross-domain

If none of those are true, do something simpler.

---

## 2) Choose output type before you search

| Output type | Use when | Default target |
|---|---|---|
| Brief memo | concise but evidence-backed answer | 800-1800 words |
| Full report | comprehensive research deliverable | 2500-6000 words |
| Delta update | continue prior work or summarize changes | 600-1800 words |

Choose the artifact first, because it determines how much context, search, and evaluation work is justified.

---

## 3) Single-agent first, fan out only when earned

### Use single-agent when
- there are 1-2 main questions
- evidence threads overlap heavily
- the task is short or medium complexity
- the extra coordination cost would outweigh the gain

### Use subagents when
- there are 3+ separable threads
- different roles or domains truly matter
- parallel work will reduce time or improve coverage
- you have a writable workspace and a place to merge artifacts

### Subagent rules
- prefer 2-4 subagents, rarely more than 5
- each subagent owns one crisp thread
- avoid two agents answering the same sub-question
- merge by notes, not by copying raw search output around

---

## 4) Build a context plan, not just a task plan

Before investigating, define three buckets.

### A. Essential now
Load these immediately:
- the user’s exact request
- output type and audience
- freshness / geography / scope constraints
- core methodology and report assembly rules

### B. Useful later
Defer until needed:
- detailed evaluator prompt
- subagent prompt
- tension discovery rules
- landscape scan playbook
- observability guide

### C. Keep out unless needed
Avoid loading by default:
- old run logs
- every prior report
- entire literature dumps
- every reference file in the skill tree

This is the difference between **context organization** and “shove everything into the prompt”.

---

## 5) Investigation loop

For each research thread:
1. Start with 2-4 broad searches.
2. Identify named entities, standards, datasets, papers, products, policies, laws, or experts.
3. Chase the highest-value entities with targeted searches.
4. Read/fetch the best sources for the claims that actually matter.
5. Write notes with facts, analysis, gaps, conflicts, and support snippets.
6. Stop when the next search is mostly duplicate / low-value, or when confidence is already good enough for the chosen artifact.

### Stop because you know enough, not because you are tired.

A thread is usually “good enough” when:
- the core question is answered from multiple relevant sources
- the main counterpoint or limitation is also covered
- additional searches mostly repeat known facts

---

## 6) Optional modules: use them selectively

### Tension discovery
Use when:
- the topic is hype-heavy
- the task is a recommendation or selection
- the popular framing might hide the real trade-off

Skip when:
- the user only needs a descriptive overview
- the topic is stable and not especially contested

### Landscape scan
Use when:
- the domain is unfamiliar or broad
- literature, standards, repos, filings, or ecosystem mapping matters
- you need to derive roles or clusters from the evidence landscape

Skip when:
- the task is narrow and already well scoped
- the domain can be covered directly without a separate scan

### Reverse search
Run when:
- the draft has benefits but almost no costs
- the notes have no failure modes, constraints, or counter-evidence
- the recommendation feels too clean

---

## 7) Evidence hierarchy is claim-specific

Do not blindly prefer one source class everywhere.

Ask: **what kind of evidence can actually support this claim?**

Examples:
- product feature claim → official docs / release notes / source code
- law or policy claim → official text / regulator / court or agency guidance
- scientific effectiveness claim → peer-reviewed studies / meta-analyses / trial reports
- market trend claim → filings / reputable research / financial disclosures / high-quality industry data
- operational failure mode claim → incident reports / postmortems / engineering docs / credible case studies

A source can be famous and still be the wrong support for the claim.

---

## 8) Merge by notes, re-open raw sources only when needed

By default, the lead agent should synthesize from notes and the registry.
That keeps the active context smaller and more stable.

Re-open raw/fetched sources for:
- high-stakes claims
- unresolved conflicts
- suspicious or overly compressed notes
- final decision-driving numbers or legal wording

This is the sweet spot: **notes-first, raw-source-on-demand**.

---

## 9) Final output rules

Every final artifact should:
- answer the user’s actual question
- distinguish evidence from interpretation
- include limitations / trade-offs
- calibrate certainty honestly
- avoid fake precision

Only force a decision framework when the user is choosing.
Only force a contrarian move when a real dominant narrative exists.
Otherwise prefer a **non-obvious insight**.

---

## 10) Learn from runs

After the run, record:
- which workflow shape was used
- where time or tools were wasted
- where evidence was thin
- what made the final result better
- what should become a new test case

A skill gets better when failures become future routing tests or output checks.
