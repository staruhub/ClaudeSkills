---
name: Geek-skills-seedream-imagegen
version: 1.0.0
description: Generate AI images using ByteDance's Seedream 4.0 API. Use when user wants to create, generate, or make images from text descriptions, especially for professional graphics, marketing materials, posters, product visualization, or high-quality visual content. Supports 2K/4K resolution, multiple aspect ratios, batch generation, and reference image guidance. Ideal for marketing assets, concept art, social media graphics, and design projects.
---

# Seedream 4.0 图像生成 Skill

此 Skill 提供使用 ByteDance Seedream 4.0 API 生成专业级 AI 图像的完整工作流程。

## 核心功能

- **高分辨率生成**: 支持 2K (2048x2048) 和 4K (4096x4096) 分辨率
- **灵活的纵横比**: 支持 1:1, 16:9, 9:16, 4:3, 3:2, 21:9 等多种比例
- **批量生成**: 单次请求最多生成 15 张图像
- **参考图像指导**: 支持最多 3 张参考图像来控制风格和构图
- **优秀的文本渲染**: 可在图像中生成清晰的文字内容
- **顺序批量生成**: 生成风格一致的系列图像

## 工作流程

### 1. 收集用户需求

在开始生成之前,务必询问用户以下信息:

#### 必需信息
- **图像描述**: 用户想要生成什么样的图像?
  - 询问: "请描述您想要生成的图像内容"
  - 提示: 鼓励用户提供详细描述,包括主题、风格、氛围等

#### 推荐询问的信息
- **尺寸需求**: 
  - 询问: "您需要什么尺寸的图像?(2K标准质量 或 4K高清质量)"
  - 默认: 2K
  - 说明: 2K 适合大多数用途,4K 适合打印或需要高清晰度的场景

- **纵横比**:
  - 询问: "您需要什么比例的图像?"
  - 常见选项及用途:
    - 1:1 (正方形) - 社交媒体、头像
    - 16:9 (横向宽屏) - 网页横幅、视频缩略图
    - 9:16 (竖向) - 手机壁纸、Stories
    - 4:3 (标准横向) - 演示文稿、打印
  - 默认: 1:1

- **数量**:
  - 询问: "需要生成几张图像?(1-15张)"
  - 默认: 1
  - 说明: 生成多张可以提供更多选择

### 2. 优化提示词

基于用户的描述,优化生成提示词。参考 `references/prompt_engineering.md` 获取详细指导。

**提示词优化原则**:
- 使用结构化描述: [主题] + [风格] + [细节] + [质量修饰词]
- 添加光照和氛围描述
- 包含具体的风格关键词
- 对于需要文字的图像,明确指定文字内容和字体风格

**示例转换**:

用户输入: "一只猫"

优化后的提示词:
```
"A fluffy orange tabby cat sitting on a wooden windowsill, 
golden hour lighting streaming through lace curtains, 
cozy home interior, warm color palette, soft focus background, 
professional photography, highly detailed fur texture"
```

### 3. 选择合适的参数

根据用户需求和图像类型选择参数:

#### 用途与参数对照表

| 用途 | size | aspect_ratio | max_images |
|------|------|--------------|------------|
| 社交媒体图片 | 2K | 1:1 或 9:16 | 1-3 |
| 网页横幅 | 2K | 16:9 或 21:9 | 1 |
| 打印海报 | 4K | 4:3 或自定义 | 1-2 |
| 产品图片 | 2K | 3:2 或 4:3 | 3-5 |
| 概念设计 | 2K | 16:9 | 5-10 |
| 营销素材 | 2K-4K | 根据媒介 | 3-5 |

### 4. 执行图像生成

使用 `scripts/generate_image.py` 脚本生成图像:

**命令行方式**:
```bash
python scripts/generate_image.py \
  --prompt "优化后的提示词" \
  --size 2K \
  --aspect-ratio 16:9 \
  --max-images 1 \
  --api-key YOUR_API_KEY \
  --output-dir ./outputs
```

**Python 代码方式**:
```python
from scripts.generate_image import SeedreamImageGenerator

generator = SeedreamImageGenerator(api_key="YOUR_API_KEY")

paths = generator.generate(
    prompt="优化后的提示词",
    size="2K",
    aspect_ratio="16:9",
    max_images=1,
    output_dir="./outputs"
)

print(f"生成的图像: {paths}")
```

### 5. 处理结果

- 图像将保存在指定的输出目录(默认 `./outputs`)
- 文件名格式: `seedream_YYYYMMDD_HHMMSS_提示词前缀.png`
- 如果生成多张图像,会自动添加编号后缀

### 6. 迭代优化

如果用户对结果不满意:
1. 询问具体需要调整的地方
2. 根据反馈优化提示词:
   - 添加更多细节描述
   - 调整风格关键词
   - 修改光照或氛围描述
3. 考虑调整技术参数:
   - 提高分辨率(2K → 4K)
   - 改变纵横比
   - 生成更多变体供选择

## 高级功能

### 使用参考图像

当需要特定风格或品牌一致性时:

```python
generator.generate(
    prompt="提示词",
    image_input=[
        "https://example.com/reference1.jpg",
        "https://example.com/reference2.jpg"
    ],
    size="2K",
    output_dir="./outputs"
)
```

参考图像用途:
- 指导艺术风格
- 保持品牌视觉一致性
- 提供构图参考

### 顺序批量生成

生成风格一致的系列图像:

```python
generator.generate(
    prompt="系列图像的统一描述",
    max_images=5,
    sequential=True,  # 启用顺序生成
    output_dir="./outputs"
)
```

适用场景:
- 产品系列图
- 故事板
- 品牌资产套件
- 社交媒体系列内容

### 自定义尺寸

对于特殊尺寸需求:

```python
generator.generate(
    prompt="提示词",
    size="custom",
    width=3000,
    height=2000,
    output_dir="./outputs"
)
```

## API 配置

### 设置 API 密钥

**方法 1: 环境变量** (推荐)
```bash
export SEGMIND_API_KEY="your_api_key_here"
```

**方法 2: 直接传递**
```python
generator = SeedreamImageGenerator(api_key="your_api_key_here")
```

### 获取 API 密钥

1. 访问 [Segmind](https://www.segmind.com/)
2. 注册账户
3. 在账户设置中生成 API 密钥

## 参考文档

当需要更详细的信息时,参考以下文档:

- **API 详细说明**: `references/api_reference.md`
  - API 参数完整说明
  - 请求示例
  - 错误处理
  - 性能指标

- **提示词工程**: `references/prompt_engineering.md`
  - 提示词结构指南
  - 风格关键词库
  - 用例示例
  - 最佳实践

## 常见场景快速参考

### 场景 1: 社交媒体图片
```python
generator.generate(
    prompt="优化的社交媒体内容描述",
    size="2K",
    aspect_ratio="1:1",
    max_images=3,  # 生成多个供选择
    output_dir="./outputs/social_media"
)
```

### 场景 2: 营销海报
```python
generator.generate(
    prompt="专业的营销海报描述,包含标题文字",
    size="4K",  # 高清晰度
    aspect_ratio="4:3",
    max_images=1,
    output_dir="./outputs/marketing"
)
```

### 场景 3: 产品概念图
```python
generator.generate(
    prompt="详细的产品描述和风格要求",
    size="2K",
    aspect_ratio="3:2",
    max_images=5,  # 多角度探索
    output_dir="./outputs/product_concepts"
)
```

### 场景 4: 品牌系列设计
```python
generator.generate(
    prompt="统一的品牌风格描述",
    size="2K",
    max_images=10,
    sequential=True,  # 保持一致性
    image_input=["品牌logo_url", "色卡_url"],
    output_dir="./outputs/brand_series"
)
```

## 故障排除

### 问题: API 返回 401 错误
- 检查 API 密钥是否正确设置
- 确认 API 密钥有效且有足够额度

### 问题: 生成的图像质量不理想
- 优化提示词,添加更多细节
- 尝试使用参考图像
- 提高分辨率到 4K
- 生成多张图像进行对比选择

### 问题: 生成时间过长
- 4K 图像需要更长时间(4-6秒)
- 批量生成会增加总时间
- 检查网络连接

### 问题: 图像中的文字不清晰
- 在提示词中明确指定字体风格
- 提高分辨率
- 添加 "high contrast", "bold typography" 等关键词

## 注意事项

- **API 额度**: 每次生成会消耗额度,注意监控剩余额度
- **生成时间**: 2K 约 1.8 秒,4K 约 4-6 秒
- **批量限制**: 单次请求最多 15 张图像
- **参考图限制**: 最多 3 张参考图像
- **提示词长度**: 建议 200-300 词以内

## 最佳实践

1. **始终优化提示词**: 不要直接使用用户的简短描述
2. **询问清楚需求**: 了解图像用途有助于选择正确参数
3. **提供多个选项**: 对于重要项目,生成 3-5 张供选择
4. **使用参考图像**: 需要特定风格时使用参考图像
5. **迭代优化**: 根据反馈持续改进提示词和参数
6. **保存成功案例**: 记录有效的提示词模板供后续使用
