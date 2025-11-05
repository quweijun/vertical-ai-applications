from typing import Dict, List, Any
from datetime import datetime, timedelta
import math

class ExamPreparer:
    """考试准备助手"""
    
    def __init__(self):
        self.study_methods = self._initialize_study_methods()
        self.exam_types = self._initialize_exam_types()
        self.review_strategies = self._initialize_review_strategies()
    
    def _initialize_study_methods(self) -> Dict:
        """初始化学习方法"""
        return {
            "concept_mapping": "概念图法 - 建立知识之间的联系",
            "active_recall": "主动回忆 - 测试自己的记忆",
            "spaced_repetition": "间隔重复 - 定期复习巩固",
            "practice_testing": "模拟测试 - 检验学习效果",
            "teaching_others": "教授他人 - 加深理解"
        }
    
    def _initialize_exam_types(self) -> Dict:
        """初始化考试类型"""
        return {
            "multiple_choice": {
                "strategies": [
                    "仔细阅读所有选项",
                    "排除明显错误的选项",
                    "注意绝对性词语",
                    "利用上下文线索"
                ]
            },
            "essay": {
                "strategies": [
                    "先列提纲再写作",
                    "明确主题句",
                    "提供具体例子",
                    "注意文章结构"
                ]
            },
            "problem_solving": {
                "strategies": [
                    "展示解题过程",
                    "检查计算步骤",
                    "验证答案合理性",
                    "注意单位格式"
                ]
            }
        }
    
    def _initialize_review_strategies(self) -> Dict:
        """初始化复习策略"""
        return {
            "1_day": "重点复习核心概念和公式",
            "1_week": "系统复习所有知识点，做模拟题",
            "1_month": "分阶段复习，注重知识整合"
        }
    
    def create_study_plan(self, subjects: List[str], exam_date: str, 
                         current_level: str, target_score: str, 
                         study_time_per_day: int = 2) -> Dict[str, Any]:
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
            "study_time_per_day": f"{study_time_per_day}小时",
            "total_study_hours": days_until_exam * study_time_per_day,
            "weekly_schedule": self._create_weekly_schedule(subjects, days_until_exam),
            "milestones": self._set_milestones(days_until_exam),
            "study_methods": self._select_study_methods(current_level, target_score),
            "progress_tracking": self._setup_progress_tracking(subjects),
            "exam_strategies": self._get_exam_strategies(subjects),
            "stress_management": self._get_stress_management_tips(days_until_exam)
        }
        
        return study_plan
    
    def _calculate_days_until(self, exam_date: str) -> int:
        """计算距离考试的天数"""
        try:
            exam = datetime.strptime(exam_date, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return (exam - today).days
        except ValueError:
            return -1
    
    def _create_weekly_schedule(self, subjects: List[str], total_days: int) -> List[Dict]:
        """创建周计划"""
        weekly_schedule = []
        weeks = math.ceil(total_days / 7)
        
        for week in range(1, weeks + 1):
            week_plan = {
                "week": week,
                "focus_subjects": [],
                "weekly_goals": [],
                "study_sessions": []
            }
            
            # 分配重点科目
            subjects_per_week = min(2, len(subjects))
            start_index = (week - 1) * subjects_per_week % len(subjects)
            week_subjects = subjects[start_index:start_index + subjects_per_week]
            week_plan["focus_subjects"] = week_subjects
            
            # 设置周目标
            if week == 1:
                week_plan["weekly_goals"] = [
                    "掌握基础概念",
                    "完成基础练习",
                    "建立知识框架"
                ]
            elif week == weeks:
                week_plan["weekly_goals"] = [
                    "全面复习",
                    "模拟考试",
                    "查漏补缺"
                ]
            else:
                week_plan["weekly_goals"] = [
                    "深入学习重点难点",
                    "提高解题速度",
                    "加强综合应用"
                ]
            
            # 安排学习时段
            study_sessions = []
            for day in range(1, 8):
                if (week - 1) * 7 + day <= total_days:
                    session = {
                        "day": f"第{(week-1)*7+day}天",
                        "subjects": week_subjects,
                        "tasks": self._generate_daily_tasks(week_subjects, week, total_days)
                    }
                    study_sessions.append(session)
            
            week_plan["study_sessions"] = study_sessions
            weekly_schedule.append(week_plan)
        
        return weekly_schedule
    
    def _generate_daily_tasks(self, subjects: List[str], week: int, total_days: int) -> List[str]:
        """生成每日学习任务"""
        tasks = []
        
        for subject in subjects:
            base_tasks = {
                "math": ["复习公式", "做练习题", "分析错题"],
                "physics": ["理解概念", "做实验题", "应用公式"],
                "chemistry": ["记忆元素", "练习方程式", "理解反应"]
            }
            
            subject_tasks = base_tasks.get(subject, ["复习知识点", "做练习题"])
            tasks.extend(subject_tasks)
        
        # 根据学习阶段调整任务
        if week == 1:
            tasks.append("建立知识框架")
        elif week > total_days // 2:
            tasks.append("重点难点突破")
        
        if week % 2 == 0:  # 每两周一次模拟
            tasks.append("进行模拟测试")
        
        return list(set(tasks))  # 去重
    
    def _set_milestones(self, total_days: int) -> List[Dict]:
        """设置里程碑"""
        milestones = []
        
        checkpoints = [
            (total_days * 0.75, "完成第一轮复习"),
            (total_days * 0.5, "完成重点难点学习"),
            (total_days * 0.25, "完成模拟测试阶段"),
            (7, "最后冲刺阶段")
        ]
        
        for days_left, milestone in checkpoints:
            if days_left < total_days:
                milestones.append({
                    "days_before_exam": int(days_left),
                    "milestone": milestone,
                    "target": f"考前{int(days_left)}天完成"
                })
        
        return milestones
    
    def _select_study_methods(self, current_level: str, target_score: str) -> List[str]:
        """选择学习方法"""
        methods = []
        
        if current_level == "beginner":
            methods.extend([
                self.study_methods["concept_mapping"],
                self.study_methods["active_recall"]
            ])
        elif current_level == "intermediate":
            methods.extend([
                self.study_methods["spaced_repetition"],
                self.study_methods["practice_testing"]
            ])
        else:  # advanced
            methods.extend([
                self.study_methods["teaching_others"],
                self.study_methods["practice_testing"]
            ])
        
        if target_score == "excellent":
            methods.append("深入探究和拓展学习")
        
        return methods
    
    def _setup_progress_tracking(self, subjects: List[str]) -> Dict[str, Any]:
        """设置进度跟踪"""
        tracking = {
            "subjects": {},
            "weekly_reviews": [],
            "adjustment_criteria": []
        }
        
        for subject in subjects:
            tracking["subjects"][subject] = {
                "completion_percentage": 0,
                "weak_areas": [],
                "strengths": [],
                "last_reviewed": None
            }
        
        tracking["adjustment_criteria"] = [
            "如果某个科目进度落后，增加该科目的学习时间",
            "如果模拟测试成绩不理想，调整学习方法",
            "如果学习效率下降，适当休息调整"
        ]
        
        return tracking
    
    def _get_exam_strategies(self, subjects: List[str]) -> Dict[str, Any]:
        """获取考试策略"""
        return {
            "general_strategies": [
                "先易后难，确保拿到基础分",
                "合理分配时间，避免在某题上耗时过多",
                "仔细审题，理解题目要求",
                "检查答案，避免粗心错误"
            ],
            "subject_specific": {
                subject: self._get_subject_strategies(subject) for subject in subjects
            },
            "time_management": self._get_time_management_tips()
        }
    
    def _get_subject_strategies(self, subject: str) -> List[str]:
        """获取科目特定策略"""
        strategies = {
            "math": [
                "注意公式的正确应用",
                "检查计算过程的准确性",
                "几何题要画图辅助思考"
            ],
            "physics": [
                "注意单位的统一",
                "理解物理过程的本质",
                "应用合适的物理定律"
            ],
            "chemistry": [
                "注意化学方程式的配平",
                "理解物质的性质变化",
                "注意实验条件和安全"
            ]
        }
        return strategies.get(subject, ["系统复习，全面准备"])
    
    def _get_time_management_tips(self) -> List[str]:
        """获取时间管理建议"""
        return [
            "考前一周：全面复习，做模拟题",
            "考前一天：复习重点，调整状态",
            "考试当天：保持冷静，正常发挥"
        ]
    
    def _get_stress_management_tips(self, days_until_exam: int) -> Dict[str, Any]:
        """获取压力管理建议"""
        tips = {
            "study_phase": [
                "保持规律作息",
                "适当体育锻炼",
                "合理安排休息"
            ],
            "final_week": [
                "保证充足睡眠",
                "保持良好心态",
                "避免过度紧张"
            ],
            "exam_day": [
                "提前到达考场",
                "保持平静心态",
                "相信自己的准备"
            ]
        }
        
        if days_until_exam <= 7:
            phase = "final_week"
        elif days_until_exam <= 1:
            phase = "exam_day"
        else:
            phase = "study_phase"
        
        return {
            "current_phase": phase,
            "tips": tips[phase],
            "additional_advice": "考试只是检验学习的一种方式，保持平常心很重要"
        }
    
    def generate_review_plan(self, subjects: List[str], weak_areas: Dict[str, List[str]], 
                           days_available: int) -> Dict[str, Any]:
        """生成复习计划"""
        return {
            "subjects": subjects,
            "review_period": f"{days_available}天",
            "focused_review_areas": weak_areas,
            "daily_review_schedule": self._create_review_schedule(subjects, weak_areas, days_available),
            "review_methods": self._select_review_methods(weak_areas),
            "effectiveness_check": self._setup_effectiveness_check()
        }
    
    def _create_review_schedule(self, subjects: List[str], weak_areas: Dict, 
                              days_available: int) -> List[Dict]:
        """创建复习计划表"""
        schedule = []
        
        for day in range(1, days_available + 1):
            daily_plan = {
                "day": day,
                "focus_subject": subjects[(day - 1) % len(subjects)],
                "review_topics": weak_areas.get(subjects[(day - 1) % len(subjects)], ["综合复习"]),
                "review_methods": ["主动回忆", "错题分析", "模拟练习"]
            }
            schedule.append(daily_plan)
        
        return schedule
    
    def _select_review_methods(self, weak_areas: Dict) -> List[str]:
        """选择复习方法"""
        methods = []
        
        for subject, areas in weak_areas.items():
            if "概念理解" in areas:
                methods.append("概念图复习法")
            if "计算错误" in areas:
                methods.append("针对性练习")
            if "应用能力" in areas:
                methods.append("综合应用题训练")
        
        return list(set(methods)) if methods else ["全面系统复习"]
    
    def _setup_effectiveness_check(self) -> Dict[str, Any]:
        """设置效果检查"""
        return {
            "checkpoints": [
                "每周进行一次模拟测试",
                "定期回顾错题本",
                "评估各科目掌握程度"
            ],
            "improvement_indicators": [
                "模拟测试成绩提高",
                "解题速度加快",
                "概念理解加深"
            ],
            "adjustment_strategies": [
                "如果进步不明显，调整学习方法",
                "如果某些领域仍然薄弱，增加专项训练",
                "如果学习效率下降，检查学习环境和方法"
            ]
        }