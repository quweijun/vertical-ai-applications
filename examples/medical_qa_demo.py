#!/usr/bin/env python3
"""
医疗问答系统演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medical_qa.medical_advisor import MedicalAdvisor
from medical_qa.symptom_checker import SymptomChecker

def demo_medical_qa():
    """医疗问答演示"""
    print("=" * 50)
    print("医疗问答系统演示")
    print("=" * 50)
    
    # 初始化组件
    advisor = MedicalAdvisor()
    checker = SymptomChecker()
    
    # 1. 症状分析演示
    print("\n1. 症状分析演示")
    print("-" * 30)
    
    symptom_sets = [
        ["头痛", "发烧"],
        ["咳嗽", "流鼻涕", "喉咙痛"],
        ["胸痛", "呼吸困难"]  # 紧急情况
    ]
    
    for symptoms in symptom_sets:
        print(f"\n症状: {', '.join(symptoms)}")
        analysis = advisor.symptom_analysis(symptoms, age=30)
        
        print(f"可能情况: {', '.join(analysis['possible_conditions'][:2])}")
        print(f"自我护理: {analysis['self_care_advice'][0]}")
        print(f"紧急程度: {analysis['urgency']}")
        print(f"建议: {analysis['recommendation']}")
    
    # 2. 药品信息演示
    print("\n2. 药品信息演示")
    print("-" * 30)
    
    drugs = ["布洛芬", "对乙酰氨基酚", "未知药品"]
    
    for drug in drugs:
        print(f"\n查询药品: {drug}")
        info = advisor.drug_information(drug)
        
        if "error" not in info:
            print(f"用途: {info['purpose']}")
            print(f"用法: {info['dosage']}")
            print(f"注意事项: {info['precautions'][0]}")
        else:
            print(f"错误: {info['error']}")
    
    # 3. 症状检查演示
    print("\n3. 症状检查演示")
    print("-" * 30)
    
    initial_symptoms = ["发烧", "咳嗽", "乏力"]
    check_result = checker.interactive_check(initial_symptoms)
    
    print(f"当前症状: {', '.join(check_result['current_symptoms'])}")
    print(f"风险评估: {check_result['risk_assessment']}")
    print(f"建议: {check_result['recommendation']}")
    
    if check_result['additional_questions']:
        print("需要进一步了解:")
        for question in check_result['additional_questions'][:2]:
            print(f"  - {question}")
    
    # 4. 用药提醒演示
    print("\n4. 用药提醒演示")
    print("-" * 30)
    
    reminder = advisor.set_reminder("布洛芬", {"times_per_day": 3})
    print(f"提醒设置: {reminder['message']}")
    print(f"下次提醒: {reminder['next_reminder']}")

if __name__ == "__main__":
    demo_medical_qa()