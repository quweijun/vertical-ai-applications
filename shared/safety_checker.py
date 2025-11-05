"""
安全检查器
"""

import re
from typing import Dict, List, Any

class SafetyChecker:
    """安全检查器"""
    
    def __init__(self):
        self.unsafe_patterns = {
            'harmful_content': [
                r'暴力', r'伤害', r'攻击', r'自杀', r'自残',
                r'炸弹', r'武器', r'毒品', r'非法'
            ],
            'medical_risks': [
                r'确诊', r'治疗', r'用药指导', r'手术',
                r'急诊', r'重症', r'癌症'
            ],
            'financial_risks': [
                r'投资建议', r'买入', r'卖出', r'保证收益',
                r'内幕', r'操纵'
            ],
            'privacy_violation': [
                r'个人信息', r'身份证', r'银行卡', r'密码'
            ]
        }
        
        self.domain_specific_rules = {
            'medical': [
                "不能提供诊断",
                "不能开具处方", 
                "紧急情况建议立即就医",
                "信息仅供参考"
            ],
            'financial': [
                "不构成投资建议",
                "市场有风险，投资需谨慎",
                "过去表现不代表未来收益"
            ],
            'education': [
                "答案仅供参考",
                "鼓励独立思考",
                "注重学习过程"
            ]
        }
    
    def check_safety(self, text: str, domain: str = None) -> Dict[str, Any]:
        """安全检查"""
        issues = []
        
        # 检查不安全内容
        for category, patterns in self.unsafe_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append({
                        "category": category,
                        "pattern": pattern,
                        "severity": self._get_severity(category)
                    })
        
        # 领域特定检查
        if domain and domain in self.domain_specific_rules:
            domain_issues = self._check_domain_safety(text, domain)
            issues.extend(domain_issues)
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "domain": domain,
            "recommendation": self._generate_recommendation(issues)
        }
    
    def _get_severity(self, category: str) -> str:
        """获取严重程度"""
        severity_map = {
            'harmful_content': 'high',
            'medical_risks': 'high', 
            'financial_risks': 'medium',
            'privacy_violation': 'medium'
        }
        return severity_map.get(category, 'low')
    
    def _check_domain_safety(self, text: str, domain: str) -> List[Dict]:
        """检查领域安全性"""
        issues = []
        rules = self.domain_specific_rules.get(domain, [])
        
        # 这里可以添加更复杂的领域特定检查逻辑
        if domain == 'medical':
            if any(word in text for word in ['诊断', '确诊', '处方']):
                issues.append({
                    "category": "medical_practice",
                    "description": "涉及医疗实践",
                    "severity": "high"
                })
        
        elif domain == 'financial':
            if any(word in text for word in ['保证收益', '稳赚', '内幕']):
                issues.append({
                    "category": "financial_advice",
                    "description": "不当投资建议",
                    "severity": "high"
                })
        
        return issues
    
    def _generate_recommendation(self, issues: List[Dict]) -> str:
        """生成建议"""
        if not issues:
            return "内容安全"
        
        high_severity = any(issue["severity"] == "high" for issue in issues)
        if high_severity:
            return "建议拒绝或修改内容"
        else:
            return "建议添加免责声明"
    
    def add_disclaimer(self, text: str, domain: str = None) -> str:
        """添加免责声明"""
        disclaimers = {
            'medical': "重要提示：本信息仅供参考，不能替代专业医疗建议。如有不适，请及时就医。",
            'financial': "风险提示：投资有风险，入市需谨慎。本信息不构成投资建议。",
            'education': "说明：本解答仅供参考，建议结合教材和课堂学习。",
            'general': "请注意：本信息仅供参考，请结合实际情况判断。"
        }
        
        disclaimer = disclaimers.get(domain, disclaimers['general'])
        return f"{text}\n\n{disclaimer}"
