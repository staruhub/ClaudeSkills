#!/usr/bin/env python3
"""
火山引擎播客大模型生成器
使用WebSocket协议生成双人播客音频
"""

import asyncio
import json
import struct
import uuid
import os
import sys
from typing import Optional, Dict, Any
import websockets


class PodcastGenerator:
    """播客生成器类"""
    
    def __init__(
        self,
        app_id: str,
        access_key: str,
        resource_id: str = "volc.bigmodel.podcaster",
        app_key: str = "aGjiRDfUWi"
    ):
        """
        初始化播客生成器
        
        Args:
            app_id: 火山引擎APP ID
            access_key: 火山引擎Access Token
            resource_id: 资源ID
            app_key: 固定值
        """
        self.app_id = app_id
        self.access_key = access_key
        self.resource_id = resource_id
        self.app_key = app_key
        self.url = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"
        
    def _create_header(
        self,
        protocol_version: int = 1,
        header_size: int = 1,
        message_type: int = 9,
        message_flags: int = 4,
        serialization: int = 1,
        compression: int = 0
    ) -> bytes:
        """创建协议头"""
        byte0 = (protocol_version << 4) | header_size
        byte1 = (message_type << 4) | message_flags
        byte2 = (serialization << 4) | compression
        byte3 = 0
        return struct.pack('BBBB', byte0, byte1, byte2, byte3)
    
    def _pack_message(
        self,
        event_type: int,
        session_id: str,
        payload: bytes
    ) -> bytes:
        """打包消息"""
        header = self._create_header()
        event_bytes = struct.pack('>I', event_type)
        session_id_bytes = session_id.encode('utf-8')
        session_id_len = struct.pack('>I', len(session_id_bytes))
        payload_len = struct.pack('>I', len(payload))
        
        return (header + event_bytes + session_id_len + 
                session_id_bytes + payload_len + payload)
    
    def _unpack_message(self, data: bytes) -> Dict[str, Any]:
        """解包消息"""
        if len(data) < 4:
            return {}
        
        # 解析头部
        byte0, byte1, byte2, byte3 = struct.unpack('BBBB', data[:4])
        protocol_version = (byte0 >> 4) & 0x0F
        header_size = byte0 & 0x0F
        message_type = (byte1 >> 4) & 0x0F
        message_flags = byte1 & 0x0F
        
        offset = 4
        
        # 读取event type (如果有)
        if message_flags & 0x04:
            event_type = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4
        else:
            event_type = None
        
        # 读取session_id长度和内容
        if offset + 4 <= len(data):
            session_id_len = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4
            session_id = data[offset:offset+session_id_len].decode('utf-8')
            offset += session_id_len
        else:
            session_id = ""
        
        # 读取payload长度和内容
        if offset + 4 <= len(data):
            payload_len = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4
            payload = data[offset:offset+payload_len]
        else:
            payload = b''
        
        return {
            'event_type': event_type,
            'session_id': session_id,
            'payload': payload,
            'message_type': message_type
        }
    
    async def generate_podcast(
        self,
        input_text: str,
        output_path: str,
        input_id: Optional[str] = None,
        scene: str = "deep_research",
        use_head_music: bool = False,
        audio_format: str = "mp3",
        sample_rate: int = 24000,
        speech_rate: int = 0,
        speakers: Optional[list] = None,
        retry_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        生成播客
        
        Args:
            input_text: 播客主题文本
            output_path: 输出音频文件路径
            input_id: 播客文本关联的唯一ID
            scene: 播客场景
            use_head_music: 是否使用开头音效
            audio_format: 音频格式 (mp3/ogg_opus/pcm/aac)
            sample_rate: 采样率
            speech_rate: 语速 (-50到100)
            speakers: 说话人列表
            retry_info: 断点续传信息
            
        Returns:
            生成结果信息
        """
        if input_id is None:
            input_id = str(uuid.uuid4())
        
        if speakers is None:
            speakers = [
                "zh_male_dayixiansheng_v2_saturn_bigtts",
                "zh_female_mizaitongxue_v2_saturn_bigtts"
            ]
        
        # 构建请求payload
        payload_dict = {
            "input_id": input_id,
            "input_text": input_text,
            "scene": scene,
            "action": 0,
            "use_head_music": use_head_music,
            "audio_config": {
                "format": audio_format,
                "sample_rate": sample_rate,
                "speech_rate": speech_rate
            },
            "speaker_info": {
                "random_order": True,
                "speakers": speakers
            },
            "aigc_watermark": False
        }
        
        if retry_info:
            payload_dict["retry_info"] = retry_info
        
        session_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        
        headers = {
            "X-Api-App-Id": self.app_id,
            "X-Api-Access-Key": self.access_key,
            "X-Api-Resource-Id": self.resource_id,
            "X-Api-App-Key": self.app_key,
            "X-Api-Request-Id": request_id
        }
        
        audio_buffer = bytearray()
        task_id = None
        last_round_id = 0
        round_count = 0
        
        try:
            async with websockets.connect(
                self.url,
                extra_headers=headers,
                max_size=10*1024*1024  # 10MB
            ) as websocket:
                print(f"📡 已连接到播客服务")
                
                # 发送StartSession消息
                payload_bytes = json.dumps(payload_dict).encode('utf-8')
                start_session_msg = self._pack_message(
                    event_type=1,  # StartSession
                    session_id=session_id,
                    payload=payload_bytes
                )
                
                await websocket.send(start_session_msg)
                print(f"✅ 已发送播客生成请求")
                print(f"📝 主题: {input_text[:50]}...")
                
                # 接收响应
                while True:
                    try:
                        message = await websocket.recv()
                        if isinstance(message, bytes):
                            parsed = self._unpack_message(message)
                            event_type = parsed.get('event_type')
                            payload = parsed.get('payload', b'')
                            
                            if event_type == 150:  # SessionStarted
                                data = json.loads(payload.decode('utf-8'))
                                task_id = data.get('task_id', session_id)
                                print(f"🎬 会话开始 (任务ID: {task_id})")
                                
                            elif event_type == 360:  # PodcastSpeaker
                                data = json.loads(payload.decode('utf-8'))
                                round_id = data.get('round_id', 0)
                                speaker = data.get('speaker', 'unknown')
                                round_count += 1
                                print(f"🎤 第 {round_count} 轮 - 说话人: {speaker}")
                                
                            elif event_type == 361:  # PodcastTTSResponse
                                # 音频数据
                                audio_buffer.extend(payload)
                                print(f"🔊 接收音频数据: {len(payload)} 字节")
                                
                            elif event_type == 362:  # PodcastTTSRoundEnd
                                data = json.loads(payload.decode('utf-8'))
                                last_round_id = data.get('round_id', last_round_id)
                                print(f"✅ 第 {round_count} 轮完成")
                                
                            elif event_type == 152:  # SessionFinished
                                data = json.loads(payload.decode('utf-8'))
                                print(f"🎉 播客生成完成!")
                                print(f"📊 总轮次: {round_count}")
                                break
                                
                    except websockets.exceptions.ConnectionClosed:
                        print(f"⚠️  连接断开")
                        # 如果还没完成,可以实现断点续传
                        if round_count > 0 and task_id:
                            print(f"💾 可使用断点续传: task_id={task_id}, last_round={last_round_id}")
                        break
                
                # 发送关闭连接消息
                finish_msg = self._pack_message(
                    event_type=2,  # FinishConnection
                    session_id=session_id,
                    payload=b'{}'
                )
                await websocket.send(finish_msg)
                
        except Exception as e:
            print(f"❌ 生成失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'task_id': task_id,
                'last_round_id': last_round_id
            }
        
        # 保存音频文件
        if audio_buffer:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(audio_buffer)
            
            file_size = len(audio_buffer) / (1024 * 1024)
            print(f"💾 音频已保存: {output_path}")
            print(f"📦 文件大小: {file_size:.2f} MB")
            
            return {
                'success': True,
                'output_path': output_path,
                'file_size': file_size,
                'rounds': round_count,
                'task_id': task_id
            }
        else:
            return {
                'success': False,
                'error': '未接收到音频数据',
                'task_id': task_id,
                'last_round_id': last_round_id
            }


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='火山引擎播客生成器')
    parser.add_argument('--text', required=True, help='播客主题文本')
    parser.add_argument('--output', required=True, help='输出音频文件路径')
    parser.add_argument('--app-id', required=True, help='火山引擎APP ID')
    parser.add_argument('--access-key', required=True, help='火山引擎Access Key')
    parser.add_argument('--format', default='mp3', choices=['mp3', 'ogg_opus', 'pcm', 'aac'], help='音频格式')
    parser.add_argument('--sample-rate', type=int, default=24000, help='采样率')
    parser.add_argument('--speech-rate', type=int, default=0, help='语速(-50到100)')
    parser.add_argument('--use-music', action='store_true', help='使用开头音效')
    
    args = parser.parse_args()
    
    generator = PodcastGenerator(
        app_id=args.app_id,
        access_key=args.access_key
    )
    
    result = await generator.generate_podcast(
        input_text=args.text,
        output_path=args.output,
        audio_format=args.format,
        sample_rate=args.sample_rate,
        speech_rate=args.speech_rate,
        use_head_music=args.use_music
    )
    
    if result['success']:
        print(f"\n✨ 播客生成成功!")
        print(f"📁 文件路径: {result['output_path']}")
    else:
        print(f"\n❌ 播客生成失败: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())