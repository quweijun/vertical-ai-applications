import sympy as sp
from typing import Dict, List, Any
from .math_solver import MathSolver

class StepByStepSolver:
    """分步解题器"""
    
    def __init__(self):
        self.math_solver = MathSolver()
    
    def solve_with_steps(self, problem: str) -> Dict[str, Any]:
        """分步解决数学问题"""
        basic_solution = self.math_solver.solve(problem)
        
        if "error" in basic_solution:
            return basic_solution
        
        detailed_steps = self._generate_detailed_steps(problem, basic_solution)
        hints = self._generate_hints(problem)
        
        result = basic_solution.copy()
        result["detailed_steps"] = detailed_steps
        result["hints"] = hints
        result["learning_points"] = self._extract_learning_points(basic_solution)
        
        return result
    
    def _generate_detailed_steps(self, problem: str, solution: Dict) -> List[Dict[str, str]]:
        """生成详细解题步骤"""
        category = solution.get("category", "general")
        
        if category == "algebra":
            return self._generate_algebra_steps(problem, solution)
        elif category == "geometry":
            return self._generate_geometry_steps(problem, solution)
        elif category == "calculus":
            return self._generate_calculus_steps(problem, solution)
        else:
            return self._generate_general_steps(problem, solution)
    
    def _generate_algebra_steps(self, problem: str, solution: Dict) -> List[Dict[str, str]]:
        """生成代数解题步骤"""
        steps = [
            {
                "step": 1,
                "title": "理解问题",
                "description": f"分析问题: {problem}",
                "detail": "识别问题类型和已知条件"
            },
            {
                "step": 2,
                "title": "建立方程",
                "description": f"建立数学方程: {solution.get('equation', '未知')}",
                "detail": "根据问题描述建立对应的数学方程"
            },
            {
                "step": 3,
                "title": "解方程",
                "description": "求解方程",
                "detail": "使用代数方法求解方程"
            },
            {
                "step": 4,
                "title": "验证解",
                "description": f"得到解: {', '.join(solution.get('solutions', []))}",
                "detail": "验证解是否符合原问题要求"
            }
        ]
        return steps
    
    def _generate_geometry_steps(self, problem: str, solution: Dict) -> List[Dict[str, str]]:
        """生成几何解题步骤"""
        steps = [
            {
                "step": 1,
                "title": "识别图形",
                "description": f"识别几何图形: {solution.get('shape', '未知')}",
                "detail": "确定几何图形的类型和特征"
            },
            {
                "step": 2,
                "title": "提取参数",
                "description": "提取已知参数",
                "detail": f"已知参数: { {k: v for k, v in solution.items() if k in ['radius', 'length', 'width', 'height']} }"
            },
            {
                "step": 3,
                "title": "应用公式",
                "description": f"应用公式: {solution.get('formula', '未知')}",
                "detail": "使用相应的几何公式进行计算"
            },
            {
                "step": 4,
                "title": "计算结果",
                "description": f"计算结果: {solution.get('area', solution.get('volume', '未知'))}",
                "detail": "完成计算并检查单位"
            }
        ]
        return steps
    
    def _generate_calculus_steps(self, problem: str, solution: Dict) -> List[Dict[str, str]]:
        """生成微积分解题步骤"""
        steps = [
            {
                "step": 1,
                "title": "识别问题类型",
                "description": f"问题类型: {solution.get('type', '未知')}",
                "detail": "确定是求导、积分还是其他微积分问题"
            },
            {
                "step": 2,
                "title": "分析函数",
                "description": f"函数: {solution.get('function', '未知')}",
                "detail": "分析函数的性质和特点"
            },
            {
                "step": 3,
                "title": "应用微积分规则",
                "description": "应用相应的微积分规则",
                "detail": "使用导数公式或积分方法"
            },
            {
                "step": 4,
                "title": "计算结果",
                "description": f"结果: {solution.get('derivative', solution.get('integral', '未知'))}",
                "detail": "完成计算并简化表达式"
            }
        ]
        return steps
    
    def _generate_general_steps(self, problem: str, solution: Dict) -> List[Dict[str, str]]:
        """生成通用解题步骤"""
        return [
            {
                "step": 1,
                "title": "分析问题",
                "description": "理解问题要求",
                "detail": "仔细阅读问题，确定需要求解的内容"
            },
            {
                "step": 2,
                "title": "制定策略",
                "description": "制定解题策略",
                "detail": "选择合适的数学方法和工具"
            },
            {
                "step": 3,
                "title": "执行计算",
                "description": "进行计算",
                "detail": "按照策略执行计算步骤"
            },
            {
                "step": 4,
                "title": "检查结果",
                "description": "验证结果合理性",
                "detail": "检查结果是否符合预期和实际情况"
            }
        ]
    
    def _generate_hints(self, problem: str) -> List[str]:
        """生成解题提示"""
        hints = []
        
        if '方程' in problem:
            hints.extend([
                "尝试将方程整理为标准形式 ax + b = 0",
                "注意等式两边的平衡",
                "检查解是否满足原方程"
            ])
        
        if '面积' in problem or '体积' in problem:
            hints.extend([
                "确认图形的类型和尺寸",
                "找到正确的面积或体积公式",
                "注意单位的一致性"
            ])
        
        if '导数' in problem:
            hints.extend([
                "回忆基本函数的导数公式",
                "注意链式法则的应用",
                "检查结果的符号和形式"
            ])
        
        if not hints:
            hints = [
                "仔细阅读题目，理解要求",
                "列出已知条件和未知量",
                "选择合适的方法和公式",
                "分步骤计算，避免错误"
            ]
        
        return hints
    
    def _extract_learning_points(self, solution: Dict) -> List[str]:
        """提取学习要点"""
        category = solution.get("category", "general")
        
        learning_points = {
            "algebra": [
                "代数方程的建立方法",
                "方程求解的基本技巧",
                "解的验证方法"
            ],
            "geometry": [
                "几何图形的性质",
                "面积体积计算公式",
                "空间想象能力"
            ],
            "calculus": [
                "导数的概念和计算",
                "微积分基本定理",
                "函数的变化率分析"
            ],
            "general": [
                "数学问题分析方法",
                "逻辑推理能力",
                "计算准确性"
            ]
        }
        
        return learning_points.get(category, ["数学思维训练"])