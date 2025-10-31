# Coze API 参考文档

本文档提供 Coze API 的详细参考信息。

## API 端点总览

| 功能 | 方法 | 端点 |
|------|------|------|
| 发起对话 | POST | `/v3/chat` |
| 查询对话状态 | GET | `/v3/chat/retrieve` |
| 获取消息列表 | GET | `/v3/chat/message/list` |
| 执行工作流 | POST | `/v3/workflows/run` |

## 1. 发起对话 API

### 端点

```
POST https://api.coze.cn/v3/chat
```

### 请求头

```json
{
  "Authorization": "Bearer {YOUR_PAT_TOKEN}",
  "Content-Type": "application/json"
}
```

### 请求体

```json
{
  "bot_id": "string (必填)",
  "user_id": "string (必填)",
  "stream": "boolean (必填)",
  "auto_save_history": "boolean (必填)",
  "additional_messages": [
    {
      "role": "string (必填)",
      "content": "string (必填)",
      "content_type": "string (必填)"
    }
  ],
  "conversation_id": "string (可选)",
  "custom_variables": {
    "key": "value"
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bot_id | string | 是 | Bot 的唯一标识符 |
| user_id | string | 是 | 用户标识符 |
| stream | boolean | 是 | 是否启用流式响应 |
| auto_save_history | boolean | 是 | 是否自动保存历史(stream=true时必须为false) |
| additional_messages | array | 是 | 消息数组 |
| conversation_id | string | 否 | 对话 ID,用于继续之前的对话 |
| custom_variables | object | 否 | 自定义变量 |

### 响应 (非流式)

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "chat_id",
    "conversation_id": "conversation_id",
    "bot_id": "bot_id",
    "created_at": 1234567890,
    "completed_at": 1234567890,
    "failed_at": null,
    "meta_data": {},
    "last_error": null,
    "status": "in_progress",
    "required_action": null,
    "usage": {
      "token_count": 100,
      "output_count": 50,
      "input_count": 50
    }
  }
}
```

### 响应 (流式)

流式响应使用 Server-Sent Events (SSE) 格式:

```
data:{"event":"conversation.message.delta","data":{"content":"你"}}

data:{"event":"conversation.message.delta","data":{"content":"好"}}

data:{"event":"conversation.message.completed","data":{...}}
```

### 事件类型

| 事件 | 说明 |
|------|------|
| conversation.message.delta | 消息增量更新 |
| conversation.message.completed | 消息完成 |
| conversation.chat.completed | 对话完成 |
| conversation.chat.failed | 对话失败 |

## 2. 查询对话状态 API

### 端点

```
GET https://api.coze.cn/v3/chat/retrieve
```

### 查询参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| conversation_id | string | 是 | 对话 ID |
| chat_id | string | 是 | 聊天 ID |

### 响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "chat_id",
    "conversation_id": "conversation_id",
    "bot_id": "bot_id",
    "status": "completed",
    "created_at": 1234567890,
    "completed_at": 1234567890,
    "usage": {
      "token_count": 100,
      "output_count": 50,
      "input_count": 50
    }
  }
}
```

### 状态值

| 状态 | 说明 |
|------|------|
| in_progress | 处理中 |
| completed | 已完成 |
| failed | 失败 |
| requires_action | 需要用户操作 |

## 3. 获取消息列表 API

### 端点

```
GET https://api.coze.cn/v3/chat/message/list
```

### 查询参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| conversation_id | string | 是 | 对话 ID |
| chat_id | string | 是 | 聊天 ID |

### 响应

```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "id": "message_id",
      "conversation_id": "conversation_id",
      "bot_id": "bot_id",
      "chat_id": "chat_id",
      "role": "assistant",
      "type": "answer",
      "content": "消息内容",
      "content_type": "text",
      "created_at": 1234567890,
      "updated_at": 1234567890
    }
  ]
}
```

### 消息角色

| 角色 | 说明 |
|------|------|
| user | 用户消息 |
| assistant | 助手消息 |
| system | 系统消息 |

### 消息类型

| 类型 | 说明 |
|------|------|
| answer | 回答 |
| function_call | 函数调用 |
| tool_output | 工具输出 |
| follow_up | 追问建议 |

## 4. 执行工作流 API

### 端点

```
POST https://api.coze.cn/v3/workflows/run
```

### 请求体

```json
{
  "workflow_id": "string (必填)",
  "parameters": {
    "key": "value"
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| workflow_id | string | 是 | 工作流 ID |
| parameters | object | 是 | 工作流参数 |

### 响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "execute_id": "execute_id",
    "workflow_id": "workflow_id",
    "data": {
      "output_key": "output_value"
    }
  }
}
```

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式和内容 |
| 401 | 认证失败 | 检查 PAT Token 是否正确 |
| 403 | 权限不足 | 检查 Bot 是否已发布为 API 服务 |
| 404 | 资源不存在 | 检查 Bot ID 或工作流 ID 是否正确 |
| 429 | 请求频率限制 | 降低请求频率或升级到专业版 |
| 500 | 服务器内部错误 | 稍后重试 |

## 速率限制

### 基础版

- QPS(每秒请求数): 2
- QPM(每分钟请求数): 60
- QPD(每天请求数): 3000
- 总调用次数: 100次(一次性)

### 专业版

- 无速率限制
- 按 Token 消耗计费

## 最佳实践

### 1. 错误重试

```python
import time
from typing import Optional

def retry_api_call(func, max_retries=3, delay=1.0):
    """带重试的 API 调用"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(delay * (i + 1))
    return None
```

### 2. 超时设置

```python
import requests

response = requests.post(
    url,
    headers=headers,
    json=data,
    timeout=30  # 30秒超时
)
```

### 3. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"发送消息: {message}")
logger.info(f"收到响应: {response.status_code}")
```

### 4. 环境变量管理

```python
import os
from dotenv import load_dotenv

load_dotenv()

PAT_TOKEN = os.getenv("COZE_PAT_TOKEN")
BOT_ID = os.getenv("COZE_BOT_ID")
```

## 常见问题

### Q1: 流式和非流式如何选择?

**流式 (stream=True)**
- 优点: 实时反馈,用户体验好
- 缺点: 实现复杂,不能自动保存历史
- 适用: 聊天应用,实时交互

**非流式 (stream=False)**
- 优点: 实现简单,自动保存历史
- 缺点: 需要轮询,响应慢
- 适用: API 集成,批量处理

### Q2: 如何维持多轮对话?

使用 `conversation_id` 参数继续之前的对话:

```python
# 第一轮对话
result1 = client.chat("你好")
conv_id = result1['data']['conversation_id']

# 第二轮对话(使用相同的 conversation_id)
result2 = client.chat("继续", conversation_id=conv_id)
```

### Q3: 如何处理超长响应?

1. 使用流式响应避免超时
2. 增加轮询的最大重试次数
3. 增加超时时间
4. 在 Bot 中设置合理的最大回复长度

### Q4: 如何获取工作流 ID?

1. 进入工作流编辑页面
2. 从 URL 中获取: `https://www.coze.cn/space/xxx/bot/xxx/workflow/73xxx47`
3. 工作流 ID 为: `73xxx47`

## 相关链接

- [官方文档](https://www.coze.cn/open/docs/developer_guides/coze_api_overview)
- [开发者平台](https://www.coze.cn/open/playground)
- [Python SDK](https://github.com/coze-dev/coze-py)
