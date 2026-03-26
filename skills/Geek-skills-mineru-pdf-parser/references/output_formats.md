# MinerU 输出格式说明

## 输出目录结构

```
output/
├── document.md                    # Markdown正文
├── document_content_list.json     # 结构化内容列表
├── document_middle.json           # 中间解析结果
├── document_layout.pdf            # 布局可视化（可选）
└── images/                        # 提取的图像
    ├── image_0.png
    ├── image_1.png
    └── ...
```

## Markdown 格式

### 结构示例

```markdown
# 文档标题

## 第一章 引言

这是正文内容...

### 1.1 背景

更多内容...

## 公式

行内公式：$E = mc^2$

块级公式：
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## 表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 值1 | 值2 | 值3 |

## 图像

![图像描述](images/image_0.png)
```

### 特殊元素处理

| 元素 | 输出格式 |
|------|----------|
| 标题 | `#` ~ `######` |
| 列表 | `-` 或 `1.` |
| 表格 | Markdown表格或HTML |
| 公式 | LaTeX格式 `$...$` 或 `$$...$$` |
| 图像 | `![alt](path)` |
| 代码 | `` `code` `` 或代码块 |

## JSON 格式 (content_list.json)

### 结构

```json
{
  "doc_id": "unique_id",
  "pages": [
    {
      "page_no": 0,
      "width": 612,
      "height": 792,
      "blocks": [...]
    }
  ]
}
```

### Block 类型

```json
{
  "type": "text",           // text, title, table, image, formula
  "bbox": [x0, y0, x1, y1], // 边界框
  "content": "文本内容",
  "page_no": 0,
  "block_id": 1
}
```

### 完整Block示例

#### 文本Block
```json
{
  "type": "text",
  "bbox": [72, 100, 540, 120],
  "content": "这是一段正文内容。",
  "page_no": 0,
  "block_id": 1,
  "lines": [
    {
      "spans": [
        {"text": "这是一段正文内容。", "font": "SimSun", "size": 12}
      ]
    }
  ]
}
```

#### 表格Block
```json
{
  "type": "table",
  "bbox": [72, 200, 540, 400],
  "page_no": 0,
  "block_id": 2,
  "table_html": "<table>...</table>",
  "table_body": [
    ["列1", "列2", "列3"],
    ["值1", "值2", "值3"]
  ]
}
```

#### 公式Block
```json
{
  "type": "formula",
  "bbox": [100, 300, 400, 340],
  "page_no": 0,
  "block_id": 3,
  "latex": "E = mc^2",
  "is_inline": false
}
```

#### 图像Block
```json
{
  "type": "image",
  "bbox": [72, 400, 300, 600],
  "page_no": 0,
  "block_id": 4,
  "image_path": "images/image_0.png",
  "caption": "图1：示例图像"
}
```

## 中间格式 (middle.json)

包含更详细的解析信息，用于调试：

```json
{
  "pdf_info": {
    "page_count": 10,
    "has_ocr": false,
    "language": "zh"
  },
  "layout_info": [...],
  "ocr_result": [...],
  "formula_result": [...],
  "table_result": [...]
}
```

## 布局可视化

使用 `--vis` 参数生成布局可视化PDF：

```bash
mineru -p input.pdf -o output/ --vis
```

可视化包含：
- 文本区域（蓝色）
- 标题区域（绿色）
- 表格区域（黄色）
- 图像区域（红色）
- 公式区域（紫色）

## 格式选择建议

| 用途 | 推荐格式 |
|------|----------|
| LLM输入 | Markdown |
| RAG分块 | content_list.json |
| 数据分析 | content_list.json |
| 人工阅读 | Markdown |
| 调试问题 | middle.json |
