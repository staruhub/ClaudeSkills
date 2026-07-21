# Seedream 4.0 提示词工程指南

## 提示词结构

有效的提示词应遵循以下结构:

```
[主题] + [风格] + [细节] + [质量修饰词]
```

### 示例

**基础版本**:
```
"A cat sitting on a windowsill"
```

**优化版本**:
```
"A fluffy orange tabby cat sitting on a wooden windowsill, 
golden hour lighting streaming through lace curtains, 
cozy home interior, warm color palette, soft focus background, 
professional photography, highly detailed fur texture"
```

## 关键元素

### 1. 主题描述 (必需)
明确说明图像的核心内容

**示例**:
- "A futuristic cityscape"
- "Portrait of an elderly woman"
- "Abstract geometric pattern"

### 2. 风格指定
指定艺术风格或视觉风格

**常用风格**:
- 摄影风格: professional photography, cinematic, documentary style
- 艺术风格: oil painting, watercolor, digital art, anime style, comic book style
- 设计风格: minimalist, cyberpunk, steampunk, art deco, bauhaus
- 渲染风格: photorealistic, hyperrealistic, stylized, low poly

### 3. 构图和布局
描述图像的构图方式

**构图术语**:
- centered composition, rule of thirds
- wide angle shot, close-up, bird's eye view, low angle
- foreground, middle ground, background
- symmetrical, asymmetrical

### 4. 光照和氛围
描述光线和整体氛围

**光照类型**:
- golden hour, blue hour, harsh sunlight
- soft lighting, dramatic lighting, rim lighting
- neon lights, ambient lighting, volumetric lighting

**氛围词**:
- serene, dramatic, mysterious, cheerful, melancholic
- ethereal, gritty, vibrant, muted, atmospheric

### 5. 色彩方案
指定色调和配色

**色彩描述**:
- warm colors, cool colors, monochromatic
- vibrant colors, muted tones, pastel palette
- blue and orange, complementary colors
- color grading, cinematic color

### 6. 细节和质量
提升图像质量和细节的修饰词

**质量修饰词**:
- highly detailed, intricate details, sharp focus
- 4K, ultra HD, professional quality
- fine art, masterpiece quality
- realistic textures, detailed materials

## 用例示例

### 营销海报

```
"Modern tech startup poster, clean minimalist design, 
title 'INNOVATION 2024' in bold sans-serif typography, 
geometric shapes in blue and purple gradient, 
white space for text placement, professional marketing aesthetic, 
high contrast, 4K resolution"
```

### 产品摄影

```
"Premium wireless headphones on marble surface, 
studio lighting setup with soft shadows, 
sleek black finish with metallic accents, 
luxury product photography style, clean background, 
sharp focus on product, shallow depth of field, 
commercial photography quality"
```

### 概念艺术

```
"Fantasy castle on floating island in the clouds, 
waterfalls cascading into mist below, 
magical glowing crystals, dragons flying in distance, 
epic fantasy art style, dramatic sunset lighting, 
vibrant colors, highly detailed architecture, 
concept art quality, matte painting aesthetic"
```

### 社交媒体图片

```
"Trendy cafe flat lay, artisanal coffee with latte art, 
fresh croissant and flowers, natural morning light, 
Instagram aesthetic, warm tones, soft shadows, 
lifestyle photography, cozy atmosphere, 
overhead shot, styled composition"
```

## 文本渲染技巧

Seedream 4.0 擅长在图像中渲染文本。使用以下格式:

```
"Modern poster design with title '{YOUR_TEXT}' in {FONT_STYLE}, 
{LAYOUT_DESCRIPTION}, {STYLE_DETAILS}"
```

**示例**:
```
"Minimalist concert poster with title 'JAZZ NIGHT' in elegant serif font, 
subtitle 'Friday 8PM' below, centered layout, 
black and gold color scheme, art deco inspired, 
geometric patterns in background"
```

## 多面板设计

创建网格布局或系列图像:

```
"{GRID_LAYOUT} grid poster, clean margins for typography,
title top-center: '{TITLE}', subtitle: '{SUBTITLE}',
Panel 1: {SCENE_A}, Panel 2: {SCENE_B}, Panel 3: {SCENE_C},
consistent {STYLE}, unified {COLOR_PALETTE}, {LIGHTING_STYLE}"
```

**示例**:
```
"2x2 grid poster showcasing four seasons, 
title 'SEASONS' at top center in bold sans-serif,
Panel 1: Spring cherry blossoms, Panel 2: Summer beach scene,
Panel 3: Autumn forest, Panel 4: Winter mountain,
consistent illustration style, vibrant colors,
soft lighting throughout, equal spacing between panels"
```

## 常见问题

### 提示词太长会怎样?
- 保持在 200-300 词以内
- 过长可能导致信息冲突
- 专注于最重要的元素

### 如何避免模糊的结果?
- 使用具体的描述词而非笼统的形容词
- 指定清晰的风格参考
- 添加质量修饰词

### 如何获得一致的风格?
- 使用参考图像
- 在提示词中明确指定风格元素
- 使用 sequential generation 模式

## 负面提示

虽然 Seedream 4.0 API 不直接支持负面提示,但可以通过正面描述来避免不想要的元素:

**不推荐**: "no blur, no watermark"
**推荐**: "sharp focus, clean image, professional quality"
