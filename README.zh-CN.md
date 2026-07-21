[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![zh-CN](https://img.shields.io/badge/语言-简体中文-red.svg)](README.zh-CN.md)

<div align="center">

# Geek Skills

**13 个精选的、把活真正干完的 Claude Code skills——做 deck、研究简报、PRD、文章、安全审计。**

端到端工作流，像软件一样被测过，不是 prompt 碎片。

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![skills](https://img.shields.io/badge/curated_skills-13-blue)](#-全部技能)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

## 输入这一句 —

```
/deck-studio 把这份季度复盘做成一套咨询风 PPT
```

**— 就还你一整套 deck。** 一次真实运行的第一页，独立盲评 **7.1/10**（7.0 = 专业设计工作室线）：

<p align="center">
<img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" width="82%">
</p>
<p align="center"><sub>共 9 页，由 skill 自己生产——没有手挑模板，没有人工补妆。<a href="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/">完整样例 →</a></sub></p>

## 你今天要交付什么？

| 我要… | Skill | 拿到 |
|-------|-------|------|
| 认真研究一个决策 | 🔬 [`deep-research`](skills/Geek-skills-deep-research/SKILL.md)（v8.1） | 带可校验引用的决策简报——定范围 → 并行调查 → 引用核实 |
| 写或评审 PRD | 📋 [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) | 开发照着就能动手的 PRD，验收标准可判定 |
| 做汇报或路演 | 🎞️ [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md)（v3） | 渲染完成的 deck：17 套风格库、注册版式、22 条视觉门禁 |
| 发一篇公众号长文 | ✍️ [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | 可直接发布的中文长文，内置反翻译腔精修 |

每个都是端到端工作流，不是单条 prompt。[全部技能 ↓](#-全部技能)

## 🚀 30 秒安装

```bash
git clone https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio      # -> ~/.claude/skills/deck-studio，然后运行 /deck-studio
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

## 📈 可复跑的质量，而非形容词

Deck 质量由**独立盲评按绝对标准打分**（10 = 设计工作室，7 = 专业乙方）——不是我自己打的。同一标准下四轮发布的轨迹：6.0 → 6.6 → 6.6 → **7.1**，首次越过工作室线。三评委、对调分组的盲评中，当前实现以 **42.3 vs 29.7** 击败旧实现。

每套样例目录都含完整生成器、渲染页和评审抓出的缺陷：
[构成主义（7.1）](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [墨白（三评委盲评）](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [英黄](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [极夜](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" width="24%">
</p>
<p align="center"><sub>17 套风格中的 4 套——包豪斯 · 构成主义 · Neubrutalism · Aicher——每套带已渲染、可复用的模板种子。美是<em>继承的，不是生成的</em>。</sub></p>

## 🧪 按软件的方式维护

- **Skill 质量标准 v1.0**——每个 skill 过 D0 门槛并带"三件套"：可判定的**验收标准**、明确的**边界**（何时不该用、移交给谁）、来自真实踩坑的**陷阱表**。
- **路由 evals**——10 个 skill 共 85 条用例（`skills/*/evals/routing-evals.json`），证明该触发时触发、不该触发时让路。
- **每次 push 跑 CI**——[两个 L1 门禁](.github/workflows/validate.yml)（结构 + 路由 eval 一致性）+ 脚本编译检查。本地复现：`python3 scripts/validate.py && python3 scripts/run_routing_evals.py`。
- **装之前先知道它能碰什么**——[SECURITY.md](SECURITY.md) 给出逐 skill 能力矩阵（读 / 写 / 联网 / 调外部命令 / 需凭证 / 可删文件）。13 个精选 skill 里 9 个零代码；只有 1 个能删文件，且默认 dry-run。

> ⚠️ 质量门禁是 Claude 的**自审**，不是第三方认证——上面的命令可自行复跑。完整重构记录见 [CHANGELOG.md](CHANGELOG.md)。

## 📚 全部技能

<a id="-全部技能"></a>

**旗舰**——上面的四个端到端工作流：[deck-studio](skills/Geek-skills-deck-studio/SKILL.md) · [deep-research](skills/Geek-skills-deep-research/SKILL.md) · [product-manager](skills/Geek-skills-product-manager/SKILL.md) · [wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)

<details>
<summary><b>核心——专业工作</b>（9 个）</summary>

| 技能 | 说明 |
|------|------|
| [`pair-programming`](skills/Geek-skills-pair-programming/SKILL.md) | 结对编程搭档，交付代码附带结构化自审，重点盯 AI 生成代码特有缺陷 |
| [`security-audit`](skills/Geek-skills-security-audit/SKILL.md) | 全面代码安全审计 |
| [`solution-architect`](skills/Geek-skills-solution-architect/SKILL.md) | 系统设计与技术选型 |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js 性能优化 |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | 面向 LLM 工作流的 PDF 解析 |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/SKILL.md) | AI 销售/咨询对话助手，把技术讲成业务语言 |
| [`keqian-method`](skills/Geek-skills-keqian-method/SKILL.md) | 克谦式 AI-Native 产品开发方法论：单 Agent、SDD、质量门禁 |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/SKILL.md) | 雪峰式 AI-Native 方法论，面向行为开放、模型驱动的产品 |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/SKILL.md) | Windows C 盘清理与空间管理（默认 dry-run） |

</details>

**实验室**——个人向与小众的 skill（备考、天气报告、图像/播客生成、A 股分析）已移入 [`lab/`](lab/)。它们**不属于精选集**、不参与上面的质量门禁，未来可能毕业进入 `skills/`，也可能移出本仓库。

<details>
<summary><b>上游同步</b>（1 个）</summary>

| 技能 | 备注 |
|------|------|
| [`llm-wiki`](llm-wiki/SKILL.md) | 保留上游原始目录结构，位于仓库根目录 |

</details>

## 🤝 社区

发现 bug，或用某个 skill 做出了东西？[提个 issue](https://github.com/staruhub/ClaudeSkills/issues)——维护约定见 [AGENTS.md](AGENTS.md)。如果某个 skill 帮你省下了一下午，点个 ⭐ 能让更多人找到它。

## License

[MIT](LICENSE)
