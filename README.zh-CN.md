[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![zh-CN](https://img.shields.io/badge/语言-简体中文-red.svg)](README.zh-CN.md)

<div align="center">

# Geek Skills

**13 个精选 Claude Code skills。每个都把活干完，交给你成品——deck、调研报告、PRD、公众号文章、安全审计。**

不是 prompt 合集。是完整的工作流，像软件一样测过。

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![skills](https://img.shields.io/badge/curated_skills-13-blue)](#-全部技能)
[![evals](https://img.shields.io/badge/routing_evals-85_cases-blue)](scripts/run_routing_evals.py)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

## 输入这一句 —

```
/deck-studio 把这份季度复盘做成一套咨询风 PPT
```

**— 拿回一整套 deck。** 这是真实跑出来的第一页，盲评 **7.1 分**（7 分 = 专业设计公司的水平线）：

<p align="center">
<img src="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/preview-cover.png" width="82%">
</p>
<p align="center"><sub>9 页全部由 skill 自己生成。没挑模板，没补妆。<a href="skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/">完整样例 →</a></sub></p>

## 你今天要交付什么？

| 你要做的事 | 用这个 | 拿到手的 |
|-----------|--------|---------|
| 认真调研一个决策 | 🔬 [`deep-research`](skills/Geek-skills-deep-research/SKILL.md)（v8.1） | 一份决策简报，每个结论带出处，能核实 |
| 写或评审 PRD | 📋 [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) | 一份开发拿了就能开工的 PRD，验收标准可核对 |
| 做汇报、路演、提案 | 🎞️ [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md)（v3） | 一套排好版的 deck，17 种风格任选，出稿过 22 条视觉门禁 |
| 发一篇公众号长文 | ✍️ [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | 一篇查过翻译腔、可以直接发的文章 |

每个都从头跑到尾，不是单条 prompt。[全部技能 ↓](#-全部技能)

## 🚀 30 秒装好

```bash
git clone https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
python3 scripts/install_skill.py deck-studio      # 装到 ~/.claude/skills/deck-studio，然后就能用 /deck-studio
```

<details>
<summary>其他装法（列出全部、装到项目里、手动装）</summary>

```bash
python3 scripts/install_skill.py --list                  # 看有哪些能装
python3 scripts/install_skill.py deep-research           # 装任何一个，用短名
python3 scripts/install_skill.py deep-research --project # 装到 ./.claude/skills/（只对当前项目生效）
```

**手动装要改名。** 装好后的**目录名**就是命令名：

```bash
cp -r skills/Geek-skills-deep-research ~/.claude/skills/deep-research
```

不改名，命令就变成 `/Geek-skills-deep-research`。另外 skill 的 `description` 和你的请求匹配时，Claude 会自动加载它——`/命令` 只是手动调用的方式。

**更新 / 卸载：**

```bash
git pull && python3 scripts/install_skill.py deck-studio --force   # 更新（装的是副本，要重装）
rm -rf ~/.claude/skills/deck-studio                                # 卸载
```

</details>

<details>
<summary>常见问题</summary>

- **装了，`/deck-studio` 不出现**——命令名来自装好后的**目录名**。手动复制没改名的话，你的命令其实是 `/Geek-skills-deck-studio`。用脚本重装，或者给目录改名。
- **skill 不自动触发**——自动加载靠 `description` 和你的话匹配，措辞有影响。打 `/命令` 永远管用。
- **`git pull` 之后要重装吗？**——要。装的是副本，重跑一遍 `python3 scripts/install_skill.py <名字> --force`。

</details>

## 📈 分数是评出来的，不是吹的

deck 的质量由盲评打分，标准是固定的：10 分 = 设计工作室，7 分 = 专业乙方。四轮发布，分数一路爬：6.0 → 6.6 → 6.6 → **7.1**，第一次过线。三个评委、对调分组再评一次，新实现 **42.3 比 29.7** 赢了旧实现，领先 42%（[方法和评分都在这 →](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/)）。

每个样例目录里，生成器、渲染出的每一页、评审挑出的毛病，全都放着——不是只挑好看的截图：
[构成主义（7.1）](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [墨白（三评委盲评）](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [英黄](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [极夜](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" width="24%">
</p>
<p align="center"><sub>17 套风格里的 4 套——包豪斯 · 构成主义 · Neubrutalism · Aicher。美是继承的，不是现生成的。</sub></p>

## 🧪 像软件一样维护

- **每个 skill 都带"三件套"**：验收标准能核对，边界写清楚（什么时候别用、该交给谁），坑全是真踩出来的。
- **85 条路由测试用例管着 10 个 skill**（`skills/*/evals/routing-evals.json`）：该出手时出手，不该管的不插手。
- **每次 push 跑 CI**——[两道 L1 门禁](.github/workflows/validate.yml)加脚本编译检查。想验证，本地跑：`python3 scripts/validate.py && python3 scripts/run_routing_evals.py`。
- **装之前先知道它能碰什么**——[SECURITY.md](SECURITY.md) 逐个列了每个 skill 会不会读文件、联网、删东西。13 个里 9 个不带任何代码；只有 1 个能删文件，默认只演习、不真删。

> ⚠️ 说清楚：质量门禁和盲评是 Claude 的**自审**，不是第三方认证。上面的命令你可以自己跑一遍验证，完整记录在 [CHANGELOG.md](CHANGELOG.md)。

## 📚 全部技能

<a id="-全部技能"></a>

**旗舰**——上面那四个：[deck-studio](skills/Geek-skills-deck-studio/SKILL.md) · [deep-research](skills/Geek-skills-deep-research/SKILL.md) · [product-manager](skills/Geek-skills-product-manager/SKILL.md) · [wechat-article-writer](skills/Geek-skills-wechat-article-writer/SKILL.md)

<details>
<summary><b>核心——专业工作</b>（9 个）</summary>

| 技能 | 干什么 |
|------|--------|
| [`pair-programming`](skills/Geek-skills-pair-programming/SKILL.md) | 写完代码自己先审一遍，专盯 AI 代码爱犯的毛病 |
| [`security-audit`](skills/Geek-skills-security-audit/SKILL.md) | 把代码安全问题一次查全 |
| [`solution-architect`](skills/Geek-skills-solution-architect/SKILL.md) | 系统设计、技术选型、架构评审 |
| [`threejs-performance`](skills/Geek-skills-threejs-performance/SKILL.md) | Three.js 性能调优 |
| [`mineru-pdf-parser`](skills/Geek-skills-mineru-pdf-parser/SKILL.md) | 把 PDF 拆成 LLM 能吃的 Markdown/JSON（需本机装 MinerU） |
| [`ai-sales-champion`](skills/Geek-skills-ai-sales-champion/SKILL.md) | 把技术话讲成客户听得懂的业务话 |
| [`keqian-method`](skills/Geek-skills-keqian-method/SKILL.md) | 克谦式 AI-Native 产品开发方法论：单 Agent、SDD、质量门禁 |
| [`xuefeng-method`](skills/Geek-skills-xuefeng-method/SKILL.md) | 雪峰式 AI-Native 方法论，做行为开放、模型驱动的产品 |
| [`c-drive-cleaner`](skills/Geek-skills-c-drive-cleaner/SKILL.md) | 清 Windows C 盘（默认只演习，不真删） |

</details>

**实验区**——个人向、小众的 skill 都在 [`lab/`](lab/)：备考、天气报告、图像和播客生成、A 股分析。不算精选，不进门禁。以后可能升上来，也可能移走。

<details>
<summary><b>上游同步</b>（1 个）</summary>

| 技能 | 说明 |
|------|------|
| [`llm-wiki`](llm-wiki/SKILL.md) | 给代码库建 wiki，源自 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)；保留上游原始目录结构 |

</details>

## 🤝 一起来

发现 bug，或者用哪个 skill 做出了东西？[提个 issue](https://github.com/staruhub/ClaudeSkills/issues)。想投稿新 skill？看 [CONTRIBUTING.md](CONTRIBUTING.md)——新 skill 先进 [`lab/`](lab/) 孵化，过了门禁就升进精选。哪个 skill 帮你省了半天活，点个 ⭐，让下一个人也找到它。

## License

[MIT](LICENSE)
