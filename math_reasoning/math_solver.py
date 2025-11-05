import sympy as sp
import numpy as np
from typing import Dict, List, Any
import re

class MathSolver:
    """数学问题求解器"""
    
    def __init__(self):
        self.categories = ['algebra', 'calculus', 'geometry', 'statistics']
    
    def solve(self, problem: str) -> Dict[str, Any]:
        """解决数学问题"""
        category = self._classify_problem(problem)
        
        try:
            if category == 'algebra':
                return self._solve_algebra(problem)
            elif category == 'calculus':
                return self._solve_calculus(problem)
            elif category == 'geometry':
                return self._solve_geometry(problem)
            else:
                return self._solve_general(problem)
        except Exception as e:
            return {"error": f"求解失败: {str(e)}"}
    
    def _classify_problem(self, problem: str) -> str:
        """问题分类"""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ['方程', '代数', 'x=', 'y=']):
            return 'algebra'
        elif any(word in problem_lower for word in ['导数', '积分', '微分']):
            return 'calculus'
        elif any(word in problem_lower for word in ['面积', '体积', '三角形', '圆']):
            return 'geometry'
        else:
            return 'general'
    
    def _solve_algebra(self, problem: str) -> Dict[str, Any]:
        """解代数方程"""
        # 提取方程
        equation_match = re.search(r'([\dx+y=\.\-\+\*\/\(\)\s]+)', problem)
        if not equation_match:
            return {"error": "未找到有效方程"}
        
        equation_str = equation_match.group(1).replace(' ', '')
        x = sp.Symbol('x')
        
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
            "solutions": [str(sol) for sol in solution],
            "steps": self._generate_algebra_steps(equation, solution)
        }
    
    def _solve_calculus(self, problem: str) -> Dict[str, Any]:
        """解微积分问题"""
        x = sp.Symbol('x')
        
        if '导数' in problem:
            # 提取函数
            func_match = re.search(r'[yf]\(x\)\s*=\s*([^,]+)', problem)
            if func_match:
                func_str = func_match.group(1)
                func = sp.sympify(func_str)
                derivative = sp.diff(func, x)
                
                return {
                    "category": "calculus",
                    "type": "differentiation",
                    "function": str(func),
                    "derivative": str(derivative)
                }
        
        return {"error": "不支持的微积分问题类型"}
    
    def _solve_geometry(self, problem: str) -> Dict[str, Any]:
        """解几何问题"""
        numbers = re.findall(r'\d+\.?\d*', problem)
        numbers = [float(num) for num in numbers]
        
        if '圆' in problem and '面积' in problem and numbers:
            radius = numbers[0]
            area = np.pi * radius ** 2
            
            return {
                "category": "geometry",
                "shape": "圆",
                "radius": radius,
                "area": round(area, 2),
                "formula": "A = πr²"
            }
        
        return {"error": "不支持的几何问题类型"}
    
    def _solve_general(self, problem: str) -> Dict[str, Any]:
        """通用求解"""
        try:
            # 尝试计算算术表达式
            expr_match = re.search(r'([\d\.\+\-\*\/\(\)\s]+)', problem)
            if expr_match:
                expression = expr_match.group(1).replace(' ', '')
                result = eval(expression)
                
                return {
                    "category": "arithmetic",
                    "expression": expression,
                    "result": result
                }
        except:
            pass
        
        return {"error": "无法求解的问题"}
    
    def _generate_algebra_steps(self, equation, solutions) -> List[str]:
        """生成解题步骤"""
        steps = [
            f"步骤1: 给定方程 {equation}",
            "步骤2: 整理方程为标准形式",
            f"步骤3: 求解得到 {solutions}" if solutions else "步骤3: 方程无解"
        ]
        return steps