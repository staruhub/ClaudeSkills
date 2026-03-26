# MinerU 最佳实践

## 场景指南

### 1. 学术论文解析

学术论文包含复杂公式、表格和引用，推荐配置：

```bash
# 使用VLM后端获得最佳效果
mineru -p paper.pdf -o output/ --backend vlm
```

**要点：**
- VLM模式对LaTeX公式识别最准确
- 表格结构保持完整
- 参考文献自动识别

### 2. 技术文档解析

技术文档通常有代码块和结构化内容：

```bash
mineru -p tech_doc.pdf -o output/ --backend hybrid
```

**要点：**
- Hybrid模式平衡速度和精度
- 代码块保持格式
- 目录结构自动识别

### 3. 商业报告解析

商业报告图表多、格式复杂：

```bash
mineru -p report.pdf -o output/ --backend pipeline
```

**要点：**
- 图表提取为图像
- 表格转换为Markdown/HTML
- 页眉页脚自动去除

### 4. 扫描件OCR处理

扫描PDF需要OCR：

```bash
mineru -p scanned.pdf -o output/ --backend vlm --lang ch
```

**要点：**
- 指定OCR语言提升准确率
- VLM模式OCR效果更好
- 支持109种语言

### 5. 批量处理

大规模PDF处理：

```python
from mineru import MinerU
from concurrent.futures import ThreadPoolExecutor
import os

mineru = MinerU(backend="hybrid")

def process_pdf(pdf_path):
    try:
        result = mineru.parse(pdf_path)
        output_dir = f"output/{os.path.basename(pdf_path)[:-4]}/"
        result.save(output_dir)
        return True
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return False

pdf_files = [f"pdfs/{f}" for f in os.listdir("pdfs/") if f.endswith(".pdf")]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_pdf, pdf_files))

print(f"Processed: {sum(results)}/{len(results)}")
```

### 6. RAG应用数据准备

为向量数据库准备文档分块：

```python
from mineru import MinerU

mineru = MinerU()
result = mineru.parse("document.pdf")

# 按章节分块
sections = result.get_sections()

chunks = []
for section in sections:
    chunk = {
        "title": section.title,
        "content": section.content,
        "metadata": {
            "page": section.page_no,
            "type": section.type
        }
    }
    chunks.append(chunk)

# 存入向量数据库
for chunk in chunks:
    embedding = embed_model.encode(chunk["content"])
    vector_db.add(
        id=chunk["title"],
        vector=embedding,
        metadata=chunk["metadata"]
    )
```

## 性能优化

### GPU加速

1. 修改配置文件 `~/.mineru.json`:
```json
{
  "device-mode": "cuda"
}
```

2. 安装GPU版PaddlePaddle:
```bash
python -m pip install paddlepaddle-gpu==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

### 内存优化

处理大文件时：
```python
# 分页处理
result = mineru.parse("large.pdf", start_page=0, end_page=50)
result.save("output/part1/")

result = mineru.parse("large.pdf", start_page=50, end_page=100)
result.save("output/part2/")
```

### 并发处理

多GPU环境：
```python
# 使用Ray分布式处理
import ray
from mineru import MinerU

ray.init()

@ray.remote(num_gpus=0.5)
def parse_pdf(pdf_path):
    mineru = MinerU(backend="vlm")
    return mineru.parse(pdf_path)

results = ray.get([parse_pdf.remote(f) for f in pdf_files])
```

## 质量保证

### 输出验证

```python
def validate_output(result):
    # 检查Markdown非空
    md = result.to_markdown()
    assert len(md) > 0, "Empty markdown"
    
    # 检查页数匹配
    json_data = result.to_json()
    assert len(json_data["pages"]) > 0, "No pages found"
    
    # 检查图像提取
    images = result.get_images()
    print(f"Extracted {len(images)} images")
    
    return True
```

### 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 公式显示乱码 | LaTeX渲染问题 | 检查Markdown渲染器 |
| 表格结构错误 | 复杂表格 | 使用vlm模式 |
| OCR不准确 | 语言设置错误 | 指定--lang参数 |
| 内存溢出 | 文件过大 | 分页处理 |
| 速度太慢 | CPU模式 | 启用GPU加速 |

### 日志调试

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from mineru import MinerU
mineru = MinerU()
result = mineru.parse("document.pdf")
```

## 部署建议

### Docker部署

```dockerfile
FROM python:3.10-slim

RUN pip install uv && uv pip install "mineru[all]"
RUN mineru-models-download

EXPOSE 8000
CMD ["mineru-api", "--host", "0.0.0.0", "--port", "8000"]
```

### 服务化部署

```yaml
# docker-compose.yml
version: '3'
services:
  mineru:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/root/.cache/mineru
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 与其他工具集成

### LangChain集成

```python
from langchain.document_loaders import BaseLoader
from mineru import MinerU

class MinerULoader(BaseLoader):
    def __init__(self, file_path):
        self.file_path = file_path
        
    def load(self):
        mineru = MinerU()
        result = mineru.parse(self.file_path)
        
        from langchain.schema import Document
        return [Document(
            page_content=result.to_markdown(),
            metadata={"source": self.file_path}
        )]

# 使用
loader = MinerULoader("document.pdf")
docs = loader.load()
```

### LlamaIndex集成

```python
from llama_index import Document
from mineru import MinerU

def load_with_mineru(file_path):
    mineru = MinerU()
    result = mineru.parse(file_path)
    
    return Document(
        text=result.to_markdown(),
        metadata={"file": file_path}
    )
```
