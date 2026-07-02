---
name: seedream-imagegen
version: 1.1.0
description: 用 ByteDance Seedream 4.0 API（经 Segmind）生成 AI 图像。当用户要从文字描述生成营销素材、海报、产品图、概念图、社交媒体配图等高质量图像，且环境配有 SEGMIND_API_KEY 时使用。支持 2K/4K、多比例、单次最多 15 张批量、最多 3 张参考图控风格。不用于：修改/编辑已有图片（用图像编辑类 skill）、视频生成、无 API 环境下的快速配图需求。
---

# Seedream 4.0 图像生成

通过 `scripts/generate_image.py` 调用 Seedream 4.0 生成专业级图像。

## 验收标准（每次生成任务完成前自查）

- [ ] 提示词经过结构化优化（[主题]+[风格]+[细节]+[质量词]），不是用户原话直接透传
- [ ] size / aspect_ratio 与用途匹配（见参数对照表），不是默认值裸跑
- [ ] 图像已落盘并把**实际文件路径**回报给用户
- [ ] 重要用途（海报/品牌）生成 ≥3 张供选择
- [ ] 告知了本次消耗（张数×分辨率），4K 提前说明更耗时耗额度

## 不做什么

- 不编辑、重绘、扩展已有图片——只做文生图（参考图仅用于风格指导）
- 无 `SEGMIND_API_KEY` 时不硬试：告知用户去 segmind.com 获取，或改用环境内其他生图 skill
- 不对生成内容的版权归属下结论
- 用户只要一张随手配图时,不展开完整需求问卷,合理默认直接出

## 工作流程

### 1. 收集需求（缺什么问什么，不逐项走问卷）
必需：图像内容描述。推荐确认：尺寸（默认 2K）、比例（默认 1:1）、数量（默认 1）。

**用途 → 参数对照表**

| 用途 | size | aspect_ratio | max_images |
|------|------|--------------|------------|
| 社交媒体 | 2K | 1:1 或 9:16 | 1-3 |
| 网页横幅 | 2K | 16:9 或 21:9 | 1 |
| 打印海报 | 4K | 4:3 或自定义 | 1-2 |
| 产品图 | 2K | 3:2 或 4:3 | 3-5 |
| 概念设计 | 2K | 16:9 | 5-10 |

### 2. 优化提示词
结构：[主题] + [风格] + [细节] + [质量修饰词]，补光照与氛围；需要图内文字时明确指定文字内容与字体风格；建议 200-300 词内。
示例："一只猫" → "A fluffy orange tabby cat on a wooden windowsill, golden hour lighting, cozy interior, warm palette, professional photography, detailed fur texture"。
风格关键词库与更多范式：`references/prompt_engineering.md`。

### 3. 执行

```bash
python scripts/generate_image.py \
  --prompt "优化后的提示词" \
  --size 2K --aspect-ratio 16:9 --max-images 1 \
  --output-dir ./outputs
# API key 从环境变量 SEGMIND_API_KEY 读取，或用 --api-key 传入
```

高级用法（参考图 `image_input` ≤3 张 / 顺序批量 `sequential=True` 保持系列一致 / `size=custom` 自定义宽高）：
Python 调用示例见 `references/quick_start.md`，参数完整说明见 `references/api_reference.md`。

### 4. 迭代
不满意时先问具体不满意什么，再对症调整：细节不足→加描述；风格不对→换风格关键词或上参考图；清晰度→升 4K；选择面→加张数。

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 401 / 额度耗尽 | API 报 401 或 quota 错误 | 检查 SEGMIND_API_KEY；额度问题如实告知用户，不静默重试烧额度 |
| 内容审核拒绝 | 提示词含敏感元素被拒 | 告知被拒原因类别，改写提示词规避后重试一次；连续被拒则停下与用户确认 |
| 图内文字模糊 | 生成的海报文字发虚、错字 | 提示词明确指定文字内容+字体风格，加 "high contrast, bold typography"；升 4K；仍不行改"留位后期加字" |
| 4K 时间预期 | 用户以为卡住 | 提前说明 2K 约 2 秒、4K 约 4-6 秒，批量线性叠加 |
| 超限参数静默失败 | >15 张或 >3 参考图 | 生成前校验参数上限，超限先拆分或询问 |
| 直接透传短提示词 | "一只猫"直接发 API，出图平庸 | 验收标准第一条：必须先优化 |

## 参考文档（按需加载）

| 文件 | 何时读 |
|------|--------|
| `references/prompt_engineering.md` | 优化提示词、查风格关键词库时 |
| `references/api_reference.md` | 需要完整参数说明、错误码、性能指标时 |
| `references/quick_start.md` | 需要 Python 调用示例（参考图/批量/自定义尺寸）时 |

`evals/routing-evals.json` — 触发边界回归用例，改 description 后用仓库根 `scripts/run_routing_evals.py` 校验。
