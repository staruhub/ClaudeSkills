---
name: coze-api
description: 调用扣子(Coze)智能体 API 进行对话、工作流执行等操作。当用户需要集成 Coze 智能体、调用 Coze API、或开发 Coze 相关应用时使用。支持流式和非流式对话、工作流调用等功能。
---

# Coze API 集成 Skill

扣子(Coze)是字节跳动推出的 AI 智能体开发平台,本 Skill 提供完整的 Coze API 调用指南。

## 核心功能

1. **对话 API (Chat API)** - 与智能体进行对话
2. **工作流 API (Workflow API)** - 执行工作流
3. **消息管理** - 查询对话状态和消息列表

## 快速开始

### 1. 准备工作

在使用 Coze API 前需要完成以下准备:

**获取访问令牌 (Personal Access Token)**
1. 登录 Coze 平台: https://www.coze.cn
2. 进入个人中心 → API 管理
3. 创建个人访问令牌(PAT)
4. 保存令牌(仅显示一次)

**获取 Bot ID**
1. 进入 Bot 编辑页面
2. 从 URL 中获取 Bot ID
   - 例如: `https://www.coze.cn/space/123/bot/7348293334`
   - Bot ID 为: `7348293334`

**发布 Bot 为 API 服务**
1. 在 Bot 页面点击"发布"
2. 选择"Bot as API"
3. 等待审核通过

### 2. API 基础信息

**API 基础 URL**
- 国内版: `https://api.coze.cn`
- API 版本: v3(推荐)

**认证方式**
```
Authorization: Bearer {YOUR_PAT_TOKEN}
Content-Type: application/json
```

**使用限制**
- 基础版: 每账号 100 次 API 调用(一次性)
- 专业版: 无限制,按 Token 消耗计费

## 对话 API (Chat API)

### 非流式对话

发起一次完整对话,等待完整结果后返回。

**API 端点**
```
POST https://api.coze.cn/v3/chat
```

**Python 示例代码**
```python
import requests
import json

API_URL = "https://api.coze.cn/v3/chat"
RETRIEVE_URL = "https://api.coze.cn/v3/chat/retrieve"
MESSAGE_LIST_URL = "https://api.coze.cn/v3/chat/message/list"

# 配置参数
PAT_TOKEN = "YOUR_PAT_TOKEN"
BOT_ID = "YOUR_BOT_ID"
USER_ID = "unique_user_id"

def send_message(message):
    """发起对话"""
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": message,
                "content_type": "text"
            }
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

def check_status(conversation_id, chat_id):
    """查询对话状态"""
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    params = {
        "conversation_id": conversation_id,
        "chat_id": chat_id
    }
    
    response = requests.get(RETRIEVE_URL, headers=headers, params=params)
    return response.json()

def get_messages(conversation_id, chat_id):
    """获取对话消息"""
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    params = {
        "conversation_id": conversation_id,
        "chat_id": chat_id
    }
    
    response = requests.get(MESSAGE_LIST_URL, headers=headers, params=params)
    return response.json()

# 使用示例
result = send_message("你好,请介绍一下自己")
print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 流式对话

实时接收 AI 回复,类似打字机效果。

**Python 示例代码**
```python
import requests
import json

def stream_chat(message):
    """流式对话"""
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": True,
        "auto_save_history": False,  # 流式时必须为 False
        "additional_messages": [
            {
                "role": "user",
                "content": message,
                "content_type": "text"
            }
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data, stream=True)
    
    # 处理流式响应
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            
            # 跳过非 data 行
            if not line_str.startswith('data:'):
                continue
                
            # 提取 JSON 数据
            json_str = line_str.split('data:', 1)[1].strip()
            
            try:
                data = json.loads(json_str)
                
                # 处理消息事件
                if data.get('event') == 'conversation.message.delta':
                    content = data.get('data', {}).get('content', '')
                    print(content, end='', flush=True)
                    
                # 处理完成事件
                elif data.get('event') == 'conversation.message.completed':
                    print("\n[对话完成]")
                    
            except json.JSONDecodeError:
                continue

# 使用示例
stream_chat("写一首关于春天的诗")
```

### 重要参数说明

**请求参数**
- `bot_id` (必填): Bot 的唯一标识符
- `user_id` (必填): 用户标识符,用于区分不同用户
- `stream` (必填): 是否使用流式输出
  - `true`: 流式输出,`auto_save_history` 必须为 `false`
  - `false`: 非流式输出,`auto_save_history` 必须为 `true`
- `auto_save_history`: 是否自动保存历史记录
- `additional_messages`: 消息数组
  - `role`: 角色,通常为 "user"
  - `content`: 消息内容
  - `content_type`: 内容类型,通常为 "text"
- `conversation_id` (可选): 对话 ID,用于继续之前的对话

**响应字段**
- `conversation_id`: 对话 ID
- `chat_id`: 本次对话的 ID
- `status`: 对话状态
  - `in_progress`: 处理中
  - `completed`: 已完成
  - `failed`: 失败

## 工作流 API

执行已发布的工作流。

**API 端点**
```
POST https://api.coze.cn/v3/workflows/run
```

**Python 示例代码**
```python
import requests
import json

WORKFLOW_RUN_URL = "https://api.coze.cn/v3/workflows/run"

def run_workflow(workflow_id, parameters):
    """执行工作流"""
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "workflow_id": workflow_id,
        "parameters": parameters
    }
    
    response = requests.post(WORKFLOW_RUN_URL, headers=headers, json=data)
    return response.json()

# 使用示例
workflow_id = "73xxx47"
params = {
    "input_text": "需要处理的文本",
    "option": "选项A"
}

result = run_workflow(workflow_id, params)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 完整示例: 轮询获取对话结果

非流式对话需要轮询查询状态,直到对话完成。

```python
import requests
import time
import json

def chat_with_polling(message, max_retries=30, interval=2):
    """
    发起对话并轮询获取结果
    
    Args:
        message: 用户消息
        max_retries: 最大重试次数
        interval: 轮询间隔(秒)
    """
    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 1. 发起对话
    data = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": message,
                "content_type": "text"
            }
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    if response.status_code != 200:
        print(f"发起对话失败: {result}")
        return None
    
    conversation_id = result['data']['conversation_id']
    chat_id = result['data']['id']
    
    print(f"对话已创建: conversation_id={conversation_id}, chat_id={chat_id}")
    
    # 2. 轮询查询状态
    retrieve_url = f"https://api.coze.cn/v3/chat/retrieve"
    params = {
        "conversation_id": conversation_id,
        "chat_id": chat_id
    }
    
    for i in range(max_retries):
        time.sleep(interval)
        
        status_response = requests.get(retrieve_url, headers=headers, params=params)
        status_data = status_response.json()
        
        status = status_data['data']['status']
        print(f"查询状态 [{i+1}/{max_retries}]: {status}")
        
        if status == "completed":
            # 3. 获取消息列表
            message_url = f"https://api.coze.cn/v3/chat/message/list"
            message_response = requests.get(message_url, headers=headers, params=params)
            message_data = message_response.json()
            
            # 提取 AI 回复
            messages = message_data['data']
            for msg in messages:
                if msg['role'] == 'assistant' and msg['type'] == 'answer':
                    print("\n=== AI 回复 ===")
                    print(msg['content'])
                    return msg['content']
            
        elif status == "failed":
            print("对话失败")
            return None
    
    print("轮询超时")
    return None

# 使用示例
response = chat_with_polling("介绍一下人工智能的发展历史")
```

## 错误处理

### 常见错误码

- `400` - 请求参数错误
  - 检查 `bot_id` 是否正确
  - 检查 `stream` 和 `auto_save_history` 的组合是否正确
  
- `401` - 认证失败
  - 检查 PAT Token 是否正确
  - 检查 Authorization 头格式是否正确

- `403` - 权限不足
  - 检查 Bot 是否已发布为 API 服务
  - 检查账号是否有权限访问该 Bot

- `429` - 请求频率限制
  - 基础版达到 100 次限制
  - 降低请求频率

- `500` - 服务器错误
  - 稍后重试

### 错误处理示例

```python
def safe_api_call(func, *args, **kwargs):
    """安全的 API 调用"""
    try:
        result = func(*args, **kwargs)
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None
```

## 最佳实践

### 1. 管理对话上下文

使用 `conversation_id` 维持多轮对话:

```python
def multi_turn_chat(conversation_id=None):
    """多轮对话"""
    data = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": "继续我们的对话",
                "content_type": "text"
            }
        ]
    }
    
    # 如果有 conversation_id,继续之前的对话
    if conversation_id:
        data["conversation_id"] = conversation_id
    
    # ... 发送请求
```

### 2. 选择合适的响应模式

- **非流式 (`stream=False`)**: 适合需要完整结果的场景
  - 数据分析
  - 批量处理
  - API 集成

- **流式 (`stream=True`)**: 适合交互式场景
  - 聊天应用
  - 实时反馈
  - 用户体验优先

### 3. 合理设置超时

```python
response = requests.post(
    API_URL, 
    headers=headers, 
    json=data,
    timeout=30  # 设置 30 秒超时
)
```

### 4. 使用自定义变量

在对话中传递上下文信息:

```python
data = {
    "bot_id": BOT_ID,
    "user_id": USER_ID,
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [...],
    "custom_variables": {
        "user_name": "张三",
        "company": "ABC公司",
        "department": "技术部"
    }
}
```

## 参考资料

- **官方文档**: https://www.coze.cn/open/docs/developer_guides/coze_api_overview
- **开发者平台**: https://www.coze.cn/open/playground
- **API 参考**: https://www.coze.cn/docs/developer_guides/chat_v3

## 注意事项

1. **Token 安全**: 不要在代码中硬编码 PAT Token,使用环境变量或配置文件
2. **费用管理**: 专业版按 Token 消耗计费,注意监控使用量
3. **版本更新**: API 可能更新,建议定期查看官方文档
4. **流式限制**: 流式模式下 `auto_save_history` 必须为 `false`
5. **用户标识**: 使用唯一的 `user_id` 区分不同用户,便于追踪和管理
