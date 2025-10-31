#!/usr/bin/env python3
"""
Coze API 客户端
提供完整的 Coze API 调用功能
"""

import requests
import json
import time
import os
from typing import Dict, Optional, List


class CozeClient:
    """Coze API 客户端"""
    
    def __init__(self, pat_token: str, bot_id: str, user_id: str = "default_user"):
        """
        初始化客户端
        
        Args:
            pat_token: 个人访问令牌
            bot_id: Bot ID
            user_id: 用户 ID
        """
        self.pat_token = pat_token
        self.bot_id = bot_id
        self.user_id = user_id
        self.base_url = "https://api.coze.cn"
        
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.pat_token}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        custom_variables: Optional[Dict] = None
    ) -> Dict:
        """
        发起非流式对话
        
        Args:
            message: 用户消息
            conversation_id: 对话 ID(可选)
            custom_variables: 自定义变量(可选)
            
        Returns:
            API 响应
        """
        url = f"{self.base_url}/v3/chat"
        
        data = {
            "bot_id": self.bot_id,
            "user_id": self.user_id,
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
        
        if conversation_id:
            data["conversation_id"] = conversation_id
            
        if custom_variables:
            data["custom_variables"] = custom_variables
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        return response.json()
    
    def stream_chat(
        self, 
        message: str,
        conversation_id: Optional[str] = None,
        custom_variables: Optional[Dict] = None
    ):
        """
        发起流式对话
        
        Args:
            message: 用户消息
            conversation_id: 对话 ID(可选)
            custom_variables: 自定义变量(可选)
            
        Yields:
            流式响应内容
        """
        url = f"{self.base_url}/v3/chat"
        
        data = {
            "bot_id": self.bot_id,
            "user_id": self.user_id,
            "stream": True,
            "auto_save_history": False,
            "additional_messages": [
                {
                    "role": "user",
                    "content": message,
                    "content_type": "text"
                }
            ]
        }
        
        if conversation_id:
            data["conversation_id"] = conversation_id
            
        if custom_variables:
            data["custom_variables"] = custom_variables
        
        response = requests.post(
            url, 
            headers=self._get_headers(), 
            json=data,
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                
                if not line_str.startswith('data:'):
                    continue
                    
                json_str = line_str.split('data:', 1)[1].strip()
                
                try:
                    data = json.loads(json_str)
                    
                    if data.get('event') == 'conversation.message.delta':
                        content = data.get('data', {}).get('content', '')
                        if content:
                            yield content
                            
                    elif data.get('event') == 'conversation.message.completed':
                        break
                        
                except json.JSONDecodeError:
                    continue
    
    def retrieve_chat(self, conversation_id: str, chat_id: str) -> Dict:
        """
        查询对话状态
        
        Args:
            conversation_id: 对话 ID
            chat_id: 聊天 ID
            
        Returns:
            对话状态
        """
        url = f"{self.base_url}/v3/chat/retrieve"
        params = {
            "conversation_id": conversation_id,
            "chat_id": chat_id
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def get_messages(self, conversation_id: str, chat_id: str) -> Dict:
        """
        获取对话消息列表
        
        Args:
            conversation_id: 对话 ID
            chat_id: 聊天 ID
            
        Returns:
            消息列表
        """
        url = f"{self.base_url}/v3/chat/message/list"
        params = {
            "conversation_id": conversation_id,
            "chat_id": chat_id
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def chat_with_polling(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        custom_variables: Optional[Dict] = None,
        max_retries: int = 30,
        interval: float = 2.0
    ) -> Optional[str]:
        """
        发起对话并轮询获取结果
        
        Args:
            message: 用户消息
            conversation_id: 对话 ID(可选)
            custom_variables: 自定义变量(可选)
            max_retries: 最大重试次数
            interval: 轮询间隔(秒)
            
        Returns:
            AI 回复内容
        """
        # 发起对话
        result = self.chat(message, conversation_id, custom_variables)
        
        if 'data' not in result:
            print(f"发起对话失败: {result}")
            return None
        
        conv_id = result['data']['conversation_id']
        chat_id = result['data']['id']
        
        # 轮询查询状态
        for i in range(max_retries):
            time.sleep(interval)
            
            status_data = self.retrieve_chat(conv_id, chat_id)
            status = status_data.get('data', {}).get('status', '')
            
            if status == "completed":
                # 获取消息列表
                message_data = self.get_messages(conv_id, chat_id)
                messages = message_data.get('data', [])
                
                # 提取 AI 回复
                for msg in messages:
                    if msg.get('role') == 'assistant' and msg.get('type') == 'answer':
                        return msg.get('content', '')
                        
            elif status == "failed":
                print("对话失败")
                return None
        
        print("轮询超时")
        return None
    
    def run_workflow(self, workflow_id: str, parameters: Dict) -> Dict:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流 ID
            parameters: 工作流参数
            
        Returns:
            执行结果
        """
        url = f"{self.base_url}/v3/workflows/run"
        
        data = {
            "workflow_id": workflow_id,
            "parameters": parameters
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        return response.json()


def main():
    """示例用法"""
    # 从环境变量读取配置
    pat_token = os.getenv("COZE_PAT_TOKEN", "")
    bot_id = os.getenv("COZE_BOT_ID", "")
    
    if not pat_token or not bot_id:
        print("请设置环境变量:")
        print("export COZE_PAT_TOKEN='your_token'")
        print("export COZE_BOT_ID='your_bot_id'")
        return
    
    # 创建客户端
    client = CozeClient(pat_token, bot_id)
    
    # 示例 1: 非流式对话(带轮询)
    print("=== 非流式对话 ===")
    response = client.chat_with_polling("介绍一下人工智能")
    if response:
        print(f"回复: {response}")
    
    # 示例 2: 流式对话
    print("\n=== 流式对话 ===")
    print("AI: ", end='', flush=True)
    for chunk in client.stream_chat("写一首关于春天的诗"):
        print(chunk, end='', flush=True)
    print()


if __name__ == "__main__":
    main()
