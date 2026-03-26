# Seedream 4.0 快速开始指南

## 安装依赖

```bash
pip install requests --break-system-packages
```

## 设置 API 密钥

### 获取 API 密钥
1. 访问 https://www.segmind.com/
2. 注册并登录账户
3. 在账户设置中生成 API 密钥

### 配置密钥

**环境变量方式**(推荐):
```bash
export SEGMIND_API_KEY="your_api_key_here"
```

## 基础使用

### 交互式模式

```bash
python scripts/generate_image.py
```

然后按照提示输入:
- 图像描述
- 选择尺寸(2K/4K)
- 选择纵横比
- 生成数量

### 命令行模式

**基础示例**:
```bash
python scripts/generate_image.py \
  --prompt "A serene mountain landscape at sunset" \
  --api-key YOUR_API_KEY
```

**高清图像**:
```bash
python scripts/generate_image.py \
  --prompt "Modern tech startup poster" \
  --size 4K \
  --aspect-ratio 16:9 \
  --api-key YOUR_API_KEY
```

**批量生成**:
```bash
python scripts/generate_image.py \
  --prompt "Abstract geometric art" \
  --max-images 5 \
  --api-key YOUR_API_KEY
```

## Python 集成

```python
from scripts.generate_image import SeedreamImageGenerator

# 初始化生成器
generator = SeedreamImageGenerator(api_key="your_api_key")

# 生成图像
paths = generator.generate(
    prompt="A futuristic city at night, neon lights, cyberpunk style",
    size="2K",
    aspect_ratio="16:9",
    max_images=1,
    output_dir="./outputs"
)

print(f"生成的图像路径: {paths}")
```

## 常见提示词示例

### 摄影风格
```
"Professional product photography of a smartphone, 
studio lighting, white background, commercial quality, 
8K resolution, sharp focus"
```

### 艺术风格
```
"Watercolor painting of a japanese garden, 
cherry blossoms, koi pond, soft colors, 
traditional art style, highly detailed"
```

### 营销设计
```
"Minimalist poster design for tech conference, 
title 'TECH 2025' in bold typography, 
blue gradient background, modern aesthetic, 
clean layout"
```

### 概念艺术
```
"Fantasy castle on floating island, 
dramatic clouds, epic scale, magical atmosphere, 
concept art style, cinematic lighting, 
highly detailed architecture"
```

## 下一步

- 查看 `api_reference.md` 了解完整 API 参数
- 阅读 `prompt_engineering.md` 学习提示词优化技巧
- 参考 `SKILL.md` 了解完整工作流程
