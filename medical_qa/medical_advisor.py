import re
from typing import Dict, List, Any
from datetime import datetime, timedelta

class MedicalAdvisor:
    """医疗顾问系统"""
    
    def __init__(self):
        self.symptom_database = self._load_symptom_database()
        self.drug_database = self._load_drug_database()
        self.medical_reminders = {}
        
        # 免责声明
        self.disclaimer = "重要提示：本系统提供的信息仅供参考，不能替代专业医疗建议。如有紧急情况，请立即就医。"
    
    def _load_symptom_database(self) -> Dict:
        """加载症状数据库"""
        return {
            'headache': {
                'name': '头痛',
                'possible_causes': ['紧张性头痛', '偏头痛', '感冒', '高血压', '视力问题'],
                'severity': 'medium',
                'self_care': ['休息', '保持水分', '避免强光', '按摩太阳穴'],
                'when_to_see_doctor': '如果头痛持续超过24小时或伴有其他症状'
            },
            'fever': {
                'name': '发烧',
                'possible_causes': ['感染', '炎症', '免疫反应', '中暑'],
                'severity': 'medium', 
                'self_care': ['多喝水', '休息', '物理降温', '服用退烧药'],
                'when_to_see_doctor': '体温超过39°C或持续超过3天'
            },
            'cough': {
                'name': '咳嗽',
                'possible_causes': ['感冒', '流感', '过敏', '支气管炎', '肺炎'],
                'severity': 'low',
                'self_care': ['多喝温水', '蜂蜜柠檬水', '避免刺激性食物', '使用加湿器'],
                'when_to_see_doctor': '咳嗽持续超过2周或伴有胸痛、呼吸困难'
            }
        }
    
    def _load_drug_database(self) -> Dict:
        """加载药品数据库"""
        return {
            'paracetamol': {
                'name': '对乙酰氨基酚',
                'purpose': '退烧、止痛',
                'dosage': '成人每次500mg，每日不超过4次',
                'side_effects': ['恶心', '皮疹', '肝功能损害（过量）'],
                'precautions': ['不要超过推荐剂量', '避免饮酒', '肝功能不全者慎用']
            },
            'ibuprofen': {
                'name': '布洛芬',
                'purpose': '消炎、止痛、退烧', 
                'dosage': '成人每次200-400mg，每日3-4次',
                'side_effects': ['胃部不适', '头晕', '过敏反应'],
                'precautions': ['饭后服用', '胃溃疡患者禁用', '避免长期使用']
            }
        }
    
    def analyze_symptoms(self, symptoms: List[str], age: int = None, 
                        preexisting_conditions: List[str] = None) -> Dict[str, Any]:
        """分析症状"""
        
        analysis = {
            "symptoms": symptoms,
            "possible_conditions": [],
            "recommended_actions": [],
            "urgency_level": "low",
            "disclaimer": self.disclaimer
        }
        
        # 分析每个症状
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            matched = False
            
            for key, info in self.symptom_database.items():
                if key in symptom_lower or info['name'] in symptom:
                    analysis["possible_conditions"].extend(info['possible_causes'])
                    analysis["recommended_actions"].extend(info['self_care'])
                    analysis["urgency_level"] = self._assess_urgency(info['severity'])
                    matched = True
            
            if not matched:
                analysis["possible_conditions"].append("需要进一步诊断")
                analysis["recommended_actions"].append("建议咨询医生")
        
        # 去重
        analysis["possible_conditions"] = list(set(analysis["possible_conditions"]))
        analysis["recommended_actions"] = list(set(analysis["recommended_actions"]))
        
        # 考虑年龄和现有疾病
        if age and age > 60:
            analysis["recommended_actions"].append("老年人建议尽早就医")
            analysis["urgency_level"] = self._escalate_urgency(analysis["urgency_level"])
        
        if preexisting_conditions:
            analysis["preexisting_considerations"] = "有基础疾病，建议谨慎对待"
        
        return analysis
    
    def get_drug_information(self, drug_name: str) -> Dict[str, Any]:
        """获取药品信息"""
        drug_lower = drug_name.lower()
        
        for key, info in self.drug_database.items():
            if key in drug_lower or info['name'] in drug_name:
                return {
                    "drug_name": info['name'],
                    "purpose": info['purpose'],
                    "dosage": info['dosage'],
                    "side_effects": info['side_effects'],
                    "precautions": info['precautions'],
                    "disclaimer": "请遵医嘱使用药物"
                }
        
        return {"error": f"未找到药品 '{drug_name}' 的信息"}
    
    def set_medication_reminder(self, drug_name: str, dosage: str, 
                              schedule: Dict[str, Any]) -> Dict[str, Any]:
        """设置用药提醒"""
        reminder_id = f"reminder_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        reminder = {
            "id": reminder_id,
            "drug_name": drug_name,
            "dosage": dosage,
            "schedule": schedule,
            "created_at": datetime.now(),
            "next_reminder": self._calculate_next_reminder(schedule)
        }
        
        self.medical_reminders[reminder_id] = reminder
        
        return {
            "reminder_id": reminder_id,
            "message": f"已设置 {drug_name} 的用药提醒",
            "next_reminder": reminder["next_reminder"].strftime("%Y-%m-%d %H:%M"),
            "schedule": schedule
        }
    
    def _assess_urgency(self, severity: str) -> str:
        """评估紧急程度"""
        urgency_map = {
            'low': '低',
            'medium': '中', 
            'high': '高'
        }
        return urgency_map.get(severity, '中')
    
    def _escalate_urgency(self, current_urgency: str) -> str:
        """提升紧急程度"""
        urgency_levels = ['低', '中', '高']
        current_index = urgency_levels.index(current_urgency)
        return urgency_levels[min(current_index + 1, len(urgency_levels) - 1)]
    
    def _calculate_next_reminder(self, schedule: Dict[str, Any]) -> datetime:
        """计算下一次提醒时间"""
        now = datetime.now()
        
        if 'times_per_day' in schedule:
            times = schedule['times_per_day']
            if times == 1:
                return now + timedelta(hours=24)
            elif times == 2:
                return now + timedelta(hours=12)
            elif times == 3:
                return now + timedelta(hours=8)
        
        return now + timedelta(hours=24)

class SymptomChecker:
    """症状检查器"""
    
    def __init__(self):
        self.symptom_questions = {
            'fever': {
                'question': '您有发烧吗？体温多少度？',
                'follow_up': '发烧持续多久了？'
            },
            'pain': {
                'question': '您感觉疼痛吗？在哪个部位？',
                'follow_up': '疼痛的程度如何（1-10分）？'
            },
            'respiratory': {
                'question': '您有咳嗽或呼吸困难吗？',
                'follow_up': '这些症状持续多久了？'
            }
        }
    
    def interactive_check(self, initial_symptoms: List[str]) -> Dict[str, Any]:
        """交互式症状检查"""
        check_result = {
            "current_symptoms": initial_symptoms,
            "additional_questions": [],
            "risk_assessment": "低风险",
            "recommendation": "建议观察"
        }
        
        # 根据初始症状生成跟进问题
        for symptom in initial_symptoms:
            symptom_lower = symptom.lower()
            
            if any(word in symptom_lower for word in ['发烧', '发热', '体温']):
                check_result["additional_questions"].append(
                    self.symptom_questions['fever']['question']
                )
            
            if any(word in symptom_lower for word in ['疼痛', '痛']):
                check_result["additional_questions"].append(
                    self.symptom_questions['pain']['question']
                )
            
            if any(word in symptom_lower for word in ['咳嗽', '呼吸', '气喘']):
                check_result["additional_questions"].append(
                    self.symptom_questions['respiratory']['question']
                )
        
        # 风险评估
        if len(initial_symptoms) >= 3:
            check_result["risk_assessment"] = "中风险"
            check_result["recommendation"] = "建议尽快就医"
        
        if any('呼吸' in symptom for symptom in initial_symptoms):
            check_result["risk_assessment"] = "高风险"
            check_result["recommendation"] = "建议立即就医"
        
        return check_result