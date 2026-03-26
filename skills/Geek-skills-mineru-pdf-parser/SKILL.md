---
name: Geek-skills-mineru-pdf-parser
version: 1.0.0
description: PDF解析工具，将复杂PDF文档转换为LLM友好的Markdown/JSON格式。适用于：(1) 将PDF转换为Markdown或JSON格式，(2) 提取PDF中的文本、表格、公式、图像，(3) 处理学术论文、技术文档、商业报告的PDF解析，(4) 为RAG应用准备高质量文档数据，(5) 批量处理PDF文件。触发关键词包括："PDF解析"、"PDF转Markdown"、"PDF转JSON"、"提取PDF表格"、"提取PDF公式"、"MinerU"、"文档解析"、"PDF extraction"、"convert PDF"、"parse PDF"等。
---

# MinerU PDF Parser

将复杂PDF文档转换为机器可读的Markdown/JSON格式，适用于LLM和RAG应用。

## 安装

```bash
# 推荐使用uv安装
pip install uv
uv pip install -U "mineru[all]"

# 下载模型（首次使用）
mineru-models-download
```

## 快速使用

### 命令行

```bash
# 解析单个PDF
mineru -p input.pdf -o output_dir

# 批量解析
mineru -p pdf_folder/ -o output_dir

# 指定解析模式
mineru -p input.pdf -o output_dir --backend vlm      # VLM模式（高精度）
mineru -p input.pdf -o output_dir --backend pipeline # Pipeline模式（快速）
mineru -p input.pdf -o output_dir --backend hybrid   # 混合模式（平衡）
```

### Python API

```python
from mineru import MinerU

mineru = MinerU()
result = mineru.parse("document.pdf")

# 获取输出
markdown = result.to_markdown()
json_data = result.to_json()
```

详细API见 [references/api_reference.md](references/api_reference.md)

## 解析模式选择

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| `pipeline` | 快速、资源少 | 简单文档、纯文本PDF |
| `vlm` | 高精度、复杂布局 | 学术论文、公式表格文档 |
| `hybrid` | 平衡速度精度 | 通用场景 |

## 输出文件

- `{filename}.md` - Markdown正文
- `{filename}_content_list.json` - 结构化JSON
- `images/` - 提取的图像
- `{filename}_middle.json` - 中间结果（调试）

格式详情见 [references/output_formats.md](references/output_formats.md)

## 最佳实践

### 学术论文
```bash
mineru -p paper.pdf -o output --backend vlm
```

### 批量处理
```python
from mineru import MinerU
import os

mineru = MinerU(backend="hybrid")
for pdf in os.listdir("pdfs/"):
    if pdf.endswith(".pdf"):
        result = mineru.parse(f"pdfs/{pdf}")
        result.save(f"output/{pdf[:-4]}/")
```

### RAG数据准备
```python
sections = result.get_sections()
for section in sections:
    vector_db.add(section.title, section.content)
```

### 启用GPU加速
修改 `~/.mineru.json` 中 `device-mode` 为 `cuda`。

更多见 [references/best_practices.md](references/best_practices.md)

## 脚本

使用 `scripts/mineru_parse.py` 进行解析，支持错误处理和日志记录。
