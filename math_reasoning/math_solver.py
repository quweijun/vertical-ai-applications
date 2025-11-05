import re
import sympy as sp
from typing import Dict, List, Any
import numpy as np

class MathSolver:
    """数学问题求解器"""
    
    def __init__(self):
        self.supported_categories = [
            'algebra', 'calculus', 'geometry', 'statistics', 'arithmetic'
        ]
    
    def solve_problem(self, problem: str, category: str = None) -> Dict[str, Any]:
        """解决数学问题"""
        
        # 自动检测问题类别
        if category is None:
            category = self._detect_category(problem)
        
        if category not in self.supported_categories:
            return {"error": f"不支持的数学类别: {category}"}
        
        # 根据类别选择求解方法
        if category == 'algebra':
            return self._solve_algebra(problem)
        elif category == 'calculus':
            return self._solve_calculus(problem)
        elif category == 'geometry':
            return self._solve_geometry(problem)
        elif category == 'statistics':
            return self._solve_statistics(problem)
        else:
            return self._solve_arithmetic(problem)
    
    def _detect_category(self, problem: str) -> str:
        """检测数学问题类别"""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ['方程', '等式', '代数', 'x=', 'y=']):
            return 'algebra'
        elif any(word in problem_lower for word in ['导数', '积分', '微分', '极限']):
            return 'calculus'
        elif any(word in problem_lower for word in ['三角形', '圆形', '面积', '体积', '角度']):
            return 'geometry'
        elif any(word in problem_lower for word in ['平均', '方差', '概率', '统计']):
            return 'statistics'
        else:
            return 'arithmetic'
    
    def _solve_algebra(self, problem: str) -> Dict[str, Any]:
        """解决代数问题"""
        try:
            # 提取方程
            equation_match = re.search(r'([\dx+y=\.\-\+\*\/\(\)\s]+)', problem)
            if not equation_match:
                return {"error": "未找到有效的方程"}
            
            equation_str = equation_match.group(1).replace(' ', '')
            
            # 使用sympy求解
            x = sp.Symbol('x')
            y = sp.Symbol('y')
            
            if '=' in equation_str:
                left, right = equation_str.split('=')
                equation = sp.Eq(sp.sympify(left), sp.sympify(right))
            else:
                equation = sp.Eq(sp.sympify(equation_str), 0)
            
            solution = sp.solve(equation, x)
            
            return {
                "category": "algebra",
                "problem": problem,
                "equation": str(equation),
                "solution": [str(sol) for sol in solution],
                "steps": self._generate_algebra_steps(equation, solution),
                "verification": self._verify_solution(equation, solution)
            }
            
        except Exception as e:
            return {"error": f"代数求解错误: {str(e)}"}
    
    def _solve_calculus(self, problem: str) -> Dict[str, Any]:
        """解决微积分问题"""
        try:
            x = sp.Symbol('x')
            
            if '导数' in problem or '微分' in problem:
                # 提取函数表达式
                func_match = re.search(r'[yf]\(x\)\s*=\s*([^,]+)', problem)
                if func_match:
                    func_str = func_match.group(1)
                    func = sp.sympify(func_str)
                    derivative = sp.diff(func, x)
                    
                    return {
                        "category": "calculus",
                        "problem": problem,
                        "function": str(func),
                        "derivative": str(derivative),
                        "type": "differentiation"
                    }
            
            elif '积分' in problem:
                # 提取积分表达式
                integral_match = re.search(r'∫([^dx]+)dx', problem.replace(' ', ''))
                if integral_match:
                    integrand_str = integral_match.group(1)
                    integrand = sp.sympify(integrand_str)
                    integral = sp.integrate(integrand, x)
                    
                    return {
                        "category": "calculus", 
                        "problem": problem,
                        "integrand": str(integrand),
                        "integral": str(integral),
                        "type": "integration"
                    }
            
            return {"error": "无法解析的微积分问题"}
            
        except Exception as e:
            return {"error": f"微积分求解错误: {str(e)}"}
    
    def _solve_geometry(self, problem: str) -> Dict[str, Any]:
        """解决几何问题"""
        # 提取数字
        numbers = re.findall(r'\d+\.?\d*', problem)
        numbers = [float(num) for num in numbers]
        
        if '圆' in problem and '面积' in problem:
            if numbers:
                radius = numbers[0]
                area = np.pi * radius ** 2
                return {
                    "category": "geometry",
                    "problem": problem,
                    "shape": "circle",
                    "radius": radius,
                    "area": area,
                    "formula": "A = πr²"
                }
        
        elif '三角形' in problem and '面积' in problem:
            if len(numbers) >= 2:
                base, height = numbers[0], numbers[1]
                area = 0.5 * base * height
                return {
                    "category": "geometry",
                    "problem": problem,
                    "shape": "triangle", 
                    "base": base,
                    "height": height,
                    "area": area,
                    "formula": "A = ½ × 底 × 高"
                }
        
        return {"error": "无法解析的几何问题"}
    
    def _solve_statistics(self, problem: str) -> Dict[str, Any]:
        """解决统计问题"""
        numbers = re.findall(r'\d+\.?\d*', problem)
        numbers = [float(num) for num in numbers]
        
        if not numbers:
            return {"error": "未找到数字数据"}
        
        if '平均' in problem:
            mean = np.mean(numbers)
            return {
                "category": "statistics",
                "problem": problem,
                "data": numbers,
                "mean": mean,
                "type": "descriptive"
            }
        
        elif '方差' in problem:
            variance = np.var(numbers)
            return {
                "category": "statistics",
                "problem": problem,
                "data": numbers, 
                "variance": variance,
                "standard_deviation": np.sqrt(variance),
                "type": "descriptive"
            }
        
        return {"error": "无法解析的统计问题"}
    
    def _solve_arithmetic(self, problem: str) -> Dict[str, Any]:
        """解决算术问题"""
        try:
            # 提取算术表达式
            expr_match = re.search(r'([\d\.\+\-\*\/\(\)\s]+)', problem)
            if expr_match:
                expression = expr_match.group(1).replace(' ', '')
                result = eval(expression)  # 注意：实际使用中应该更安全地计算
                
                return {
                    "category": "arithmetic",
                    "problem": problem,
                    "expression": expression,
                    "result": result
                }
        except:
            pass
        
        return {"error": "无法解析的算术问题"}
    
    def _generate_algebra_steps(self, equation, solution) -> List[str]:
        """生成代数解题步骤"""
        steps = [
            f"1. 给定方程: {equation}",
            f"2. 移项整理方程",
            f"3. 求解得到: x = {solution[0]}" if solution else "3. 方程无解"
        ]
        return steps
    
    def _verify_solution(self, equation, solution) -> bool:
        """验证解的正确性"""
        if not solution:
            return False
        
        try:
            # 简单的验证：将解代入方程检查是否成立
            x = sp.Symbol('x')
            for sol in solution:
                if not equation.subs(x, sol).equals(0):
                    return False
            return True
        except:
            return False

class StepByStepSolver:
    """分步解题器"""
    
    def __init__(self):
        self.solver = MathSolver()
    
    def solve_with_steps(self, problem: str) -> Dict[str, Any]:
        """分步解决数学问题"""
        
        # 先获取基本解
        basic_solution = self.solver.solve_problem(problem)
        
        if "error" in basic_solution:
            return basic_solution
        
        # 添加详细步骤
        detailed_steps = self._generate_detailed_steps(problem, basic_solution)
        
        result = basic_solution.copy()
        result["detailed_steps"] = detailed_steps
        result["hints"] = self._generate_hints(problem)
        
        return result
    
    def _generate_detailed_steps(self, problem: str, solution: Dict) -> List[Dict]:
        """生成详细解题步骤"""
        steps = []
        
        if solution["category"] == "algebra":
            steps = [
                {
                    "step": 1,
                    "description": "分析问题，识别方程类型",
                    "detail": f"问题: {problem}"
                },
                {
                    "step": 2, 
                    "description": "提取数学方程",
                    "detail": f"方程: {solution.get('equation', '未知')}"
                },
                {
                    "step": 3,
                    "description": "移项整理方程",
                    "detail": "将方程整理为标准形式"
                },
                {
                    "step": 4,
                    "description": "求解方程",
                    "detail": f"解: {', '.join(solution.get('solution', []))}"
                }
            ]
        
        elif solution["category"] == "geometry":
            steps = [
                {
                    "step": 1,
                    "description": "识别几何图形",
                    "detail": f"图形: {solution.get('shape', '未知')}"
                },
                {
                    "step": 2,
                    "description": "提取已知参数", 
                    "detail": f"参数: {solution}"
                },
                {
                    "step": 3,
                    "description": "应用几何公式",
                    "detail": f"公式: {solution.get('formula', '未知')}"
                },
                {
                    "step": 4,
                    "description": "计算结果",
                    "detail": f"结果: {solution.get('area', '未知')}"
                }
            ]
        
        return steps
    
    def _generate_hints(self, problem: str) -> List[str]:
        """生成解题提示"""
        hints = []
        
        if '方程' in problem:
            hints.extend([
                "尝试将方程整理为标准形式",
                "注意正负号的变化",
                "检查解是否满足原方程"
            ])
        
        elif '面积' in problem:
            hints.extend([
                "确认图形的类型",
                "找到正确的面积公式", 
                "检查单位是否一致"
            ])
        
        return hints