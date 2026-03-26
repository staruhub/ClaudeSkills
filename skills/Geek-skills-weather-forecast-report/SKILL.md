---
name: Geek-skills-weather-forecast-report
version: 1.0.0
description: |
  将天气要素（风速、能见度、降雨量等）单站预报系统的项目文档、模型、报告、评估结果整理成符合省级自然科学基金项目编写规范的专题研究报告。适用于：(1) 基于Claude Code + OpenSpec开发的气象预报系统结题报告编写，(2) 将技术文档转换为学术研究报告格式，(3) 生成符合省级自然科学基金规范的专题研究报告，(4) 整合项目代码、模型、评估指标等技术材料为规范化学术报告。触发关键词："专题研究报告"、"结题报告"、"天气预报系统"、"基金项目报告"、"风速预报"、"能见度预报"、"降雨量预报"、"气象预测"、"单站预报"等。
---

# 天气要素专题研究报告生成器

## 概述

本skill用于将Claude Code + OpenSpec开发的天气要素单站预报系统相关材料（项目文档、模型文件、评估结果等）整理成符合省级自然科学基金项目编写规范的专题研究报告。

## 工作流程

### 第一步：材料收集与分析

1. **识别输入材料类型**
   - 项目文档（README、设计文档、API文档等）
   - 模型文件（.pkl、.h5、.pt等）
   - 评估报告（准确率、RMSE、MAE等指标）
   - 代码文件（数据处理、特征工程、模型训练等）
   - 可视化图表（训练曲线、预测对比图等）

2. **确定天气要素类型**
   - 风速预报
   - 能见度预报
   - 降雨量预报
   - 温度预报
   - 湿度预报
   - 气压预报

3. **提取关键信息**
   - 研究背景与科学问题
   - 技术方案与创新点
   - 实验数据与评估指标
   - 结论与应用价值

### 第二步：报告结构规划

参照 [references/report-structure.md](references/report-structure.md) 中的详细结构说明，按省级自然科学基金规范组织报告。

### 第三步：内容撰写

1. **阅读撰写指南**：先阅读 [references/writing-guidelines.md](references/writing-guidelines.md)
2. **使用报告模板**：参考 [assets/report-template.md](assets/report-template.md)
3. **格式规范**：遵循 [references/format-standards.md](references/format-standards.md)

### 第四步：生成DOCX文档

使用docx skill生成规范的Word文档：
1. 读取 `/mnt/skills/public/docx/SKILL.md` 了解docx生成方法
2. 读取 `/mnt/skills/public/docx/docx-js.md` 了解具体API
3. 按规范格式生成最终报告

## 关键要求

### 学术规范性要求
- 一级标题：黑体四号加粗
- 二级标题：黑体小四号
- 正文：宋体小四号，首行缩进2字符
- 英文与数字：Times New Roman
- 行距：固定值26-28磅
- 序号格式：一、（一）、1、(1)、①

### 内容质量要求
- 科学性：数据准确、方法严谨、结论可靠
- 创新性：突出技术创新点和研究贡献
- 规范性：符合学术写作规范和基金报告要求
- 完整性：研究逻辑链条完整闭环

### 图表规范
- 图表需有编号和标题
- 表格标题置于表格上方
- 图片标题置于图片下方
- 图表应在正文中被引用

## 资源文件说明

| 文件 | 用途 |
|------|------|
| references/report-structure.md | 省级基金报告详细结构说明 |
| references/writing-guidelines.md | 学术写作指南与注意事项 |
| references/format-standards.md | 格式规范与排版要求 |
| references/evaluation-metrics.md | 气象预报评估指标说明 |
| assets/report-template.md | 研究报告Markdown模板 |

## 示例：风速预报专题研究报告

**输入材料**：
- wind_speed_model.py（模型代码）
- evaluation_results.json（评估结果）
- README.md（项目说明）
- training_log.txt（训练日志）

**输出报告结构**：
```
风速要素单站预报方法研究报告
├── 摘要（中英文各400字）
├── 关键词（3-5个）
├── 一、研究背景与意义
├── 二、研究目标与内容
├── 三、研究方法与技术路线
├── 四、数据来源与处理
├── 五、模型构建与训练
├── 六、实验结果与分析
├── 七、结论与展望
├── 参考文献
└── 附录
```
