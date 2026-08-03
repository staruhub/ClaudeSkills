[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![zh-CN](https://img.shields.io/badge/语言-简体中文-red.svg)](README.zh-CN.md)

<p align="center">
  <img src="assets/claudeskills-readme-hero.png" alt="ClaudeSkills: help Claude Code finish work through repeatable workflows" width="100%">
</p>

<div align="center">

# ClaudeSkills

**Give Claude Code workflows that finish the job.**

Thirteen curated skills package the steps, templates, scripts, examples, and quality gates behind repeatable work—not just one-off prompts. Start with four flagship workflows for research, product documents, decks, and WeChat publishing.

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![release](https://img.shields.io/badge/release-1.0.0-2746d8)](https://github.com/staruhub/ClaudeSkills/releases/tag/1.0.0)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Website](https://staruhub.github.io/ClaudeSkills/) · [Release 1.0.0](https://github.com/staruhub/ClaudeSkills/releases/tag/1.0.0) · [30-second install](#-install-in-30-seconds) · [What's new](#four-flagship-workflows-rebuilt) · [All 13 skills](#-all-skills) · [Security](SECURITY.md)

</div>

## Four flagship workflows, rebuilt

| You ask | The workflow does | You get |
|---|---|---|
| “Compare three RAG architectures for our support team.” | 🔬 [`deep-research`](skills/Geek-skills-deep-research/SKILL.md) scopes the question, gathers multiple sources, maintains a source registry, and checks citations | A decision memo or full report with conclusions, evidence, trade-offs, and explicit limitations |
| “Don't code yet. Ask me one question at a time until the product is clear.” | 📋 [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) enters **grill-me-to-doc**: it reads repository evidence first, asks one decision per turn, and can resume after interruption | A reviewable PRODUCT-DOC, decision log, and open questions—with a hard stop before implementation |
| “Turn this quarterly review into a consulting-style deck.” | 🎞️ [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md) confirms the outline before page briefs, registered layouts, and visual QA | Deck content, per-slide visuals, or an infographic set, depending on the delivery mode |
| “Turn these notes into a WeChat article, including image prompts and layout.” | ✍️ [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) can run `article`, `image-prompts`, `layout`, or the full pipeline | An article, provider-neutral image-prompt manifest, and WeChat-safe inline HTML—without pretending prompts are images or auto-publishing |

Each flagship exposes the work between request and deliverable: when it asks, which references it loads, what it validates, and where it stops. You are installing an inspectable workflow, not a magic sentence.

## 🚀 Install in 30 seconds

Start with one skill you will actually use:

```bash
git clone --depth 1 https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio
```

Then, in Claude Code:

```text
/deck-studio Turn this quarterly review into an 8-slide consulting deck
```

The installer copies it to `~/.claude/skills/deck-studio`. Replace `deck-studio` with `deep-research`, `product-manager`, or `wechat-article-writer` to install another flagship.

<details>
<summary><b>Other install options, updates, removal, and FAQ</b></summary>

```bash
python3 scripts/install_skill.py --list                  # list short names
python3 scripts/install_skill.py deep-research           # install any skill
python3 scripts/install_skill.py deep-research --project # install for this project only
```

For a manual install, copy **and rename** the directory:

```bash
cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research
```

The installed directory name becomes the slash command. Without the rename, the command is `/Geek-skills-deep-research`.

```bash
git pull && python3 scripts/install_skill.py deck-studio --force   # update
rm -rf ~/.claude/skills/deck-studio                                # uninstall
```

- **Installed but no command?** Check the installed directory name.
- **No automatic trigger?** Auto-loading matches the skill `description` against your wording. The explicit `/command` is the reliable path.
- **Re-install after `git pull`?** Yes. Installed skills are copies.

</details>

## Not another prompt dump

| A disposable prompt | ClaudeSkills |
|---|---|
| The conversation ends; next time you start over | Workflows, templates, and references live in version control |
| The model improvises every intermediate step | Inputs, stages, stop conditions, and deliverables are explicit |
| An interruption can erase decisions | Stateful workflows write resumable handoff files, including grill-me-to-doc and research delta updates |
| “Looks good” is the only test | Deterministic parts use schemas, scripts, fixtures, and negative cases; subjective quality stays subject to review |
| You discover file, network, or shell access after install | [`SECURITY.md`](SECURITY.md) discloses reads, writes, network, commands, credentials, and deletion per skill |

Actual capabilities still depend on the tools and permissions available in your Claude Code session. This repository makes the workflow and its boundaries inspectable; it does not bypass permissions or market static checks as production performance.

## Try one in 60 seconds

| If you are working on | Start with | Inspect first |
|---|---|---|
| Technical, competitive, or policy research | `/deep-research Compare… and produce a cited decision memo for leadership` | [Research workflow and artifacts](skills/Geek-skills-deep-research/SKILL.md) |
| Turning an early idea into a product document | `/product-manager grill me to doc: I want to build…` | [One-question interview contract](skills/Geek-skills-product-manager/references/GRILL-ME-TO-DOC.md) |
| A presentation, pitch, or training deck | `/deck-studio Turn… into a 10-slide …-style deck` | [Delivery modes and layout system](skills/Geek-skills-deck-studio/SKILL.md) |
| WeChat copy, image prompts, and inline HTML | `/wechat-article-writer full-pipeline: turn… into…` | [Four execution modes](skills/Geek-skills-wechat-article-writer/SKILL.md) |

Do not install all 13 at once. Run one workflow against a real task this week; keep it if it earns the slot.

## Inspect the artifacts before you install

Deck Studio keeps generators, rendered pages, rubrics, and judge feedback in the repository. Here are four of its 17 rendered style seeds:

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" alt="Bauhaus deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" alt="Constructivist deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" alt="Neubrutalism deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" alt="Aicher deck style preview" width="24%">
</p>

[Constructivist](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [Moshiro consulting report](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [Yinghuang bootcamp proposal](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [Polar Night AI Native](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

In the repository's blind **model-based self-evaluation**, the Constructivist example scored **7.1/10** on the documented rubric; a position-swapped three-judge comparison scored the current pipeline **42.3 vs 29.7**. These are reproducible project artifacts, not third-party certification.

<details>
<summary><b>How the four flagship workflows were tested</b></summary>

| Check | What it establishes | What it does not establish |
|---|---|---|
| `python3 tests/task_b/run_contract_tests.py` | 17 deterministic contract cases cover success, resume, and failure paths across the four flagships; Deck also uses real Chrome rendering and PPTX assembly | Subjective quality from an arbitrary future model, a live image provider, or WeChat publishing |
| `python3 scripts/validate.py` | All 13 curated skill directories satisfy the repository structure contract | Live business-task E2E for every skill |
| `python3 scripts/run_routing_evals.py` | Schema, target, uniqueness, and conflict checks pass for 91 routing case definitions across 10 skills | Model-executed routing accuracy |
| Python / Node compile checks | 13 bundled Python files and 7 related JavaScript files parse | Network, external-tool, or production availability |
| Deck example directories | Generators, rendered pages, rubrics, scores, and recorded defects are present | Independent external certification |

Re-run the baseline gates:

```bash
python3 scripts/validate.py
python3 scripts/run_routing_evals.py
python3 scripts/validate_site.py
```

See [`verification/2026-07-31/README.md`](verification/2026-07-31/README.md) for the independent acceptance record.

</details>

## 📚 All Skills

<a id="-all-skills"></a>

**Flagships (4)**

[deck-studio](skills/Geek-skills-deck-studio/SKILL.md) · [deep-research](skills/Geek-skills-deep-research/SKILL.md) · [product-manager](skills/Geek-skills-product-manager/SKILL.md) · [wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)

<details>
<summary><b>Professional work (9)</b></summary>

| Skill | What it does |
|---|---|
| [`pair-programming`](skills/Geek-skills-pair-programming/SKILL.md) | Implements code with structured self-review for common AI-code defects |
| [`security-audit`](skills/Geek-skills-security-audit/SKILL.md) | Reviews code and dependencies for security issues |
| [`solution-architect`](skills/Geek-skills-solution-architect/SKILL.md) | Supports system design, technology choices, and architecture reviews |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/SKILL.md) | Diagnoses and improves Three.js performance |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | Converts PDF to Markdown or JSON with a local MinerU installation |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/SKILL.md) | Turns technical capabilities into customer-facing business value |
| [`keqian-method`](skills/Geek-skills-keqian-method/SKILL.md) | Uses a single-agent, SDD, quality-gated product-development method |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/SKILL.md) | Applies an open-behavior, model-driven AI-native product method |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Performs guarded Windows C-drive cleanup, dry-run by default |

</details>

**Lab**

Personal and experimental workflows—exam prep, weather reports, image and podcast generation, and A-share analysis—live in [`lab/`](lab/). They are not part of the 13-skill curated set or its gates.

<details>
<summary><b>Upstream-synced (1)</b></summary>

[`llm-wiki`](llm-wiki/SKILL.md) builds a codebase wiki from [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and keeps the upstream layout at the repository root.

</details>

## Help make it better

Found a bug, or built something with a skill? [Open an issue](https://github.com/staruhub/ClaudeSkills/issues) with a redacted input, output, and reproduction steps when possible. To contribute a skill, start with [CONTRIBUTING.md](CONTRIBUTING.md): new work incubates in [`lab/`](lab/) and graduates after meeting the repository gates.

If a workflow genuinely saved you time, leave a ⭐ and send it to someone still rebuilding the same prompts every week. Stars help discovery; they are not a quality certificate.

The WeChat launch poster and ready-to-send copy live in [`assets/social/`](assets/social/).

## License

[MIT](LICENSE)
