import ast
import re
from typing import Dict, List, Any

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
            ],
            'javascript': [
                "使用const和let代替var",
                "使用严格模式",
                "避免全局变量",
                "使用箭头函数",
                "处理异步错误"
            ]
        }
        
        self.code_smells = {
            'long_function': 50,  # 行数阈值
            'long_parameter_list': 5,  # 参数个数阈值
            'complex_logic': 10  # 圈复杂度阈值
        }
    
    def review_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """审查代码质量"""
        issues = self._analyze_code(code, language)
        score = self._calculate_score(issues)
        
        return {
            "score": score,
            "grade": self._get_grade(score),
            "issues": issues,
            "suggestions": self._generate_suggestions(issues),
            "best_practices": self.best_practices.get(language, [])
        }
    
    def _analyze_code(self, code: str, language: str) -> List[Dict[str, Any]]:
        """分析代码问题"""
        issues = []
        
        if language == 'python':
            issues.extend(self._analyze_python_code(code))
        
        # 通用分析
        lines = code.split('\n')
        
        # 检查代码行数
        if len(lines) > self.code_smells['long_function']:
            issues.append({
                "type": "long_function",
                "severity": "medium",
                "description": f"函数过长 ({len(lines)} 行)，建议拆分为小函数",
                "line": "multiple"
            })
        
        # 检查注释比例
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        comment_ratio = comment_lines / len(lines) if lines else 0
        
        if comment_ratio < 0.1:
            issues.append({
                "type": "lack_of_comments",
                "severity": "low",
                "description": "代码注释不足",
                "suggestion": "为关键逻辑添加注释"
            })
        
        # 检查魔法数字
        magic_numbers = re.findall(r'\b\d+\b', code)
        if len(magic_numbers) > 5:
            issues.append({
                "type": "magic_numbers",
                "severity": "low",
                "description": f"发现 {len(magic_numbers)} 个魔法数字",
                "suggestion": "考虑使用常量代替魔法数字"
            })
        
        return issues
    
    def _analyze_python_code(self, code: str) -> List[Dict[str, Any]]:
        """分析Python代码"""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # 检查函数定义
                if isinstance(node, ast.FunctionDef):
                    # 检查参数数量
                    if len(node.args.args) > self.code_smells['long_parameter_list']:
                        issues.append({
                            "type": "too_many_parameters",
                            "severity": "medium",
                            "description": f"函数 '{node.name}' 参数过多 ({len(node.args.args)} 个)",
                            "line": node.lineno,
                            "suggestion": "考虑使用对象参数或拆分为多个函数"
                        })
                    
                    # 检查函数长度
                    function_lines = self._get_function_lines(node, code)
                    if function_lines > 30:
                        issues.append({
                            "type": "long_function",
                            "severity": "medium",
                            "description": f"函数 '{node.name}' 过长 ({function_lines} 行)",
                            "line": node.lineno,
                            "suggestion": "考虑拆分为更小的函数"
                        })
                
                # 检查异常处理
                if isinstance(node, ast.Try):
                    has_generic_except = any(
                        isinstance(handler, ast.ExceptHandler) and handler.type is None
                        for handler in node.handlers
                    )
                    if has_generic_except:
                        issues.append({
                            "type": "bare_except",
                            "severity": "high",
                            "description": "使用了空的except语句",
                            "line": node.lineno,
                            "suggestion": "指定具体的异常类型"
                        })
        
        except SyntaxError:
            issues.append({
                "type": "syntax_error",
                "severity": "high",
                "description": "代码存在语法错误，无法进行完整分析"
            })
        
        return issues
    
    def _get_function_lines(self, function_node, code: str) -> int:
        """获取函数行数"""
        lines = code.split('\n')
        start_line = function_node.lineno - 1
        end_line = function_node.end_lineno if hasattr(function_node, 'end_lineno') else start_line + 1
        return end_line - start_line
    
    def _calculate_score(self, issues: List[Dict]) -> float:
        """计算代码质量分数"""
        base_score = 100
        severity_weights = {
            "high": 20,
            "medium": 10,
            "low": 5
        }
        
        deduction = sum(severity_weights.get(issue.get("severity", "low"), 5) for issue in issues)
        return max(0, base_score - deduction)
    
    def _get_grade(self, score: float) -> str:
        """获取代码等级"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "一般"
        elif score >= 60:
            return "及格"
        else:
            return "需要改进"
    
    def _generate_suggestions(self, issues: List[Dict]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        for issue in issues:
            if issue["type"] == "long_function":
                suggestions.append("将长函数拆分为多个单一职责的小函数")
            elif issue["type"] == "too_many_parameters":
                suggestions.append("使用字典或数据类来组织相关参数")
            elif issue["type"] == "lack_of_comments":
                suggestions.append("为复杂算法和关键业务逻辑添加注释")
            elif issue["type"] == "magic_numbers":
                suggestions.append("将魔法数字定义为有意义的常量")
            elif issue["type"] == "bare_except":
                suggestions.append("指定具体的异常类型，避免隐藏错误")
        
        return list(set(suggestions))  # 去重