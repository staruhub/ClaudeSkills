---
name: Geek-skills-mineru-pdf-parser
version: 1.1.0
description: 用 MinerU 将复杂PDF文档转换为LLM友好的Markdown/JSON格式。适用于：(1) PDF转Markdown/JSON，(2) 提取PDF中的文本、表格、公式、图像，(3) 解析学术论文、技术文档、商业报告，(4) 为RAG应用准备文档数据，(5) 批量处理PDF。触发关键词："PDF解析"、"PDF转Markdown"、"提取PDF表格/公式"、"MinerU"、"parse PDF"等。不用于：PDF的阅读/填表/签名/拆分合并（用宿主pdf工具）、Word/PPT等非PDF格式解析、只需读几页内容的场景（直接读即可，不必转换）。
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

## 验收标准（解析任务完成前自查）

- [ ] 输出目录里 `.md` 与 `_content_list.json` 都存在,把实际路径回报用户
- [ ] 抽查 1-2 页对照原 PDF:表格/公式没有明显丢失或错乱;有问题主动告知而不是静默交付
- [ ] backend 选择有依据(简单文本→pipeline;公式表格密集→vlm;拿不准→hybrid)
- [ ] 批量任务报告成功/失败清单,失败的给原因

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| 首次运行缺模型 | 未执行 mineru-models-download 直接解析报错 | 安装后先跑模型下载;下载体积大,提前告知用户耗时 |
| 无 GPU 硬跑 vlm | CPU 上 vlm 模式极慢,像卡死 | 无 GPU 时用 pipeline/hybrid;有 GPU 改 `~/.mineru.json` 的 device-mode 为 cuda |
| 扫描件预期过高 | 低清晰度扫描 PDF 解析质量差 | 提前告知扫描件效果取决于清晰度;结果差时换 backend 重试一次,仍差则如实报告 |
| 大文件内存压力 | 数百页 PDF 单次解析内存暴涨 | 大文件分批解析或按章节拆分 |

## 脚本

使用 `scripts/mineru_parse.py` 进行解析，支持错误处理和日志记录。
