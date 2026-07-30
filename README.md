[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![zh-CN](https://img.shields.io/badge/语言-简体中文-red.svg)](README.zh-CN.md)

<div align="center">

# Geek Skills

**13 curated Claude Code skills for turning real work into inspectable deliverables.**

Start with four flagship workflows for research, product documents, decks, and Chinese long-form writing. Then inspect the instructions, examples, checks, and capability boundaries before you install.

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Website](https://staruhub.github.io/ClaudeSkills/) · [Install](#-install-in-30-seconds) · [All 13 skills](#-all-skills) · [Security](SECURITY.md)

</div>

## Start with a flagship workflow

| Your job | Workflow | Inspectable output |
|----------|----------|--------------------|
| Research a decision | 🔬 [`deep-research`](skills/Geek-skills-deep-research/SKILL.md) (v8.1) | A scoped memo or report with a source registry, citation checks, trade-offs, and stated limitations |
| Write or review a product document | 📋 [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) | A structured PRD or review with decision framing and checkable acceptance criteria |
| Present, pitch, or teach | 🎞️ [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md) (v3) | An approved outline, page briefs, registered layouts, and a rendered visual path with an explicit QA checklist |
| Draft a Chinese long-form article | ✍️ [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | A structured article draft with title, voice, and anti-translationese review |

These are repeatable instruction packages, not one-line prompt snippets. Capabilities still depend on the tools and permissions available in your Claude Code session.

## 🚀 Install in 30 seconds

```bash
git clone --depth 1 https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio      # -> ~/.claude/skills/deck-studio, then run /deck-studio
```

<details>
<summary>Other install options (list all, per-project, manual)</summary>

```bash
python3 scripts/install_skill.py --list                  # see installable names
python3 scripts/install_skill.py deep-research           # any skill by short name
python3 scripts/install_skill.py deep-research --project # -> ./.claude/skills/ (project-level)
```

**Manual:** the installed *directory name* is the slash command, so copy **and rename**:

```bash
cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research
```

Copy without renaming → the command becomes `/Geek-skills-deep-research`. Claude also auto-loads a skill when its `description` matches; `/command` is just the explicit way in.

**Update / uninstall:**

```bash
git pull && python3 scripts/install_skill.py deck-studio --force   # update (installed skills are copies)
rm -rf ~/.claude/skills/deck-studio                                # uninstall
```

</details>

<details>
<summary>FAQ</summary>

- **Installed, but `/deck-studio` doesn't appear** — the slash command comes from the installed **directory name**. If you copied manually without renaming, your command is `/Geek-skills-deck-studio`. Re-install with the script, or rename the directory.
- **The skill doesn't trigger automatically** — auto-loading matches the skill's `description` against your request, so phrasing matters. The `/command` form always works.
- **Do I need to re-install after `git pull`?** — yes: installed skills are copies. Re-run `python3 scripts/install_skill.py <name> --force`.

</details>

## 📈 Inspect an artifact, not a promise

The Deck Studio examples include generators, rendered pages, and judge feedback. In the repository's blind **model-based self-evaluation**, the Constructivist example scored **7.1/10** on the documented rubric; the position-swapped three-judge comparison scored the current pipeline **42.3 vs 29.7** ([method and scores](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/)). These results are reproducible project evidence, not third-party certification.

[constructivist (7.1)](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [moshiro (3-judge eval)](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [yinghuang](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [polar-night](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" alt="Bauhaus deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" alt="Constructivist deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" alt="Neubrutalism deck style preview" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" alt="Aicher deck style preview" width="24%">
</p>
<p align="center"><sub>Four of the 17 rendered style seeds: Bauhaus · Constructivist · Neubrutalism · Aicher.</sub></p>

## 🧪 What the checks prove

| Check | Current repository evidence | Does not prove |
|-------|-----------------------------|----------------|
| `python3 scripts/validate.py` | Structural L1 assertions for all 13 curated skill directories | Output quality or live integrations |
| `python3 scripts/run_routing_evals.py` | Schema, target, uniqueness, and conflict checks for 91 routing case definitions across 10 skills | Model-executed routing accuracy |
| Python compile check in CI | All 10 bundled `skills/**/*.py` files parse and compile | Runtime behavior, network access, or external tools |
| Deck example directories | Generators, rendered pages, rubrics, scores, and recorded defects | Independent external certification |

Re-run the repository and site checks locally:

```bash
python3 scripts/validate.py
python3 scripts/run_routing_evals.py
python3 scripts/validate_site.py
```

Before installing, read the [per-skill capability matrix](SECURITY.md): it separates bundled-script risk from actions that still require Claude Code permissions. See [CHANGELOG.md](CHANGELOG.md) for the refactor record.

## 📚 All Skills

<a id="-all-skills"></a>

**Flagship** — the four workflows above: [deck-studio](skills/Geek-skills-deck-studio/SKILL.md) · [deep-research](skills/Geek-skills-deep-research/SKILL.md) · [product-manager](skills/Geek-skills-product-manager/SKILL.md) · [wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)

<details>
<summary><b>Core — professional work</b> (9 skills)</summary>

| Skill | Description |
|-------|-------------|
| [`pair-programming`](skills/Geek-skills-pair-programming/SKILL.md) | Pair-programming partner: delivers code with a structured self-review, focused on AI-specific defects |
| [`security-audit`](skills/Geek-skills-security-audit/SKILL.md) | Comprehensive code security audit |
| [`solution-architect`](skills/Geek-skills-solution-architect/SKILL.md) | System design, tech selection, and architecture review |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js performance optimization |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | PDF to Markdown or JSON for LLM workflows (requires a local MinerU install) |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI sales/consulting dialogue helper — turn tech into business language |
| [`keqian-method`](skills/Geek-skills-keqian-method/SKILL.md) | Keqian's AI-Native product dev methodology: single-agent, SDD, quality gates |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/SKILL.md) | Xuefeng's AI-Native methodology for open-behavior, model-driven products |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C drive cleanup and disk space management (dry-run by default) |

</details>

**Lab** — experimental and personal skills (exam prep, weather reports, image/podcast generation, A-share analysis) live in [`lab/`](lab/). They are **not part of the curated set**, are excluded from the quality gates above, and may graduate into `skills/` or move out of this repo.

<details>
<summary><b>Upstream-synced</b> (1)</summary>

| Skill | Notes |
|-------|-------|
| [`llm-wiki`](llm-wiki/SKILL.md) | Codebase wiki builder, based on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f); kept in its original upstream layout at repo root |

</details>

## 🤝 Community

Found a bug, or built something with a skill? [Open an issue](https://github.com/staruhub/ClaudeSkills/issues). Want to contribute a skill or a fix? Start with [CONTRIBUTING.md](CONTRIBUTING.md) — new skills incubate in [`lab/`](lab/) and graduate into the curated set by passing the quality gates. If a skill saved you an afternoon, a ⭐ helps other people find it.

## License

[MIT](LICENSE)
