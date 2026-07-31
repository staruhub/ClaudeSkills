# ClaudeSkills 微信群宣传素材

配图：[`claudeskills-update-wechat-20260731.png`](claudeskills-update-wechat-20260731.png)

README 横版头图：[`../claudeskills-readme-hero.png`](../claudeskills-readme-hero.png)

## 推荐群文案

把 Claude Code 从“会回答”，升级成“会按流程把活做完”。

ClaudeSkills 这次不是简单加几个 prompt，而是把 4 条核心 Skill 升级成了完整、可检查的工作流。

主要升级点：

1. **Deep Research：新增更完整的调研闭环**

   从问题拆解、研究范围、多源检索、来源登记，到引用核对、局限说明和增量续研，最终交付能复查的研究报告。

2. **Product Manager：加入 grill-me-to-doc 模式**

   Agent 会先读现有资料，每轮只追问一个关键决策，并给出推荐答案和理由；中断后可以继续，最后形成 PRODUCT-DOC，在批准前停止，不会擅自开始写代码。

3. **Deck Studio：从“做 PPT”升级为整套演示生产流程**

   先确认叙事和大纲，再生成逐页 brief、注册版式和视觉页面，最后通过真实浏览器渲染与画面检查，组装成 PPTX。

4. **WeChat Article Writer：新增四种执行模式**

   支持 `article`、`image-prompts`、`layout` 和 `full-pipeline`。可以一次交付文章、与生图平台无关的配图提示词清单，以及适合微信公众号的内联 HTML 排版；不会把提示词冒充成成图，也不会自动发布。

README 和中英文官网也全部重做了：安装后第一条命令更清楚，13 个精选 Skill 的用途、安全边界和验证结果都可以直接查看。

官网：https://staruhub.github.io/ClaudeSkills/

GitHub：https://github.com/staruhub/ClaudeSkills

开源免费。建议先看源码和安全说明，再挑一个最常用的装起来。这次不是“看起来更丰富”，而是让 Claude Code 真正能按流程把活做完。

## 一句话版本

ClaudeSkills 更新了：13 个可复用 AI 工作流，重点升级深度研究、产品文档、演示文稿和微信公众号四条主线。不是 prompt 合集，而是能查看步骤、产物和边界的 Claude Code 工作流。

## 生图记录

- 模式：Codex 内置 `imagegen`
- 用途：微信群竖版更新海报
- 成图尺寸：1086 × 1448
- SHA-256：`243A07B1BEB613D6AFD50071710CEE188C8FE333F65B0BC3D9644635EB1052D0`
- README 横版头图：1774 × 887，SHA-256 `C29B69BCABD08451F03A74FA391A7EA542C89DD6F5CE494CE9AAF2B57C84AAA8`
- 微信群竖版海报提示词：

> Use case: ads-marketing. Create a premium vertical social announcement poster for sharing in Chinese WeChat groups, celebrating a GitHub open-source repository update. Project: ClaudeSkills / Geek Skills, a curated collection of reusable Claude Code workflows. Composition: portrait 3:4, editorial tech poster, clean cream paper background, deep forest green as primary color, warm signal orange accents, subtle black typography, strong asymmetric grid. Central visual metaphor: four modular workflow cards or tracks flowing from rough user input into polished deliverables—research report, PRD document, presentation deck, and WeChat article—connected by elegant arrows and tiny code-like marks. Include a small GitHub/octocat-inspired open-source cue without copying the official logo exactly. Add restrained abstract generative geometry and paper texture; crisp, modern, credible, no glossy 3D, no generic AI robot, no neon cyberpunk. Render these Chinese strings exactly and prominently, with no other prose: headline “ClaudeSkills 全新升级”; subheadline “13 个可复用 AI 工作流”; four compact labels “深度研究” “产品文档” “演示文稿” “微信长文”; footer “github.com/staruhub/ClaudeSkills”. Make the hierarchy readable on a phone screen, generous whitespace, highly shareable, polished like an award-winning open-source launch poster.

- README 横版头图提示词：

> Recompose the same ClaudeSkills launch identity as a clean 2:1 landscape GitHub README hero. Preserve the cream paper, deep forest green, warm orange, black editorial type, four connected workflow modules, abstract geometry, and restrained open-source cue. Make it readable at repository-header size, with generous negative space and no small decorative prose. Render only these strings, exactly: “ClaudeSkills”; “让 Claude Code 按流程把活做完”; “13 个精选 Skill”; “4 条旗舰主线”; “深度研究”; “产品文档”; “演示文稿”; “微信长文”. No robot, no glossy 3D, no neon cyberpunk.
