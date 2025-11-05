"""
代码调试器模块
提供智能错误分析、调试建议和自动修复功能
"""

import re
import ast
import tokenize
from io import StringIO
from typing import Dict, List, Any, Tuple
import traceback


class CodeDebugger:
    """智能代码调试器"""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        self.fix_suggestions = self._initialize_fix_suggestions()
        self.common_bugs = self._initialize_common_bugs()
        
    def _initialize_error_patterns(self) -> Dict[str, Dict]:
        """初始化错误模式库"""
        return {
            'SyntaxError': {
                'patterns': [
                    r'SyntaxError: invalid syntax',
                    r'SyntaxError: unexpected EOF while parsing',
                    r'SyntaxError: unmatched \'\)\'',
                    r'SyntaxError: invalid character',
                    r'SyntaxError: expected \':\''
                ],
                'description': '语法错误 - 代码不符合Python语法规则'
            },
            'NameError': {
                'patterns': [
                    r'NameError: name \'(.+?)\' is not defined',
                    r'NameError: free variable \'(.+?)\' referenced before assignment'
                ],
                'description': '名称错误 - 使用了未定义的变量或函数'
            },
            'TypeError': {
                'patterns': [
                    r'TypeError: unsupported operand type\(s\)',
                    r'TypeError: \'(.+?)\' object is not callable',
                    r'TypeError: can only concatenate',
                    r'TypeError: must be (.+?), not (.+?)'
                ],
                'description': '类型错误 - 操作或函数应用于不兼容的类型'
            },
            'IndexError': {
                'patterns': [
                    r'IndexError: list index out of range',
                    r'IndexError: string index out of range',
                    r'IndexError: tuple index out of range'
                ],
                'description': '索引错误 - 访问了不存在的列表/字符串索引'
            },
            'KeyError': {
                'patterns': [
                    r'KeyError: \'(.+?)\''
                ],
                'description': '键错误 - 访问了字典中不存在的键'
            },
            'AttributeError': {
                'patterns': [
                    r'AttributeError: \'(.+?)\' object has no attribute \'(.+?)\'',
                    r'AttributeError: module \'(.+?)\' has no attribute \'(.+?)\''
                ],
                'description': '属性错误 - 访问了对象不存在的属性'
            },
            'ValueError': {
                'patterns': [
                    r'ValueError: invalid literal for (.+?) with base (.+?)',
                    r'ValueError: too many values to unpack',
                    r'ValueError: I/O operation on closed file'
                ],
                'description': '值错误 - 函数接收到正确类型但不合适的值'
            },
            'ImportError': {
                'patterns': [
                    r'ImportError: No module named \'(.+?)\'',
                    r'ImportError: cannot import name \'(.+?)\''
                ],
                'description': '导入错误 - 导入模块或名称失败'
            },
            'IndentationError': {
                'patterns': [
                    r'IndentationError: unexpected indent',
                    r'IndentationError: expected an indented block',
                    r'IndentationError: unindent does not match any outer indentation level'
                ],
                'description': '缩进错误 - 代码缩进不正确'
            }
        }
    
    def _initialize_fix_suggestions(self) -> Dict[str, List[str]]:
        """初始化修复建议库"""
        return {
            'SyntaxError': [
                "检查括号、引号、方括号是否配对",
                "检查冒号的使用，特别是在if、for、while、def语句后",
                "检查代码结构是否完整",
                "使用代码编辑器的语法高亮功能辅助检查"
            ],
            'NameError': [
                "检查变量名拼写是否正确",
                "确保变量在使用前已经定义",
                "检查变量作用域是否正确",
                "确认导入的模块和函数名称正确"
            ],
            'TypeError': [
                "检查操作符两边的数据类型是否兼容",
                "确认函数参数的类型是否正确",
                "使用type()函数检查变量类型",
                "考虑使用类型转换函数如int(), str()等"
            ],
            'IndexError': [
                "在访问列表元素前检查列表长度",
                "使用len()函数获取列表长度",
                "考虑使用try-except处理可能的索引错误",
                "使用有效的索引范围（0 到 len(list)-1）"
            ],
            'KeyError': [
                "在访问字典键之前使用'in'操作符检查键是否存在",
                "使用dict.get()方法提供默认值",
                "使用try-except处理可能的键错误",
                "检查字典键的拼写和大小写"
            ],
            'AttributeError': [
                "检查对象是否确实拥有该属性",
                "确认导入的模块包含该属性",
                "检查属性名称拼写是否正确",
                "使用hasattr()函数检查属性是否存在"
            ],
            'ValueError': [
                "检查输入数据的格式和范围",
                "确认函数参数的值在有效范围内",
                "使用适当的验证函数检查输入",
                "查看函数文档了解参数要求"
            ],
            'ImportError': [
                "检查模块名称拼写是否正确",
                "确认模块已安装或路径正确",
                "检查Python路径设置",
                "尝试重新安装缺失的模块"
            ],
            'IndentationError': [
                "统一使用空格或制表符进行缩进（推荐使用4个空格）",
                "检查所有代码块的缩进是否一致",
                "使用编辑器的显示空白字符功能",
                "确保函数、类、控制结构后的代码正确缩进"
            ]
        }
    
    def _initialize_common_bugs(self) -> Dict[str, Dict]:
        """初始化常见Bug模式"""
        return {
            'off_by_one': {
                'pattern': r'range\(.*\d+.*\)',
                'description': 'off-by-one错误（差一错误）',
                'example': '使用range(len(list))时注意索引从0开始',
                'fix': '检查循环边界条件，确认是否应该使用<=或<'
            },
            'mutable_default': {
                'pattern': r'def \w+\(.*=(\[\]|\{\}|\(\)).*\):',
                'description': '可变默认参数问题',
                'example': 'def func(arg=[]): 会导致多个调用共享同一个列表',
                'fix': '使用None作为默认值，在函数内部初始化可变对象'
            },
            'variable_scope': {
                'pattern': r'local variable.*referenced before assignment',
                'description': '变量作用域问题',
                'example': '在函数内部修改全局变量未使用global关键字',
                'fix': '使用global或nonlocal关键字声明变量作用域'
            },
            'string_formatting': {
                'pattern': r'TypeError: not all arguments converted during string formatting',
                'description': '字符串格式化错误',
                'example': '格式化字符串与参数数量不匹配',
                'fix': '检查格式化字符串中的占位符与参数数量是否一致'
            }
        }
    
    def analyze_error(self, error_message: str, code: str, language: str = 'python') -> Dict[str, Any]:
        """分析错误并提供调试建议"""
        
        if language != 'python':
            return {"error": f"暂不支持 {language} 语言的调试"}
        
        analysis = {
            "error_message": error_message,
            "code_snippet": code[:200] + "..." if len(code) > 200 else code,
            "error_type": "Unknown",
            "error_details": {},
            "possible_causes": [],
            "fix_suggestions": [],  # 修复：统一使用 fix_suggestions 而不是 solutions
            "debugging_steps": [],
            "prevention_tips": [],
            "common_patterns": [],
            "line_info": self._extract_line_info(error_message),
            "severity": "medium"
        }
        
        # 识别错误类型
        error_type = self._identify_error_type(error_message)
        analysis["error_type"] = error_type
        
        # 提取错误详情
        analysis["error_details"] = self._extract_error_details(error_message, error_type)
        
        # 获取可能的原因
        analysis["possible_causes"] = self._get_possible_causes(error_type, code)
        
        # 获取修复建议 - 修复：统一使用 fix_suggestions
        analysis["fix_suggestions"] = self.fix_suggestions.get(error_type, ["检查代码逻辑"])
        
        # 生成调试步骤
        analysis["debugging_steps"] = self._generate_debugging_steps(error_type, code)
        
        # 预防建议
        analysis["prevention_tips"] = self._get_prevention_tips(error_type)
        
        # 常见模式匹配
        analysis["common_patterns"] = self._find_common_patterns(code, error_type)
        
        # 设置严重程度
        analysis["severity"] = self._assess_severity(error_type)
        
        # 代码检查
        analysis["code_issues"] = self._inspect_code(code)
        
        return analysis
    
    def _identify_error_type(self, error_message: str) -> str:
        """识别错误类型"""
        for error_type, info in self.error_patterns.items():
            for pattern in info['patterns']:
                if re.search(pattern, error_message):
                    return error_type
        return "UnknownError"
    
    def _extract_error_details(self, error_message: str, error_type: str) -> Dict[str, str]:
        """提取错误详情"""
        details = {}
        
        if error_type == 'NameError':
            match = re.search(r"name '(.+?)' is not defined", error_message)
            if match:
                details['undefined_name'] = match.group(1)
        
        elif error_type == 'TypeError':
            match = re.search(r"unsupported operand type\(s\) for (.+?): '(.+?)' and '(.+?)'", error_message)
            if match:
                details['operation'] = match.group(1)
                details['type1'] = match.group(2)
                details['type2'] = match.group(3)
        
        elif error_type == 'KeyError':
            match = re.search(r"KeyError: '(.+?)'", error_message)
            if match:
                details['missing_key'] = match.group(1)
        
        elif error_type == 'AttributeError':
            match = re.search(r"object has no attribute '(.+?)'", error_message)
            if match:
                details['missing_attribute'] = match.group(1)
        
        elif error_type == 'ImportError':
            match = re.search(r"No module named '(.+?)'", error_message)
            if match:
                details['missing_module'] = match.group(1)
        
        return details
    
    def _extract_line_info(self, error_message: str) -> Dict[str, Any]:
        """提取行号信息"""
        line_info = {
            "line_number": None,
            "file_name": None,
            "code_snippet": None
        }
        
        # 提取行号
        line_match = re.search(r'line (\d+)', error_message)
        if line_match:
            line_info["line_number"] = int(line_match.group(1))
        
        # 提取文件名
        file_match = re.search(r'File "(.+?)"', error_message)
        if file_match:
            line_info["file_name"] = file_match.group(1)
        
        return line_info
    
    def _get_possible_causes(self, error_type: str, code: str) -> List[str]:
        """获取可能的原因"""
        causes = []
        
        base_causes = {
            'SyntaxError': [
                "代码结构不完整（缺少括号、引号等）",
                "缩进不正确",
                "错误的关键字使用",
                "表达式语法错误"
            ],
            'NameError': [
                "变量名拼写错误",
                "变量在使用前未定义",
                "导入语句错误",
                "变量作用域问题"
            ],
            'TypeError': [
                "操作符用于不支持的数据类型",
                "函数参数类型不匹配",
                "方法调用对象类型错误",
                "类型转换问题"
            ],
            'IndexError': [
                "列表索引超出范围",
                "空列表访问",
                "循环边界条件错误",
                "索引计算错误"
            ]
        }
        
        causes.extend(base_causes.get(error_type, ["需要进一步分析代码逻辑"]))
        
        # 基于代码内容添加特定原因
        if error_type == 'NameError' and 'import' in code:
            causes.append("导入的模块未正确安装或路径配置问题")
        
        if error_type == 'AttributeError' and 'self.' in code:
            causes.append("类属性未正确定义或初始化")
        
        return causes
    
    def _generate_debugging_steps(self, error_type: str, code: str) -> List[str]:
        """生成调试步骤"""
        steps = []
        
        # 通用调试步骤
        steps.extend([
            "1. 仔细阅读错误信息，理解错误类型和位置",
            "2. 定位到错误发生的具体行号",
            "3. 检查相关变量和表达式的值"
        ])
        
        # 类型特定步骤
        if error_type == 'NameError':
            steps.extend([
                "4. 检查变量名拼写是否正确",
                "5. 确认变量在使用前已经定义",
                "6. 检查变量作用域"
            ])
        
        elif error_type == 'TypeError':
            steps.extend([
                "4. 使用type()函数检查变量类型",
                "5. 确认操作符支持的数据类型",
                "6. 检查函数参数类型"
            ])
        
        elif error_type == 'IndexError':
            steps.extend([
                "4. 使用len()检查列表长度",
                "5. 验证索引值的范围",
                "6. 检查循环边界条件"
            ])
        
        elif error_type == 'SyntaxError':
            steps.extend([
                "4. 检查括号、引号是否配对",
                "5. 验证代码缩进是否正确",
                "6. 检查冒号使用"
            ])
        
        steps.append("7. 使用print语句或调试器跟踪程序执行")
        steps.append("8. 简化代码，隔离问题")
        
        return steps
    
    def _get_prevention_tips(self, error_type: str) -> List[str]:
        """获取预防建议"""
        tips = []
        
        prevention_guides = {
            'NameError': [
                "使用有意义的变量名",
                "在函数开头定义所有局部变量",
                "使用IDE的代码补全功能",
                "定期进行代码审查"
            ],
            'TypeError': [
                "使用类型注解",
                "添加输入验证",
                "编写单元测试覆盖不同类型输入",
                "使用静态类型检查工具"
            ],
            'IndexError': [
                "在访问列表前检查长度",
                "使用enumerate()遍历列表",
                "考虑使用try-except处理边界情况",
                "编写边界测试用例"
            ],
            'SyntaxError': [
                "使用代码格式化工具",
                "遵循PEP8代码风格指南",
                "使用语法高亮的编辑器",
                "定期进行代码审查"
            ]
        }
        
        tips.extend(prevention_guides.get(error_type, [
            "编写清晰的代码",
            "添加适当的注释",
            "进行充分的测试",
            "使用版本控制跟踪更改"
        ]))
        
        return tips
    
    def _find_common_patterns(self, code: str, error_type: str) -> List[Dict]:
        """查找常见错误模式"""
        patterns = []
        
        for pattern_name, pattern_info in self.common_bugs.items():
            if re.search(pattern_info['pattern'], code):
                patterns.append({
                    'name': pattern_name,
                    'description': pattern_info['description'],
                    'example': pattern_info['example'],
                    'fix': pattern_info['fix']
                })
        
        return patterns
    
    def _assess_severity(self, error_type: str) -> str:
        """评估错误严重程度"""
        severity_map = {
            'SyntaxError': 'high',
            'NameError': 'medium',
            'TypeError': 'medium',
            'IndexError': 'medium',
            'KeyError': 'medium',
            'AttributeError': 'medium',
            'ValueError': 'medium',
            'ImportError': 'high',
            'IndentationError': 'high'
        }
        return severity_map.get(error_type, 'medium')
    
    def _inspect_code(self, code: str) -> List[Dict]:
        """检查代码中的潜在问题"""
        issues = []
        
        try:
            # 检查语法
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'type': 'syntax',
                'description': f'语法错误: {str(e)}',
                'severity': 'high'
            })
        
        # 检查常见问题模式
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line_issues = self._check_line_issues(line, i)
            issues.extend(line_issues)
        
        return issues
    
    def _check_line_issues(self, line: str, line_number: int) -> List[Dict]:
        """检查单行代码的问题"""
        issues = []
        
        # 检查未使用的导入
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            # 简化检查 - 实际应该分析整个文件的导入使用情况
            pass
        
        # 检查可能的拼写错误
        if 'def ' in line and '()' in line and ': ' not in line:
            issues.append({
                'type': 'style',
                'description': f'第{line_number}行: 函数定义后缺少冒号',
                'severity': 'medium',
                'line': line_number
            })
        
        # 检查比较操作符
        if ' = ' in line and ' == ' not in line and 'def ' not in line:
            # 可能是赋值操作误写为比较操作
            if re.search(r'if.*=.*:', line) or re.search(r'while.*=.*:', line):
                issues.append({
                    'type': 'logic',
                    'description': f'第{line_number}行: 可能误用赋值操作符=而不是比较操作符==',
                    'severity': 'high',
                    'line': line_number
                })
        
        return issues
    
    def suggest_fix(self, error_analysis: Dict) -> List[str]:
        """基于错误分析提供具体的修复建议"""
        suggestions = []
        error_type = error_analysis["error_type"]
        details = error_analysis["error_details"]
        
        if error_type == 'NameError' and 'undefined_name' in details:
            var_name = details['undefined_name']
            suggestions.append(f"定义变量 '{var_name}' 或检查拼写是否正确")
            suggestions.append(f"如果 '{var_name}' 是导入的，检查导入语句")
        
        elif error_type == 'TypeError' and 'operation' in details:
            op = details['operation']
            type1 = details.get('type1', '未知类型')
            type2 = details.get('type2', '未知类型')
            suggestions.append(f"操作 '{op}' 不支持类型 {type1} 和 {type2}")
            suggestions.append(f"考虑将操作数转换为兼容的类型")
        
        elif error_type == 'KeyError' and 'missing_key' in details:
            key = details['missing_key']
            suggestions.append(f"在访问字典键 '{key}' 之前检查其是否存在")
            suggestions.append(f"使用 dict.get('{key}') 方法提供默认值")
        
        elif error_type == 'IndexError':
            suggestions.append("在访问列表元素前检查列表长度")
            suggestions.append("使用有效的索引范围 (0 到 len(list)-1)")
        
        return suggestions if suggestions else ["请参考通用修复建议"]
    
    def generate_test_case(self, error_analysis: Dict) -> str:
        """生成测试用例来重现和验证修复"""
        error_type = error_analysis["error_type"]
        
        test_cases = {
            'NameError': '''
# 测试用例 - 重现NameError
def test_name_error():
    try:
        # 这里应该会引发NameError
        print(undefined_variable)
    except NameError as e:
        print(f"捕获到NameError: {e}")
        return True
    return False
''',
            'TypeError': '''
# 测试用例 - 重现TypeError  
def test_type_error():
    try:
        # 这里应该会引发TypeError
        result = "string" + 123
    except TypeError as e:
        print(f"捕获到TypeError: {e}")
        return True
    return False
''',
            'IndexError': '''
# 测试用例 - 重现IndexError
def test_index_error():
    try:
        # 这里应该会引发IndexError
        my_list = [1, 2, 3]
        print(my_list[5])
    except IndexError as e:
        print(f"捕获到IndexError: {e}")
        return True
    return False
'''
        }
        
        return test_cases.get(error_type, '''
# 通用测试用例模板
def test_error_reproduction():
    try:
        # 在这里重现错误
        pass
    except Exception as e:
        print(f"捕获到错误: {e}")
        return True
    return False
''')
    
    def interactive_debugging(self, code: str, error_message: str) -> Dict[str, Any]:
        """交互式调试指导"""
        analysis = self.analyze_error(error_message, code)
        
        interactive_guide = {
            "error_analysis": analysis,
            "step_by_step_guide": [
                {
                    "step": 1,
                    "action": "理解错误类型",
                    "details": f"这是一个 {analysis['error_type']} 错误",
                    "question": "你理解这个错误类型的意思吗？"
                },
                {
                    "step": 2, 
                    "action": "定位错误位置",
                    "details": f"错误发生在: {analysis['line_info']}",
                    "question": "你能找到错误发生的具体位置吗？"
                },
                {
                    "step": 3,
                    "action": "分析可能原因", 
                    "details": f"可能的原因: {analysis['possible_causes'][:2]}",
                    "question": "这些原因中哪个最符合你的情况？"
                },
                {
                    "step": 4,
                    "action": "尝试修复",
                    "details": f"修复建议: {analysis['fix_suggestions'][:2]}", 
                    "question": "你尝试了哪种修复方法？结果如何？"
                }
            ],
            "debugging_tools": [
                "使用print语句输出变量值",
                "使用Python调试器(pdb)",
                "使用IDE的调试功能", 
                "简化代码，逐步排查"
            ]
        }
        
        return interactive_guide


class AdvancedDebugger(CodeDebugger):
    """高级调试器 - 提供更深入的代码分析"""
    
    def __init__(self):
        super().__init__()
        self.performance_patterns = self._initialize_performance_patterns()
    
    def _initialize_performance_patterns(self) -> Dict:
        """初始化性能问题模式"""
        return {
            'nested_loops': {
                'pattern': r'for.*:\s*\n\s*for.*:',
                'description': '嵌套循环可能导致性能问题',
                'suggestion': '考虑使用更高效的算法或数据结构'
            },
            'string_concatenation': {
                'pattern': r'\+\=.*[\'\"].*[\'\"]',
                'description': '在循环中使用字符串连接可能低效',
                'suggestion': '使用列表和str.join()方法'
            },
            'repeated_calculation': {
                'pattern': r'for.*:\s*\n.*len\(.*\).*\n',
                'description': '在循环中重复计算不变的值',
                'suggestion': '在循环外预先计算不变的值'
            }
        }
    
    def performance_analysis(self, code: str) -> List[Dict]:
        """性能问题分析"""
        issues = []
        
        for pattern_name, pattern_info in self.performance_patterns.items():
            if re.search(pattern_info['pattern'], code, re.MULTILINE):
                issues.append({
                    'type': 'performance',
                    'pattern': pattern_name,
                    'description': pattern_info['description'],
                    'suggestion': pattern_info['suggestion'],
                    'severity': 'low'
                })
        
        return issues
    
    def code_complexity_analysis(self, code: str) -> Dict[str, Any]:
        """代码复杂度分析"""
        try:
            tree = ast.parse(code)
            complexity_info = {
                'function_count': 0,
                'class_count': 0,
                'import_count': 0,
                'avg_function_length': 0,
                'complexity_issues': []
            }
            
            function_lengths = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity_info['function_count'] += 1
                    # 估算函数长度
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                    function_lengths.append(end_line - start_line)
                
                elif isinstance(node, ast.ClassDef):
                    complexity_info['class_count'] += 1
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    complexity_info['import_count'] += 1
            
            # 计算平均函数长度
            if function_lengths:
                complexity_info['avg_function_length'] = sum(function_lengths) / len(function_lengths)
                
                # 检查过长的函数
                for length in function_lengths:
                    if length > 50:
                        complexity_info['complexity_issues'].append(
                            f"发现函数长度超过50行，建议拆分为更小的函数"
                        )
            
            return complexity_info
            
        except SyntaxError:
            return {'error': '代码存在语法错误，无法进行复杂度分析'}
    
    def comprehensive_analysis(self, code: str, error_message: str = None) -> Dict[str, Any]:
        """综合分析代码"""
        analysis = {}
        
        if error_message:
            analysis['error_analysis'] = self.analyze_error(error_message, code)
        
        analysis['performance_issues'] = self.performance_analysis(code)
        analysis['complexity_analysis'] = self.code_complexity_analysis(code)
        analysis['code_quality'] = self._assess_code_quality(code)
        
        return analysis
    
    def _assess_code_quality(self, code: str) -> Dict[str, Any]:
        """评估代码质量"""
        quality_score = 100
        issues = []
        
        # 检查注释比例
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        comment_lines = [line for line in non_empty_lines if line.strip().startswith('#')]
        
        comment_ratio = len(comment_lines) / len(non_empty_lines) if non_empty_lines else 0
        if comment_ratio < 0.1:
            quality_score -= 10
            issues.append("代码注释不足")
        
        # 检查函数长度
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                    function_length = end_line - start_line
                    
                    if function_length > 30:
                        quality_score -= 5
                        issues.append(f"函数 '{node.name}' 过长 ({function_length} 行)")
        except:
            pass
        
        return {
            'score': max(0, quality_score),
            'grade': '优秀' if quality_score >= 90 else '良好' if quality_score >= 80 else '一般',
            'issues': issues,
            'comment_ratio': f"{comment_ratio:.1%}"
        }


# 使用示例和测试函数
def debug_demo():
    """调试器演示函数"""
    debugger = CodeDebugger()
    advanced_debugger = AdvancedDebugger()
    
    # 示例错误代码
    error_code = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers) + 1):  # 这里会有IndexError
        total += numbers[i]
    return total / len(numbers)

result = calculate_average([1, 2, 3])
print(result)
"""
    
    error_message = "IndexError: list index out of range"
    
    print("基础调试分析:")
    print("=" * 50)
    analysis = debugger.analyze_error(error_message, error_code)
    print(f"错误类型: {analysis['error_type']}")
    print(f"严重程度: {analysis['severity']}")
    print(f"可能原因: {analysis['possible_causes'][0]}")
    print(f"修复建议: {analysis['fix_suggestions'][0]}")  # 修复：使用 fix_suggestions
    
    print("\n高级分析:")
    print("=" * 50)
    comprehensive = advanced_debugger.comprehensive_analysis(error_code, error_message)
    print(f"代码质量评分: {comprehensive['code_quality']['score']}")
    print(f"性能问题: {len(comprehensive['performance_issues'])} 个")
    print(f"复杂度分析 - 函数数量: {comprehensive['complexity_analysis']['function_count']}")


if __name__ == "__main__":
    debug_demo()