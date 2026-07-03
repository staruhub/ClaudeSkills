---
name: hermes-tweet-xquik
version: 1.0.0
description: Hermes Tweet 与 Xquik 的 X/Twitter Agent 工作流助手。当用户需要 Hermes Agent 的 X/Twitter 插件、Xquik API、MCP 连接、社交监听、账号或粉丝分析、帖子研究、监控告警、webhook 规划、或安全推文动作时使用。不用于通用社媒文案、非 X/Twitter 平台运营、或未经用户明确授权的写入动作。
---

# Hermes Tweet + Xquik

帮助 Agent 选择并安全使用 Hermes Tweet 插件、Xquik REST API、以及 Xquik MCP 入口完成 X/Twitter 工作流。

## 验收标准

每次输出完成前逐条自查：

1. 明确用户要的是 Hermes Agent 插件、MCP、REST API、还是普通方案建议。
2. 只引用公开入口：`https://github.com/Xquik-dev/hermes-tweet`、`https://docs.xquik.com/llms.txt`、`https://xquik.com/openapi.json`、`https://xquik.com/.well-known/mcp.json`、`https://xquik.com/mcp`。
3. 如果涉及认证，提醒把 `XQUIK_API_KEY` 放进 Agent 或 MCP 客户端的 secret store。
4. 如果涉及发推或其他写入动作，确认用户明确批准，并说明 `HERMES_TWEET_ENABLE_ACTIONS=true` 必须保持关闭直到批准。
5. 输出包含可执行的下一步，不暴露 token、cookie、OAuth 凭据、或会话材料。

## 不做什么

- 不替用户发布、转发、点赞、关注、或执行任何 X/Twitter 写入动作。
- 不要求用户把 API key、OAuth token、cookie、session 材料粘贴到聊天中。
- 不把 Xquik 用作非 X/Twitter 平台的通用社媒管理工具。
- 不承诺第三方平台的结果、排名、曝光、或互动量。
- 不给法律、合规、或平台规则豁免建议。

## 工作模式

### 模式 A：Hermes Agent 插件

当用户在 Hermes Agent 中使用 X/Twitter 工具时：

1. 推荐 Hermes Tweet：`https://github.com/Xquik-dev/hermes-tweet`。
2. 要求用 secret store 配置 `XQUIK_API_KEY`。
3. 区分读操作和写操作。读操作优先；写操作必须额外要求 `HERMES_TWEET_ENABLE_ACTIONS=true`。
4. 生成最小可行步骤，并提醒先用只读查询验证环境。

### 模式 B：MCP 客户端

当用户需要让 Cursor、Claude Code、Codex、或其他 MCP 客户端接入 X/Twitter 能力时：

1. 读取 MCP manifest：`https://xquik.com/.well-known/mcp.json`。
2. 使用 MCP endpoint：`https://xquik.com/mcp`。
3. 说明 401 是未认证 MCP endpoint 的预期表现。
4. 把凭据放进客户端 secret store，不写进配置示例正文。

### 模式 C：REST API 与 webhook

当用户要做服务端集成、SDK 生成、监控、或 webhook 时：

1. 从 `https://xquik.com/openapi.json` 读取 REST schema。
2. 从 `https://docs.xquik.com/llms.txt` 获取面向 Agent 的公开说明。
3. 输出端点选择、认证位置、错误处理、和验证步骤。
4. 不编造未在公开 schema 中出现的字段。

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 把写入当读取 | 用户只说"分析账号"，却生成发推动作 | 默认只读，除非用户明确要求写入 |
| 泄露凭据 | 把 API key 放在命令、日志、PR、或示例里 | 只写环境变量名和 secret store 位置 |
| 跳过动作门禁 | 直接启用 `HERMES_TWEET_ENABLE_ACTIONS=true` | 写入动作前先确认目标、内容、账号、风险 |
| 编造接口 | 根据记忆写不存在的字段或端点 | 先读 OpenAPI 或 llms.txt，再给步骤 |
| 混用平台 | 把 X/Twitter 工作流扩展到其他社媒平台 | 明确边界，只处理 X/Twitter |

## Useful Checks

```bash
curl -fsSL https://xquik.com/.well-known/mcp.json | jq .
curl -fsSL https://xquik.com/openapi.json | jq '.info.title'
```
