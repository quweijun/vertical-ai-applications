import re
from typing import Dict, List, Any
from datetime import datetime, timedelta

class HomeworkHelper:
    """作业助手"""
    
    def __init__(self):
        self.subject_keywords = self._initialize_subject_keywords()
        self.difficulty_indicators = self._initialize_difficulty_indicators()
        self.problem_solving_strategies = self._initialize_strategies()
    
    def _initialize_subject_keywords(self) -> Dict:
        """初始化学科关键词"""
        return {
            "math": {
                "algebra": ["方程", "代数", "变量", "表达式", "不等式"],
                "geometry": ["三角形", "圆形", "面积", "体积", "角度", "平行"],
                "calculus": ["导数", "积分", "微分", "极限", "函数"],
                "statistics": ["概率", "统计", "平均数", "方差", "图表"]
            },
            "physics": {
                "mechanics": ["力", "运动", "加速度", "牛顿", "动量", "能量"],
                "electromagnetism": ["电路", "电流", "电压", "电阻", "磁场", "电场"],
                "optics": ["光", "反射", "折射", "透镜", "成像"],
                "thermodynamics": ["热", "温度", "热量", "熵", "热机"]
            },
            "chemistry": {
                "reactions": ["反应", "化学式", "平衡", "氧化", "还原"],
                "periodic": ["元素", "周期表", "原子", "分子", "化学键"],
                "organic": ["有机", "烃", "醇", "酸", "酯"],
                "analytical": ["浓度", "pH", "滴定", "分析"]
            }
        }
    
    def _initialize_difficulty_indicators(self) -> Dict:
        """初始化难度指示词"""
        return {
            "easy": ["简单", "基础", "计算", "直接", "基本"],
            "medium": ["应用", "分析", "理解", "推导", "证明"],
            "hard": ["复杂", "综合", "创新", "探究", "研究", "难题"]
        }
    
    def _initialize_strategies(self) -> Dict:
        """初始化解题策略"""
        return {
            "math": [
                "仔细阅读题目，理解问题要求",
                "列出已知条件和未知量",
                "选择合适的公式或方法",
                "分步骤计算，确保每一步正确",
                "验证答案的合理性",
                "检查计算过程和单位"
            ],
            "physics": [
                "分析物理过程和现象",
                "画出受力图、电路图或示意图",
                "应用物理定律和公式",
                "注意单位换算和量纲一致性",
                "考虑边界条件和特殊情况",
                "验证结果的物理意义"
            ],
            "chemistry": [
                "理解化学反应的本质",
                "写出完整的化学方程式",
                "注意物质的量和化学计量",
                "考虑反应条件和影响因素",
                "分析物质的性质和变化",
                "验证化学平衡和反应限度"
            ]
        }
    
    def analyze_homework(self, homework_description: str, subject: str = None) -> Dict[str, Any]:
        """分析作业要求"""
        if subject is None:
            subject = self._detect_subject(homework_description)
        
        analysis = {
            "homework_description": homework_description,
            "detected_subject": subject,
            "identified_topics": self._identify_topics(homework_description, subject),
            "difficulty_level": self._assess_difficulty(homework_description),
            "estimated_time": self._estimate_completion_time(homework_description, subject),
            "key_concepts": self._extract_key_concepts(homework_description, subject),
            "suggested_approach": self._suggest_approach(subject),
            "learning_objectives": self._identify_learning_objectives(homework_description),
            "common_mistakes": self._warn_common_mistakes(subject),
            "resources": self._recommend_resources(subject)
        }
        
        return analysis
    
    def _detect_subject(self, description: str) -> str:
        """检测学科"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['方程', '函数', '几何', '概率']):
            return "math"
        elif any(word in description_lower for word in ['力', '运动', '电路', '光']):
            return "physics"
        elif any(word in description_lower for word in ['化学', '反应', '元素', '分子']):
            return "chemistry"
        else:
            return "general"
    
    def _identify_topics(self, description: str, subject: str) -> List[str]:
        """识别主题"""
        topics = []
        description_lower = description.lower()
        
        if subject in self.subject_keywords:
            for topic, keywords in self.subject_keywords[subject].items():
                if any(keyword in description_lower for keyword in keywords):
                    topics.append(topic)
        
        return topics if topics else ["综合应用"]
    
    def _assess_difficulty(self, description: str) -> str:
        """评估难度"""
        description_lower = description.lower()
        
        # 检查难度指示词
        for level, indicators in self.difficulty_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                if level == "hard":
                    return "困难"
                elif level == "medium":
                    return "中等"
        
        # 基于问题特征评估
        if any(word in description_lower for word in ['证明', '推导', '分析', '探究']):
            return "困难"
        elif any(word in description_lower for word in ['应用', '计算', '求解']):
            return "中等"
        else:
            return "简单"
    
    def _estimate_completion_time(self, description: str, subject: str) -> str:
        """估计完成时间"""
        difficulty = self._assess_difficulty(description)
        topic_count = len(self._identify_topics(description, subject))
        
        # 基础时间估算
        base_time_per_topic = {
            "简单": 15,  # 分钟
            "中等": 30,
            "困难": 45
        }
        
        total_minutes = base_time_per_topic.get(difficulty, 30) * max(1, topic_count)
        
        # 考虑问题复杂度调整
        if '综合' in description or '多个' in description:
            total_minutes *= 1.5
        
        if total_minutes < 60:
            return f"约{int(total_minutes)}分钟"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"约{int(hours)}小时{int(minutes)}分钟"
    
    def _extract_key_concepts(self, description: str, subject: str) -> List[str]:
        """提取关键概念"""
        concepts = []
        
        if subject == "math":
            if any(word in description for word in ['方程', '等式']):
                concepts.extend(["方程求解", "代数运算", "变量关系"])
            if any(word in description for word in ['几何', '图形']):
                concepts.extend(["几何性质", "空间关系", "图形计算"])
        
        elif subject == "physics":
            if any(word in description for word in ['力', '运动']):
                concepts.extend(["牛顿定律", "运动学", "力学分析"])
            if any(word in description for word in ['电路', '电流']):
                concepts.extend(["电路原理", "欧姆定律", "电功率"])
        
        return concepts if concepts else [f"{subject}基本概念"]
    
    def _suggest_approach(self, subject: str) -> List[str]:
        """建议解题方法"""
        return self.problem_solving_strategies.get(subject, [
            "理解问题要求",
            "分析已知条件",
            "制定解题计划",
            "执行计算分析",
            "检查验证结果"
        ])
    
    def _identify_learning_objectives(self, description: str) -> List[str]:
        """识别学习目标"""
        objectives = []
        
        if any(word in description for word in ['计算', '求解']):
            objectives.append("掌握计算方法")
        
        if any(word in description for word in ['证明', '推导']):
            objectives.append("培养逻辑推理能力")
        
        if any(word in description for word in ['分析', '解释']):
            objectives.append("提高分析理解能力")
        
        if any(word in description for word in ['应用', '实际']):
            objectives.append("增强实际应用能力")
        
        return objectives if objectives else ["完成学习任务"]
    
    def _warn_common_mistakes(self, subject: str) -> List[str]:
        """警告常见错误"""
        mistakes = {
            "math": [
                "计算粗心错误",
                "公式应用错误",
                "单位不一致",
                "符号错误"
            ],
            "physics": [
                "概念理解错误",
                "公式适用条件忽略",
                "单位换算错误",
                "物理意义理解偏差"
            ],
            "chemistry": [
                "化学式写错",
                "反应条件忽略",
                "计量计算错误",
                "物质性质混淆"
            ]
        }
        return mistakes.get(subject, ["注意审题和计算"])
    
    def _recommend_resources(self, subject: str) -> List[str]:
        """推荐学习资源"""
        resources = {
            "math": ["数学公式手册", "例题解析", "在线计算器", "几何画板"],
            "physics": ["物理定律总结", "实验指导", "单位换算表", "模拟实验"],
            "chemistry": ["元素周期表", "化学方程式手册", "实验安全指南", "物质性质表"]
        }
        return resources.get(subject, ["教科书", "课堂笔记", "在线学习平台"])
    
    def generate_study_plan(self, homework_analysis: Dict, available_time: str) -> Dict[str, Any]:
        """生成学习计划"""
        time_estimate = homework_analysis["estimated_time"]
        topics = homework_analysis["identified_topics"]
        
        return {
            "homework_description": homework_analysis["homework_description"],
            "available_time": available_time,
            "suggested_schedule": self._create_schedule(topics, time_estimate, available_time),
            "study_tips": self._generate_study_tips(homework_analysis),
            "break_suggestions": self._suggest_breaks(time_estimate),
            "completion_checklist": self._create_checklist(topics)
        }
    
    def _create_schedule(self, topics: List[str], time_estimate: str, available_time: str) -> List[Dict]:
        """创建学习计划表"""
        schedule = []
        
        # 简化实现 - 平均分配时间给每个主题
        topic_count = len(topics)
        for i, topic in enumerate(topics):
            schedule.append({
                "topic": topic,
                "suggested_time": f"{30 // max(1, topic_count)}分钟",
                "order": i + 1,
                "focus": f"掌握{topic}相关概念和方法"
            })
        
        return schedule
    
    def _generate_study_tips(self, analysis: Dict) -> List[str]:
        """生成学习建议"""
        tips = [
            "先从简单的题目开始，建立信心",
            "遇到难题先标记，稍后回来解决",
            "定期复习已学内容",
            "保持良好的学习环境"
        ]
        
        if analysis["difficulty_level"] == "困难":
            tips.extend([
                "可以寻求老师或同学的帮助",
                "分解复杂问题为小问题",
                "多练习类似题目"
            ])
        
        return tips
    
    def _suggest_breaks(self, time_estimate: str) -> List[Dict]:
        """建议休息时间"""
        return [
            {"after": "25分钟学习", "break": "5分钟休息"},
            {"after": "50分钟学习", "break": "10分钟休息"},
            {"after": "2小时学习", "break": "15-20分钟休息"}
        ]
    
    def _create_checklist(self, topics: List[str]) -> List[Dict]:
        """创建完成检查表"""
        checklist = []
        for topic in topics:
            checklist.append({
                "item": f"完成{topic}相关练习",
                "completed": False,
                "priority": "高" if "综合" in topic else "中"
            })
        return checklist