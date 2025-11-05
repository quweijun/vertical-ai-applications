import ast
import re
from typing import Dict, List, Any
import tokenize
from io import StringIO

class CodeGenerator:
    """代码生成器"""
    
    def __init__(self, model=None):
        self.model = model
        self.supported_languages = ['python', 'javascript', 'java', 'cpp', 'go']
    
    def generate_function(self, description: str, language: str = 'python', 
                         requirements: List[str] = None) -> Dict[str, Any]:
        """根据描述生成函数代码"""
        
        if language not in self.supported_languages:
            return {"error": f"不支持的语言: {language}"}
        
        # 构建提示词
        prompt = self._build_function_prompt(description, language, requirements)
        
        # 生成代码（这里使用模拟，实际应该调用模型）
        generated_code = self._simulate_code_generation(prompt, language)
        
        # 验证代码语法
        syntax_valid, syntax_error = self._validate_syntax(generated_code, language)
        
        return {
            "code": generated_code,
            "language": language,
            "syntax_valid": syntax_valid,
            "syntax_error": syntax_error if not syntax_valid else None,
            "description": description
        }
    
    def _build_function_prompt(self, description: str, language: str, requirements: List[str]) -> str:
        """构建代码生成提示词"""
        prompt = f"""
请用{language}编写一个函数，满足以下要求：

功能描述: {description}

{"额外要求: " + ", ".join(requirements) if requirements else ""}

请提供:
1. 完整的函数实现
2. 适当的注释
3. 类型注解（如果语言支持）
4. 示例使用代码

只返回代码部分，不要额外解释。
"""
        return prompt
    
    def _simulate_code_generation(self, prompt: str, language: str) -> str:
        """模拟代码生成（实际项目应该调用真实模型）"""
        
        if language == 'python':
            if '排序' in prompt or 'sort' in prompt.lower():
                return '''def sort_numbers(numbers: List[int], reverse: bool = False) -> List[int]:
    """
    对数字列表进行排序
    
    Args:
        numbers: 要排序的数字列表
        reverse: 是否降序排列，默认为False（升序）
    
    Returns:
        排序后的数字列表
    """
    return sorted(numbers, reverse=reverse)

# 示例使用
if __name__ == "__main__":
    sample_numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_asc = sort_numbers(sample_numbers)
    sorted_desc = sort_numbers(sample_numbers, reverse=True)
    print(f"升序: {sorted_asc}")
    print(f"降序: {sorted_desc}")'''
        
        return f"# {language}代码生成功能\n# 描述: {prompt}"
    
    def _validate_syntax(self, code: str, language: str) -> tuple:
        """验证代码语法"""
        if language == 'python':
            try:
                ast.parse(code)
                return True, None
            except SyntaxError as e:
                return False, str(e)
        else:
            # 对于其他语言，这里可以集成相应的语法检查器
            return True, None  # 暂时返回True

class CodeDebugger:
    """代码调试器"""
    
    def __init__(self):
        self.common_errors = {
            'python': {
                'NameError': '变量未定义',
                'SyntaxError': '语法错误',
                'TypeError': '类型错误',
                'IndexError': '索引错误',
                'KeyError': '键错误'
            }
        }
    
    def analyze_error(self, error_message: str, code: str, language: str = 'python') -> Dict[str, Any]:
        """分析错误信息并提供修复建议"""
        
        error_type = self._extract_error_type(error_message)
        error_location = self._extract_error_location(error_message)
        
        analysis = {
            "error_type": error_type,
            "error_message": error_message,
            "error_location": error_location,
            "possible_causes": self._suggest_possible_causes(error_type, code, language),
            "fix_suggestions": self._suggest_fixes(error_type, code, language),
            "prevention_tips": self._suggest_prevention(error_type, language)
        }
        
        return analysis
    
    def _extract_error_type(self, error_message: str) -> str:
        """提取错误类型"""
        for error in ['NameError', 'SyntaxError', 'TypeError', 'IndexError', 'KeyError']:
            if error in error_message:
                return error
        return "UnknownError"
    
    def _extract_error_location(self, error_message: str) -> str:
        """提取错误位置"""
        # 简化实现，实际应该更精确地解析错误信息
        if "line" in error_message:
            line_match = re.search(r'line (\d+)', error_message)
            if line_match:
                return f"第{line_match.group(1)}行"
        return "未知位置"
    
    def _suggest_possible_causes(self, error_type: str, code: str, language: str) -> List[str]:
        """建议可能的原因"""
        causes = []
        
        if error_type == 'NameError':
            causes = [
                "变量名拼写错误",
                "变量在使用前未定义",
                "导入的模块未正确安装",
                "作用域问题"
            ]
        elif error_type == 'SyntaxError':
            causes = [
                "缺少括号、引号或其他符号",
                "缩进错误",
                "错误的关键字使用",
                "表达式不完整"
            ]
        elif error_type == 'TypeError':
            causes = [
                "函数参数类型不匹配",
                "操作符用于不支持的类型",
                "方法调用对象类型错误"
            ]
        
        return causes
    
    def _suggest_fixes(self, error_type: str, code: str, language: str) -> List[str]:
        """建议修复方法"""
        fixes = []
        
        if error_type == 'NameError':
            fixes = [
                "检查变量名拼写",
                "确保变量在使用前已定义",
                "检查导入语句是否正确",
                "确认变量作用域"
            ]
        elif error_type == 'SyntaxError':
            fixes = [
                "检查括号、引号是否配对",
                "统一使用空格或制表符进行缩进",
                "查看Python官方文档确认语法",
                "使用代码编辑器的高亮功能"
            ]
        
        return fixes
    
    def _suggest_prevention(self, error_type: str, language: str) -> List[str]:
        """建议预防措施"""
        prevention = []
        
        if error_type == 'NameError':
            prevention = [
                "使用有意义的变量名",
                "在函数开头定义所有变量",
                "使用IDE的自动补全功能",
                "定期进行代码审查"
            ]
        
        return prevention

class CodeReviewer:
    """代码审查器"""
    
    def __init__(self):
        self.best_practices = {
            'python': [
                "使用有意义的变量名",
                "函数应该只做一件事",
                "避免过长的函数",
                "使用类型注解",
                "添加适当的文档字符串",
                "处理异常情况"
            ]
        }
    
    def review_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """审查代码质量"""
        
        issues = self._find_issues(code, language)
        score = self._calculate_code_score(issues)
        
        return {
            "score": score,
            "grade": self._get_grade(score),
            "issues": issues,
            "suggestions": self._generate_suggestions(issues),
            "best_practices": self.best_practices.get(language, [])
        }
    
    def _find_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """发现代码问题"""
        issues = []
        
        # 检查代码长度
        lines = code.split('\n')
        if len(lines) > 50:
            issues.append({
                "type": "structure",
                "severity": "medium",
                "description": "代码过长，建议拆分为更小的函数",
                "line": "multiple"
            })
        
        # 检查注释
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        comment_ratio = len(comment_lines) / len(lines) if lines else 0
        if comment_ratio < 0.1:
            issues.append({
                "type": "documentation", 
                "severity": "low",
                "description": "代码注释不足",
                "line": "multiple"
            })
        
        # 检查函数长度（简化实现）
        for i, line in enumerate(lines, 1):
            if 'def ' in line and '(' in line:
                # 简单的函数开始检测
                issues.append({
                    "type": "function",
                    "severity": "info", 
                    "description": f"函数定义: {line.strip()}",
                    "line": i
                })
        
        return issues
    
    def _calculate_code_score(self, issues: List[Dict]) -> float:
        """计算代码质量分数"""
        base_score = 100
        severity_weights = {
            "high": 20,
            "medium": 10, 
            "low": 5,
            "info": 0
        }
        
        deduction = sum(severity_weights[issue["severity"]] for issue in issues)
        return max(0, base_score - deduction)
    
    def _get_grade(self, score: float) -> str:
        """获取代码等级"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "一般"
        else:
            return "需要改进"
    
    def _generate_suggestions(self, issues: List[Dict]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        for issue in issues:
            if issue["type"] == "structure" and issue["severity"] == "medium":
                suggestions.append("将长函数拆分为多个小函数，每个函数只负责一个明确的任务")
            elif issue["type"] == "documentation":
                suggestions.append("为关键算法和复杂逻辑添加注释")
        
        return suggestions