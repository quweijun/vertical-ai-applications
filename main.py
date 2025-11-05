#!/usr/bin/env python3
"""
垂直领域AI应用项目 - 主程序111
"""

import sys
import os
from typing import Dict, Any

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from examples.code_generation_demo import demo_code_generation
from examples.math_solving_demo import demo_math_solving
from examples.medical_qa_demo import demo_medical_qa
from examples.financial_analysis_demo import demo_financial_analysis
from examples.education_tutor_demo import demo_education_tutor

def show_menu():
    """显示主菜单"""
    print("=" * 60)
    print("          垂直领域AI应用项目")
    print("=" * 60)
    print("1. 代码生成与调试")
    print("2. 数学推理与解题")
    print("3. 医疗问答系统")
    print("4. 金融分析助手")
    print("5. 教育辅导应用")
    print("6. 运行所有演示")
    print("0. 退出")
    print("-" * 60)

def main():
    """主程序"""
    while True:
        show_menu()
        choice = input("请选择功能 (0-6): ").strip()
        
        if choice == '0':
            print("感谢使用！")
            break
        elif choice == '1':
            print("\n运行代码生成与调试演示...")
            demo_code_generation()
        elif choice == '2':
            print("\n运行数学推理与解题演示...")
            demo_math_solving()
        elif choice == '3':
            print("\n运行医疗问答系统演示...")
            demo_medical_qa()
        elif choice == '4':
            print("\n运行金融分析助手演示...")
            demo_financial_analysis()
        elif choice == '5':
            print("\n运行教育辅导应用演示...")
            demo_education_tutor()
        elif choice == '6':
            print("\n运行所有演示...")
            demo_code_generation()
            demo_math_solving()
            demo_medical_qa()
            demo_financial_analysis()
            demo_education_tutor()
        else:
            print("无效选择，请重新输入！")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()