from typing import Dict, List, Any
import random

class SubjectTutor:
    """学科辅导老师"""
    
    def __init__(self):
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> Dict:
        """初始化知识库"""
        return {
            "math": {
                "algebra": ["一次方程", "二次方程", "不等式", "函数"],
                "geometry": ["三角形", "圆形", "立体几何", "解析几何"],
                "calculus": ["导数", "积分", "极限"]
            },
            "physics": {
                "mechanics": ["运动学", "动力学", "静力学"],
                "electromagnetism": ["电路", "磁场", "电磁感应"],
                "optics": ["几何光学", "波动光学"]
            }
        }
    
    def get_learning_path(self, subject: str, level: str) -> Dict[str, Any]:
        """获取学习路径"""
        if subject not in self.knowledge_base:
            return {"error": f"不支持学科: {subject}"}
        
        topics = self.knowledge_base[subject]
        
        return {
            "subject": subject,
            "level": level,
            "recommended_topics": self._select_topics(topics, level),
            "study_plan": self._create_study_plan(level),
            "learning_goals": self._set_learning_goals(subject, level)
        }
    
    def _select_topics(self, topics: Dict, level: str) -> List[str]:
        """选择学习主题"""
        if level == "beginner":
            return [list(chapter.values())[0][0] for chapter in topics.values()][:2]
        elif level == "intermediate":
            selected = []
            for chapter in topics.values():
                selected.extend(chapter[:2])
            return selected
        else:  # advanced
            selected = []
            for chapter in topics.values():
                selected.extend(chapter)
            return selected
    
    def _create_study_plan(self, level: str) -> Dict[str, Any]:
        """创建学习计划"""
        plans = {
            "beginner": {
                "duration": "2周",
                "weekly_hours": 5,
                "focus": "基础概念掌握"
            },
            "intermediate": {
                "duration": "4周", 
                "weekly_hours": 8,
                "focus": "应用能力提升"
            },
            "advanced": {
                "duration": "6周",
                "weekly_hours": 12,
                "focus": "综合能力培养"
            }
        }
        return plans.get(level, plans["intermediate"])
    
    def _set_learning_goals(self, subject: str, level: str) -> List[str]:
        """设置学习目标"""
        goals = {
            "math": {
                "beginner": ["掌握基本概念", "解决简单问题"],
                "intermediate": ["应用数学方法", "分析复杂问题"],
                "advanced": ["解决实际问题", "培养数学思维"]
            },
            "physics": {
                "beginner": ["理解物理现象", "掌握基本定律"],
                "intermediate": ["应用物理原理", "解决物理问题"],
                "advanced": ["进行物理建模", "创新应用"]
            }
        }
        return goals.get(subject, {}).get(level, ["完成学习任务"])
    
    def generate_quiz(self, subject: str, topic: str, difficulty: str) -> Dict[str, Any]:
        """生成测验题目"""
        question_bank = self._get_question_bank(subject, topic)
        
        if not question_bank:
            return {"error": f"暂无{topic}相关题目"}
        
        questions = random.sample(question_bank, min(5, len(question_bank)))
        
        return {
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "questions": questions,
            "total_score": len(questions) * 10
        }
    
    def _get_question_bank(self, subject: str, topic: str) -> List[Dict]:
        """获取题目库"""
        bank = {
            "math": {
                "algebra": [
                    {
                        "question": "解方程: 2x + 5 = 13",
                        "options": ["x=4", "x=3", "x=5", "x=6"],
                        "answer": "x=4",
                        "explanation": "2x = 13 - 5 = 8, 所以 x = 4"
                    }
                ]
            }
        }
        return bank.get(subject, {}).get(topic, [])