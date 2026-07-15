<div align="center">

# Geek Skills

**19 个把模糊需求变成可交付成果的 Claude Code Skills。**

带引用的研究简报 · 开发能开工的 PRD · 可以上台讲的 PPT · 能直接发布的中文文章 · 可执行的工程审计

**这里没有 1000 条 Prompt。只有 19 条经过整理的完整工作流：有真实案例、有验收标准、有路由评测，也把安全边界写在明面上。**

[![CI](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![精选 Skills](https://img.shields.io/badge/精选_Skills-19-00C878)](#全部-19-个精选-skills)
[![安全矩阵](https://img.shields.io/badge/安全-能力矩阵-FF4444)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-0D1117)](#开源协议)

[English](README.md) · [简体中文](README.zh-CN.md)

[按交付物选择](#先说你要交付什么) · [30 秒安装](#30-秒开始使用) · [查看真实产出](#先看一个真实结果) · [浏览全部 Skills](#全部-19-个精选-skills)

</div>

---

## 先说你要交付什么

不用先学一套框架。找到你今天要交付的东西，直接从对应 Skill 开始。

| 我需要交付…… | 从这里开始 | 最终会得到 |
|---|---|---|
| 一份经得起追问的决策简报 | [`deep-research`](skills/Geek-skills-deep-research/SKILL.md) **v8.1.1** | 研究计划、来源台账、已核验引用、初稿、评测与运行摘要 |
| 一份开发拿到就能开工的产品文档 | [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) **v1.1.0** | PRD、验收标准、评审意见、产品策略或优先级方案 |
| 一套可以正式演示的 PPT | [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md) **v3.0.0** | 大纲、逐页 Brief、页面视觉、质量门禁与可复现的制稿流程 |
| 一篇能直接发布的中文文章 | [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | 正文、备选标题、摘要、配图方案与中文表达精修 |

这四个最适合第一次体验。仓库里还覆盖架构设计、安全审计、结对编程、金融研究、教育规划、图片生成、播客制作等场景。

## 30 秒开始使用

### 1. 克隆仓库

```bash
git clone https://github.com/staruhub/ClaudeSkills.git
cd ClaudeSkills
python3 scripts/install_skill.py --list
```

### 2. 安装你需要的 Skill

```bash
# 默认安装到 ~/.claude/skills/<name>
python3 scripts/install_skill.py deep-research

# 也可以从这几个开始
python3 scripts/install_skill.py product-manager
python3 scripts/install_skill.py deck-studio
python3 scripts/install_skill.py wechat-article-writer
```

### 3. 在 Claude Code 中直接使用

```text
/deep-research 对比三种适合 20 人律所的本地优先 RAG 架构，给出引用和决策建议。
/product-manager 把这个功能想法整理成开发可执行的 PRD，并补齐验收标准。
/deck-studio 根据这份季度复盘，制作一套 12 页的投资人更新 PPT。
/wechat-article-writer 把这份调研写成一篇有判断、可直接发布的公众号文章。
```

<details>
<summary><strong>只在当前项目安装</strong></summary>

安装到 `./.claude/skills/`，让 Skill 跟随项目：

```bash
python3 scripts/install_skill.py deep-research --project
```

</details>

<details>
<summary><strong>手动安装</strong></summary>

复制 Skill 目录，并去掉目录名前面的 `Geek-skills-`：

```bash
cp -R skills/Geek-skills-deck-studio ~/.claude/skills/deck-studio
```

安装后重启 Claude Code。

</details>

## 先看一个真实结果

### `deck-studio`：输入一份 Brief，输出一套完整 Deck

示例需求：

```text
为一家 AI Native 创业公司制作一套 9 页的设计宪法。
每一页都要有不同的视觉构图，但整套内容必须保持统一系统。
```

<table>
  <tr>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" alt="构成主义设计宪法 Deck" width="100%" />
      <br /><strong>构成主义红</strong><br />9 页设计宪法
    </td>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/preview-cover.png" alt="水墨白咨询报告 Deck" width="100%" />
      <br /><strong>水墨咨询白</strong><br />咨询报告
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/preview-cover.png" alt="黑金提案 Deck" width="100%" />
      <br /><strong>黑金提案</strong><br />项目方案
    </td>
    <td width="50%" align="center">
      <img src="skills/Geek-skills-deck-studio/examples/polar-night-ai-native/preview-cover.png" alt="极夜 AI Native 方法论 Deck" width="100%" />
      <br /><strong>极夜科技</strong><br />AI Native 方法论
    </td>
  </tr>
</table>

每个案例目录都包含生成器、渲染页面和复盘记录。可以继续查看完整的 [`deck-studio` 案例库](skills/Geek-skills-deck-studio/examples/)。

<details>
<summary><strong>这套制稿流程是怎么评测的？</strong></summary>

`deck-studio` v3 使用 22 项视觉质量门禁和 14 种已登记版式。仓库还保留了一次盲测：工作流版本得分 **42.3/50**，旧版单 Prompt 工作方式为 **29.7/50**。

这些结果来自仓库自测，其中包含模型辅助的视觉评审，不是第三方认证。完整记录与限制请查看 [`CHANGELOG`](CHANGELOG.md)。

</details>

## 为什么是 Geek Skills

| 原则 | 在这个仓库里意味着什么 |
|---|---|
| **少而精** | 19 条持续维护的工作流，比一堆来历不明、彼此重复的 Prompt 更容易理解、审查和改进。 |
| **交付物优先** | 每个 Skill 都围绕一种明确成果展开：研究报告、PRD、PPT、审计、实现方案、预测或媒体资产。 |
| **完整流程，不是一锤子买卖** | 好 Skill 会定义输入、阶段、中间产物、验证方式和停止条件，而不只是给模型套一个人设。 |
| **风险看得见** | 网络访问、本地执行、凭据使用和破坏性行为，都集中记录在仓库级能力矩阵中。 |

## 不靠口号，靠可检查的证据

- **14 个 Skills、113 条路由用例**，专门检查该触发时没触发、不该触发时误触发的问题。
- **持续集成校验**会检查元数据、路径、命名、内部链接，以及适用代码的编译结果。
- **仓库标准检查只有两条命令：**

  ```bash
  python3 scripts/validate.py
  python3 scripts/run_routing_evals.py
  ```

- **安全边界写进 [`SECURITY.md`](SECURITY.md)**：19 个精选 Skills 中有 11 个只包含提示词；唯一带删除能力的 `c-drive-cleaner` 默认只做 dry-run。
- **所有重要变化可追溯**：评测结果、已知问题和版本变化都记录在 [`CHANGELOG.md`](CHANGELOG.md)。

这些都不是第三方认证。目的只有一个：把证据摆出来，让你在授予 Skill 工作权限之前，可以自己判断它是否值得信任。

## 全部 19 个精选 Skills

### 开发与架构

| Skill | 适合解决 |
|---|---|
| [`pair-programming`](skills/Geek-skills-pair-programming/) | 有结构的结对编程、调试与代码评审 |
| [`security-audit`](skills/Geek-skills-security-audit/) | 仓库安全审计与可执行整改清单 |
| [`solution-architect`](skills/Geek-skills-solution-architect/) | 架构决策、方案权衡与落地规划 |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/) | Three.js / WebGL 性能诊断与优化 |

### AI Native 方法

| Skill | 适合解决 |
|---|---|
| [`keqian-method`](skills/Geek-skills-keqian-method/) | 系统拆解与第一性原理分析 |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/) | 结构化分析与决策支持 |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/) | AI 辅助的销售洞察、表达与转化 |

### 产品与内容

| Skill | 适合解决 |
|---|---|
| [`product-manager`](skills/Geek-skills-product-manager/) | PRD、产品评审、策略、优先级与增长诊断 |
| [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/) | 有判断、能发布的中文长文 |
| [`deck-studio`](skills/Geek-skills-deck-studio/) | 从规划、设计到评测的完整演示文稿工作流 |
| [`podcast-generator`](skills/Geek-skills-podcast-generator/) | 从研究、脚本到音频的播客制作流程 |

### 工具与数据

| Skill | 适合解决 |
|---|---|
| [`a-share-analyst`](skills/Geek-skills-a-share-analyst/) | 有证据链的 A 股公司分析 |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/) | Windows C 盘安全清理，默认仅预演 |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/) | 从复杂 PDF 中提取结构化内容 |
| [`seedream-imagegen`](skills/Geek-skills-seedream-imagegen/) | Seedream 图片提示词设计与生成流程 |

### 教育与研究

| Skill | 适合解决 |
|---|---|
| [`deep-research`](skills/Geek-skills-deep-research/) | 带来源、引用、过程资产和评测的深度研究 |
| [`gaokao-expert`](skills/Geek-skills-gaokao-expert/) | 高考规划与有依据的决策建议 |
| [`university-exam-prep`](skills/Geek-skills-university-exam-prep/) | 结构化的大学考试备考方案 |
| [`weather-forecast-report`](skills/Geek-skills-weather-forecast-report/) | 带引用、面向决策的天气预测报告 |

### 上游 Skill

[`llm-wiki`](skills/llm-wiki/) 不计入 19 个精选 Skills。它是一个独立跟踪的上游工作流，用来把一个主题整理成结构化学习页面。

## 参与贡献

好的贡献，不是让 Skill 变得更长，而是让它更值得信任。

提交 Pull Request 前，请确认：

1. Skill 聚焦于一个明确、可验证的交付目标。
2. 写清输入、工作阶段、产出、失败模式与安全边界。
3. 如果触发逻辑发生变化，同步新增或更新路由用例。
4. 运行两项仓库检查：

   ```bash
   python3 scripts/validate.py
   python3 scripts/run_routing_evals.py
   ```

发现问题，欢迎[提交 Issue](https://github.com/staruhub/ClaudeSkills/issues)；有经过验证的改进，欢迎[发起 Pull Request](https://github.com/staruhub/ClaudeSkills/pulls)。

## 如果它帮你节省了时间

请给仓库一个 Star。既方便以后找回来，也能让更多人发现：Prompt 大合集之外，还有一种更小、更透明、更容易审查的选择。

## 开源协议

MIT © ChaoGeek
