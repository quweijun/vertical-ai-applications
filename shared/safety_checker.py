import re
from typing import Dict, List, Any

class SafetyChecker:
    """安全检查器"""
    
    def __init__(self):
        self.unsafe_patterns = {
            'harmful': [r'暴力', r'伤害', r'非法'],
            'medical_risk': [r'确诊', r'治疗', r'用药指导'],
            'financial_risk': [r'投资建议', r'保证收益']
        }
    
    def check_content(self, text: str, domain: str = None) -> Dict[str, Any]:
        """内容安全检查"""
        issues = []
        
        for category, patterns in self.unsafe_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append({
                        "category": category,
                        "issue": f"检测到{category}相关内容",
                        "severity": "high" if category in ['harmful', 'medical_risk'] else "medium"
                    })
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "recommendation": "通过" if not issues else "建议审核"
        }
    
    def add_disclaimer(self, text: str, domain: str) -> str:
        """添加免责声明"""
        disclaimers = {
            'medical': "医疗免责声明：本信息仅供参考，不能替代专业医疗建议。",
            'financial': "投资风险提示：市场有风险，投资需谨慎。",
            'education': "教育说明：本内容仅供参考学习。"
        }
        return f"{text}\n\n{disclaimers.get(domain, '')}"