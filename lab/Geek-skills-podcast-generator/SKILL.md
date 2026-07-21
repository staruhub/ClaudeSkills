---
name: podcast-generator
version: 1.1.0
description: 用火山引擎 Podcast AI 模型生成中文双人对话播客。当用户要把文章、报告、话题文本转成播客音频、生成对话式音频内容时使用，需要环境具备火山引擎 APP_ID 和 ACCESS_KEY。支持 mp3/ogg_opus/pcm/aac、语速调节、自定义音色、断点续传。不用于：单人朗读式 TTS（用普通语音合成）、英文播客（模型主要优化中文）、播客文稿本身的撰写（先用写作类 skill 产出文本再来）。
---

# 播客生成器（火山引擎双人对话）

把中文文本变成双人对话播客音频，接口封装在 `scripts/generate_podcast.py`。

## 验收标准（每次生成完成前自查）

- [ ] 音频文件已落盘，把**实际路径与文件大小**回报用户
- [ ] 输入文本 ≤25,000 字符（超长必须先与用户确认拆分方案，不能让模型静默截断）
- [ ] 生成中断时使用了 retry_info 续传而不是从头重来
- [ ] 参数选择有依据：分发用 mp3，后期加工用 pcm；教学内容语速 -20 左右
- [ ] 凭证缺失时未硬试：告知用户去火山引擎控制台（speech/service/10028）获取

## 不做什么

- 不写播客文稿——输入文本的质量是上游任务（文稿创作找写作类 skill）
- 不做单人朗读、配音、音效制作
- 不在输出里回显用户的 ACCESS_KEY

## 工作流程

### 1. 准备输入
必需：中文文本（≤25k 字符）+ APP_ID + ACCESS_KEY（无则告知获取方式后停止）。
可选：格式（默认 mp3）/ 采样率（默认 24000）/ 语速（-50~100，0=正常，100=2 倍速）/ 音色 / 开场音乐（默认关）。

**最佳文本长度 500-3000 字**——播客时长与听感的最优区间；一篇长文建议先摘要再生成。

### 2. 生成

```bash
python scripts/generate_podcast.py \
  --text "播客话题或内容文本" \
  --output "/path/to/output.mp3" \
  --app-id "$VOLC_APP_ID" --access-key "$VOLC_ACCESS_KEY" \
  --format mp3 --sample-rate 24000 --speech-rate 0
```

脚本会流式接收音频、按轮次显示进度、落盘后返回统计（大小/轮次数）。
Python 模块调用、自定义音色 ID、断点续传 retry_info 的写法见脚本内 docstring 与 `references/api_reference.md`。

### 3. 交付
回报文件路径、大小、时长预估;失败时给出具体错误与下一步(见陷阱表)。

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 超长静默截断 | >25k 字符时模型直接截断，播客缺尾 | 生成前校验长度，超长先与用户确认拆分或摘要 |
| WebSocket 连不上 | 连接错误/超时 | 依次排查：凭证是否正确 → 网络 → 防火墙是否放行 WebSocket |
| 中断后从头重试 | 长文本生成到一半断了，重跑烧双倍额度 | 从日志取 task_id 和 last_finished_round_id，用 retry_info 续传 |
| 输出路径不可写 | 生成完成但保存失败 | 生成前检查目录存在且可写、磁盘空间充足 |
| 文本结构差出烂稿 | 口水文本生成的对话生硬 | 输入用结构清晰的中文文本；效果差时先改文本再调参数 |

## 依赖与凭证

```bash
pip install websockets
```
凭证从火山引擎控制台获取（console.volcengine.com/speech/service/10028）。建议走环境变量,不要写进代码。

## 参考文档（按需加载）

- `references/api_reference.md` — 完整参数规格、WebSocket 协议细节、事件类型、错误码;协议级调试时读
- `scripts/generate_podcast.py` — CLI 与模块双接口,含自动重试与流式接收实现
