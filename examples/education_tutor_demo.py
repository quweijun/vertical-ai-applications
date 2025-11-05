#!/usr/bin/env python3
"""
教育辅导应用演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from education_tutor.subject_tutor import SubjectTutor
from education_tutor.homework_helper import HomeworkHelper
from education_tutor.exam_preparer import ExamPreparer

def demo_education_tutor():
    """教育辅导演示"""
    print("=" * 50)
    print("教育辅导应用演示")
    print("=" * 50)
    
    # 初始化组件
    tutor = SubjectTutor()
    helper = HomeworkHelper()
    preparer = ExamPreparer()
    
    # 1. 学科辅导演示
    print("\n1. 学科辅导演示")
    print("-" * 30)
    
    subjects_levels = [
        ("math", "beginner"),
        ("physics", "intermediate"),
        ("chemistry", "advanced")
    ]
    
    for subject, level in subjects_levels:
        print(f"\n{subject} - {level} 级别学习路径:")
        learning_path = tutor.get_learning_path(subject, level)
        
        print(f"推荐主题: {', '.join(learning_path['recommended_topics'][:3])}")
        plan = learning_path['study_plan']
        print(f"学习计划: {plan['duration']}, 每周{plan['weekly_hours']}小时")
        print(f"学习目标: {', '.join(learning_path['learning_goals'][:2])}")
    
    # 2. 作业帮助演示
    print("\n2. 作业帮助演示")
    print("-" * 30)
    
    homework_examples = [
        "求解二次方程 x^2 - 5x + 6 = 0，并分析根的性质",
        "计算一个半径为3cm的圆的面积和周长",
        "分析牛顿第二定律在现实生活中的应用"
    ]
    
    for homework in homework_examples[:2]:
        print(f"\n作业分析: {homework}")
        analysis = helper.analyze_homework(homework)
        
        print(f"检测学科: {analysis['detected_subject']}")
        print(f"识别主题: {', '.join(analysis['identified_topics'])}")
        print(f"难度等级: {analysis['difficulty_level']}")
        print(f"预计时间: {analysis['estimated_time']}")
        print(f"关键概念: {', '.join(analysis['key_concepts'][:2])}")
        print(f"建议方法: {analysis['suggested_approach'][0]}")
    
    # 3. 考试准备演示
    print("\n3. 考试准备演示")
    print("-" * 30)
    
    # 设置考试日期（30天后）
    from datetime import datetime, timedelta
    exam_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    study_plan = preparer.create_study_plan(
        subjects=["math", "physics", "chemistry"],
        exam_date=exam_date,
        current_level="intermediate",
        target_score="优秀",
        study_time_per_day=3
    )
    
    print(f"考试日期: {study_plan['exam_date']}")
    print(f"剩余天数: {study_plan['days_until_exam']}天")
    print(f"当前水平: {study_plan['current_level']}")
    print(f"目标成绩: {study_plan['target_score']}")
    print(f"每日学习: {study_plan['study_time_per_day']}")
    print(f"总学习时长: {study_plan['total_study_hours']}小时")
    
    # 显示第一周计划
    first_week = study_plan['weekly_schedule'][0]
    print(f"\n第一周重点科目: {', '.join(first_week['focus_subjects'])}")
    print(f"周目标: {', '.join(first_week['weekly_goals'])}")
    
    # 显示学习方法
    print(f"\n推荐学习方法:")
    for method in study_plan['study_methods'][:2]:
        print(f"  - {method}")
    
    # 显示考试策略
    print(f"\n考试策略:")
    for strategy in study_plan['exam_strategies']['general_strategies'][:2]:
        print(f"  - {strategy}")
    
    # 4. 生成测验题目
    print("\n4. 测验题目生成")
    print("-" * 30)
    
    quiz = tutor.generate_quiz("math", "algebra", "medium")
    if "error" not in quiz:
        print(f"学科: {quiz['subject']}")
        print(f"主题: {quiz['topic']}")
        print(f"难度: {quiz['difficulty']}")
        print(f"题目数量: {len(quiz['questions'])}")
        print(f"总分: {quiz['total_score']}")
        
        if quiz['questions']:
            first_question = quiz['questions'][0]
            print(f"\n示例题目: {first_question['question']}")
            print(f"选项: {', '.join(first_question['options'])}")
            print(f"答案: {first_question['answer']}")

if __name__ == "__main__":
    demo_education_tutor()