"""
测试用例生成器模块
提供智能测试用例生成、测试代码模板和测试覆盖分析功能
"""

import ast
import re
import inspect
from typing import Dict, List, Any, Tuple, Optional
import random
from datetime import datetime


class TestGenerator:
    """智能测试用例生成器"""
    
    def __init__(self):
        self.test_frameworks = self._initialize_test_frameworks()
        self.test_patterns = self._initialize_test_patterns()
        self.mock_libraries = self._initialize_mock_libraries()
        
    def _initialize_test_frameworks(self) -> Dict[str, Dict]:
        """初始化测试框架配置"""
        return {
            'pytest': {
                'imports': ['import pytest'],
                'decorators': ['@pytest.mark.parametrize'],
                'assertions': ['assert'],
                'fixtures': ['@pytest.fixture'],
                'file_naming': 'test_{module_name}.py'
            },
            'unittest': {
                'imports': ['import unittest'],
                'decorators': [],
                'assertions': ['self.assertEqual', 'self.assertTrue', 'self.assertFalse'],
                'fixtures': ['setUp', 'tearDown'],
                'file_naming': 'test_{module_name}.py'
            },
            'doctest': {
                'imports': [],
                'decorators': [],
                'assertions': ['>>>'],
                'fixtures': [],
                'file_naming': '{module_name}.py'
            }
        }
    
    def _initialize_test_patterns(self) -> Dict[str, Dict]:
        """初始化测试模式"""
        return {
            'unit_test': {
                'description': '单元测试 - 测试单个函数或方法',
                'focus': '函数逻辑、边界条件、异常处理',
                'coverage': '函数级别的代码覆盖'
            },
            'integration_test': {
                'description': '集成测试 - 测试多个组件的交互',
                'focus': '组件接口、数据流、系统集成',
                'coverage': '组件交互覆盖'
            },
            'functional_test': {
                'description': '功能测试 - 测试系统功能需求',
                'focus': '用户场景、业务流程、功能验证',
                'coverage': '功能需求覆盖'
            },
            'edge_case_test': {
                'description': '边界测试 - 测试边界条件和极端情况',
                'focus': '边界值、异常输入、极限条件',
                'coverage': '边界条件覆盖'
            },
            'performance_test': {
                'description': '性能测试 - 测试系统性能指标',
                'focus': '响应时间、资源使用、负载能力',
                'coverage': '性能指标验证'
            }
        }
    
    def _initialize_mock_libraries(self) -> Dict[str, List[str]]:
        """初始化模拟库配置"""
        return {
            'pytest': [
                'from unittest.mock import Mock, MagicMock, patch',
                'import pytest_mock'
            ],
            'unittest': [
                'from unittest.mock import Mock, MagicMock, patch'
            ],
            'standalone': [
                'from unittest.mock import Mock, MagicMock, patch'
            ]
        }
    
    def generate_unit_tests(self, code: str, framework: str = 'pytest', 
                          coverage_target: float = 0.8) -> Dict[str, Any]:
        """为代码生成单元测试"""
        
        analysis = self._analyze_code_structure(code)
        test_cases = self._generate_test_cases(analysis, coverage_target)
        
        test_code = self._build_test_file(analysis, test_cases, framework)
        
        return {
            "framework": framework,
            "test_file_name": self._get_test_file_name(analysis['module_name'], framework),
            "test_code": test_code,
            "test_cases": test_cases,
            "coverage_estimation": self._estimate_coverage(test_cases, analysis),
            "imports_required": self._get_required_imports(analysis, framework),
            "mock_requirements": self._identify_mock_requirements(analysis),
            "setup_instructions": self._generate_setup_instructions(framework)
        }
    
    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """分析代码结构"""
        try:
            tree = ast.parse(code)
            analysis = {
                'module_name': 'example_module',
                'functions': [],
                'classes': [],
                'imports': [],
                'global_variables': [],
                'code_complexity': 'low',
                'dependencies': []
            }
            
            # 分析函数
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = self._analyze_function(node)
                    analysis['functions'].append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node)
                    analysis['classes'].append(class_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self._analyze_import(node)
                    analysis['imports'].append(import_info)
                    analysis['dependencies'].extend(import_info['modules'])
            
            # 估算代码复杂度
            analysis['code_complexity'] = self._assess_complexity(analysis)
            
            return analysis
            
        except SyntaxError as e:
            return {
                'error': f'代码语法错误: {str(e)}',
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def _analyze_function(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """分析函数定义"""
        func_info = {
            'name': func_node.name,
            'args': [],
            'returns': None,
            'docstring': ast.get_docstring(func_node),
            'line_count': 0,
            'complexity': 'low',
            'test_categories': []
        }
        
        # 分析参数
        for arg in func_node.args.args:
            func_info['args'].append({
                'name': arg.arg,
                'type': 'any'  # 简化处理
            })
        
        # 分析返回值
        returns = []
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return):
                if node.value:
                    returns.append('value')
                else:
                    returns.append('none')
        
        if returns:
            func_info['returns'] = 'value' if 'value' in returns else 'none'
        
        # 估算函数长度
        start_line = func_node.lineno
        end_line = func_node.end_lineno if hasattr(func_node, 'end_lineno') else start_line
        func_info['line_count'] = end_line - start_line
        
        # 确定测试类别
        func_info['test_categories'] = self._determine_test_categories(func_node)
        
        return func_info
    
    def _analyze_class(self, class_node: ast.ClassDef) -> Dict[str, Any]:
        """分析类定义"""
        class_info = {
            'name': class_node.name,
            'methods': [],
            'attributes': [],
            'docstring': ast.get_docstring(class_node),
            'inheritance': [base.id for base in class_node.bases if isinstance(base, ast.Name)],
            'test_categories': ['class_test']
        }
        
        # 分析方法
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                method_info = self._analyze_function(node)
                class_info['methods'].append(method_info)
        
        return class_info
    
    def _analyze_import(self, import_node: ast.AST) -> Dict[str, Any]:
        """分析导入语句"""
        if isinstance(import_node, ast.Import):
            modules = [alias.name for alias in import_node.names]
        elif isinstance(import_node, ast.ImportFrom):
            module = import_node.module or ''
            modules = [f"{module}.{alias.name}" for alias in import_node.names]
        else:
            modules = []
        
        return {
            'type': 'import' if isinstance(import_node, ast.Import) else 'import_from',
            'modules': modules,
            'line': import_node.lineno
        }
    
    def _assess_complexity(self, analysis: Dict) -> str:
        """评估代码复杂度"""
        total_functions = len(analysis['functions'])
        total_methods = sum(len(cls['methods']) for cls in analysis['classes'])
        total_elements = total_functions + total_methods
        
        if total_elements == 0:
            return 'empty'
        elif total_elements <= 5:
            return 'low'
        elif total_elements <= 15:
            return 'medium'
        else:
            return 'high'
    
    def _determine_test_categories(self, func_node: ast.FunctionDef) -> List[str]:
        """确定测试类别"""
        categories = ['unit_test']
        
        # 基于函数特征确定测试类别
        function_code = ast.unparse(func_node)
        
        if 'import' in function_code:
            categories.append('integration_test')
        
        if any(keyword in function_code for keyword in ['file', 'open', 'read', 'write']):
            categories.append('io_test')
        
        if any(keyword in function_code for keyword in ['network', 'request', 'http']):
            categories.append('network_test')
        
        if any(keyword in function_code for keyword in ['database', 'db', 'sql']):
            categories.append('database_test')
        
        return categories
    
    def _generate_test_cases(self, analysis: Dict, coverage_target: float) -> List[Dict[str, Any]]:
        """生成测试用例"""
        test_cases = []
        
        # 为每个函数生成测试用例
        for func in analysis['functions']:
            func_test_cases = self._generate_function_test_cases(func, coverage_target)
            test_cases.extend(func_test_cases)
        
        # 为每个类生成测试用例
        for cls in analysis['classes']:
            class_test_cases = self._generate_class_test_cases(cls, coverage_target)
            test_cases.extend(class_test_cases)
        
        return test_cases
    
    def _generate_function_test_cases(self, func_info: Dict, coverage_target: float) -> List[Dict]:
        """为函数生成测试用例"""
        test_cases = []
        func_name = func_info['name']
        
        # 基础测试用例
        base_cases = [
            {
                'name': f'test_{func_name}_basic',
                'type': 'normal',
                'description': f'测试 {func_name} 的基本功能',
                'input': self._generate_sample_input(func_info),
                'expected': 'None',  # 根据实际情况调整
                'category': 'unit_test'
            }
        ]
        test_cases.extend(base_cases)
        
        # 边界测试用例
        if coverage_target > 0.6:
            edge_cases = self._generate_edge_cases(func_info)
            test_cases.extend(edge_cases)
        
        # 异常测试用例
        if coverage_target > 0.8:
            exception_cases = self._generate_exception_cases(func_info)
            test_cases.extend(exception_cases)
        
        return test_cases
    
    def _generate_class_test_cases(self, class_info: Dict, coverage_target: float) -> List[Dict]:
        """为类生成测试用例"""
        test_cases = []
        class_name = class_info['name']
        
        # 为每个方法生成测试用例
        for method in class_info['methods']:
            if not method['name'].startswith('_'):  # 跳过私有方法
                method_cases = self._generate_method_test_cases(method, class_name)
                test_cases.extend(method_cases)
        
        # 类级别测试用例
        class_level_cases = [
            {
                'name': f'test_{class_name}_initialization',
                'type': 'initialization',
                'description': f'测试 {class_name} 类的初始化',
                'input': {'args': []},
                'expected': 'instance_created',
                'category': 'class_test'
            }
        ]
        test_cases.extend(class_level_cases)
        
        return test_cases
    
    def _generate_method_test_cases(self, method_info: Dict, class_name: str) -> List[Dict]:
        """为类方法生成测试用例"""
        test_cases = []
        method_name = method_info['name']
        
        test_case = {
            'name': f'test_{class_name}_{method_name}',
            'type': 'method',
            'description': f'测试 {class_name}.{method_name} 方法',
            'input': {
                'instance_args': [],
                'method_args': self._generate_sample_input(method_info)
            },
            'expected': 'method_executed',
            'category': 'unit_test'
        }
        test_cases.append(test_case)
        
        return test_cases
    
    def _generate_sample_input(self, func_info: Dict) -> Dict[str, Any]:
        """生成示例输入数据"""
        inputs = {}
        
        for arg in func_info['args']:
            arg_name = arg['name']
            if arg_name == 'self':
                continue
            
            # 基于参数名生成示例值
            if any(keyword in arg_name for keyword in ['name', 'title', 'description']):
                inputs[arg_name] = f"test_{arg_name}"
            elif any(keyword in arg_name for keyword in ['count', 'size', 'length', 'index']):
                inputs[arg_name] = 5
            elif any(keyword in arg_name for keyword in ['price', 'amount', 'value']):
                inputs[arg_name] = 100.0
            elif any(keyword in arg_name for keyword in ['flag', 'is_', 'has_']):
                inputs[arg_name] = True
            elif 'list' in arg_name or 'array' in arg_name:
                inputs[arg_name] = [1, 2, 3, 4, 5]
            elif 'dict' in arg_name or 'map' in arg_name:
                inputs[arg_name] = {'key1': 'value1', 'key2': 'value2'}
            else:
                inputs[arg_name] = f"sample_{arg_name}"
        
        return inputs
    
    def _generate_edge_cases(self, func_info: Dict) -> List[Dict]:
        """生成边界测试用例"""
        edge_cases = []
        func_name = func_info['name']
        
        common_edge_values = {
            'numeric': [0, -1, 1, 1000, -1000, 0.0, -0.0],
            'string': ['', 'a', ' '*100, '特殊字符!@#$%'],
            'list': [[], [1], [1]*100],
            'boolean': [True, False],
            'none': [None]
        }
        
        for arg in func_info['args']:
            if arg['name'] == 'self':
                continue
            
            for value_type, values in common_edge_values.items():
                for value in values[:2]:  # 每个类型取前两个值
                    edge_case = {
                        'name': f'test_{func_name}_edge_{arg["name"]}_{value_type}',
                        'type': 'edge',
                        'description': f'测试 {func_name} 的边界情况: {arg["name"]}={value}',
                        'input': {arg['name']: value},
                        'expected': 'handle_appropriately',
                        'category': 'edge_case_test'
                    }
                    edge_cases.append(edge_case)
        
        return edge_cases
    
    def _generate_exception_cases(self, func_info: Dict) -> List[Dict]:
        """生成异常测试用例"""
        exception_cases = []
        func_name = func_info['name']
        
        # 常见的异常情况
        exception_scenarios = [
            {
                'name': 'invalid_type',
                'description': '无效类型输入',
                'input': {'invalid_arg': object()},
                'expected_exception': 'TypeError'
            },
            {
                'name': 'missing_required',
                'description': '缺少必需参数',
                'input': {},
                'expected_exception': 'TypeError'
            }
        ]
        
        for scenario in exception_scenarios:
            exception_case = {
                'name': f'test_{func_name}_exception_{scenario["name"]}',
                'type': 'exception',
                'description': f'测试 {func_name} 的异常情况: {scenario["description"]}',
                'input': scenario['input'],
                'expected_exception': scenario['expected_exception'],
                'category': 'exception_test'
            }
            exception_cases.append(exception_case)
        
        return exception_cases
    
    def _build_test_file(self, analysis: Dict, test_cases: List[Dict], framework: str) -> str:
        """构建测试文件内容"""
        lines = []
        
        # 添加文件头
        lines.extend(self._generate_file_header(analysis, framework))
        
        # 添加导入语句
        lines.extend(self._generate_imports(analysis, framework))
        
        # 添加测试类或函数
        if framework == 'unittest':
            lines.extend(self._build_unittest_class(analysis, test_cases))
        else:  # pytest
            lines.extend(self._build_pytest_functions(analysis, test_cases))
        
        # 添加文件尾
        lines.extend(self._generate_file_footer())
        
        return '\n'.join(lines)
    
    def _generate_file_header(self, analysis: Dict, framework: str) -> List[str]:
        """生成文件头"""
        header = [
            '"""',
            f'自动生成的测试文件',
            f'框架: {framework}',
            f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            f'模块: {analysis.get("module_name", "unknown")}',
            '"""',
            ''
        ]
        return header
    
    def _generate_imports(self, analysis: Dict, framework: str) -> List[str]:
        """生成导入语句"""
        imports = []
        
        # 添加测试框架导入
        framework_imports = self.test_frameworks[framework]['imports']
        imports.extend(framework_imports)
        
        # 添加模拟库导入
        mock_imports = self.mock_libraries.get(framework, [])
        imports.extend(mock_imports)
        
        # 添加被测试模块导入
        module_name = analysis.get('module_name', 'example_module')
        imports.append(f'import {module_name}')
        imports.append('')
        
        return imports
    
    def _build_unittest_class(self, analysis: Dict, test_cases: List[Dict]) -> List[str]:
        """构建unittest测试类"""
        lines = []
        class_name = f"Test{analysis.get('module_name', 'Module').title()}"
        
        lines.append(f'class {class_name}(unittest.TestCase):')
        lines.append('')
        
        # 添加setUp方法
        lines.append('    def setUp(self):')
        lines.append('        """测试准备"""')
        lines.append('        pass')
        lines.append('')
        
        # 添加测试方法
        for test_case in test_cases:
            method_lines = self._build_unittest_method(test_case)
            lines.extend(['    ' + line for line in method_lines])
            lines.append('')
        
        # 添加tearDown方法
        lines.append('    def tearDown(self):')
        lines.append('        """测试清理"""')
        lines.append('        pass')
        lines.append('')
        
        # 添加主程序
        lines.append('if __name__ == "__main__":')
        lines.append('    unittest.main()')
        
        return lines
    
    def _build_unittest_method(self, test_case: Dict) -> List[str]:
        """构建unittest测试方法"""
        lines = []
        
        lines.append(f'def {test_case["name"]}(self):')
        lines.append(f'    """{test_case["description"]}"""')
        
        if test_case['type'] == 'exception':
            lines.append(f'    with self.assertRaises({test_case["expected_exception"]}):')
            lines.append(f'        # 测试代码')
            lines.append(f'        pass')
        else:
            lines.append(f'    # 测试代码')
            lines.append(f'    # 输入: {test_case["input"]}')
            lines.append(f'    # 期望: {test_case["expected"]}')
            lines.append(f'    self.assertTrue(True)  # 示例断言')
        
        return lines
    
    def _build_pytest_functions(self, analysis: Dict, test_cases: List[Dict]) -> List[str]:
        """构建pytest测试函数"""
        lines = []
        
        for test_case in test_cases:
            func_lines = self._build_pytest_function(test_case)
            lines.extend(func_lines)
            lines.append('')
        
        return lines
    
    def _build_pytest_function(self, test_case: Dict) -> List[str]:
        """构建pytest测试函数"""
        lines = []
        
        lines.append(f'def {test_case["name"]}():')
        lines.append(f'    """{test_case["description"]}"""')
        
        if test_case['type'] == 'exception':
            lines.append(f'    with pytest.raises({test_case["expected_exception"]}):')
            lines.append(f'        # 测试代码')
            lines.append(f'        pass')
        else:
            lines.append(f'    # 测试代码')
            lines.append(f'    # 输入: {test_case["input"]}')
            lines.append(f'    # 期望: {test_case["expected"]}')
            lines.append(f'    assert True  # 示例断言')
        
        return lines
    
    def _generate_file_footer(self) -> List[str]:
        """生成文件尾"""
        return ['']
    
    def _get_test_file_name(self, module_name: str, framework: str) -> str:
        """获取测试文件名"""
        pattern = self.test_frameworks[framework]['file_naming']
        return pattern.format(module_name=module_name)
    
    def _estimate_coverage(self, test_cases: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """估算测试覆盖率"""
        total_functions = len(analysis['functions'])
        total_methods = sum(len(cls['methods']) for cls in analysis['classes'])
        total_testable = total_functions + total_methods
        
        if total_testable == 0:
            return {
                'line_coverage': 0,
                'function_coverage': 0,
                'branch_coverage': 0,
                'overall': 0
            }
        
        # 简化估算
        covered_functions = min(len(test_cases), total_testable)
        function_coverage = covered_functions / total_testable
        
        return {
            'line_coverage': function_coverage * 0.8,  # 估算
            'function_coverage': function_coverage,
            'branch_coverage': function_coverage * 0.6,  # 估算
            'overall': function_coverage
        }
    
    def _get_required_imports(self, analysis: Dict, framework: str) -> List[str]:
        """获取需要的导入"""
        imports = []
        
        # 添加被测试模块的依赖
        for dependency in analysis.get('dependencies', []):
            imports.append(f'import {dependency}')
        
        return imports
    
    def _identify_mock_requirements(self, analysis: Dict) -> List[str]:
        """识别模拟需求"""
        mock_needs = []
        
        # 检查外部依赖
        external_keywords = ['requests', 'http', 'database', 'file', 'network']
        for imp in analysis.get('imports', []):
            for module in imp.get('modules', []):
                if any(keyword in module for keyword in external_keywords):
                    mock_needs.append(f'需要模拟: {module}')
        
        return mock_needs
    
    def _generate_setup_instructions(self, framework: str) -> List[str]:
        """生成设置说明"""
        instructions = [
            f'1. 安装测试框架: pip install {framework}',
            '2. 运行测试:',
            f'   - {framework}: pytest test_file.py',
            '   - unittest: python -m unittest test_file.py',
            '3. 查看测试报告:',
            '   - pytest --verbose test_file.py',
            '   - coverage run -m pytest test_file.py && coverage report'
        ]
        return instructions


class AdvancedTestGenerator(TestGenerator):
    """高级测试生成器 - 提供更复杂的测试生成功能"""
    
    def __init__(self):
        super().__init__()
        self.performance_patterns = self._initialize_performance_patterns()
        self.security_patterns = self._initialize_security_patterns()
    
    def _initialize_performance_patterns(self) -> Dict:
        """初始化性能测试模式"""
        return {
            'load_test': {
                'description': '负载测试 - 测试系统在正常和峰值负载下的表现',
                'metrics': ['响应时间', '吞吐量', '资源使用率'],
                'tools': ['pytest-benchmark', 'locust']
            },
            'stress_test': {
                'description': '压力测试 - 测试系统在极限负载下的表现',
                'metrics': ['系统稳定性', '错误率', '恢复时间'],
                'tools': ['pytest-benchmark', 'jmeter']
            },
            'endurance_test': {
                'description': '耐久测试 - 测试系统在长时间运行下的表现',
                'metrics': ['内存泄漏', '性能衰减', '系统稳定性'],
                'tools': ['pytest-benchmark']
            }
        }
    
    def _initialize_security_patterns(self) -> Dict:
        """初始化安全测试模式"""
        return {
            'sql_injection': {
                'description': 'SQL注入测试',
                'test_cases': ["' OR '1'='1", "'; DROP TABLE users; --"],
                'vulnerability': 'high'
            },
            'xss': {
                'description': '跨站脚本攻击测试',
                'test_cases': ['<script>alert("XSS")</script>', '<img src=x onerror=alert(1)>'],
                'vulnerability': 'medium'
            },
            'path_traversal': {
                'description': '路径遍历测试',
                'test_cases': ['../../../etc/passwd', '..\\..\\windows\\system32\\config'],
                'vulnerability': 'high'
            }
        }
    
    def generate_performance_tests(self, code: str, test_type: str = 'load_test') -> Dict[str, Any]:
        """生成性能测试"""
        analysis = self._analyze_code_structure(code)
        
        performance_tests = {
            'test_type': test_type,
            'description': self.performance_patterns[test_type]['description'],
            'test_code': self._build_performance_test(analysis, test_type),
            'metrics': self.performance_patterns[test_type]['metrics'],
            'tools': self.performance_patterns[test_type]['tools'],
            'configuration': self._generate_performance_config(test_type)
        }
        
        return performance_tests
    
    def _build_performance_test(self, analysis: Dict, test_type: str) -> str:
        """构建性能测试代码"""
        if test_type == 'load_test':
            return self._build_load_test(analysis)
        elif test_type == 'stress_test':
            return self._build_stress_test(analysis)
        else:
            return self._build_endurance_test(analysis)
    
    def _build_load_test(self, analysis: Dict) -> str:
        """构建负载测试"""
        code = [
            'import time',
            'import pytest',
            '',
            '@pytest.mark.performance',
            'def test_load_performance():',
            '    """负载性能测试"""',
            '    start_time = time.time()',
            '    ',
            '    # 模拟负载测试',
            '    for i in range(1000):',
            '        # 执行被测试函数',
            '        pass',
            '    ',
            '    end_time = time.time()',
            '    execution_time = end_time - start_time',
            '    ',
            '    # 性能断言',
            '    assert execution_time < 1.0, f"执行时间过长: {execution_time}秒"',
            ''
        ]
        return '\n'.join(code)
    
    def generate_security_tests(self, code: str) -> Dict[str, Any]:
        """生成安全测试"""
        analysis = self._analyze_code_structure(code)
        security_tests = []
        
        for vuln_type, vuln_info in self.security_patterns.items():
            test_case = {
                'vulnerability': vuln_type,
                'description': vuln_info['description'],
                'test_cases': vuln_info['test_cases'],
                'risk_level': vuln_info['vulnerability'],
                'test_code': self._build_security_test(analysis, vuln_type)
            }
            security_tests.append(test_case)
        
        return {
            'security_tests': security_tests,
            'overall_risk': self._assess_security_risk(security_tests),
            'recommendations': self._generate_security_recommendations(security_tests)
        }
    
    def _build_security_test(self, analysis: Dict, vuln_type: str) -> str:
        """构建安全测试代码"""
        test_cases = self.security_patterns[vuln_type]['test_cases']
        
        code = [
            'import pytest',
            '',
            f'@pytest.mark.security',
            f'def test_security_{vuln_type}():',
            f'    """安全测试: {self.security_patterns[vuln_type]["description"]}"""',
            f'    ',
            f'    test_inputs = {test_cases}',
            f'    ',
            f'    for malicious_input in test_inputs:',
            f'        # 测试恶意输入处理',
            f'        try:',
            f'            # 使用恶意输入调用被测试函数',
            f'            result = process_input(malicious_input)',
            f'            # 验证结果没有被恶意影响',
            f'            assert is_safe(result), f"安全漏洞: 输入 {malicious_input} 未被正确处理"',
            f'        except Exception as e:',
            f'            # 期望的异常处理',
            f'            assert isinstance(e, ExpectedSecurityException)',
            f''
        ]
        return '\n'.join(code)
    
    def _assess_security_risk(self, security_tests: List[Dict]) -> str:
        """评估安全风险"""
        high_risks = sum(1 for test in security_tests if test['risk_level'] == 'high')
        
        if high_risks > 0:
            return 'high'
        elif any(test['risk_level'] == 'medium' for test in security_tests):
            return 'medium'
        else:
            return 'low'
    
    def _generate_security_recommendations(self, security_tests: List[Dict]) -> List[str]:
        """生成安全建议"""
        recommendations = []
        
        for test in security_tests:
            if test['risk_level'] == 'high':
                recommendations.append(
                    f"立即修复 {test['vulnerability']} 漏洞"
                )
            elif test['risk_level'] == 'medium':
                recommendations.append(
                    f"评估并修复 {test['vulnerability']} 潜在风险"
                )
        
        if not recommendations:
            recommendations.append("当前未发现高风险安全问题")
        
        return recommendations
    
    def _build_stress_test(self, analysis: Dict) -> str:
        """构建压力测试"""
        return self._build_load_test(analysis)  # 简化实现
    
    def _build_endurance_test(self, analysis: Dict) -> str:
        """构建耐久测试"""
        return self._build_load_test(analysis)  # 简化实现
    
    def _generate_performance_config(self, test_type: str) -> Dict[str, Any]:
        """生成性能测试配置"""
        configs = {
            'load_test': {
                'iterations': 1000,
                'concurrent_users': 10,
                'duration': '5 minutes',
                'acceptable_response_time': '1 second'
            },
            'stress_test': {
                'iterations': 10000,
                'concurrent_users': 100,
                'duration': '15 minutes',
                'acceptable_response_time': '5 seconds'
            },
            'endurance_test': {
                'iterations': 100000,
                'concurrent_users': 5,
                'duration': '24 hours',
                'acceptable_response_time': '2 seconds'
            }
        }
        return configs.get(test_type, {})


class TestCoverageAnalyzer:
    """测试覆盖分析器"""
    
    def __init__(self):
        self.coverage_metrics = self._initialize_coverage_metrics()
    
    def _initialize_coverage_metrics(self) -> Dict[str, Dict]:
        """初始化覆盖指标"""
        return {
            'line_coverage': {
                'description': '行覆盖 - 测试执行的代码行比例',
                'target': 0.8,
                'importance': 'high'
            },
            'branch_coverage': {
                'description': '分支覆盖 - 测试覆盖的控制流分支比例',
                'target': 0.7,
                'importance': 'high'
            },
            'function_coverage': {
                'description': '函数覆盖 - 测试覆盖的函数比例',
                'target': 0.9,
                'importance': 'medium'
            },
            'condition_coverage': {
                'description': '条件覆盖 - 测试覆盖的布尔条件比例',
                'target': 0.6,
                'importance': 'medium'
            }
        }
    
    def analyze_coverage(self, code: str, test_code: str) -> Dict[str, Any]:
        """分析测试覆盖情况"""
        code_analysis = self._analyze_code_elements(code)
        test_analysis = self._analyze_test_coverage(test_code, code_analysis)
        
        return {
            'code_analysis': code_analysis,
            'test_analysis': test_analysis,
            'coverage_gaps': self._identify_coverage_gaps(code_analysis, test_analysis),
            'improvement_suggestions': self._generate_improvement_suggestions(test_analysis),
            'overall_score': self._calculate_overall_score(test_analysis)
        }
    
    def _analyze_code_elements(self, code: str) -> Dict[str, Any]:
        """分析代码元素"""
        try:
            tree = ast.parse(code)
            analysis = {
                'total_lines': len(code.split('\n')),
                'functions': [],
                'classes': [],
                'branches': 0,
                'conditions': 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, (ast.If, ast.While, ast.For)):
                    analysis['branches'] += 1
                elif isinstance(node, ast.BoolOp):
                    analysis['conditions'] += 1
            
            return analysis
        except SyntaxError:
            return {'error': '代码语法错误'}
    
    def _analyze_test_coverage(self, test_code: str, code_analysis: Dict) -> Dict[str, float]:
        """分析测试覆盖情况"""
        # 简化实现 - 实际应该使用覆盖率工具
        covered_functions = min(len(code_analysis.get('functions', [])), 
                               test_code.count('def test_'))
        
        total_functions = len(code_analysis.get('functions', []))
        function_coverage = covered_functions / total_functions if total_functions > 0 else 0
        
        return {
            'line_coverage': function_coverage * 0.8,
            'branch_coverage': function_coverage * 0.6,
            'function_coverage': function_coverage,
            'condition_coverage': function_coverage * 0.5
        }
    
    def _identify_coverage_gaps(self, code_analysis: Dict, test_analysis: Dict) -> List[Dict]:
        """识别覆盖缺口"""
        gaps = []
        
        for metric, target in self.coverage_metrics.items():
            current = test_analysis.get(metric, 0)
            if current < target['target']:
                gaps.append({
                    'metric': metric,
                    'current': current,
                    'target': target['target'],
                    'gap': target['target'] - current,
                    'importance': target['importance']
                })
        
        return gaps
    
    def _generate_improvement_suggestions(self, test_analysis: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if test_analysis.get('function_coverage', 0) < 0.8:
            suggestions.append("增加更多函数测试用例")
        
        if test_analysis.get('branch_coverage', 0) < 0.6:
            suggestions.append("添加边界条件和异常情况测试")
        
        if test_analysis.get('condition_coverage', 0) < 0.5:
            suggestions.append("增加布尔条件组合测试")
        
        return suggestions
    
    def _calculate_overall_score(self, test_analysis: Dict) -> float:
        """计算总体评分"""
        weights = {
            'line_coverage': 0.3,
            'branch_coverage': 0.3,
            'function_coverage': 0.2,
            'condition_coverage': 0.2
        }
        
        total_score = 0
        for metric, weight in weights.items():
            total_score += test_analysis.get(metric, 0) * weight
        
        return total_score


# 使用示例和演示函数
def test_generator_demo():
    """测试生成器演示"""
    print("测试用例生成器演示")
    print("=" * 50)
    
    # 示例代码
    sample_code = """
def calculate_factorial(n):
    \"\"\"计算阶乘\"\"\"
    if n < 0:
        raise ValueError("阶乘不能计算负数")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

def is_prime(number):
    \"\"\"判断是否为质数\"\"\"
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True
"""
    
    # 基础测试生成
    generator = TestGenerator()
    print("\n1. 基础单元测试生成:")
    print("-" * 30)
    
    unit_tests = generator.generate_unit_tests(sample_code, 'pytest', 0.8)
    print(f"测试框架: {unit_tests['framework']}")
    print(f"测试文件: {unit_tests['test_file_name']}")
    print(f"测试用例数量: {len(unit_tests['test_cases'])}")
    print(f"预估覆盖率: {unit_tests['coverage_estimation']['overall']:.1%}")
    
    # 显示部分测试代码
    print(f"\n生成的测试代码片段:")
    test_lines = unit_tests['test_code'].split('\n')[:10]
    for line in test_lines:
        print(f"  {line}")
    
    # 高级测试生成
    advanced_generator = AdvancedTestGenerator()
    print("\n2. 安全测试生成:")
    print("-" * 30)
    
    security_tests = advanced_generator.generate_security_tests(sample_code)
    print(f"安全风险等级: {security_tests['overall_risk']}")
    for test in security_tests['security_tests'][:2]:
        print(f"  漏洞: {test['vulnerability']} - 风险: {test['risk_level']}")
    
    # 覆盖分析
    print("\n3. 测试覆盖分析:")
    print("-" * 30)
    
    coverage_analyzer = TestCoverageAnalyzer()
    coverage_report = coverage_analyzer.analyze_coverage(sample_code, unit_tests['test_code'])
    print(f"总体评分: {coverage_report['overall_score']:.1%}")
    
    for metric, value in coverage_report['test_analysis'].items():
        print(f"  {metric}: {value:.1%}")


if __name__ == "__main__":
    test_generator_demo()