#!/usr/bin/env python3
"""
高考试卷结构分析工具
用于分析整份试卷的结构，包括知识分布、能力分布、难度分布等
"""

import json
import sys
from typing import Dict, List, Any
from collections import Counter


class PaperAnalyzer:
    """试卷结构分析器"""
    
    def __init__(self):
        self.knowledge_modules = []
        self.ability_levels = []
        self.difficulties = []
        self.question_types = []
        
    def analyze(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析试卷结构"""
        results = {
            "基本信息": {},
            "知识分布": {},
            "能力分布": {},
            "难度分布": {},
            "题型分布": {},
            "时间分配": {},
            "结构评价": {},
            "改进建议": []
        }
        
        questions = paper_data.get("questions", [])
        total_score = paper_data.get("total_score", 150)
        time_limit = paper_data.get("time_limit", 150)
        
        # 基本信息
        results["基本信息"] = {
            "题目总数": len(questions),
            "总分": total_score,
            "考试时间": f"{time_limit}分钟",
            "平均每题分值": f"{total_score/len(questions):.1f}分" if questions else "0分",
            "平均每题时间": f"{time_limit/len(questions):.1f}分钟" if questions else "0分钟"
        }
        
        # 分析知识分布
        results["知识分布"] = self._analyze_knowledge_distribution(questions)
        
        # 分析能力分布
        results["能力分布"] = self._analyze_ability_distribution(questions)
        
        # 分析难度分布
        results["难度分布"] = self._analyze_difficulty_distribution(questions)
        
        # 分析题型分布
        results["题型分布"] = self._analyze_question_type_distribution(questions)
        
        # 分析时间分配
        results["时间分配"] = self._analyze_time_allocation(questions, time_limit)
        
        # 结构评价
        results["结构评价"] = self._evaluate_structure(results)
        
        # 改进建议
        results["改进建议"] = self._provide_suggestions(results)
        
        return results
    
    def _analyze_knowledge_distribution(self, questions: List[Dict]) -> Dict:
        """分析知识分布"""
        knowledge_dist = {}
        total_score = sum(q.get("score", 0) for q in questions)
        
        for question in questions:
            for knowledge in question.get("knowledge_points", []):
                score = question.get("score", 0)
                if knowledge in knowledge_dist:
                    knowledge_dist[knowledge] += score
                else:
                    knowledge_dist[knowledge] = score
        
        # 计算百分比
        knowledge_percent = {
            k: {"分值": v, "占比": f"{v/total_score*100:.1f}%"} 
            for k, v in knowledge_dist.items()
        }
        
        return knowledge_percent
    
    def _analyze_ability_distribution(self, questions: List[Dict]) -> Dict:
        """分析能力分布"""
        ability_dist = Counter()
        total_score = sum(q.get("score", 0) for q in questions)
        
        for question in questions:
            ability = question.get("ability_level", "应用")
            score = question.get("score", 0)
            ability_dist[ability] += score
        
        # 按能力层级排序
        ability_order = ["识记", "理解", "应用", "分析", "综合", "评价"]
        ability_percent = {}
        
        for ability in ability_order:
            if ability in ability_dist:
                score = ability_dist[ability]
                ability_percent[ability] = {
                    "分值": score,
                    "占比": f"{score/total_score*100:.1f}%"
                }
        
        return ability_percent
    
    def _analyze_difficulty_distribution(self, questions: List[Dict]) -> Dict:
        """分析难度分布"""
        difficulty_ranges = {
            "容易题(0.7-1.0)": 0,
            "中等题(0.4-0.7)": 0,
            "较难题(0.2-0.4)": 0,
            "难题(0.0-0.2)": 0
        }
        
        total_score = sum(q.get("score", 0) for q in questions)
        
        for question in questions:
            difficulty = question.get("difficulty", 0.5)
            score = question.get("score", 0)
            
            if difficulty >= 0.7:
                difficulty_ranges["容易题(0.7-1.0)"] += score
            elif difficulty >= 0.4:
                difficulty_ranges["中等题(0.4-0.7)"] += score
            elif difficulty >= 0.2:
                difficulty_ranges["较难题(0.2-0.4)"] += score
            else:
                difficulty_ranges["难题(0.0-0.2)"] += score
        
        # 计算百分比
        difficulty_percent = {
            k: {"分值": v, "占比": f"{v/total_score*100:.1f}%", "建议占比": suggest}
            for k, v, suggest in [
                ("容易题(0.7-1.0)", difficulty_ranges["容易题(0.7-1.0)"], "30%"),
                ("中等题(0.4-0.7)", difficulty_ranges["中等题(0.4-0.7)"], "50%"),
                ("较难题(0.2-0.4)", difficulty_ranges["较难题(0.2-0.4)"], "15%"),
                ("难题(0.0-0.2)", difficulty_ranges["难题(0.0-0.2)"], "5%")
            ]
        }
        
        # 计算平均难度
        avg_difficulty = sum(
            q.get("difficulty", 0.5) * q.get("score", 0) 
            for q in questions
        ) / total_score if total_score > 0 else 0
        
        difficulty_percent["平均难度系数"] = f"{avg_difficulty:.2f}"
        
        return difficulty_percent
    
    def _analyze_question_type_distribution(self, questions: List[Dict]) -> Dict:
        """分析题型分布"""
        type_dist = Counter()
        total_score = sum(q.get("score", 0) for q in questions)
        
        for question in questions:
            qtype = question.get("type", "未知")
            score = question.get("score", 0)
            type_dist[qtype] += score
        
        # 计算百分比
        type_percent = {
            k: {
                "分值": v,
                "占比": f"{v/total_score*100:.1f}%",
                "题量": sum(1 for q in questions if q.get("type") == k)
            }
            for k, v in type_dist.items()
        }
        
        return type_percent
    
    def _analyze_time_allocation(self, questions: List[Dict], time_limit: int) -> Dict:
        """分析时间分配"""
        time_allocation = {}
        total_score = sum(q.get("score", 0) for q in questions)
        
        for qtype in set(q.get("type", "未知") for q in questions):
            type_questions = [q for q in questions if q.get("type") == qtype]
            type_score = sum(q.get("score", 0) for q in type_questions)
            type_count = len(type_questions)
            
            # 按分值比例分配时间
            allocated_time = (type_score / total_score) * time_limit
            avg_time_per_question = allocated_time / type_count if type_count > 0 else 0
            
            time_allocation[qtype] = {
                "总时间": f"{allocated_time:.1f}分钟",
                "题量": type_count,
                "平均每题": f"{avg_time_per_question:.1f}分钟"
            }
        
        return time_allocation
    
    def _evaluate_structure(self, results: Dict) -> Dict:
        """评价试卷结构"""
        evaluation = {
            "总体评价": "良好",
            "评分": 0.0,
            "优点": [],
            "问题": []
        }
        
        score = 100.0
        
        # 评价难度分布
        difficulty = results["难度分布"]
        easy_percent = float(difficulty.get("容易题(0.7-1.0)", {}).get("占比", "0%").rstrip("%"))
        medium_percent = float(difficulty.get("中等题(0.4-0.7)", {}).get("占比", "0%").rstrip("%"))
        hard_percent = float(difficulty.get("较难题(0.2-0.4)", {}).get("占比", "0%").rstrip("%"))
        
        # 检查难度分布是否合理
        if 25 <= easy_percent <= 35:
            evaluation["优点"].append("容易题比例合理")
        else:
            evaluation["问题"].append(f"容易题比例{easy_percent:.1f}%，建议在25%-35%之间")
            score -= 10
        
        if 45 <= medium_percent <= 55:
            evaluation["优点"].append("中等题比例合理")
        else:
            evaluation["问题"].append(f"中等题比例{medium_percent:.1f}%，建议在45%-55%之间")
            score -= 10
        
        if 15 <= hard_percent <= 25:
            evaluation["优点"].append("难题比例合理")
        else:
            evaluation["问题"].append(f"难题比例{hard_percent:.1f}%，建议在15%-25%之间")
            score -= 10
        
        # 评价能力分布
        ability = results["能力分布"]
        high_ability = sum(
            float(ability.get(level, {}).get("占比", "0%").rstrip("%"))
            for level in ["分析", "综合", "评价"]
        )
        
        if high_ability >= 40:
            evaluation["优点"].append("高阶思维能力考查充分")
        else:
            evaluation["问题"].append(f"高阶思维能力考查比例{high_ability:.1f}%，建议至少40%")
            score -= 15
        
        # 评价知识覆盖
        knowledge = results["知识分布"]
        if len(knowledge) >= 5:
            evaluation["优点"].append("知识点覆盖面广")
        else:
            evaluation["问题"].append("知识点覆盖不够全面")
            score -= 10
        
        evaluation["评分"] = max(0, score)
        
        if score >= 90:
            evaluation["总体评价"] = "优秀"
        elif score >= 75:
            evaluation["总体评价"] = "良好"
        elif score >= 60:
            evaluation["总体评价"] = "合格"
        else:
            evaluation["总体评价"] = "需改进"
        
        return evaluation
    
    def _provide_suggestions(self, results: Dict) -> List[str]:
        """提供改进建议"""
        suggestions = []
        evaluation = results["结构评价"]
        
        for problem in evaluation["问题"]:
            if "容易题" in problem:
                suggestions.append("建议调整容易题比例，适当增加或减少基础题目")
            elif "中等题" in problem:
                suggestions.append("建议调整中等题比例，确保大部分学生能够完成")
            elif "难题" in problem:
                suggestions.append("建议调整难题比例，保证有效的区分度")
            elif "高阶思维" in problem:
                suggestions.append("建议增加分析、综合、评价类题目，提升能力考查层次")
            elif "知识点" in problem:
                suggestions.append("建议扩大知识点覆盖范围，全面考查学科内容")
        
        # 通用建议
        if not suggestions:
            suggestions.append("试卷结构合理，继续保持")
        
        suggestions.append("建议根据实际施测数据进一步优化试卷结构")
        
        return suggestions
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """生成分析报告"""
        report = []
        report.append("=" * 70)
        report.append("高考试卷结构分析报告")
        report.append("=" * 70)
        report.append("")
        
        # 基本信息
        report.append("一、基本信息")
        report.append("-" * 70)
        for key, value in results["基本信息"].items():
            report.append(f"  {key:12s}: {value}")
        report.append("")
        
        # 知识分布
        report.append("二、知识分布")
        report.append("-" * 70)
        for knowledge, data in results["知识分布"].items():
            report.append(f"  {knowledge:20s}: {data['分值']:6.1f}分  ({data['占比']})")
        report.append("")
        
        # 能力分布
        report.append("三、能力分布")
        report.append("-" * 70)
        for ability, data in results["能力分布"].items():
            report.append(f"  {ability:12s}: {data['分值']:6.1f}分  ({data['占比']})")
        report.append("")
        
        # 难度分布
        report.append("四、难度分布")
        report.append("-" * 70)
        for difficulty, data in results["难度分布"].items():
            if difficulty == "平均难度系数":
                report.append(f"  {difficulty}: {data}")
            else:
                report.append(
                    f"  {difficulty:20s}: {data['分值']:6.1f}分  "
                    f"({data['占比']:>6s})  [建议: {data['建议占比']}]"
                )
        report.append("")
        
        # 题型分布
        report.append("五、题型分布")
        report.append("-" * 70)
        for qtype, data in results["题型分布"].items():
            report.append(
                f"  {qtype:12s}: {data['分值']:6.1f}分  "
                f"({data['占比']:>6s})  {data['题量']}题"
            )
        report.append("")
        
        # 时间分配
        report.append("六、时间分配建议")
        report.append("-" * 70)
        for qtype, data in results["时间分配"].items():
            report.append(
                f"  {qtype:12s}: {data['总时间']:>12s}  "
                f"({data['题量']}题, 平均{data['平均每题']})"
            )
        report.append("")
        
        # 结构评价
        report.append("七、结构评价")
        report.append("-" * 70)
        evaluation = results["结构评价"]
        report.append(f"  总体评价: {evaluation['总体评价']}")
        report.append(f"  评分: {evaluation['评分']:.1f}/100.0")
        report.append("")
        
        if evaluation["优点"]:
            report.append("  主要优点:")
            for i, strength in enumerate(evaluation["优点"], 1):
                report.append(f"    {i}. {strength}")
            report.append("")
        
        if evaluation["问题"]:
            report.append("  存在问题:")
            for i, issue in enumerate(evaluation["问题"], 1):
                report.append(f"    {i}. {issue}")
            report.append("")
        
        # 改进建议
        report.append("八、改进建议")
        report.append("-" * 70)
        for i, suggestion in enumerate(results["改进建议"], 1):
            report.append(f"  {i}. {suggestion}")
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python analyze_paper.py <试卷JSON文件>")
        print("\n试卷JSON格式示例:")
        print(json.dumps({
            "total_score": 150,
            "time_limit": 150,
            "questions": [
                {
                    "id": 1,
                    "type": "选择题",
                    "score": 5,
                    "knowledge_points": ["函数", "导数"],
                    "ability_level": "应用",
                    "difficulty": 0.6
                },
                {
                    "id": 2,
                    "type": "解答题",
                    "score": 12,
                    "knowledge_points": ["立体几何", "向量"],
                    "ability_level": "综合",
                    "difficulty": 0.4
                }
            ]
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # 读取试卷数据
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            paper_data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    
    # 创建分析器
    analyzer = PaperAnalyzer()
    
    # 分析试卷
    results = analyzer.analyze(paper_data)
    
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
