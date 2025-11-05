#!/usr/bin/env python3
"""
数学推理与解题演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_reasoning.math_solver import MathSolver
from math_reasoning.step_by_step_solver import StepByStepSolver

def demo_math_solving():
    """数学解题演示"""
    print("=" * 50)
    print("数学推理与解题演示")
    print("=" * 50)
    
    # 初始化求解器
    solver = MathSolver()
    step_solver = StepByStepSolver()
    
    # 测试问题
    problems = [
        "解方程: 2x + 5 = 13",
        "计算半径为5的圆的面积",
        "求函数f(x)=x^2的导数",
        "计算表达式: (3 + 5) × 2 - 4"
    ]
    
    print("\n基础求解演示:")
    print("-" * 30)
    
    for problem in problems:
        print(f"\n问题: {problem}")
        result = solver.solve(problem)
        
        if "error" not in result:
            print(f"类别: {result['category']}")
            if 'solutions' in result:
                print(f"解: {result['solutions']}")
            elif 'area' in result:
                print(f"面积: {result['area']}")
            elif 'derivative' in result:
                print(f"导数: {result['derivative']}")
            elif 'result' in result:
                print(f"结果: {result['result']}")
        else:
            print(f"错误: {result['error']}")
    
    print("\n分步求解演示:")
    print("-" * 30)
    
    complex_problems = [
        "解二次方程: x^2 - 5x + 6 = 0",
        "一个长方形的长是8cm，宽是5cm，求面积和周长"
    ]
    
    for problem in complex_problems:
        print(f"\n问题: {problem}")
        result = step_solver.solve_with_steps(problem)
        
        if "error" not in result:
            print(f"解题步骤:")
            for step in result.get('detailed_steps', []):
                print(f"步骤{step['step']}: {step['title']} - {step['description']}")
            
            print(f"\n学习要点: {', '.join(result.get('learning_points', []))}")
            print(f"提示: {result.get('hints', [])[0]}")
        else:
            print(f"错误: {result['error']}")

if __name__ == "__main__":
    demo_math_solving()