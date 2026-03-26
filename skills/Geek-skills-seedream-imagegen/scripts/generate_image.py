#!/usr/bin/env python3
"""
Seedream 4.0 图像生成脚本

这个脚本通过 Segmind API 调用 ByteDance 的 Seedream 4.0 模型生成高质量图像。
支持多种尺寸、纵横比和批量生成选项。
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path
from datetime import datetime


class SeedreamImageGenerator:
    """Seedream 4.0 图像生成器类"""
    
    def __init__(self, api_key=None):
        """
        初始化生成器
        
        Args:
            api_key: Segmind API 密钥,如果未提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv('SEGMIND_API_KEY')
        if not self.api_key:
            raise ValueError(
                "需要 API 密钥。请设置 SEGMIND_API_KEY 环境变量或通过参数传递"
            )
        
        self.api_url = "https://api.segmind.com/v1/seedream-4"
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def generate(
        self,
        prompt,
        size="2K",
        width=None,
        height=None,
        aspect_ratio="1:1",
        max_images=1,
        image_input=None,
        sequential=False,
        output_dir="./outputs"
    ):
        """
        生成图像
        
        Args:
            prompt: 图像描述文本
            size: 图像分辨率 ("2K", "4K", "custom")
            width: 自定义宽度 (size="custom" 时使用, 1024-4096)
            height: 自定义高度 (size="custom" 时使用, 1024-4096)
            aspect_ratio: 纵横比 ("1:1", "16:9", "9:16", "4:3", "3:2", "21:9" 等)
            max_images: 生成图像数量 (1-15)
            image_input: 参考图像 URL 列表 (最多3个)
            sequential: 是否启用顺序生成
            output_dir: 输出目录
        
        Returns:
            生成的图像文件路径列表
        """
        # 构建请求数据
        data = {
            "prompt": prompt,
            "size": size,
            "aspect_ratio": aspect_ratio,
            "max_images": max_images,
            "sequential_image_generation": "auto" if sequential else "disabled"
        }
        
        # 如果是自定义尺寸,添加宽高参数
        if size == "custom":
            if not width or not height:
                raise ValueError("自定义尺寸需要提供 width 和 height 参数")
            data["width"] = width
            data["height"] = height
        
        # 添加参考图像(如果有)
        if image_input:
            if not isinstance(image_input, list):
                image_input = [image_input]
            if len(image_input) > 3:
                raise ValueError("最多支持3张参考图像")
            data["image_input"] = image_input
        
        # 发送请求
        print(f"🎨 正在生成图像...")
        print(f"   提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        print(f"   尺寸: {size} ({aspect_ratio})")
        print(f"   数量: {max_images}")
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers=self.headers,
                timeout=60
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 检查剩余额度
            remaining_credits = response.headers.get('x-remaining-credits')
            if remaining_credits:
                print(f"   剩余额度: {remaining_credits}")
            
            # 保存图像
            output_paths = self._save_images(
                response.content,
                prompt,
                output_dir,
                max_images
            )
            
            print(f"✅ 成功生成 {len(output_paths)} 张图像")
            return output_paths
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ API 请求失败: {e}")
            if response.text:
                print(f"   错误详情: {response.text}")
            raise
        except Exception as e:
            print(f"❌ 生成图像时发生错误: {e}")
            raise
    
    def _save_images(self, content, prompt, output_dir, count):
        """
        保存生成的图像
        
        Args:
            content: 响应内容
            prompt: 提示词(用于文件命名)
            output_dir: 输出目录
            count: 图像数量
        
        Returns:
            保存的文件路径列表
        """
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名前缀(使用时间戳和简短的提示词)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理提示词用于文件名
        prompt_short = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' 
                               for c in prompt[:30]).strip().replace(' ', '_')
        
        saved_paths = []
        
        # 如果是单张图像
        if count == 1:
            filename = f"seedream_{timestamp}_{prompt_short}.png"
            filepath = output_path / filename
            with open(filepath, 'wb') as f:
                f.write(content)
            saved_paths.append(str(filepath))
            print(f"   💾 已保存: {filepath}")
        else:
            # 多张图像需要解析 JSON 响应
            try:
                result = json.loads(content)
                # 假设 API 返回图像 URL 列表
                if isinstance(result, list):
                    for i, img_url in enumerate(result):
                        filename = f"seedream_{timestamp}_{prompt_short}_{i+1}.png"
                        filepath = output_path / filename
                        img_response = requests.get(img_url, timeout=30)
                        with open(filepath, 'wb') as f:
                            f.write(img_response.content)
                        saved_paths.append(str(filepath))
                        print(f"   💾 已保存: {filepath}")
            except json.JSONDecodeError:
                # 如果不是 JSON,作为单个文件保存
                filename = f"seedream_{timestamp}_{prompt_short}.png"
                filepath = output_path / filename
                with open(filepath, 'wb') as f:
                    f.write(content)
                saved_paths.append(str(filepath))
                print(f"   💾 已保存: {filepath}")
        
        return saved_paths


def interactive_mode():
    """交互式图像生成模式"""
    print("=" * 60)
    print("🎨 Seedream 4.0 图像生成器 - 交互式模式")
    print("=" * 60)
    print()
    
    # 获取 API 密钥
    api_key = os.getenv('SEGMIND_API_KEY')
    if not api_key:
        api_key = input("请输入 Segmind API 密钥: ").strip()
        if not api_key:
            print("❌ 需要 API 密钥才能继续")
            return
    
    generator = SeedreamImageGenerator(api_key)
    
    # 获取提示词
    print("\n📝 请描述您想要生成的图像:")
    print("   (例如: 'A futuristic city at sunset with flying cars')")
    prompt = input("提示词: ").strip()
    if not prompt:
        print("❌ 提示词不能为空")
        return
    
    # 选择尺寸
    print("\n📐 选择图像尺寸:")
    print("   1. 2K (2048x2048) - 标准质量")
    print("   2. 4K (4096x4096) - 高清质量")
    print("   3. Custom - 自定义尺寸")
    size_choice = input("选择 (1-3) [默认: 1]: ").strip() or "1"
    
    size_map = {"1": "2K", "2": "4K", "3": "custom"}
    size = size_map.get(size_choice, "2K")
    
    width, height = None, None
    if size == "custom":
        width = int(input("宽度 (1024-4096): ").strip() or "2048")
        height = int(input("高度 (1024-4096): ").strip() or "2048")
    
    # 选择纵横比
    print("\n📏 选择纵横比:")
    print("   1. 1:1 (正方形)")
    print("   2. 16:9 (横向宽屏)")
    print("   3. 9:16 (竖向)")
    print("   4. 4:3 (标准横向)")
    print("   5. 3:2 (摄影标准)")
    aspect_choice = input("选择 (1-5) [默认: 1]: ").strip() or "1"
    
    aspect_map = {
        "1": "1:1", "2": "16:9", "3": "9:16",
        "4": "4:3", "5": "3:2"
    }
    aspect_ratio = aspect_map.get(aspect_choice, "1:1")
    
    # 生成数量
    max_images = int(input("\n🔢 生成图像数量 (1-15) [默认: 1]: ").strip() or "1")
    max_images = max(1, min(15, max_images))
    
    # 输出目录
    output_dir = input("\n📁 输出目录 [默认: ./outputs]: ").strip() or "./outputs"
    
    # 生成图像
    print()
    try:
        paths = generator.generate(
            prompt=prompt,
            size=size,
            width=width,
            height=height,
            aspect_ratio=aspect_ratio,
            max_images=max_images,
            output_dir=output_dir
        )
        print("\n" + "=" * 60)
        print("✨ 图像生成完成!")
        print("=" * 60)
        for path in paths:
            print(f"   📸 {path}")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Seedream 4.0 图像生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  python generate_image.py
  
  # 命令行模式 - 基础用法
  python generate_image.py --prompt "未来城市日落" --api-key YOUR_KEY
  
  # 高清图像
  python generate_image.py --prompt "赛博朋克街景" --size 4K --api-key YOUR_KEY
  
  # 自定义尺寸和纵横比
  python generate_image.py --prompt "山水画" --size custom --width 3000 --height 2000 --api-key YOUR_KEY
  
  # 批量生成
  python generate_image.py --prompt "抽象艺术" --max-images 5 --api-key YOUR_KEY
        """
    )
    
    parser.add_argument(
        '--prompt', '-p',
        help='图像描述提示词'
    )
    parser.add_argument(
        '--api-key', '-k',
        help='Segmind API 密钥 (或设置 SEGMIND_API_KEY 环境变量)'
    )
    parser.add_argument(
        '--size', '-s',
        choices=['2K', '4K', 'custom'],
        default='2K',
        help='图像尺寸 (默认: 2K)'
    )
    parser.add_argument(
        '--width', '-w',
        type=int,
        help='自定义宽度 (1024-4096, size=custom 时需要)'
    )
    parser.add_argument(
        '--height', '-h',
        type=int,
        help='自定义高度 (1024-4096, size=custom 时需要)'
    )
    parser.add_argument(
        '--aspect-ratio', '-a',
        choices=['1:1', '16:9', '9:16', '4:3', '3:2', '3:4', '2:3', '21:9'],
        default='1:1',
        help='纵横比 (默认: 1:1)'
    )
    parser.add_argument(
        '--max-images', '-n',
        type=int,
        default=1,
        help='生成图像数量 (1-15, 默认: 1)'
    )
    parser.add_argument(
        '--image-input', '-i',
        nargs='+',
        help='参考图像 URL (最多3个)'
    )
    parser.add_argument(
        '--sequential',
        action='store_true',
        help='启用顺序批量生成'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='./outputs',
        help='输出目录 (默认: ./outputs)'
    )
    
    args = parser.parse_args()
    
    # 如果没有提供提示词,进入交互模式
    if not args.prompt:
        interactive_mode()
        return
    
    # 命令行模式
    try:
        generator = SeedreamImageGenerator(args.api_key)
        paths = generator.generate(
            prompt=args.prompt,
            size=args.size,
            width=args.width,
            height=args.height,
            aspect_ratio=args.aspect_ratio,
            max_images=args.max_images,
            image_input=args.image_input,
            sequential=args.sequential,
            output_dir=args.output_dir
        )
        print("\n✨ 成功!")
        for path in paths:
            print(f"   📸 {path}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
