<div align="center">

# Geek Skills

**Claude Code skills that ship with quality gates, routing evals, and blind-eval scores — a product, not a prompt collection.**

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![skills](https://img.shields.io/badge/curated_skills-19-blue)](#-all-skills)
[![license](https://img.shields.io/badge/license-MIT-green)](#license)

[English](#english) | [中文](#中文)

</div>

<a id="english"></a>

---

## 🎞️ See it first — `/deck-studio`

One sentence in → a full deck out. Every image below was produced by the skill itself (HTML → headless-Chrome screenshot pipeline, fonts locked at render time) and scored by an **independent blind judge on an absolute rubric** (10 = design studio, 7 = professional agency).

| | |
|:---:|:---:|
| <img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" width="100%"><br>**Constructivist Red** — 9 pages, **7.1/10**<br>highest of four rounds, first past the 7.0 studio line | <img src="skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/preview-cover.png" width="100%"><br>**Ink-White Consulting** — 3-judge blind eval<br>**42.3 vs 29.7** against the old pipeline (position-swapped) |
| <img src="skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/preview-cover.png" width="100%"><br>**Black-Gold Proposal** — **6.6/10** | <img src="skills/Geek-skills-deck-studio/examples/polar-night-ai-native/preview-cover.png" width="100%"><br>**Polar Night Tech** — **6.0/10** |

Each example directory ships the full generator + rendered pages + the lessons the judge caught: [constructivist](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [moshiro](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [yinghuang](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [polar-night](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

**Why the scores go up:** beauty is *inherited, not generated*. The skill freezes taste into a 17-style library with rendered template seeds, 14 registered layouts (L01–L14), and a 22-rule post-render visual gate (Duarte / Tufte / Müller-Brockmann / Butterick / W3C clreq + 10 battle-tested rules). Score trajectory on the same rubric: 6.0 → 6.6 → 6.6 → **7.1**.

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" width="24%">
</p>
<p align="center"><sub>Four of the 17 styles — Bauhaus · Constructivist · Neubrutalism · Aicher — each with a rendered, reusable template seed.</sub></p>

## 🚀 Install in 30 seconds

```bash
git clone https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio      # -> ~/.claude/skills/deck-studio
```

Then in Claude Code:

```
/deck-studio Turn this quarterly review into a consulting-style deck
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

</details>

## ⭐ Featured Skills

Four flagships — each an end-to-end workflow, not a single prompt:

| Skill | What it does | Reach for it when |
|-------|--------------|-------------------|
| 🎞️ **[deck-studio](skills/Geek-skills-deck-studio/SKILL.md)** (v3) | PPT production agent: scene → 17-style library → outline → page schema (registered layouts) → rendered deck or per-page visuals, gated by a 22-rule visual checklist. | Making a report, pitch, course, or proposal deck — or turning an outline/article into slides or infographics. |
| 🔬 **[deep-research](skills/Geek-skills-deep-research/SKILL.md)** (v8.1) | Evidence-based research pipeline: scoped plan → parallel investigation → verified citations → decision brief. Single-agent by default, fans out only when it pays off; ships with evals and a degraded mode. | You need a cited memo, literature review, market/tech landscape, or a decision brief — not a quick lookup. |
| 📋 **[product-manager](skills/Geek-skills-product-manager/SKILL.md)** | Senior PM: PRD authoring & review, retention/growth diagnosis, competitive research, feature prioritization — with "dev can start from this" acceptance bars. | Writing/reviewing a PRD, diagnosing low retention, or prioritizing features. |
| ✍️ **[wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)** | Multi-style WeChat article writing with a built-in anti-translationese (反翻译腔) pass so Chinese long-form reads natively. | Turning material into a publishable Chinese article (tech blog, product intro, event recap). |

## 🧪 What makes this repo different

Most skill repos are prompt collections. This one is maintained like software:

- **Skill Quality Standard v1.0** — every skill passes a D0 gate and carries the "三件套": checkable **acceptance criteria**, explicit **boundaries** (when *not* to use, with hand-offs), and **pitfall tables** drawn from real failures.
- **Routing evals** — 113 cases across 14 skills (`evals/routing-evals.json`) proving each skill triggers when it should and defers when it shouldn't; mutually-exclusive pairs are mirrored on both sides.
- **CI on every push** — [two L1 gates](.github/workflows/validate.yml) (structure + routing-eval consistency) plus a script compile check. Reproduce locally:

  ```bash
  python3 scripts/validate.py            # -> L1 PASS
  python3 scripts/run_routing_evals.py   # -> L1 PASS
  ```

- **Evidence, not adjectives** — visual quality claims above come from blind, position-swapped, multi-judge evals; the score trajectory and every caught defect are recorded in [CHANGELOG.md](CHANGELOG.md) and the example READMEs.
- **No stale hardcoding** — CVE numbers, years, platform paths replaced with live-search instructions or relative paths.
- **Know what you install** — [SECURITY.md](SECURITY.md) gives a per-skill capability matrix (reads files / writes / network / shells out / needs credentials / can delete), derived by grepping the bundled scripts. 11 of 19 skills are prompt-only (ship zero code); exactly one can delete files, and it defaults to dry-run.

> ⚠️ This is a **self-audit** by Claude (Fable 5), not a third-party certification. The two commands above let you re-run the gate yourself; full refactor record in [CHANGELOG.md](CHANGELOG.md).

## 📚 All Skills

<a id="-all-skills"></a>

<details>
<summary><b>19 curated skills by category</b> (click to expand)</summary>

### Development & Architecture

| Skill | Path | Description |
|-------|------|-------------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | Pair-programming partner: delivers code with a structured self-review, focused on AI-specific defects |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | Comprehensive code security audit |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | System design, tech selection, and architecture review |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js performance optimization |

### AI-Native Methodology

| Skill | Path | Description |
|-------|------|-------------|
| `keqian-method` | [skills/Geek-skills-keqian-method](skills/Geek-skills-keqian-method/SKILL.md) | Keqian's AI-Native product dev methodology: single-agent, SDD, quality gates |
| `xuefeng-method` | [skills/Geek-skills-xuefeng-method](skills/Geek-skills-xuefeng-method/SKILL.md) | Xuefeng's AI-Native methodology for open-behavior, model-driven products |
| `ai-sales-champion` | [skills/Geek-skills-ai-sales-champion](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI sales/consulting dialogue helper — turn tech into business language |

### Product & Content

| Skill | Path | Description |
|-------|------|-------------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD writing, requirement analysis, and product strategy |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | Multi-style WeChat article writing |
| `deck-studio` | [skills/Geek-skills-deck-studio](skills/Geek-skills-deck-studio/SKILL.md) | PPT production agent: scene → style library → outline → page schema → deck or per-page visuals (v3) |
| `podcast-generator` | [skills/Geek-skills-podcast-generator](skills/Geek-skills-podcast-generator/SKILL.md) | Volcano Engine dual-speaker AI podcast generator |

### Tools & Utilities

| Skill | Path | Description |
|-------|------|-------------|
| `a-share-analyst` | [skills/Geek-skills-a-share-analyst](skills/Geek-skills-a-share-analyst/SKILL.md) | A-share technical and fundamental analysis |
| `c-drive-cleaner` | [skills/Geek-skills-c-drive-cleaner](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C drive cleanup and disk space management |
| `mineru-pdf-parser` | [skills/Geek-skills-mineru-pdf-parser](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | PDF to Markdown or JSON for LLM workflows |
| `seedream-imagegen` | [skills/Geek-skills-seedream-imagegen](skills/Geek-skills-seedream-imagegen/SKILL.md) | Seedream 4.0 image generation |

### Education & Research

| Skill | Path | Description |
|-------|------|-------------|
| `deep-research` | [skills/Geek-skills-deep-research](skills/Geek-skills-deep-research/SKILL.md) | Evidence-based research workflow with observability, evals, and decision briefs |
| `gaokao-expert` | [skills/Geek-skills-gaokao-expert](skills/Geek-skills-gaokao-expert/SKILL.md) | Gaokao question design expert |
| `university-exam-prep` | [skills/Geek-skills-university-exam-prep](skills/Geek-skills-university-exam-prep/SKILL.md) | University exam prep with Socratic learning |
| `weather-forecast-report` | [skills/Geek-skills-weather-forecast-report](skills/Geek-skills-weather-forecast-report/SKILL.md) | Weather element research report generator |

### Upstream-Synced

| Skill | Path | Notes |
|-------|------|-------|
| `llm-wiki` | [llm-wiki](llm-wiki/SKILL.md) | Preserved in original upstream layout at repo root |

</details>

## 🛠️ For Maintainers

Repository conventions, layout rules, and the maintenance workflow live in [AGENTS.md](AGENTS.md). Pre-publish checks:

```bash
python3 scripts/validate.py && python3 scripts/run_routing_evals.py   # both must print L1 PASS
git ls-files | rg '(^|/)\._'                                          # must print nothing
```

## License

MIT

---

<a id="中文"></a>

<div align="center">

# Geek Skills（中文）

**带质量门禁、路由 evals 和盲评分数的 Claude Code skills 仓库——是产品，不是 prompt 合集。**

</div>

## 🎞️ 先看效果 — `/deck-studio`

一句话进 → 整套 deck 出。下面每张图都由 skill 自己生产（HTML → headless Chrome 截图管线，渲染机锁定字体），并由**独立盲评按绝对标准打分**（10 = 设计工作室，7 = 专业乙方）。

| | |
|:---:|:---:|
| <img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" width="100%"><br>**构成主义红** — 9 页，**7.1/10**<br>四轮最高，首破 7 分工作室线 | <img src="skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/preview-cover.png" width="100%"><br>**墨白咨询** — 三评委盲评<br>**42.3 vs 29.7** 击败旧实现（对调组一致） |
| <img src="skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/preview-cover.png" width="100%"><br>**黑金提案** — **6.6/10** | <img src="skills/Geek-skills-deck-studio/examples/polar-night-ai-native/preview-cover.png" width="100%"><br>**极夜科技** — **6.0/10** |

每套样例目录都含完整生成器 + 渲染页 + 评审抓出的教训：[构成主义](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [墨白](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [英黄](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [极夜](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

**分数为什么在涨：** 美是继承的，不是生成的。skill 把品味冻结进 17 套风格库（含已渲染模板种子）、14 个注册版式（L01–L14）和渲染后 22 条视觉门禁（Duarte / Tufte / Müller-Brockmann / Butterick / W3C clreq + 10 条实战教训）。同一绝对标准下的分数轨迹：6.0 → 6.6 → 6.6 → **7.1**。

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" width="24%">
</p>
<p align="center"><sub>17 套风格中的 4 套——包豪斯 · 构成主义 · Neubrutalism · Aicher——每套带已渲染、可复用的模板种子。</sub></p>

## 🚀 30 秒安装

```bash
git clone https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio      # -> ~/.claude/skills/deck-studio
```

然后在 Claude Code 里：

```
/deck-studio 把这份季度复盘做成一套咨询风 PPT
```

<details>
<summary>其他安装方式（列出全部、项目级、手动）</summary>

```bash
python3 scripts/install_skill.py --list                  # 查看可安装的名字
python3 scripts/install_skill.py deep-research           # 任意 skill，用短名
python3 scripts/install_skill.py deep-research --project # -> ./.claude/skills/（项目级）
```

**手动：** 安装后的**目录名**就是 slash command，所以复制时要改名：

```bash
cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research
```

不改名直接复制 → 命令是 `/Geek-skills-deep-research`。Claude 也会在 `description` 匹配时自动加载，`/命令` 只是显式调用方式之一。

</details>

## ⭐ 核心推荐

四个旗舰 skill，每个都是端到端工作流，不是单条 prompt：

| Skill | 做什么 | 什么时候用 |
|-------|--------|-----------|
| 🎞️ **[deck-studio](skills/Geek-skills-deck-studio/SKILL.md)**（v3） | PPT 生产 Agent：场景 → 17 套风格库 → 大纲 → 页面语法（注册版式）→ 渲染成 deck 或逐页视觉图，出稿过 22 条视觉门禁。 | 做汇报/路演/课件/提案的 PPT，或把大纲、文章做成 slides、信息图。 |
| 🔬 **[deep-research](skills/Geek-skills-deep-research/SKILL.md)**（v8.1） | 循证研究流水线：定范围 → 并行调查 → 校验引用 → 决策简报。默认单 Agent，值得时才并行；内置 evals 与降级模式。 | 需要带引用的备忘、综述、市场/技术全景或决策简报——而不是快速查一下。 |
| 📋 **[product-manager](skills/Geek-skills-product-manager/SKILL.md)** | 资深 PM：PRD 创作与评审、留存/增长诊断、竞品研究、功能优先级——验收标准做到"开发照着就能动手"。 | 写/评审 PRD、诊断留存低、给功能排优先级。 |
| ✍️ **[wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)** | 多风格公众号文章创作，内置反翻译腔精修，让中文长文读起来是"人写的"。 | 把素材写成可发布的中文长文（技术博客、产品介绍、活动回顾）。 |

## 🧪 这个仓库有什么不同

多数 skill 仓库是 prompt 合集，这个仓库按软件的方式维护：

- **Skill 质量标准 v1.0**——每个 skill 过 D0 门槛并带"三件套"：可判定的**验收标准**、明确的**边界**（何时不该用、移交给谁）、来自真实踩坑的**陷阱表**。
- **路由 evals**——14 个 skill 共 113 条用例（`evals/routing-evals.json`），证明该触发时触发、不该触发时让路；互斥对双向镜像。
- **每次 push 跑 CI**——[两个 L1 门禁](.github/workflows/validate.yml)（结构 + 路由 eval 一致性）+ 脚本编译检查。本地复现：

  ```bash
  python3 scripts/validate.py            # -> L1 PASS
  python3 scripts/run_routing_evals.py   # -> L1 PASS
  ```

- **证据而非形容词**——上面的视觉质量结论来自盲评（对调分组、多评委）；分数轨迹与每条被抓缺陷都记录在 [CHANGELOG.md](CHANGELOG.md) 和样例 README 里。
- **无过时硬编码**——写死的 CVE 编号、年份、平台路径全部改为实时搜索指令或相对路径。
- **装之前先知道它能碰什么**——[SECURITY.md](SECURITY.md) 给出逐 skill 能力矩阵（读文件 / 写文件 / 联网 / 调外部命令 / 需凭证 / 可删文件），由 grep 打包脚本核实得出。19 个里 11 个是纯 prompt（零代码）；只有 1 个能删文件，且默认 dry-run。

> ⚠️ 这是 Claude（Fable 5）的**自审**，不是第三方认证。上面两条命令可自行复跑门禁；完整重构记录见 [CHANGELOG.md](CHANGELOG.md)。

## 📚 全部技能

<details>
<summary><b>19 个自维护技能（按类别）</b>（点击展开）</summary>

### 开发与架构

| 技能 | 路径 | 说明 |
|------|------|------|
| `pair-programming` | [skills/Geek-skills-pair-programming](skills/Geek-skills-pair-programming/SKILL.md) | 结对编程搭档，交付代码附带结构化自审，重点盯 AI 生成代码特有缺陷 |
| `security-audit` | [skills/Geek-skills-security-audit](skills/Geek-skills-security-audit/SKILL.md) | 全面代码安全审计 |
| `solution-architect` | [skills/Geek-skills-solution-architect](skills/Geek-skills-solution-architect/SKILL.md) | 系统设计与技术选型 |
| `threejs-performance` | [skills/Geek-skills-threejs-performance](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js 性能优化 |

### AI-Native 方法论

| 技能 | 路径 | 说明 |
|------|------|------|
| `keqian-method` | [skills/Geek-skills-keqian-method](skills/Geek-skills-keqian-method/SKILL.md) | 克谦式 AI-Native 产品开发方法论：单 Agent、SDD、质量门禁 |
| `xuefeng-method` | [skills/Geek-skills-xuefeng-method](skills/Geek-skills-xuefeng-method/SKILL.md) | 雪峰式 AI-Native 方法论，面向行为开放、模型驱动的产品 |
| `ai-sales-champion` | [skills/Geek-skills-ai-sales-champion](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI 销售/咨询对话助手，把技术讲成业务语言 |

### 产品与内容

| 技能 | 路径 | 说明 |
|------|------|------|
| `product-manager` | [skills/Geek-skills-product-manager](skills/Geek-skills-product-manager/SKILL.md) | PRD 创作、需求分析与产品策略 |
| `wechat-article-writer` | [skills/Geek-skills-wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md) | 多风格微信公众号文章创作 |
| `deck-studio` | [skills/Geek-skills-deck-studio](skills/Geek-skills-deck-studio/SKILL.md) | PPT 生产 Agent：场景识别 → 风格库 → 大纲 → 页面语法 → 内容稿或逐页视觉图（v3） |
| `podcast-generator` | [skills/Geek-skills-podcast-generator](skills/Geek-skills-podcast-generator/SKILL.md) | 火山引擎双人 AI 播客生成 |

### 工具与效率

| 技能 | 路径 | 说明 |
|------|------|------|
| `a-share-analyst` | [skills/Geek-skills-a-share-analyst](skills/Geek-skills-a-share-analyst/SKILL.md) | A 股技术面与基本面分析 |
| `c-drive-cleaner` | [skills/Geek-skills-c-drive-cleaner](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C 盘清理与空间管理 |
| `mineru-pdf-parser` | [skills/Geek-skills-mineru-pdf-parser](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | 面向 LLM 工作流的 PDF 解析 |
| `seedream-imagegen` | [skills/Geek-skills-seedream-imagegen](skills/Geek-skills-seedream-imagegen/SKILL.md) | Seedream 4.0 图像生成 |

### 教育与研究

| 技能 | 路径 | 说明 |
|------|------|------|
| `deep-research` | [skills/Geek-skills-deep-research](skills/Geek-skills-deep-research/SKILL.md) | 带可观测性、评估资产和决策简报能力的深度研究流水线 |
| `gaokao-expert` | [skills/Geek-skills-gaokao-expert](skills/Geek-skills-gaokao-expert/SKILL.md) | 高考命题专家 |
| `university-exam-prep` | [skills/Geek-skills-university-exam-prep](skills/Geek-skills-university-exam-prep/SKILL.md) | 大学备考苏格拉底式学习助手 |
| `weather-forecast-report` | [skills/Geek-skills-weather-forecast-report](skills/Geek-skills-weather-forecast-report/SKILL.md) | 天气要素研究报告生成器 |

### 上游同步

| 技能 | 路径 | 备注 |
|------|------|------|
| `llm-wiki` | [llm-wiki](llm-wiki/SKILL.md) | 保留上游原始目录结构，位于仓库根目录 |

</details>

## 🛠️ 维护者入口

目录约定、维护流程与提交规范见 [AGENTS.md](AGENTS.md)。发布前检查：

```bash
python3 scripts/validate.py && python3 scripts/run_routing_evals.py   # 两者都须打印 L1 PASS
git ls-files | rg '(^|/)\._'                                          # 应无输出
```

## License

MIT
