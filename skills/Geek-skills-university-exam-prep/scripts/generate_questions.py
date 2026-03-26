#!/usr/bin/env python3
"""
应用型练习题生成脚本
基于用户材料生成不同难度级别的练习题框架
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from enum import Enum

class Difficulty(Enum):
    LEVEL1 = "基础热身"
    LEVEL2 = "变式挑战"
    LEVEL3 = "陷阱识别"
    LEVEL4 = "综合实战"

class QuestionType(Enum):
    CHOICE = "选择题"
    FILL_BLANK = "填空题"
    SHORT_ANSWER = "简答题"
    CALCULATION = "计算题"
    APPLICATION = "应用题"
    COMPARISON = "对比辨析"

@dataclass
class Question:
    """练习题结构"""
    topic: str  # 考点/主题
    difficulty: Difficulty
    question_type: QuestionType
    description: str  # 题目描述
    source_reference: str  # 来源参考（如"基于课本第X页例题"）
    key_points: List[str] = field(default_factory=list)  # 考查要点
    traps: List[str] = field(default_factory=list)  # 可能的陷阱
    follow_up_questions: List[str] = field(default_factory=list)  # 追问问题
    hints: List[str] = field(default_factory=list)  # 阶梯提示

@dataclass
class QuestionSet:
    """题目集合"""
    topic: str
    questions: List[Question] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    estimated_time: int = 30  # 预计时间（分钟）

# 题目模板
QUESTION_TEMPLATES = {
    "concept": {
        Difficulty.LEVEL1: {
            "description_template": "根据{source}的定义，请解释{concept}的基本含义。",
            "follow_up": [
                "你能用自己的话再解释一遍吗？",
                "这个定义中，哪个词是关键词？",
                "如果有人问你什么是{concept}，你会怎么简短回答？"
            ]
        },
        Difficulty.LEVEL2: {
            "description_template": "比较{concept1}和{concept2}的异同点。",
            "follow_up": [
                "它们最本质的区别是什么？",
                "在什么情况下容易混淆这两个概念？",
                "你能举一个生活中的例子来区分它们吗？"
            ]
        },
        Difficulty.LEVEL3: {
            "description_template": "判断以下关于{concept}的说法是否正确：\n{statements}",
            "traps": [
                "偷换概念",
                "以偏概全",
                "因果倒置",
                "混淆充分必要条件"
            ],
            "follow_up": [
                "你为什么认为选项X是错误的？",
                "如果把选项Y改成...它就正确了吗？"
            ]
        }
    },
    "application": {
        Difficulty.LEVEL1: {
            "description_template": "使用{method}解决以下问题：{problem}",
            "hints": [
                "第一步应该做什么？",
                "回想一下课本上类似的例题...",
                "这个问题的核心是什么？"
            ]
        },
        Difficulty.LEVEL2: {
            "description_template": "如果将{original_problem}中的{condition}改为{new_condition}，结果会怎样？",
            "follow_up": [
                "为什么改变这个条件会影响结果？",
                "还有哪些条件可能影响结果？"
            ]
        },
        Difficulty.LEVEL4: {
            "description_template": "设计一个解决{real_scenario}的方案，要求综合运用{concepts}。",
            "follow_up": [
                "你的方案有什么优缺点？",
                "如果资源有限，你会怎么简化？",
                "有没有其他可行的方案？"
            ]
        }
    }
}

def create_question_framework(
    topic: str,
    source_reference: str,
    concept: Optional[str] = None,
    method: Optional[str] = None,
    **kwargs
) -> QuestionSet:
    """
    创建一套练习题框架
    
    Args:
        topic: 考点主题
        source_reference: 材料来源
        concept: 核心概念（用于概念类题目）
        method: 解题方法（用于应用类题目）
        **kwargs: 其他参数
    
    Returns:
        QuestionSet: 包含多个难度级别的题目集
    """
    
    question_set = QuestionSet(
        topic=topic,
        learning_objectives=[
            f"理解{topic}的基本概念",
            f"能够运用{topic}相关知识解决问题",
            f"识别{topic}相关的常见陷阱"
        ]
    )
    
    # Level 1: 基础热身
    q1 = Question(
        topic=topic,
        difficulty=Difficulty.LEVEL1,
        question_type=QuestionType.SHORT_ANSWER,
        description=f"【基础确认】请用自己的话解释{topic}的核心概念。",
        source_reference=source_reference,
        key_points=["概念理解", "基本定义"],
        follow_up_questions=[
            "这个概念最重要的特点是什么？",
            "你在哪里见过这个概念的应用？"
        ],
        hints=[
            f"回顾{source_reference}中的定义...",
            "想想这个概念解决了什么问题"
        ]
    )
    question_set.questions.append(q1)
    
    # Level 2: 变式挑战
    q2 = Question(
        topic=topic,
        difficulty=Difficulty.LEVEL2,
        question_type=QuestionType.APPLICATION,
        description=f"【变式题】基于{source_reference}的例题，如果条件变化，结果会怎样？\n\n[此处需要具体的变式题目，基于用户上传的材料生成]",
        source_reference=source_reference,
        key_points=["灵活运用", "条件变化理解"],
        follow_up_questions=[
            "为什么改变这个条件会导致不同结果？",
            "还有哪些条件变化会影响答案？"
        ],
        hints=[
            "回忆原题的解法...",
            "思考新条件改变了什么"
        ]
    )
    question_set.questions.append(q2)
    
    # Level 3: 陷阱识别
    q3 = Question(
        topic=topic,
        difficulty=Difficulty.LEVEL3,
        question_type=QuestionType.CHOICE,
        description=f"【陷阱题】关于{topic}，以下哪个说法是正确的？\n\nA. [选项A - 可能的陷阱]\nB. [选项B]\nC. [选项C - 可能的陷阱]\nD. [正确答案]\n\n不仅给出答案，还要解释为什么排除其他选项。",
        source_reference=source_reference,
        key_points=["深度理解", "陷阱识别"],
        traps=[
            "混淆相似概念",
            "忽略边界条件",
            "因果关系错误"
        ],
        follow_up_questions=[
            "选项A的错误在哪里？",
            "如果修改选项C使其正确，应该怎么改？"
        ]
    )
    question_set.questions.append(q3)
    
    # Level 4: 综合实战
    q4 = Question(
        topic=topic,
        difficulty=Difficulty.LEVEL4,
        question_type=QuestionType.APPLICATION,
        description=f"【综合题】结合{topic}的知识，分析并解决以下实际问题：\n\n[此处需要结合多个知识点的综合题目]\n\n要求：\n1. 写出完整的分析过程\n2. 说明每一步的依据\n3. 检验答案的合理性",
        source_reference=source_reference,
        key_points=["综合运用", "多知识点结合", "完整解题过程"],
        follow_up_questions=[
            "如果时间紧张，你会如何简化解题过程？",
            "这道题还可以用什么其他方法？",
            "如果加入新的约束条件，答案会怎么变？"
        ],
        hints=[
            "先识别这道题涉及哪几个知识点",
            "按步骤逐个分析",
            "检查是否遗漏了什么条件"
        ]
    )
    question_set.questions.append(q4)
    
    return question_set

def output_question_set(qs: QuestionSet, output_format: str = "markdown") -> str:
    """输出题目集"""
    
    if output_format == "json":
        # 需要处理Enum类型
        def convert(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj
        
        data = {
            "topic": qs.topic,
            "learning_objectives": qs.learning_objectives,
            "estimated_time": qs.estimated_time,
            "questions": []
        }
        for q in qs.questions:
            q_dict = asdict(q)
            q_dict["difficulty"] = q.difficulty.value
            q_dict["question_type"] = q.question_type.value
            data["questions"].append(q_dict)
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    # Markdown格式
    lines = []
    lines.append(f"# 📝 练习题集：{qs.topic}\n")
    
    lines.append("## 学习目标\n")
    for obj in qs.learning_objectives:
        lines.append(f"- {obj}")
    lines.append(f"\n⏱️ 预计用时：{qs.estimated_time}分钟\n")
    
    lines.append("---\n")
    
    for i, q in enumerate(qs.questions, 1):
        lines.append(f"## 题目{i}：{q.difficulty.value}\n")
        lines.append(f"**题型**：{q.question_type.value}\n")
        lines.append(f"**参考来源**：{q.source_reference}\n")
        lines.append(f"\n### 题目描述\n\n{q.description}\n")
        
        if q.key_points:
            lines.append("\n**考查要点**：")
            lines.append(", ".join(q.key_points))
            lines.append("")
        
        if q.traps:
            lines.append("\n**常见陷阱**：")
            for trap in q.traps:
                lines.append(f"- ⚠️ {trap}")
            lines.append("")
        
        lines.append("\n### 苏格拉底式追问\n")
        lines.append("*学生作答后使用以下问题深入探讨：*\n")
        for fq in q.follow_up_questions:
            lines.append(f"- 「{fq}」")
        lines.append("")
        
        if q.hints:
            lines.append("\n### 阶梯提示\n")
            lines.append("*学生遇到困难时，按顺序给出提示：*\n")
            for j, hint in enumerate(q.hints, 1):
                lines.append(f"{j}. {hint}")
            lines.append("")
        
        lines.append("\n---\n")
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 3:
        print("用法: python generate_questions.py <考点主题> <来源参考> [输出格式:markdown/json]")
        print("示例: python generate_questions.py '二叉树遍历' '课本第4章第2节' markdown")
        sys.exit(1)
    
    topic = sys.argv[1]
    source_reference = sys.argv[2]
    output_format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
    
    # 生成题目集
    question_set = create_question_framework(topic, source_reference)
    
    # 输出
    output = output_question_set(question_set, output_format)
    print(output)

if __name__ == "__main__":
    main()
