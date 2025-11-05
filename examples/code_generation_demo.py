#!/usr/bin/env python3
"""
代码生成与调试演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_generation.code_generator import CodeGenerator
from code_generation.code_debugger import CodeDebugger
from code_generation.code_reviewer import CodeReviewer

def demo_code_generation():
    """代码生成演示"""
    print("=" * 50)
    print("代码生成与调试演示")
    print("=" * 50)
    
    # 初始化组件
    generator = CodeGenerator()
    debugger = CodeDebugger()
    reviewer = CodeReviewer()
    
    # 1. 代码生成演示
    print("\n1. 代码生成演示")
    print("-" * 30)
    
    descriptions = [
        "实现一个快速排序算法",
        "编写一个函数计算斐波那契数列",
        "创建一个简单的计算器类"
    ]
    
    for desc in descriptions:
        print(f"\n生成代码: {desc}")
        result = generator.generate_function(desc, "python")
        
        if "error" not in result:
            print(f"生成的代码:")
            print(result["code"][:200] + "..." if len(result["code"]) > 200 else result["code"])
            print(f"语法检查: {'通过' if result['syntax_valid'] else '不通过'}")
        else:
            print(f"错误: {result['error']}")
    
    # 2. 代码调试演示
    print("\n2. 代码调试演示")
    print("-" * 30)
    
    error_examples = [
        "NameError: name 'undefined_var' is not defined",
        "SyntaxError: invalid syntax",
        "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    ]
    
    for error_msg in error_examples:
        print(f"\n错误分析: {error_msg}")
        debug_result = debugger.analyze_error(error_msg, "示例代码")
        print(f"错误类型: {debug_result['error_type']}")
        print(f"可能原因: {debug_result['possible_causes'][0]}")
        # 修复：使用 fix_suggestions 而不是 solutions
        print(f"修复建议: {debug_result['fix_suggestions'][0]}")
    
    # 3. 代码审查演示
    print("\n3. 代码审查演示")
    print("-" * 30)
    
    sample_code = """
def process_data(input_data):
    # 这是一个很长的函数，包含很多功能
    result = []
    for i in range(len(input_data)):
        item = input_data[i]
        if item > 0:
            # 处理正数
            processed = item * 2 + 5 - 3 * 4 / 2
            result.append(processed)
        else:
            # 处理负数
            processed = item * 3 - 2 + 7 / 1
            result.append(processed)
    return result
"""
    
    print("审查示例代码...")
    review_result = reviewer.review_code(sample_code, "python")
    print(f"代码评分: {review_result['score']}/100")
    print(f"代码等级: {review_result['grade']}")
    print(f"发现 {len(review_result['issues'])} 个问题")
    
    for i, issue in enumerate(review_result['issues'][:3], 1):
        print(f"问题 {i}: {issue['description']}")

if __name__ == "__main__":
    demo_code_generation()