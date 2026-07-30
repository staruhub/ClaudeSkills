[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![zh-CN](https://img.shields.io/badge/语言-简体中文-red.svg)](README.zh-CN.md)

<div align="center">

# Geek Skills

**13 个精选 Claude Code skills，把真实工作变成看得见、查得清的交付物。**

先从调研、产品文档、演示文稿和中文长文四条旗舰工作流开始。安装前，你可以直接查看指令、样例、校验脚本和能力边界。

[![validate](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml/badge.svg)](https://github.com/staruhub/ClaudeSkills/actions/workflows/validate.yml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[官网](https://staruhub.github.io/ClaudeSkills/) · [30 秒安装](#-30-秒装好) · [全部 13 个 skills](#-全部技能) · [安全边界](SECURITY.md)

</div>

## 先选一条旗舰工作流

| 你要完成的工作 | 工作流 | 可以检查的交付物 |
|---------------|--------|------------------|
| 调研一个重要决策 | 🔬 [`deep-research`](skills/Geek-skills-deep-research/SKILL.md)（v8.1） | 有范围、有来源登记、有引用校验、有取舍和局限说明的简报或报告 |
| 写或评审产品文档 | 📋 [`product-manager`](skills/Geek-skills-product-manager/SKILL.md) | 结构化 PRD 或评审稿，包含决策框架和可核对的验收标准 |
| 做汇报、路演或培训 | 🎞️ [`deck-studio`](skills/Geek-skills-deck-studio/SKILL.md)（v3） | 确认后的大纲、逐页 brief、注册版式，以及带明确视觉检查表的渲染路径 |
| 写一篇中文长文 | ✍️ [`wechat-article-writer`](skills/Geek-skills-wechat-article-writer/SKILL.md) | 有标题、口吻和“去翻译腔”复核的结构化文章草稿 |

它们是可重复执行的指令包，不是一句话 prompt。最终能做到哪一步，仍取决于你的 Claude Code 会话里有哪些工具和权限。

## 🚀 30 秒装好

```bash
git clone --depth 1 https://github.com/staruhub/ClaudeSkills.git && cd ClaudeSkills
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

## 📈 看交付物，不听口号

Deck Studio 的样例目录保留了生成器、渲染页面和评审意见。在仓库记录的盲评**模型自测**中，构成主义样例按公开量表拿到 **7.1/10**；三评委、对调位置的比较中，新管线是 **42.3 比 29.7**（[方法和评分](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/)）。这些是可以复查的项目证据，不是第三方认证。

[构成主义（7.1）](skills/Geek-skills-deck-studio/examples/constructivist-design-constitution/) · [墨白（三评委盲评）](skills/Geek-skills-deck-studio/examples/moshiro-consulting-report/) · [英黄](skills/Geek-skills-deck-studio/examples/yinghuang-bootcamp-proposal/) · [极夜](skills/Geek-skills-deck-studio/examples/polar-night-ai-native/)

<p align="center">
<img src="skills/Geek-skills-deck-studio/style-library/creative/bauhaus-preview.png" alt="包豪斯 deck 风格预览" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/creative/constructivist-preview.png" alt="构成主义 deck 风格预览" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/media/neubrutalism-preview.png" alt="新粗野主义 deck 风格预览" width="24%"> <img src="skills/Geek-skills-deck-studio/style-library/business/aicher-preview.png" alt="Aicher deck 风格预览" width="24%">
</p>
<p align="center"><sub>17 套已渲染风格种子中的 4 套：包豪斯 · 构成主义 · Neubrutalism · Aicher。</sub></p>

## 🧪 这些检查到底证明了什么

| 检查 | 当前仓库里的证据 | 不能证明什么 |
|------|------------------|--------------|
| `python3 scripts/validate.py` | 对 13 个精选 skill 目录做结构化 L1 断言 | 产出质量和真实集成 |
| `python3 scripts/run_routing_evals.py` | 检查 10 个 skill、91 条路由用例定义的 schema、目标、唯一性和冲突 | 大模型实际执行时的路由准确率 |
| CI 的 Python 编译检查 | 10 个 `skills/**/*.py` 文件都能解析和编译 | 运行行为、网络访问和外部工具可用性 |
| Deck 样例目录 | 生成器、渲染页面、量表、分数和已记录缺陷 | 独立外部认证 |

你可以在本地重跑仓库和网站检查：

```bash
python3 scripts/validate.py
python3 scripts/run_routing_evals.py
python3 scripts/validate_site.py
```

安装前先看[逐 skill 能力矩阵](SECURITY.md)：它把“skill 自带脚本的风险”和“仍需 Claude Code 权限确认的动作”分开写清楚。完整重构记录见 [CHANGELOG.md](CHANGELOG.md)。

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
