#!/usr/bin/env python3
"""
高考题目质量分析工具
用于分析单个题目的质量，包括知识点、能力层级、情境设计等
"""

import json
import sys
from typing import Dict, List, Any


class QuestionAnalyzer:
    """题目质量分析器"""
    
    def __init__(self):
        self.quality_dimensions = {
            "知识点覆盖": 0,
            "能力层级": 0,
            "情境设计": 0,
            "难度适中": 0,
            "创新性": 0,
            "育人价值": 0,
            "科学规范": 0
        }
        
    def analyze(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析题目质量"""
        results = {
            "总体评分": 0,
            "维度评分": {},
            "优点": [],
            "问题": [],
            "改进建议": []
        }
        
        # 分析各个维度
        results["维度评分"]["知识点覆盖"] = self._analyze_knowledge(question_data)
        results["维度评分"]["能力层级"] = self._analyze_ability(question_data)
        results["维度评分"]["情境设计"] = self._analyze_context(question_data)
        results["维度评分"]["难度适中"] = self._analyze_difficulty(question_data)
        results["维度评分"]["创新性"] = self._analyze_innovation(question_data)
        results["维度评分"]["育人价值"] = self._analyze_education(question_data)
        results["维度评分"]["科学规范"] = self._analyze_norm(question_data)
        
        # 计算总体评分
        results["总体评分"] = sum(results["维度评分"].values()) / len(results["维度评分"])
        
        # 识别优点和问题
        results["优点"] = self._identify_strengths(results["维度评分"])
        results["问题"] = self._identify_issues(results["维度评分"])
        
        # 提供改进建议
        results["改进建议"] = self._provide_suggestions(results["维度评分"])
        
        return results
    
    def _analyze_knowledge(self, data: Dict) -> float:
        """分析知识点覆盖情况"""
        score = 5.0
        knowledge = data.get("knowledge_points", [])
        
        if len(knowledge) == 0:
            score -= 2.0
        elif len(knowledge) > 3:
            score += 1.0  # 综合性强
            
        # 检查是否涵盖主干知识
        if data.get("core_knowledge", False):
            score += 1.0
            
        return min(10.0, max(0.0, score))
    
    def _analyze_ability(self, data: Dict) -> float:
        """分析能力层级"""
        score = 5.0
        ability_level = data.get("ability_level", "应用")
        
        ability_scores = {
            "识记": 3.0,
            "理解": 5.0,
            "应用": 7.0,
            "分析": 8.0,
            "综合": 9.0,
            "评价": 10.0
        }
        
        score = ability_scores.get(ability_level, 5.0)
        
        # 检查是否考查多种能力
        if data.get("multiple_abilities", False):
            score = min(10.0, score + 1.0)
            
        return score
    
    def _analyze_context(self, data: Dict) -> float:
        """分析情境设计"""
        score = 5.0
        context = data.get("context", {})
        
        # 检查情境真实性
        if context.get("authentic", False):
            score += 2.0
        
        # 检查情境新颖性
        if context.get("novel", False):
            score += 1.5
        
        # 检查情境适切性
        if context.get("appropriate", False):
            score += 1.5
        
        # 检查情境教育性
        if context.get("educational", False):
            score += 1.0
            
        return min(10.0, max(0.0, score))
    
    def _analyze_difficulty(self, data: Dict) -> float:
        """分析难度适中性"""
        score = 5.0
        difficulty = data.get("difficulty", 0.5)
        
        # 难度系数在0.3-0.7为佳
        if 0.3 <= difficulty <= 0.7:
            score = 10.0
        elif 0.2 <= difficulty < 0.3 or 0.7 < difficulty <= 0.8:
            score = 7.0
        else:
            score = 4.0
            
        return score
    
    def _analyze_innovation(self, data: Dict) -> float:
        """分析创新性"""
        score = 5.0
        innovation = data.get("innovation", {})
        
        if innovation.get("new_angle", False):
            score += 2.0
        
        if innovation.get("new_format", False):
            score += 2.0
        
        if innovation.get("interdisciplinary", False):
            score += 1.0
            
        return min(10.0, max(0.0, score))
    
    def _analyze_education(self, data: Dict) -> float:
        """分析育人价值"""
        score = 5.0
        education = data.get("education", {})
        
        if education.get("values", False):
            score += 2.0
        
        if education.get("culture", False):
            score += 1.5
        
        if education.get("practical", False):
            score += 1.5
            
        return min(10.0, max(0.0, score))
    
    def _analyze_norm(self, data: Dict) -> float:
        """分析科学规范性"""
        score = 10.0
        norm = data.get("norm", {})
        
        # 发现问题扣分
        if norm.get("ambiguity", False):
            score -= 3.0
        
        if norm.get("inaccuracy", False):
            score -= 3.0
        
        if norm.get("unfairness", False):
            score -= 4.0
            
        return max(0.0, score)
    
    def _identify_strengths(self, scores: Dict[str, float]) -> List[str]:
        """识别优点"""
        strengths = []
        for dimension, score in scores.items():
            if score >= 8.0:
                strengths.append(f"{dimension}设计优秀（{score:.1f}分）")
        return strengths
    
    def _identify_issues(self, scores: Dict[str, float]) -> List[str]:
        """识别问题"""
        issues = []
        for dimension, score in scores.items():
            if score < 6.0:
                issues.append(f"{dimension}需要改进（{score:.1f}分）")
        return issues
    
    def _provide_suggestions(self, scores: Dict[str, float]) -> List[str]:
        """提供改进建议"""
        suggestions = []
        
        if scores["知识点覆盖"] < 6.0:
            suggestions.append("建议增加主干知识点的考查，提高知识覆盖的广度和深度")
        
        if scores["能力层级"] < 6.0:
            suggestions.append("建议提升考查的能力层次，从识记理解向应用分析综合评价发展")
        
        if scores["情境设计"] < 6.0:
            suggestions.append("建议选择更真实、新颖、适切的情境素材，增强情境的教育价值")
        
        if scores["难度适中"] < 6.0:
            suggestions.append("建议调整题目难度，使难度系数在0.3-0.7之间")
        
        if scores["创新性"] < 6.0:
            suggestions.append("建议从考查角度、题型形式、跨学科融合等方面增强创新性")
        
        if scores["育人价值"] < 6.0:
            suggestions.append("建议融入正确价值观、传统文化、实践应用等育人元素")
        
        if scores["科学规范"] < 8.0:
            suggestions.append("建议仔细检查题目的科学性、准确性、规范性和公平性")
            
        return suggestions
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """生成分析报告"""
        report = []
        report.append("=" * 60)
        report.append("高考题目质量分析报告")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"总体评分：{results['总体评分']:.1f}/10.0")
        report.append("")
        
        report.append("各维度评分：")
        for dimension, score in results["维度评分"].items():
            stars = "★" * int(score / 2) + "☆" * (5 - int(score / 2))
            report.append(f"  {dimension:12s}: {score:4.1f}/10.0  {stars}")
        report.append("")
        
        if results["优点"]:
            report.append("主要优点：")
            for i, strength in enumerate(results["优点"], 1):
                report.append(f"  {i}. {strength}")
            report.append("")
        
        if results["问题"]:
            report.append("存在问题：")
            for i, issue in enumerate(results["问题"], 1):
                report.append(f"  {i}. {issue}")
            report.append("")
        
        if results["改进建议"]:
            report.append("改进建议：")
            for i, suggestion in enumerate(results["改进建议"], 1):
                report.append(f"  {i}. {suggestion}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python analyze_question.py <题目JSON文件>")
        print("\n题目JSON格式示例:")
        print(json.dumps({
            "knowledge_points": ["函数", "导数", "极值"],
            "core_knowledge": True,
            "ability_level": "综合",
            "multiple_abilities": True,
            "context": {
                "authentic": True,
                "novel": True,
                "appropriate": True,
                "educational": True
            },
            "difficulty": 0.5,
            "innovation": {
                "new_angle": True,
                "new_format": False,
                "interdisciplinary": False
            },
            "education": {
                "values": True,
                "culture": False,
                "practical": True
            },
            "norm": {
                "ambiguity": False,
                "inaccuracy": False,
                "unfairness": False
            }
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # 读取题目数据
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            question_data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    
    # 创建分析器
    analyzer = QuestionAnalyzer()
    
    # 分析题目
    results = analyzer.analyze(question_data)
    
    # 生成报告
    report = analyzer.generate_report(results)
    print(report)
    
    # 保存报告
    output_file = sys.argv[1].replace('.json', '_analysis.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n分析报告已保存至: {output_file}")


if __name__ == "__main__":
    main()
