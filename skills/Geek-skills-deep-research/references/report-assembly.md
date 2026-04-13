# Report Assembly V7 — Draft from Notes

## Core Rule

The report is written from task notes and the citation registry.
The lead agent never references raw search results — only the distilled
findings in task files and approved sources in registry.md.

## Section Design

Adapt to topic type. Do NOT use a fixed template.

| Topic Type | Recommended Sections |
|------------|---------------------|
| Historical comparison | Background per case, Cross-case patterns, Modern parallel, Speed analysis |
| Technology survey | Background, Architecture, Key features, Ecosystem, Comparison, Outlook |
| Competitive analysis | Market overview, Player profiles, Comparison matrix, Strategic insights |
| Policy analysis | Context, Current framework, Stakeholder views, Impact, Recommendations |
| Scientific review | Background, Methods landscape, Evidence, Debates, Open questions |

Rename sections to be topic-specific.

## Cross-Topic Synthesis Section (NEW — from Wave 2)

Reports with 3+ research lines MUST include a cross-topic synthesis section
drawing from `W2-cross-topic-synthesis.md`:

```markdown
## Cross-Topic Analysis

### Shared Foundations
{Facts that hold across all research lines} [n][m] **[FACT]**

### Structural Patterns
{What appears different but shares underlying mechanism} [n][m] **[ANALYSIS]**

### Divergent Findings
{Where research lines genuinely disagree, with evidence} [n][m] **[ANALYSIS]**

### Tracking Priorities
{Entities worth long-term monitoring and why} [n] **[TREND]**
```

## Evidence Classification Tags (NEW)

Every conclusion paragraph ends with a classification:

- **[FACT]** — directly verifiable, supported by primary evidence
- **[ANALYSIS]** — interpretive synthesis, evidence-informed
- **[TREND]** — time-dependent projection, may become outdated

Example:
```markdown
The protocol achieves consensus through three-phase commit. [4][6] **[FACT]**

This design likely reflects Paxos-family influence, though not explicitly
cited by the authors. [4][7] **[ANALYSIS]**

Given the 2025-2026 trend toward Byzantine-tolerant designs, BFT guarantees
may become expected within 2 years. [5][12] **[TREND]**
```

For mixed paragraphs: tag the dominant type.

## Conflict Sections (from P3.5)

Same as V6:
```markdown
### Disputed: {Topic}
{Source A}: {claim [n]}. {Source B}: {claim [m]}.
Discrepancy stems from {analysis}. [n][m]
```

Rules: never silently pick one side; present both; explain source of disagreement.

## Generation Order

1. Body sections (outline order from P4)
2. Cross-Topic Analysis (from Wave 2)
3. Key Findings (synthesize from body)
4. Limitations (from task Gaps sections)
5. Executive Summary (compress whole report)
6. References (from registry)
7. Metadata header

Never write the summary first.

## Per-Section Protocol

```
For each section:
  1. Re-read mapped task notes (from P4 outline)
  2. Write section
  3. Insert [n] citations — ONLY from Approved list
  4. Add evidence classification tags to conclusion paragraphs
  5. Checkpoint: uncited claims? Wrong [n]? Missing tags?
  6. Add confidence marker
  7. Next section
```

## Dynamic Word Count Targets

| Topic Type | Words/Section (Standard) | Words/Section (Lightweight) |
|------------|-------------------------|---------------------------|
| Data-heavy | 800-1200 | 500-750 |
| Narrative | 600-1000 | 400-650 |
| Comparative | 500-800 | 350-550 |
| Exploratory | 500-800 | 350-550 |

## Citation Rules

- [n] from P3 registry are final
- Each source gets one [n], reuse for multiple citations
- Cross-check: every [n] in text has matching Reference entry
- Every Reference is cited at least once

## Confidence Markers

```
**Confidence:** High/Medium/Low
**Basis:** {reason}
```

- **High:** 3+ agreeing high-authority sources, specific data
- **Medium:** 2+ sources but some gaps
- **Low:** Few sources, mostly indirect

## Final Report Structure (V7)

```markdown
# {Title}

> Date: YYYY-MM-DD | Sources: N | Words: ~XXXX | Mode: Standard/Lightweight
> Complexity: Medium | Topic: Comparative | Evaluator: Passed R2
> Research Lines: 4 | Progressive Round: 1 (or "Single")

## Executive Summary
{200-400 words, written LAST}

## {Section 1 — topic-specific title}
{content with [n] citations}
{conclusion} **[FACT/ANALYSIS/TREND]**
Confidence: High — {reason}

## {Section 2}
...

### Disputed: {Conflict Topic}  ← if P3.5 found conflicts
{debate format}

## Cross-Topic Analysis  ← if 3+ research lines
{from Wave 2 synthesis}

## Key Findings
- Finding 1 [n][m] **[FACT]**
- Finding 2 [n] **[ANALYSIS]**
- Finding 3 [n] **[TREND]**

## Limitations
- {from task Gaps}
- {methodological limitations}

## References
[1] Author/Org. Title. URL. Accessed YYYY-MM-DD.
[2] ...
```

## Limitations Section

Draw from subagent Gaps sections + stop condition gaps:
```
- No Chinese-language academic sources found (task-w1-01 gap)
- Counterevidence for line 02 limited to 1 source (stop condition partial)
- Limited to web-accessible sources; paywalled journals not accessible
```
