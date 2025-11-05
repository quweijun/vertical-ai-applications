"""
响应格式化器
"""

from typing import Dict, List, Any
import json

class ResponseFormatter:
    """响应格式化器"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """加载模板"""
        return {
            'code': """
```{language}
{code}