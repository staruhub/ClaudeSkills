#!/usr/bin/env python3
"""
材料分析脚本
分析用户上传的课本/PPT等材料，提取可能的考点
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

@dataclass
class KeyPoint:
    """考点数据结构"""
    name: str
    priority: str  # high, medium, low
    source: str  # 来源位置
    keywords: List[str] = field(default_factory=list)
    exam_type: str = ""  # 预测题型
    notes: str = ""  # 备注

@dataclass
class MaterialAnalysis:
    """材料分析结果"""
    title: str
    material_type: str  # ppt, textbook, syllabus, notes
    total_sections: int
    key_points: List[KeyPoint] = field(default_factory=list)
    signal_words_found: Dict[str, int] = field(default_factory=dict)
    structure_summary: str = ""
    recommendations: List[str] = field(default_factory=list)

# 信号词配置
SIGNAL_WORDS = {
    "high_priority": [
        "重点", "重中之重", "必须掌握", "必背", "考试常考", 
        "历年真题", "注意", "特别注意", "关键", "核心",
        "必考", "高频", "常见题型"
    ],
    "medium_priority": [
        "区别", "比较", "异同", "原因", "意义", "影响",
        "步骤", "流程", "过程", "例如", "比如",
        "公式", "定理", "法则", "总结", "归纳"
    ],
    "structure": [
        "本章学习目标", "学习要点", "章节小结", "练习题",
        "思考题", "复习题", "应用举例", "案例分析"
    ]
}

# 题型关键词映射
EXAM_TYPE_KEYWORDS = {
    "选择题": ["判断", "下列", "哪个", "哪些", "正确的是", "错误的是"],
    "填空题": ["定义", "概念", "称为", "叫做"],
    "简答题": ["原因", "意义", "影响", "特点", "区别", "比较"],
    "计算题": ["计算", "求", "公式", "算法"],
    "应用题": ["设计", "分析", "案例", "实际", "应用"]
}

def analyze_text(text: str) -> MaterialAnalysis:
    """分析文本内容，提取考点信息"""
    
    analysis = MaterialAnalysis(
        title="材料分析",
        material_type="unknown",
        total_sections=0
    )
    
    # 识别材料类型
    if "PPT" in text or "slide" in text.lower():
        analysis.material_type = "ppt"
    elif "第一章" in text or "Chapter" in text:
        analysis.material_type = "textbook"
    elif "考试大纲" in text or "考核要求" in text:
        analysis.material_type = "syllabus"
    else:
        analysis.material_type = "notes"
    
    # 统计章节数量
    chapter_patterns = [
        r"第[一二三四五六七八九十\d]+章",
        r"Chapter\s*\d+",
        r"Unit\s*\d+"
    ]
    for pattern in chapter_patterns:
        matches = re.findall(pattern, text)
        if matches:
            analysis.total_sections = max(analysis.total_sections, len(matches))
    
    # 检测信号词
    for priority, words in SIGNAL_WORDS.items():
        for word in words:
            count = text.count(word)
            if count > 0:
                analysis.signal_words_found[word] = count
    
    # 提取可能的考点
    # 基于信号词周围的文本
    sentences = re.split(r'[。！？\n]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 5:
            continue
        
        # 检查高优先级信号词
        for word in SIGNAL_WORDS["high_priority"]:
            if word in sentence:
                key_point = KeyPoint(
                    name=sentence[:50] + "..." if len(sentence) > 50 else sentence,
                    priority="high",
                    source=f"包含关键词'{word}'",
                    keywords=[word]
                )
                # 预测题型
                for exam_type, keywords in EXAM_TYPE_KEYWORDS.items():
                    if any(kw in sentence for kw in keywords):
                        key_point.exam_type = exam_type
                        break
                
                analysis.key_points.append(key_point)
                break
        
        # 检查中优先级信号词
        for word in SIGNAL_WORDS["medium_priority"]:
            if word in sentence:
                # 避免重复添加
                if not any(kp.name == sentence[:50] for kp in analysis.key_points):
                    key_point = KeyPoint(
                        name=sentence[:50] + "..." if len(sentence) > 50 else sentence,
                        priority="medium",
                        source=f"包含关键词'{word}'",
                        keywords=[word]
                    )
                    for exam_type, keywords in EXAM_TYPE_KEYWORDS.items():
                        if any(kw in sentence for kw in keywords):
                            key_point.exam_type = exam_type
                            break
                    
                    analysis.key_points.append(key_point)
                break
    
    # 生成结构摘要
    analysis.structure_summary = generate_structure_summary(analysis)
    
    # 生成复习建议
    analysis.recommendations = generate_recommendations(analysis)
    
    return analysis

def generate_structure_summary(analysis: MaterialAnalysis) -> str:
    """生成结构摘要"""
    summary_parts = []
    
    summary_parts.append(f"材料类型：{analysis.material_type}")
    summary_parts.append(f"章节数量：{analysis.total_sections}")
    summary_parts.append(f"识别到的考点：{len(analysis.key_points)}个")
    
    high_count = sum(1 for kp in analysis.key_points if kp.priority == "high")
    medium_count = sum(1 for kp in analysis.key_points if kp.priority == "medium")
    
    summary_parts.append(f"  - 高优先级：{high_count}个")
    summary_parts.append(f"  - 中优先级：{medium_count}个")
    
    # 统计信号词
    if analysis.signal_words_found:
        top_words = sorted(analysis.signal_words_found.items(), 
                          key=lambda x: x[1], reverse=True)[:5]
        summary_parts.append(f"高频信号词：{', '.join([w for w, c in top_words])}")
    
    return "\n".join(summary_parts)

def generate_recommendations(analysis: MaterialAnalysis) -> List[str]:
    """生成复习建议"""
    recommendations = []
    
    high_priority = [kp for kp in analysis.key_points if kp.priority == "high"]
    if high_priority:
        recommendations.append(
            f"🔴 高优先级考点有{len(high_priority)}个，建议优先复习"
        )
    
    # 检查题型分布
    exam_types = Counter(kp.exam_type for kp in analysis.key_points if kp.exam_type)
    if exam_types:
        most_common = exam_types.most_common(1)[0]
        recommendations.append(
            f"📝 预测最常见题型：{most_common[0]}（出现{most_common[1]}次）"
        )
    
    # 检查信号词
    if "公式" in analysis.signal_words_found or "计算" in str(analysis.key_points):
        recommendations.append("📐 材料包含公式/计算内容，建议准备计算题练习")
    
    if "比较" in analysis.signal_words_found or "区别" in analysis.signal_words_found:
        recommendations.append("⚖️ 材料包含对比内容，建议整理对比表格")
    
    return recommendations

def output_report(analysis: MaterialAnalysis, output_format: str = "markdown") -> str:
    """生成分析报告"""
    
    if output_format == "json":
        return json.dumps(asdict(analysis), ensure_ascii=False, indent=2)
    
    # Markdown格式
    report = []
    report.append("# 📚 材料分析报告\n")
    report.append(f"## 基本信息\n")
    report.append(analysis.structure_summary)
    report.append("")
    
    # 高优先级考点
    high_points = [kp for kp in analysis.key_points if kp.priority == "high"]
    if high_points:
        report.append("\n## 🔴 高优先级考点（必考）\n")
        for i, kp in enumerate(high_points[:10], 1):  # 最多显示10个
            report.append(f"### {i}. {kp.name}")
            report.append(f"- 来源：{kp.source}")
            if kp.exam_type:
                report.append(f"- 预测题型：{kp.exam_type}")
            report.append("")
    
    # 中优先级考点
    medium_points = [kp for kp in analysis.key_points if kp.priority == "medium"]
    if medium_points:
        report.append("\n## 🟡 中优先级考点（大概率考）\n")
        for i, kp in enumerate(medium_points[:10], 1):
            report.append(f"### {i}. {kp.name}")
            report.append(f"- 来源：{kp.source}")
            if kp.exam_type:
                report.append(f"- 预测题型：{kp.exam_type}")
            report.append("")
    
    # 复习建议
    if analysis.recommendations:
        report.append("\n## 💡 复习建议\n")
        for rec in analysis.recommendations:
            report.append(f"- {rec}")
    
    return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_material.py <材料文本文件路径> [输出格式:markdown/json]")
        print("示例: python analyze_material.py material.txt markdown")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_format = sys.argv[2] if len(sys.argv) > 2 else "markdown"
    
    if not input_file.exists():
        print(f"错误：文件不存在 - {input_file}")
        sys.exit(1)
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 分析材料
    analysis = analyze_text(text)
    
    # 输出报告
    report = output_report(analysis, output_format)
    print(report)

if __name__ == "__main__":
    main()
