"""
基础模型类
提供统一的AI模型接口和安全检查
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import json
from .safety_checker import SafetyChecker

class BaseAIModel(ABC):
    """AI模型基类"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        self.safety_checker = SafetyChecker()
        self.usage_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "safety_blocks": 0
        }
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """生成响应 - 子类必须实现"""
        pass
    
    def safe_generate(self, prompt: str, domain: str = None, **kwargs) -> Dict[str, Any]:
        """安全生成响应"""
        self.usage_stats["total_requests"] += 1
        
        # 输入安全检查
        input_safety = self.safety_checker.check_content(prompt, domain)
        if not input_safety["is_safe"]:
            self.usage_stats["safety_blocks"] += 1
            return {
                "success": False,
                "error": "输入内容不符合安全要求",
                "safety_issues": input_safety["issues"],
                "response": None,
                "usage_stats": self.usage_stats
            }
        
        try:
            # 生成响应
            response = self.generate_response(prompt, **kwargs)
            
            # 响应安全检查
            response_safety = self.safety_checker.check_content(response, domain)
            if not response_safety["is_safe"]:
                self.usage_stats["safety_blocks"] += 1
                response = "抱歉，我无法提供这个信息。请咨询相关专业人士。"
            
            # 添加免责声明
            if domain:
                response = self.safety_checker.add_disclaimer(response, domain)
            
            self.usage_stats["successful_requests"] += 1
            
            return {
                "success": True,
                "response": response,
                "safety_check": response_safety,
                "usage_stats": self.usage_stats
            }
            
        except Exception as e:
            self.usage_stats["failed_requests"] += 1
            return {
                "success": False,
                "error": f"生成响应时出错: {str(e)}",
                "response": None,
                "usage_stats": self.usage_stats
            }
    
    def get_usage_statistics(self) -> Dict[str, int]:
        """获取使用统计"""
        return self.usage_stats.copy()
    
    def reset_statistics(self):
        """重置统计信息"""
        self.usage_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "safety_blocks": 0
        }

class MockModel(BaseAIModel):
    """模拟模型（用于演示和测试）"""
    
    def __init__(self, model_name: str = "mock_model"):
        super().__init__(model_name)
        self.responses = self._load_default_responses()
    
    def _load_default_responses(self) -> Dict[str, str]:
        """加载默认响应"""
        return {
            "code_generation": """def example_function(input_data):
    \"\"\"
    示例函数实现
    \"\"\"
    # 这里是生成的代码
    result = process_data(input_data)
    return result

# 使用示例
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    output = example_function(data)
    print(f"处理结果: {output}")""",
            
            "math_solving": """解题步骤：
1. 分析问题：理解题目要求
2. 建立模型：将问题转化为数学表达式
3. 求解计算：应用数学方法求解
4. 验证结果：检查答案的合理性

最终答案: 需要具体问题具体分析""",
            
            "medical_advice": """基于您描述的症状，建议：

1. 多休息，保证充足睡眠
2. 保持水分补充
3. 如有持续或加重症状，请及时就医

注意：本建议仅供参考，不能替代专业医疗诊断。""",
            
            "financial_analysis": """投资分析：

当前市场情况需要谨慎对待。
建议：
1. 分散投资风险
2. 关注长期价值
3. 定期评估投资组合

风险提示：投资有风险，入市需谨慎。""",
            
            "education_tutoring": """学习建议：

1. 理解基本概念
2. 多做练习题巩固
3. 定期复习已学内容
4. 寻求老师指导解惑

记住：持续的努力是成功的关键。"""
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """生成模拟响应"""
        # 简单的关键词匹配
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['代码', '编程', 'function', 'def']):
            return self.responses["code_generation"]
        elif any(word in prompt_lower for word in ['数学', '方程', '计算', 'solve']):
            return self.responses["math_solving"]
        elif any(word in prompt_lower for word in ['医疗', '症状', '医生', '健康']):
            return self.responses["medical_advice"]
        elif any(word in prompt_lower for word in ['金融', '投资', '股票', '风险']):
            return self.responses["financial_analysis"]
        elif any(word in prompt_lower for word in ['学习', '教育', '作业', '考试']):
            return self.responses["education_tutoring"]
        else:
            return "这是一个模拟响应。在实际应用中，这里会调用真实的AI模型生成更准确和详细的回答。"
    
    def add_custom_response(self, category: str, response: str):
        """添加自定义响应"""
        self.responses[category] = response
    
    def set_response_mapping(self, keyword: str, response: str):
        """设置关键词映射"""
        self.responses[keyword] = response