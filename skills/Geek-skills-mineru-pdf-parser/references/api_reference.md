# MinerU API Reference

## 命令行工具

### 基本用法

```bash
mineru -p <input_path> -o <output_path> [options]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --path` | 输入PDF文件或目录路径 | 必需 |
| `-o, --output` | 输出目录路径 | 必需 |
| `--backend` | 解析后端: `pipeline`, `vlm`, `hybrid` | `hybrid` |
| `--lang` | OCR语言代码 | 自动检测 |
| `--source` | 模型源: `huggingface`, `modelscope` | `huggingface` |

### 示例

```bash
# 基本解析
mineru -p document.pdf -o output/

# 使用VLM高精度模式
mineru -p paper.pdf -o output/ --backend vlm

# 指定中文OCR
mineru -p chinese_doc.pdf -o output/ --lang ch

# 批量处理目录
mineru -p ./pdfs/ -o ./output/
```

## Python API

### MinerU 类

```python
from mineru import MinerU

# 初始化
mineru = MinerU(
    backend="hybrid",    # 解析后端
    device="cuda",       # 设备: cuda/cpu/mps
    lang="auto"          # OCR语言
)

# 解析PDF
result = mineru.parse(
    path="document.pdf", # PDF路径
    start_page=0,        # 起始页（可选）
    end_page=None        # 结束页（可选）
)
```

### ParseResult 对象

```python
# 获取Markdown
markdown = result.to_markdown()

# 获取JSON
json_data = result.to_json()

# 获取章节列表
sections = result.get_sections()

# 获取表格
tables = result.get_tables()

# 获取公式
formulas = result.get_formulas()

# 获取图像
images = result.get_images()

# 保存结果
result.save(output_dir="output/")
```

### 批量处理

```python
from mineru import MinerU
from pathlib import Path

mineru = MinerU(backend="hybrid")

# 批量解析
pdf_files = list(Path("pdfs/").glob("*.pdf"))
results = mineru.batch_parse(pdf_files, workers=4)

for result in results:
    result.save(f"output/{result.filename}/")
```

## FastAPI 服务

### 启动服务

```bash
mineru-api --host 0.0.0.0 --port 8000
```

### API 端点

#### POST /parse
解析PDF文件

**请求体:**
```json
{
  "file": "base64编码的PDF内容",
  "backend": "hybrid",
  "output_format": "markdown"
}
```

**响应:**
```json
{
  "status": "success",
  "markdown": "# 文档标题\n...",
  "metadata": {
    "pages": 10,
    "tables": 3,
    "formulas": 15
  }
}
```

#### GET /health
健康检查

**响应:**
```json
{
  "status": "ok",
  "version": "2.7.0"
}
```

### 访问API文档

启动服务后访问 `http://127.0.0.1:8000/docs` 查看完整Swagger文档。

## Gradio WebUI

```bash
mineru-webui --port 7860
```

访问 `http://127.0.0.1:7860` 使用图形界面。

## 配置文件

配置文件位于 `~/.mineru.json`:

```json
{
  "device-mode": "cuda",
  "models-dir": "/path/to/models",
  "formula-delimiter": "$",
  "llm-aided-config": {
    "api_key": "your_api_key",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4",
    "enable": false
  }
}
```

## 错误处理

```python
from mineru import MinerU, MinerUError

mineru = MinerU()

try:
    result = mineru.parse("document.pdf")
except MinerUError as e:
    print(f"解析错误: {e}")
```
