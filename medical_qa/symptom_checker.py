from typing import Dict, List, Any
import re

class SymptomChecker:
    """症状检查器"""
    
    def __init__(self):
        self.symptom_questions = self._initialize_questions()
        self.emergency_keywords = ['胸痛', '呼吸困难', '昏迷', '大出血', '意识丧失']
    
    def _initialize_questions(self) -> Dict:
        """初始化症状问题库"""
        return {
            'fever': {
                'question': '您有发烧吗？体温多少度？',
                'follow_up': '发烧持续多久了？',
                'severity_question': '发烧的程度如何？'
            },
            'pain': {
                'question': '您感觉疼痛吗？在哪个部位？',
                'follow_up': '疼痛的程度如何（1-10分）？',
                'severity_question': '疼痛的性质是怎样的？'
            },
            'respiratory': {
                'question': '您有咳嗽、呼吸困难或胸痛吗？',
                'follow_up': '这些症状持续多久了？',
                'severity_question': '症状对日常活动的影响程度？'
            },
            'digestive': {
                'question': '您有恶心、呕吐、腹泻或腹痛吗？',
                'follow_up': '症状出现多久了？',
                'severity_question': '能否正常进食？'
            }
        }
    
    def interactive_check(self, initial_symptoms: List[str]) -> Dict[str, Any]:
        """交互式症状检查"""
        check_result = {
            "current_symptoms": initial_symptoms,
            "additional_questions": [],
            "risk_assessment": "低风险",
            "urgency_level": "常规",
            "recommendation": "建议观察，如有加重请就医",
            "emergency_warning": False
        }
        
        # 检查紧急情况
        emergency_symptoms = [symptom for symptom in initial_symptoms 
                            if any(keyword in symptom for keyword in self.emergency_keywords)]
        
        if emergency_symptoms:
            check_result.update({
                "risk_assessment": "高风险",
                "urgency_level": "紧急",
                "recommendation": "建议立即就医或拨打急救电话",
                "emergency_warning": True
            })
            return check_result
        
        # 生成跟进问题
        for symptom in initial_symptoms:
            symptom_lower = symptom.lower()
            
            if any(word in symptom_lower for word in ['发烧', '发热', '体温']):
                check_result["additional_questions"].append(
                    self.symptom_questions['fever']['question']
                )
            
            if any(word in symptom_lower for word in ['疼痛', '痛', '酸痛']):
                check_result["additional_questions"].append(
                    self.symptom_questions['pain']['question']
                )
            
            if any(word in symptom_lower for word in ['咳嗽', '呼吸', '气喘', '胸痛']):
                check_result["additional_questions"].append(
                    self.symptom_questions['respiratory']['question']
                )
            
            if any(word in symptom_lower for word in ['恶心', '呕吐', '腹泻', '腹痛']):
                check_result["additional_questions"].append(
                    self.symptom_questions['digestive']['question']
                )
        
        # 风险评估
        symptom_count = len(initial_symptoms)
        if symptom_count >= 3:
            check_result["risk_assessment"] = "中风险"
            check_result["urgency_level"] = "尽快就医"
            check_result["recommendation"] = "建议尽快就医检查"
        
        # 特定症状风险升级
        if any(symptom in ['高烧', '持续发烧', '剧烈头痛'] for symptom in initial_symptoms):
            check_result["risk_assessment"] = "中高风险"
            check_result["urgency_level"] = "尽快就医"
        
        return check_result
    
    def assess_symptom_severity(self, symptom: str, responses: Dict[str, str]) -> Dict[str, Any]:
        """评估症状严重程度"""
        severity_score = 0
        factors = []
        
        symptom_lower = symptom.lower()
        
        # 持续时间评估
        if 'duration' in responses:
            duration = responses['duration']
            if '天' in duration or '周' in duration:
                try:
                    days = int(re.search(r'\d+', duration).group())
                    if days > 7:
                        severity_score += 2
                        factors.append("症状持续时间较长")
                    elif days > 3:
                        severity_score += 1
                        factors.append("症状持续数天")
                except:
                    pass
        
        # 严重程度评估
        if 'severity' in responses:
            severity = responses['severity']
            if any(word in severity for word in ['严重', '剧烈', '非常']):
                severity_score += 3
                factors.append("症状程度严重")
            elif any(word in severity for word in ['中度', '明显']):
                severity_score += 2
                factors.append("症状程度中等")
            else:
                severity_score += 1
        
        # 影响评估
        if 'impact' in responses:
            impact = responses['impact']
            if any(word in impact for word in ['无法', '严重影响', '不能']):
                severity_score += 2
                factors.append("严重影响日常活动")
        
        # 确定严重等级
        if severity_score >= 5:
            severity_level = "严重"
            recommendation = "建议立即就医"
        elif severity_score >= 3:
            severity_level = "中等"
            recommendation = "建议尽快就医"
        else:
            severity_level = "轻微"
            recommendation = "建议观察，如有加重请就医"
        
        return {
            "symptom": symptom,
            "severity_score": severity_score,
            "severity_level": severity_level,
            "factors": factors,
            "recommendation": recommendation
        }
    
    def generate_self_care_advice(self, symptoms: List[str]) -> List[str]:
        """生成自我护理建议"""
        advice = []
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            
            if any(word in symptom_lower for word in ['发烧', '发热']):
                advice.extend([
                    "多喝水，保持水分",
                    "适当休息，避免劳累",
                    "可以使用物理降温方法",
                    "注意观察体温变化"
                ])
            
            if any(word in symptom_lower for word in ['咳嗽', '感冒']):
                advice.extend([
                    "多喝温水",
                    "避免吸烟和刺激性气体",
                    "保持室内空气流通",
                    "可以使用蜂蜜水缓解咳嗽"
                ])
            
            if any(word in symptom_lower for word in ['头痛']):
                advice.extend([
                    "在安静环境中休息",
                    "避免强光和噪音",
                    "可以适当按摩太阳穴",
                    "保持规律的作息时间"
                ])
        
        # 通用建议
        advice.extend([
            "保持充足的睡眠",
            "均衡饮食，多吃蔬菜水果",
            "避免过度劳累",
            "注意个人卫生"
        ])
        
        return list(set(advice))  # 去重