import ast
import re
from typing import Dict, List, Any

class CodeGenerator:
    """智能代码生成器"""
    
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'java', 'cpp']
    
    def generate_function(self, description: str, language: str = 'python') -> Dict[str, Any]:
        """根据描述生成函数代码"""
        if language not in self.supported_languages:
            return {"error": f"不支持的语言: {language}"}
        
        prompt = self._build_prompt(description, language)
        generated_code = self._generate_code(prompt, language)
        
        # 验证语法
        syntax_valid, error = self._validate_syntax(generated_code, language)
        
        return {
            "code": generated_code,
            "language": language,
            "syntax_valid": syntax_valid,
            "error": error,
            "description": description
        }
    
    def _build_prompt(self, description: str, language: str) -> str:
        """构建生成提示"""
        return f"""
用{language}编写一个函数：
要求：{description}

要求：
1. 完整的函数实现
2. 适当的注释
3. 类型注解（如支持）
4. 示例使用

只返回代码：
"""
    
    def _generate_code(self, prompt: str, language: str) -> str:
        """生成代码（模拟实现）"""
        if language == 'python':
            if '排序' in prompt or 'sort' in prompt:
                return '''def bubble_sort(arr: list) -> list:
    """
    冒泡排序算法
    
    Args:
        arr: 待排序的列表
        
    Returns:
        排序后的列表
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# 使用示例
if __name__ == "__main__":
    numbers = [64, 34, 25, 12, 22, 11, 90]
    sorted_numbers = bubble_sort(numbers)
    print(f"排序结果: {sorted_numbers}")'''
        
        return f"# {language}代码实现\n# 功能: {prompt}"
    
    def _validate_syntax(self, code: str, language: str) -> tuple:
        """验证代码语法"""
        if language == 'python':
            try:
                ast.parse(code)
                return True, None
            except SyntaxError as e:
                return False, str(e)
        return True, None

class CodeDebugger:
    """代码调试助手"""
    
    def analyze_error(self, error_msg: str, code: str) -> Dict[str, Any]:
        """分析错误并提供修复建议"""
        error_type = self._classify_error(error_msg)
        
        return {
            "error_type": error_type,
            "error_message": error_msg,
            "possible_causes": self._get_possible_causes(error_type, code),
            "solutions": self._get_solutions(error_type),
            "prevention_tips": self._get_prevention_tips(error_type)
        }
    
    def _classify_error(self, error_msg: str) -> str:
        """错误分类"""
        error_patterns = {
            'SyntaxError': r'SyntaxError',
            'NameError': r'NameError',
            'TypeError': r'TypeError',
            'IndexError': r'IndexError',
            'KeyError': r'KeyError'
        }
        
        for error_type, pattern in error_patterns.items():
            if re.search(pattern, error_msg):
                return error_type
        return "UnknownError"
    
    def _get_possible_causes(self, error_type: str, code: str) -> List[str]:
        """获取可能原因"""
        causes = {
            'SyntaxError': [
                "缺少括号、引号或冒号",
                "缩进错误",
                "错误的关键字使用"
            ],
            'NameError': [
                "变量名拼写错误",
                "变量未定义",
                "作用域问题"
            ],
            'TypeError': [
                "类型不匹配",
                "函数参数错误",
                "操作符用于不支持的类型"
            ]
        }
        return causes.get(error_type, ["需要进一步分析"])
    
    def _get_solutions(self, error_type: str) -> List[str]:
        """获取解决方案"""
        solutions = {
            'SyntaxError': [
                "检查括号、引号是否配对",
                "统一缩进为4个空格",
                "检查冒号使用"
            ],
            'NameError': [
                "检查变量名拼写",
                "确保变量在使用前定义",
                "检查导入的模块"
            ]
        }
        return solutions.get(error_type, ["检查代码逻辑"])