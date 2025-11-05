"""
基础模型类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import json

class BaseAIModel(ABC):
    """AI模型基类"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        self.safety_checker = SafetyChecker()
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """生成响应"""
        pass
    
    def safe_generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """安全生成响应"""
        # 安全检查
        safety_result = self.safety_checker.check_safety(prompt)
        
        if not safety_result["is_safe"]:
            return {
                "success": False,
                "error": "输入内容不符合安全要求",
                "safety_issues": safety_result["issues"],
                "response": None
            }
        
        try:
            response = self.generate_response(prompt, **kwargs)
            
            # 检查响应安全性
            response_safety = self.safety_checker.check_safety(response)
            if not response_safety["is_safe"]:
                response = "抱歉，我无法提供这个信息。"
            
            return {
                "success": True,
                "response": response,
                "safety_check": response_safety
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

class MockModel(BaseAIModel):
    """模拟模型（用于演示）"""
    
    def __init__(self):
        super().__init__("mock_model")
        self.responses = self._load_responses()
    
    def _load_responses(self) -> Dict[str, str]:
        """加载模拟响应"""
        return {
            "代码生成": "这里是一个示例代码实现...",
            "数学解题": "解题步骤如下：1. 分析问题 2. 应用公式 3. 计算结果",
            "医疗建议": "建议多休息，如有持续症状请及时就医。",
            "金融分析": "基于当前数据，建议谨慎投资。",
            "学习辅导": "这个知识点需要重点掌握以下内容..."
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """生成模拟响应"""
        for key in self.responses:
            if key in prompt:
                return self.responses[key]
        
        return "这是一个模拟响应。在实际应用中，这里会调用真实的AI模型。"