<div align="center">

# Geek Skills

**19 curated Claude Code skills that turn vague requests into work you can actually ship.**

Cited research briefs · build-ready PRDs · presentation-ready decks · publishable Chinese articles · engineering audits

**Not 1,000 prompt snippets. Nineteen end-to-end workflows with real examples, acceptance criteria, routing evaluations, and explicit safety boundaries.**

[![CI](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![Curated skills](https://img.shields.io/badge/curated_skills-19-00C878)](#all-19-curated-skills)
[![Security](https://img.shields.io/badge/security-capability_matrix-FF4444)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-0D1117)](#license)

[English](README.md) · [简体中文](README.zh-CN.md)

[Choose a workflow](#start-with-the-outcome) · [Quick start](#quick-start) · [See a real result](#see-a-real-result) · [Browse all skills](#all-19-curated-skills)

</div>

---

## Start with the outcome

You do not need to learn a framework first. Pick the artifact you need to deliver.

| I need to ship... | Start with | What it produces |
|---|---|---|
| A decision brief I can defend | [`deep-research`](skills/Geek-skills-deep-research/SKILL.md) **v8.1.1** | Research plan, source registry, verified citations, draft, evaluation, and run summary |
| A product spec engineering can build | [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) **v1.1.0** | PRD, acceptance criteria, review findings, product strategy, or prioritization |
| A deck I can present | [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md) **v3.0.0** | Outline, page briefs, slide visuals, quality gates, and a reproducible deck workflow |
| A Chinese article I can publish | [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | Article, title options, abstract, visual plan, and anti-translationese polish |

These four are the best entry points. The repository also covers architecture, security, pair programming, finance, education, image generation, podcasting, and more.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/staruhub/ClaudeSkills.git
cd ClaudeSkills
python3 scripts/install_skill.py --list
```

### 2. Install the one skill you need

```bash
# Install to ~/.claude/skills/<name>
python3 scripts/install_skill.py deep-research

# Other good starting points
python3 scripts/install_skill.py product-manager
python3 scripts/install_skill.py deck-studio
python3 scripts/install_skill.py wechat-article-writer
```

### 3. Use it in Claude Code

```text
/deep-research Compare three local-first RAG architectures for a 20-person legal team.
/product-manager Turn this feature idea into a build-ready PRD with acceptance criteria.
/deck-studio Create a 12-slide investor update from this quarterly memo.
/wechat-article-writer 把这份调研写成一篇有判断、可直接发布的公众号文章。
```

<details>
<summary><strong>Project-scoped install</strong></summary>

Install into `./.claude/skills/` so the skill travels with a single project:

```bash
python3 scripts/install_skill.py deep-research --project
```

</details>

<details>
<summary><strong>Manual install</strong></summary>

Copy a skill directory and remove the `Geek-skills-` prefix:

```bash
cp -R skills/Geek-skills-deck-studio ~/.claude/skills/deck-studio
```

Restart Claude Code after installing.

</details>

## See a real result

### `deck-studio`: one brief in, a complete deck out

Prompt:

```text
Create a 9-page design constitution for an AI-native startup.
Make every page visually distinct while preserving one coherent system.
```

<table>
  <tr>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" alt="Constructivist design constitution deck" width="100%" />
      <br /><strong>Constructivist Red</strong><br />9-page design constitution
    </td>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/preview-cover.png" alt="Ink-white consulting report deck" width="100%" />
      <br /><strong>Ink-White Consulting</strong><br />Consulting report
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/preview-cover.png" alt="Black-gold proposal deck" width="100%" />
      <br /><strong>Black-Gold Proposal</strong><br />Program proposal
    </td>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/polar-night-ai-native/preview-cover.png" alt="Polar night AI-native methodology deck" width="100%" />
      <br /><strong>Polar Night Tech</strong><br />AI-native methodology
    </td>
  </tr>
</table>

Each example includes its generator, rendered pages, and lessons learned. Browse the full [`deck-studio` example suite](skills/Geek-skills-deck-studio/examples/).

<details>
<summary><strong>How the deck workflow is evaluated</strong></summary>

`deck-studio` v3 uses 22 visual gates and 14 registered layout families. The repository includes a blind comparison in which the workflow-oriented version scored **42.3/50** against **29.7/50** for the legacy prompt-oriented version.

These are repository self-evaluations, including model-assisted visual review. They are useful engineering signals, not third-party certification. See the [`CHANGELOG`](CHANGELOG.md) for the full record.

</details>

## Why Geek Skills

| Principle | What it means here |
|---|---|
| **Curated over bulk** | Nineteen maintained workflows are easier to inspect, learn, and improve than a directory of anonymous prompt snippets. |
| **Artifacts over advice** | Each skill is designed around a concrete deliverable: a report, PRD, deck, audit, implementation, forecast, or media asset. |
| **Workflow over one-shot prompting** | Strong skills define inputs, stages, intermediate artifacts, validation, and stopping conditions—not just a persona prompt. |
| **Inspectable risk** | Network access, local execution, credentials, and destructive behavior are documented in a repository-wide capability matrix. |

## Quality without the marketing fog

- **113 routing cases across 14 skills** help catch false triggers and missed triggers.
- **Continuous validation** checks metadata, paths, naming, internal links, and compilation where applicable.
- **Canonical repository checks** are one command each:

  ```bash
  python3 scripts/validate.py
  python3 scripts/run_routing_evals.py
  ```

- **Explicit safety boundaries** live in [`SECURITY.md`](SECURITY.md). Eleven curated skills are prompt-only; the one skill with deletion behavior, `c-drive-cleaner`, defaults to dry-run.
- **Changes are inspectable** in [`CHANGELOG.md`](CHANGELOG.md), including evaluation results and known limitations.

No quality claim here is a third-party certification. The goal is simpler: make the evidence visible enough that you can decide whether a skill deserves access to your work.

## All 19 curated skills

### Development & architecture

| Skill | Use it when you need... |
|---|---|
| [`pair-programming`](skills/Geek-skills-pair-programming/) | Structured collaborative coding, debugging, and review |
| [`security-audit`](skills/Geek-skills-security-audit/) | A repository security audit with actionable findings |
| [`solution-architect`](skills/Geek-skills-solution-architect/) | Architecture decisions, trade-offs, and implementation planning |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/) | Diagnosis and optimization of Three.js or WebGL performance |

### AI-native methods

| Skill | Use it when you need... |
|---|---|
| [`keqian-method`](skills/Geek-skills-keqian-method/) | Systematic decomposition and first-principles reasoning |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/) | Structured analysis and decision support |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/) | AI-assisted sales discovery, messaging, and conversion work |

### Product & content

| Skill | Use it when you need... |
|---|---|
| [`product-manager`](skills/Geek-skills-product-manager/) | A PRD, product review, strategy, prioritization, or growth diagnosis |
| [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/) | A polished, publishable Chinese long-form article |
| [`deck-studio`](skills/Geek-skills-deck-studio/) | A planned, designed, and evaluated presentation workflow |
| [`podcast-generator`](skills/Geek-skills-podcast-generator/) | A research-to-script-to-audio podcast pipeline |

### Tools & data

| Skill | Use it when you need... |
|---|---|
| [`a-share-analyst`](skills/Geek-skills-a-share-analyst/) | Evidence-based analysis of China A-share companies |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/) | A safe, dry-run-first Windows C-drive cleanup plan |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/) | Structured extraction from complex PDF documents |
| [`seedream-imagegen`](skills/Geek-skills-seedream-imagegen/) | Prompt design and generation workflows for Seedream images |

### Education & research

| Skill | Use it when you need... |
|---|---|
| [`deep-research`](skills/Geek-skills-deep-research/) | Source-backed research with citations, artifacts, and evaluation |
| [`gaokao-expert`](skills/Geek-skills-gaokao-expert/) | Chinese Gaokao planning and evidence-backed guidance |
| [`university-exam-prep`](skills/Geek-skills-university-exam-prep/) | A structured university exam preparation plan |
| [`weather-forecast-report`](skills/Geek-skills-weather-forecast-report/) | A cited, decision-oriented weather forecast report |

### Upstream skill

[`llm-wiki`](skills/llm-wiki/) is tracked separately from the 19 curated skills. It is an upstream, reusable workflow for turning a topic into a structured learning page.

## Contributing

Good contributions make a skill easier to trust, not merely longer.

Before opening a pull request:

1. Keep the skill focused on a concrete outcome.
2. Document inputs, workflow stages, outputs, failure modes, and safety boundaries.
3. Add or update routing cases when trigger behavior changes.
4. Run both repository checks:

   ```bash
   python3 scripts/validate.py
   python3 scripts/run_routing_evals.py
   ```

Found a rough edge? [Open an issue](https://github.com/staruhub/ClaudeSkills/issues). Have a tested improvement? [Open a pull request](https://github.com/staruhub/ClaudeSkills/pulls).

## If this saved you time

Star the repository so you can find it again—and so more builders discover a smaller, inspectable alternative to prompt collections.

## License

MIT © ChaoGeek
