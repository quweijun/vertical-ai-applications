import random
from typing import Dict, List, Any
from datetime import datetime

class SubjectTutor:
    """学科辅导老师"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.learning_progress = {}
    
    def _initialize_knowledge_base(self) -> Dict:
        """初始化知识库"""
        return {
            "math": {
                "elementary": {
                    "topics": ["加减法", "乘除法", "分数", "小数", "几何基础"],
                    "difficulty": "easy"
                },
                "middle": {
                    "topics": ["代数", "几何", "概率", "统计", "函数"],
                    "difficulty": "medium"
                },
                "high": {
                    "topics": ["微积分", "线性代数", "概率论", "数理统计", "离散数学"],
                    "difficulty": "hard"
                }
            },
            "physics": {
                "elementary": {
                    "topics": ["力学基础", "热学", "光学", "电学基础"],
                    "difficulty": "easy"
                },
                "middle": {
                    "topics": ["牛顿力学", "电磁学", "波动光学", "热力学"],
                    "difficulty": "medium"
                },
                "high": {
                    "topics": ["相对论", "量子力学", "统计物理", "电动力学"],
                    "difficulty": "hard"
                }
            },
            "chemistry": {
                "elementary": {
                    "topics": ["元素周期表", "化学反应", "溶液", "气体定律"],
                    "difficulty": "easy"
                },
                "middle": {
                    "topics": ["化学平衡", "电化学", "有机化学", "分析化学"],
                    "difficulty": "medium"
                },
                "high": {
                    "topics": ["物理化学", "结构化学", "高分子化学", "生物化学"],
                    "difficulty": "hard"
                }
            }
        }
    
    def get_learning_path(self, subject: str, level: str, student_level: str) -> Dict[str, Any]:
        """获取学习路径"""
        if subject not in self.knowledge_base:
            return {"error": f"不支持学科: {subject}"}
        
        if level not in self.knowledge_base[subject]:
            return {"error": f"不支持难度级别: {level}"}
        
        subject_data = self.knowledge_base[subject][level]
        
        # 根据学生水平调整学习路径
        adjusted_topics = self._adjust_topics_by_level(subject_data["topics"], student_level)
        
        learning_path = {
            "subject": subject,
            "level": level,
            "recommended_topics": adjusted_topics,
            "estimated_duration": self._estimate_duration(level, len(adjusted_topics)),
            "learning_objectives": self._generate_learning_objectives(subject, level),
            "assessment_criteria": self._get_assessment_criteria(level)
        }
        
        return learning_path
    
    def _adjust_topics_by_level(self, topics: List[str], student_level: str) -> List[str]:
        """根据学生水平调整主题"""
        if student_level == "beginner":
            return topics[:3]  # 只推荐前3个主题
        elif student_level == "intermediate":
            return topics
        else:  # advanced
            return topics + ["进阶应用", "综合练习"]
    
    def _estimate_duration(self, level: str, topic_count: int) -> str:
        """估计学习时长"""
        base_hours = {
            "easy": 2,
            "medium": 4,
            "hard": 6
        }
        total_hours = base_hours.get(level, 3) * topic_count
        return f"{total_hours}小时"
    
    def _generate_learning_objectives(self, subject: str, level: str) -> List[str]:
        """生成学习目标"""
        objectives = {
            "math": {
                "easy": ["掌握基本运算", "理解数学概念", "解决简单问题"],
                "medium": ["应用数学方法", "分析复杂问题", "培养逻辑思维"],
                "hard": ["掌握高级数学工具", "进行数学证明", "解决实际问题"]
            },
            "physics": {
                "easy": ["理解物理现象", "掌握基本定律", "进行简单实验"],
                "medium": ["应用物理原理", "分析物理过程", "解决物理问题"],
                "hard": ["掌握理论物理", "进行科学研究", "创新物理应用"]
            }
        }
        return objectives.get(subject, {}).get(level, ["完成学习任务"])
    
    def _get_assessment_criteria(self, level: str) -> Dict[str, Any]:
        """获取评估标准"""
        criteria = {
            "easy": {
                "understanding": "基本概念理解",
                "application": "简单问题解决",
                "mastery": "基础技能掌握"
            },
            "medium": {
                "understanding": "原理深入理解", 
                "application": "复杂问题分析",
                "mastery": "方法灵活运用"
            },
            "hard": {
                "understanding": "理论系统掌握",
                "application": "创新问题解决", 
                "mastery": "高级技能应用"
            }
        }
        return criteria.get(level, {})
    
    def generate_practice_problems(self, subject: str, topic: str, difficulty: str, count: int = 5) -> Dict[str, Any]:
        """生成练习题"""
        problem_templates = self._get_problem_templates(subject, topic)
        
        if not problem_templates:
            return {"error": f"找不到 {subject} - {topic} 的练习题模板"}
        
        problems = []
        for i in range(min(count, len(problem_templates))):
            template = random.choice(problem_templates)
            problem = self._generate_problem_from_template(template, difficulty)
            problems.append(problem)
        
        return {
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "problems": problems,
            "total_count": len(problems),
            "estimated_time": f"{len(problems) * 5}分钟"
        }
    
    def _get_problem_templates(self, subject: str, topic: str) -> List[Dict]:
        """获取问题模板"""
        templates = {
            "math": {
                "代数": [
                    {
                        "template": "解方程: {a}x + {b} = {c}",
                        "variables": {"a": (1, 10), "b": (1, 20), "c": (10, 50)},
                        "solution": "x = (c - b) / a"
                    },
                    {
                        "template": "计算表达式: ({a} + {b}) × {c}",
                        "variables": {"a": (1, 10), "b": (1, 10), "c": (2, 5)},
                        "solution": "(a + b) * c"
                    }
                ],
                "几何": [
                    {
                        "template": "计算半径为 {r} 的圆的面积",
                        "variables": {"r": (1, 10)},
                        "solution": "π * r²"
                    }
                ]
            },
            "physics": {
                "力学": [
                    {
                        "template": "质量为 {m}kg 的物体，受到 {f}N 的力，求加速度",
                        "variables": {"m": (1, 10), "f": (5, 50)},
                        "solution": "a = f / m"
                    }
                ]
            }
        }
        return templates.get(subject, {}).get(topic, [])
    
    def _generate_problem_from_template(self, template: Dict, difficulty: str) -> Dict[str, Any]:
        """从模板生成问题"""
        problem_text = template["template"]
        variables = {}
        
        for var, range_val in template["variables"].items():
            if difficulty == "easy":
                value = random.randint(range_val[0], min(range_val[1], 5))
            elif difficulty == "medium":
                value = random.randint(range_val[0], range_val[1])
            else:  # hard
                value = random.randint(range_val[0] * 2, range_val[1] * 2)
            
            variables[var] = value
            problem_text = problem_text.replace(f"{{{var}}}", str(value))
        
        return {
            "problem": problem_text,
            "variables": variables,
            "hint": self._generate_hint(template["solution"]),
            "solution_formula": template["solution"]
        }
    
    def _generate_hint(self, solution_formula: str) -> str:
        """生成提示"""
        hints = {
            "x = (c - b) / a": "先移项，再除以系数",
            "(a + b) * c": "先计算括号内的加法",
            "π * r²": "使用圆的面积公式",
            "a = f / m": "使用牛顿第二定律"
        }
        return hints.get(solution_formula, "仔细分析问题，应用相关公式")

class HomeworkHelper:
    """作业助手"""
    
    def __init__(self):
        self.tutor = SubjectTutor()
    
    def analyze_homework(self, homework_description: str, subject: str) -> Dict[str, Any]:
        """分析作业"""
        analysis = {
            "homework_description": homework_description,
            "subject": subject,
            "identified_topics": [],
            "difficulty_level": "unknown",
            "estimated_time": "未知",
            "suggested_approach": [],
            "resources": []
        }
        
        # 识别主题
        analysis["identified_topics"] = self._identify_topics(homework_description, subject)
        
        # 评估难度
        analysis["difficulty_level"] = self._assess_difficulty(homework_description)
        
        # 估计时间
        analysis["estimated_time"] = self._estimate_completion_time(analysis["identified_topics"], analysis["difficulty_level"])
        
        # 建议方法
        analysis["suggested_approach"] = self._suggest_approach(subject, analysis["identified_topics"])
        
        # 学习资源
        analysis["resources"] = self._recommend_resources(subject, analysis["identified_topics"])
        
        return analysis
    
    def _identify_topics(self, description: str, subject: str) -> List[str]:
        """识别主题"""
        topic_keywords = {
            "math": {
                "代数": ["方程", "代数", "变量", "表达式"],
                "几何": ["三角形", "圆形", "面积", "体积", "角度"],
                "统计": ["平均", "概率", "数据", "图表"]
            },
            "physics": {
                "力学": ["力", "运动", "加速度", "牛顿"],
                "电学": ["电路", "电流", "电压", "电阻"],
                "光学": ["光", "反射", "折射", "透镜"]
            }
        }
        
        identified = []
        subjects_topics = topic_keywords.get(subject, {})
        
        for topic, keywords in subjects_topics.items():
            if any(keyword in description for keyword in keywords):
                identified.append(topic)
        
        return identified if identified else ["综合题目"]
    
    def _assess_difficulty(self, description: str) -> str:
        """评估难度"""
        easy_indicators = ["简单", "基础", "计算", "直接"]
        hard_indicators = ["证明", "推导", "分析", "综合", "复杂"]
        
        if any(indicator in description for indicator in hard_indicators):
            return "困难"
        elif any(indicator in description for indicator in easy_indicators):
            return "简单"
        else:
            return "中等"
    
    def _estimate_completion_time(self, topics: List[str], difficulty: str) -> str:
        """估计完成时间"""
        base_time = len(topics) * 15  # 每个主题15分钟
        multiplier = {"简单": 0.7, "中等": 1.0, "困难": 1.5}
        total_minutes = base_time * multiplier.get(difficulty, 1.0)
        
        if total_minutes < 60:
            return f"{int(total_minutes)}分钟"
        else:
            return f"{int(total_minutes // 60)}小时{int(total_minutes % 60)}分钟"
    
    def _suggest_approach(self, subject: str, topics: List[str]) -> List[str]:
        """建议解题方法"""
        approaches = {
            "math": [
                "仔细阅读题目，理解要求",
                "列出已知条件和未知量",
                "选择合适的公式或方法",
                "分步骤计算，检查每一步",
                "验证答案的合理性"
            ],
            "physics": [
                "分析物理过程",
                "画出受力图或电路图", 
                "应用物理定律和公式",
                "注意单位换算",
                "检查量纲一致性"
            ]
        }
        return approaches.get(subject, [
            "理解题目要求",
            "分析解题思路", 
            "逐步解决问题",
            "检查最终答案"
        ])
    
    def _recommend_resources(self, subject: str, topics: List[str]) -> List[str]:
        """推荐学习资源"""
        resources = {
            "math": ["数学公式手册", "例题解析", "在线计算器"],
            "physics": ["物理定律总结", "实验指导", "单位换算表"],
            "chemistry": ["元素周期表", "化学方程式", "实验安全指南"]
        }
        return resources.get(subject, ["教科书", "课堂笔记", "在线资料"])

class ExamPreparer:
    """考试准备助手"""
    
    def __init__(self):
        self.study_plans = {}
    
    def create_study_plan(self, subjects: List[str], exam_date: str, 
                         current_level: str, target_score: str) -> Dict[str, Any]:
        """创建学习计划"""
        days_until_exam = self._calculate_days_until(exam_date)
        
        if days_until_exam <= 0:
            return {"error": "考试日期已过或无效"}
        
        study_plan = {
            "subjects": subjects,
            "exam_date": exam_date,
            "days_until_exam": days_until_exam,
            "current_level": current_level,
            "target_score": target_score,
            "daily_schedule": self._create_daily_schedule(subjects, days_until_exam),
            "weekly_goals": self._set_weekly_goals(subjects, days_until_exam),
            "review_schedule": self._create_review_schedule(days_until_exam),
            "preparation_tips": self._get_preparation_tips(current_level, target_score)
        }
        
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.study_plans[plan_id] = study_plan
        
        study_plan["plan_id"] = plan_id
        return study_plan
    
    def _calculate_days_until(self, exam_date: str) -> int:
        """计算距离考试的天数"""
        try:
            exam = datetime.strptime(exam_date, "%Y-%m-%d")
            today = datetime.now()
            return (exam - today).days
        except:
            return -1
    
    def _create_daily_schedule(self, subjects: List[str], total_days: int) -> List[Dict]:
        """创建每日学习计划"""
        schedule = []
        subjects_count = len(subjects)
        
        for day in range(1, min(total_days, 30) + 1):  # 最多显示30天
            daily_plan = {
                "day": day,
                "focus_subjects": [],
                "study_time": "2-3小时",
                "tasks": []
            }
            
            # 轮换重点科目
            focus_index = (day - 1) % subjects_count
            daily_plan["focus_subjects"].append(subjects[focus_index])
            
            # 添加复习科目
            if day > 1:
                review_index = (day - 2) % subjects_count
                if subjects[review_index] not in daily_plan["focus_subjects"]:
                    daily_plan["focus_subjects"].append(subjects[review_index])
            
            # 生成学习任务
            for subject in daily_plan["focus_subjects"]:
                daily_plan["tasks"].extend(self._generate_daily_tasks(subject, day))
            
            schedule.append(daily_plan)
        
        return schedule
    
    def _generate_daily_tasks(self, subject: str, day: int) -> List[str]:
        """生成每日学习任务"""
        base_tasks = {
            "math": ["复习公式", "做练习题", "分析错题"],
            "physics": ["理解概念", "做实验题", "应用公式"],
            "chemistry": ["记忆元素", "练习方程式", "理解反应"]
        }
        
        tasks = base_tasks.get(subject, ["复习知识点", "做练习题"])
        
        # 根据学习天数调整任务
        if day % 7 == 0:  # 每周进行一次模拟测试
            tasks.append("进行模拟测试")
        if day % 3 == 0:  # 每3天进行一次重点复习
            tasks.append("重点难点复习")
        
        return tasks
    
    def _set_weekly_goals(self, subjects: List[str], total_days: int) -> List[Dict]:
        """设置每周目标"""
        weekly_goals = []
        weeks = (total_days + 6) // 7  # 计算总周数
        
        for week in range(1, weeks + 1):
            goal = {
                "week": week,
                "goals": [],
                "focus": ""
            }
            
            if week == 1:
                goal["focus"] = "基础知识巩固"
                goal["goals"] = ["掌握基本概念", "完成基础练习"]
            elif week == weeks:  # 最后一周
                goal["focus"] = "全面复习和模拟"
                goal["goals"] = ["进行模拟考试", "查漏补缺", "调整状态"]
            else:
                goal["focus"] = "能力提升"
                goal["goals"] = ["提高解题速度", "攻克难点", "综合应用"]
            
            weekly_goals.append(goal)
        
        return weekly_goals
    
    def _create_review_schedule(self, total_days: int) -> Dict[str, Any]:
        """创建复习计划"""
        return {
            "daily_review": "每天花30分钟复习前一天的内容",
            "weekly_review": "每周末进行本周知识总结",
            "mock_exams": [
                f"第{total_days-14}天: 第一次模拟考试",
                f"第{total_days-7}天: 第二次模拟考试",
                f"第{total_days-3}天: 最后一次模拟考试"
            ] if total_days > 14 else ["根据剩余时间安排模拟考试"]
        }
    
    def _get_preparation_tips(self, current_level: str, target_score: str) -> List[str]:
        """获取备考建议"""
        tips = [
            "制定合理的学习计划并坚持执行",
            "注重基础知识的学习和巩固",
            "定期进行模拟测试检验学习效果",
            "保持良好的作息和饮食习惯",
            "考试前适当放松，调整心态"
        ]
        
        if current_level == "较差" and target_score == "优秀":
            tips.extend([
                "重点突破基础题型",
                "建立错题本，定期复习",
                "寻求老师或同学的帮助"
            ])
        elif current_level == "中等" and target_score == "优秀":
            tips.extend([
                "加强综合应用能力",
                "提高解题速度和准确率",
                "注重考试技巧训练"
            ])
        
        return tips