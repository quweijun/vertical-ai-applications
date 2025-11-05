from typing import Dict, List, Any
from datetime import datetime, timedelta

class MedicalAdvisor:
    """医疗咨询助手"""
    
    def __init__(self):
        self.symptom_db = self._init_symptom_database()
        self.drug_db = self._init_drug_database()
        self.disclaimer = "重要提示：本建议仅供参考，不能替代专业医疗诊断。如有紧急情况请立即就医。"
    
    def _init_symptom_database(self) -> Dict:
        """初始化症状数据库"""
        return {
            'headache': {
                'name': '头痛',
                'possible_causes': ['紧张性头痛', '偏头痛', '感冒', '疲劳'],
                'self_care': ['休息', '保持水分', '避免强光', '适当按摩'],
                'see_doctor': '如持续不缓解或加重'
            },
            'fever': {
                'name': '发烧',
                'possible_causes': ['感染', '炎症', '免疫反应'],
                'self_care': ['多喝水', '物理降温', '充足休息'],
                'see_doctor': '体温超过39°C或持续3天以上'
            },
            'cough': {
                'name': '咳嗽',
                'possible_causes': ['感冒', '过敏', '支气管炎'],
                'self_care': ['多喝温水', '蜂蜜水', '避免刺激'],
                'see_doctor': '咳嗽持续2周以上或伴有胸痛'
            }
        }
    
    def _init_drug_database(self) -> Dict:
        """初始化药品数据库"""
        return {
            'paracetamol': {
                'name': '对乙酰氨基酚',
                'purpose': '退烧止痛',
                'dosage': '成人每次500mg，每日不超过4次',
                'precautions': ['不要超量', '避免饮酒']
            },
            'ibuprofen': {
                'name': '布洛芬',
                'purpose': '消炎止痛',
                'dosage': '成人每次200-400mg，每日3-4次',
                'precautions': ['饭后服用', '胃病患者慎用']
            }
        }
    
    def symptom_analysis(self, symptoms: List[str], age: int = None) -> Dict[str, Any]:
        """症状分析"""
        analysis = {
            "symptoms": symptoms,
            "possible_conditions": [],
            "self_care_advice": [],
            "when_to_see_doctor": [],
            "urgency": "low",
            "disclaimer": self.disclaimer
        }
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for key, info in self.symptom_db.items():
                if key in symptom_lower or info['name'] in symptom:
                    analysis["possible_conditions"].extend(info['possible_causes'])
                    analysis["self_care_advice"].extend(info['self_care'])
                    analysis["when_to_see_doctor"].append(info['see_doctor'])
        
        # 去重
        analysis["possible_conditions"] = list(set(analysis["possible_conditions"]))
        analysis["self_care_advice"] = list(set(analysis["self_care_advice"]))
        
        # 风险评估
        if len(symptoms) >= 3:
            analysis["urgency"] = "medium"
        if any(s in ['呼吸', '胸痛', '意识'] for s in symptoms):
            analysis["urgency"] = "high"
        
        return analysis
    
    def drug_information(self, drug_name: str) -> Dict[str, Any]:
        """药品信息查询"""
        drug_lower = drug_name.lower()
        
        for key, info in self.drug_db.items():
            if key in drug_lower or info['name'] in drug_name:
                return {
                    "drug_name": info['name'],
                    "purpose": info['purpose'],
                    "dosage": info['dosage'],
                    "precautions": info['precautions'],
                    "disclaimer": "请遵医嘱使用"
                }
        
        return {"error": f"未找到药品 '{drug_name}' 的信息"}
    
    def set_reminder(self, medication: str, schedule: Dict) -> Dict[str, Any]:
        """设置用药提醒"""
        reminder_id = f"med_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        reminder = {
            "id": reminder_id,
            "medication": medication,
            "schedule": schedule,
            "next_reminder": self._calculate_next_reminder(schedule),
            "created": datetime.now()
        }
        
        return {
            "reminder_id": reminder_id,
            "message": f"已设置 {medication} 提醒",
            "next_reminder": reminder["next_reminder"].strftime("%Y-%m-%d %H:%M")
        }
    
    def _calculate_next_reminder(self, schedule: Dict) -> datetime:
        """计算下次提醒时间"""
        now = datetime.now()
        if 'times_per_day' in schedule:
            times = schedule['times_per_day']
            interval = 24 // times
            return now + timedelta(hours=interval)
        return now + timedelta(hours=24)