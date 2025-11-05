"""
投资顾问模块
提供智能投资组合建议、资产配置和投资策略分析
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta
import math
from enum import Enum


class RiskTolerance(Enum):
    """风险承受能力等级"""
    CONSERVATIVE = "conservative"      # 保守型
    MODERATE = "moderate"             # 稳健型
    AGGRESSIVE = "aggressive"         # 进取型
    VERY_AGGRESSIVE = "very_aggressive"  # 激进型


class InvestmentGoal(Enum):
    """投资目标"""
    CAPITAL_PRESERVATION = "capital_preservation"  # 资本保值
    INCOME_GENERATION = "income_generation"        # 收益生成
    GROWTH = "growth"                             # 资本增长
    SPECULATION = "speculation"                   # 投机


class InvestmentHorizon(Enum):
    """投资期限"""
    SHORT_TERM = "short_term"     # 短期 (< 1年)
    MEDIUM_TERM = "medium_term"   # 中期 (1-5年)
    LONG_TERM = "long_term"       # 长期 (> 5年)


class InvestmentAdvisor:
    """智能投资顾问"""
    
    def __init__(self):
        self.risk_profiles = self._initialize_risk_profiles()
        self.asset_classes = self._initialize_asset_classes()
        self.investment_strategies = self._initialize_strategies()
        self.market_indicators = self._initialize_market_indicators()
        
    def _initialize_risk_profiles(self) -> Dict[str, Dict]:
        """初始化风险偏好配置"""
        return {
            RiskTolerance.CONSERVATIVE.value: {
                "description": "保守型投资者 - 注重本金安全，接受较低回报",
                "max_drawdown_tolerance": 0.10,  # 最大回撤容忍度
                "volatility_tolerance": 0.08,    # 波动率容忍度
                "target_return": 0.04,           # 目标年化回报
                "risk_score": 25
            },
            RiskTolerance.MODERATE.value: {
                "description": "稳健型投资者 - 平衡风险与回报",
                "max_drawdown_tolerance": 0.20,
                "volatility_tolerance": 0.12,
                "target_return": 0.07,
                "risk_score": 50
            },
            RiskTolerance.AGGRESSIVE.value: {
                "description": "进取型投资者 - 追求较高回报，接受较大波动",
                "max_drawdown_tolerance": 0.35,
                "volatility_tolerance": 0.18,
                "target_return": 0.10,
                "risk_score": 75
            },
            RiskTolerance.VERY_AGGRESSIVE.value: {
                "description": "激进型投资者 - 追求高回报，接受高风险",
                "max_drawdown_tolerance": 0.50,
                "volatility_tolerance": 0.25,
                "target_return": 0.15,
                "risk_score": 90
            }
        }
    
    def _initialize_asset_classes(self) -> Dict[str, Dict]:
        """初始化资产类别配置"""
        return {
            "stocks": {
                "name": "股票",
                "subclasses": {
                    "large_cap": {"name": "大盘股", "risk": "medium", "return": "medium_high"},
                    "small_cap": {"name": "小盘股", "risk": "high", "return": "high"},
                    "growth": {"name": "成长股", "risk": "high", "return": "high"},
                    "value": {"name": "价值股", "risk": "medium", "return": "medium"},
                    "dividend": {"name": "股息股", "risk": "low_medium", "return": "low_medium"}
                },
                "expected_return": 0.08,
                "volatility": 0.18,
                "correlation": {
                    "bonds": -0.2,
                    "cash": 0.1,
                    "real_estate": 0.6
                }
            },
            "bonds": {
                "name": "债券",
                "subclasses": {
                    "government": {"name": "国债", "risk": "low", "return": "low"},
                    "corporate": {"name": "企业债", "risk": "medium", "return": "medium"},
                    "high_yield": {"name": "高收益债", "risk": "high", "return": "high"},
                    "municipal": {"name": "市政债", "risk": "low_medium", "return": "low_medium"}
                },
                "expected_return": 0.04,
                "volatility": 0.06,
                "correlation": {
                    "stocks": -0.2,
                    "cash": 0.3,
                    "real_estate": 0.2
                }
            },
            "cash": {
                "name": "现金等价物",
                "subclasses": {
                    "savings": {"name": "储蓄存款", "risk": "very_low", "return": "very_low"},
                    "money_market": {"name": "货币基金", "risk": "very_low", "return": "very_low"},
                    "treasury_bills": {"name": "短期国债", "risk": "very_low", "return": "very_low"}
                },
                "expected_return": 0.02,
                "volatility": 0.01,
                "correlation": {
                    "stocks": 0.1,
                    "bonds": 0.3,
                    "real_estate": 0.1
                }
            },
            "real_estate": {
                "name": "房地产",
                "subclasses": {
                    "reits": {"name": "房地产信托", "risk": "medium", "return": "medium"},
                    "commercial": {"name": "商业地产", "risk": "medium_high", "return": "medium_high"},
                    "residential": {"name": "住宅地产", "risk": "medium", "return": "medium"}
                },
                "expected_return": 0.06,
                "volatility": 0.12,
                "correlation": {
                    "stocks": 0.6,
                    "bonds": 0.2,
                    "cash": 0.1
                }
            },
            "commodities": {
                "name": "大宗商品",
                "subclasses": {
                    "gold": {"name": "黄金", "risk": "medium", "return": "low_medium"},
                    "oil": {"name": "原油", "risk": "high", "return": "high"},
                    "agriculture": {"name": "农产品", "risk": "high", "return": "medium_high"}
                },
                "expected_return": 0.05,
                "volatility": 0.20,
                "correlation": {
                    "stocks": 0.3,
                    "bonds": 0.1,
                    "inflation": 0.7
                }
            }
        }
    
    def _initialize_strategies(self) -> Dict[str, Dict]:
        """初始化投资策略"""
        return {
            "value_investing": {
                "name": "价值投资",
                "description": "寻找被低估的优质公司，长期持有",
                "suitable_for": [RiskTolerance.MODERATE.value, RiskTolerance.AGGRESSIVE.value],
                "key_principle": "安全边际，买入价格低于内在价值",
                "holding_period": "长期",
                "risk_level": "中等"
            },
            "growth_investing": {
                "name": "成长投资",
                "description": "投资高成长潜力的公司，关注收入增长和市场份额",
                "suitable_for": [RiskTolerance.AGGRESSIVE.value],
                "key_principle": "投资未来增长，接受较高估值",
                "holding_period": "中长期",
                "risk_level": "较高"
            },
            "income_investing": {
                "name": "收益投资",
                "description": "关注稳定现金流和股息收入",
                "suitable_for": [RiskTolerance.CONSERVATIVE.value, RiskTolerance.MODERATE.value],
                "key_principle": "稳定收益，低波动性",
                "holding_period": "长期",
                "risk_level": "较低"
            },
            "index_investing": {
                "name": "指数投资",
                "description": "通过指数基金实现市场平均回报",
                "suitable_for": "所有风险类型",
                "key_principle": "市场有效性，低成本分散",
                "holding_period": "长期",
                "risk_level": "与市场同步"
            },
            "momentum_investing": {
                "name": "动量投资",
                "description": "跟随市场趋势，买入表现好的资产",
                "suitable_for": [RiskTolerance.AGGRESSIVE.value],
                "key_principle": "趋势延续，及时止损",
                "holding_period": "短期",
                "risk_level": "高"
            }
        }
    
    def _initialize_market_indicators(self) -> Dict[str, Dict]:
        """初始化市场指标"""
        return {
            "pe_ratio": {
                "name": "市盈率",
                "interpretation": {
                    "low": "可能被低估",
                    "medium": "合理估值",
                    "high": "可能被高估"
                },
                "thresholds": {
                    "low": 15,
                    "high": 25
                }
            },
            "shiller_pe": {
                "name": "席勒市盈率",
                "interpretation": {
                    "low": "市场低估",
                    "medium": "市场合理",
                    "high": "市场高估"
                },
                "thresholds": {
                    "low": 16,
                    "high": 25
                }
            },
            "dividend_yield": {
                "name": "股息率",
                "interpretation": {
                    "high": "收益有吸引力",
                    "low": "增长预期强"
                },
                "thresholds": {
                    "low": 0.02,
                    "high": 0.04
                }
            },
            "market_sentiment": {
                "name": "市场情绪",
                "indicators": ["VIX指数", "投资者信心指数", "资金流向"]
            }
        }
    
    def create_investment_portfolio(self, 
                                  risk_tolerance: str,
                                  investment_amount: float,
                                  investment_goal: str,
                                  time_horizon: str,
                                  age: int = None,
                                  income_stability: str = "stable") -> Dict[str, Any]:
        """创建个性化投资组合"""
        
        # 验证输入参数
        if risk_tolerance not in self.risk_profiles:
            return {"error": f"无效的风险偏好: {risk_tolerance}"}
        
        if investment_amount <= 0:
            return {"error": "投资金额必须大于0"}
        
        # 获取风险配置
        risk_profile = self.risk_profiles[risk_tolerance]
        
        # 生成资产配置
        asset_allocation = self._generate_asset_allocation(
            risk_tolerance, investment_goal, time_horizon, age
        )
        
        # 计算具体分配金额
        allocation_breakdown = self._calculate_allocation_breakdown(
            asset_allocation, investment_amount
        )
        
        # 生成具体投资建议
        investment_suggestions = self._generate_investment_suggestions(
            asset_allocation, risk_tolerance, time_horizon
        )
        
        # 预期表现分析
        expected_performance = self._calculate_expected_performance(
            asset_allocation, risk_profile
        )
        
        return {
            "portfolio_summary": {
                "risk_tolerance": risk_tolerance,
                "investment_amount": investment_amount,
                "investment_goal": investment_goal,
                "time_horizon": time_horizon,
                "age_considered": age is not None,
                "creation_date": datetime.now().strftime("%Y-%m-%d")
            },
            "asset_allocation": asset_allocation,
            "allocation_breakdown": allocation_breakdown,
            "investment_suggestions": investment_suggestions,
            "expected_performance": expected_performance,
            "risk_management": self._generate_risk_management_plan(risk_tolerance, time_horizon),
            "rebalancing_strategy": self._generate_rebalancing_strategy(time_horizon),
            "tax_considerations": self._generate_tax_considerations(investment_goal)
        }
    
    def _generate_asset_allocation(self, 
                                 risk_tolerance: str,
                                 investment_goal: str,
                                 time_horizon: str,
                                 age: int = None) -> Dict[str, float]:
        """生成资产配置比例"""
        
        # 基础配置基于风险偏好
        base_allocations = {
            RiskTolerance.CONSERVATIVE.value: {
                "stocks": 0.30, "bonds": 0.50, "cash": 0.15, "real_estate": 0.05, "commodities": 0.00
            },
            RiskTolerance.MODERATE.value: {
                "stocks": 0.55, "bonds": 0.30, "cash": 0.05, "real_estate": 0.08, "commodities": 0.02
            },
            RiskTolerance.AGGRESSIVE.value: {
                "stocks": 0.75, "bonds": 0.15, "cash": 0.03, "real_estate": 0.05, "commodities": 0.02
            },
            RiskTolerance.VERY_AGGRESSIVE.value: {
                "stocks": 0.85, "bonds": 0.05, "cash": 0.02, "real_estate": 0.05, "commodities": 0.03
            }
        }
        
        allocation = base_allocations.get(risk_tolerance, base_allocations[RiskTolerance.MODERATE.value]).copy()
        
        # 根据投资目标调整
        allocation = self._adjust_for_investment_goal(allocation, investment_goal)
        
        # 根据投资期限调整
        allocation = self._adjust_for_time_horizon(allocation, time_horizon)
        
        # 根据年龄调整（如果提供）
        if age is not None:
            allocation = self._adjust_for_age(allocation, age)
        
        # 确保总和为100%
        total = sum(allocation.values())
        if abs(total - 1.0) > 0.01:
            allocation = {k: v/total for k, v in allocation.items()}
        
        return allocation
    
    def _adjust_for_investment_goal(self, allocation: Dict[str, float], goal: str) -> Dict[str, float]:
        """根据投资目标调整配置"""
        adjustments = {
            InvestmentGoal.CAPITAL_PRESERVATION.value: {
                "stocks": -0.10, "bonds": +0.05, "cash": +0.05
            },
            InvestmentGoal.INCOME_GENERATION.value: {
                "stocks": -0.05, "bonds": +0.10, "dividend_stocks": +0.05
            },
            InvestmentGoal.GROWTH.value: {
                "stocks": +0.10, "bonds": -0.05, "cash": -0.05
            },
            InvestmentGoal.SPECULATION.value: {
                "stocks": +0.15, "commodities": +0.05, "cash": -0.10
            }
        }
        
        if goal in adjustments:
            for asset, adjustment in adjustments[goal].items():
                if asset in allocation:
                    allocation[asset] += adjustment
        
        # 确保比例在合理范围内
        return self._clamp_allocation(allocation)
    
    def _adjust_for_time_horizon(self, allocation: Dict[str, float], horizon: str) -> Dict[str, float]:
        """根据投资期限调整配置"""
        adjustments = {
            InvestmentHorizon.SHORT_TERM.value: {
                "stocks": -0.20, "cash": +0.20
            },
            InvestmentHorizon.MEDIUM_TERM.value: {
                # 中等期限保持相对平衡
            },
            InvestmentHorizon.LONG_TERM.value: {
                "stocks": +0.10, "cash": -0.10
            }
        }
        
        if horizon in adjustments:
            for asset, adjustment in adjustments[horizon].items():
                if asset in allocation:
                    allocation[asset] += adjustment
        
        return self._clamp_allocation(allocation)
    
    def _adjust_for_age(self, allocation: Dict[str, float], age: int) -> Dict[str, float]:
        """根据年龄调整配置（传统年龄法则：100-年龄投资股票）"""
        # 传统法则：股票比例 = 100 - 年龄
        traditional_stock_ratio = (100 - age) / 100
        
        # 现代调整：考虑寿命延长，更积极配置
        modern_stock_ratio = min(0.75, (110 - age) / 100)
        
        # 使用现代法则但保持保守
        target_stock_ratio = modern_stock_ratio
        
        current_stock_ratio = allocation.get("stocks", 0)
        adjustment = target_stock_ratio - current_stock_ratio
        
        # 调整股票和债券比例
        if adjustment > 0:
            # 需要增加股票
            bond_reduction = min(adjustment, allocation.get("bonds", 0))
            allocation["stocks"] += bond_reduction
            allocation["bonds"] -= bond_reduction
        else:
            # 需要减少股票
            stock_reduction = min(-adjustment, allocation.get("stocks", 0))
            allocation["stocks"] -= stock_reduction
            allocation["bonds"] += stock_reduction
        
        return self._clamp_allocation(allocation)
    
    def _clamp_allocation(self, allocation: Dict[str, float]) -> Dict[str, float]:
        """确保资产配置比例在合理范围内"""
        min_limits = {
            "stocks": 0.0, "bonds": 0.0, "cash": 0.02, 
            "real_estate": 0.0, "commodities": 0.0
        }
        
        max_limits = {
            "stocks": 0.95, "bonds": 0.80, "cash": 0.50,
            "real_estate": 0.20, "commodities": 0.10
        }
        
        clamped_allocation = {}
        for asset, ratio in allocation.items():
            min_val = min_limits.get(asset, 0.0)
            max_val = max_limits.get(asset, 1.0)
            clamped_allocation[asset] = max(min_val, min(ratio, max_val))
        
        # 重新标准化
        total = sum(clamped_allocation.values())
        if total > 0:
            clamped_allocation = {k: v/total for k, v in clamped_allocation.items()}
        
        return clamped_allocation
    
    def _calculate_allocation_breakdown(self, allocation: Dict[str, float], 
                                      investment_amount: float) -> Dict[str, Any]:
        """计算具体分配金额"""
        breakdown = {
            "total_amount": investment_amount,
            "allocations": {}
        }
        
        for asset_class, ratio in allocation.items():
            amount = investment_amount * ratio
            asset_info = self.asset_classes.get(asset_class, {})
            
            breakdown["allocations"][asset_class] = {
                "name": asset_info.get("name", asset_class),
                "allocation_ratio": ratio,
                "amount": round(amount, 2),
                "subclass_suggestions": self._get_subclass_suggestions(asset_class, ratio)
            }
        
        return breakdown
    
    def _get_subclass_suggestions(self, asset_class: str, ratio: float) -> List[Dict]:
        """获取子类别投资建议"""
        asset_info = self.asset_classes.get(asset_class, {})
        subclasses = asset_info.get("subclasses", {})
        
        suggestions = []
        for subclass_key, subclass_info in subclasses.items():
            # 基于风险特征分配子类别比例
            if ratio > 0:
                suggestion = {
                    "subclass": subclass_key,
                    "name": subclass_info["name"],
                    "suggested_ratio": self._calculate_subclass_ratio(subclass_info, ratio),
                    "risk_level": subclass_info["risk"],
                    "suitable_for": self._get_suitable_investors(subclass_info["risk"])
                }
                suggestions.append(suggestion)
        
        return suggestions
    
    def _calculate_subclass_ratio(self, subclass_info: Dict, total_ratio: float) -> float:
        """计算子类别分配比例"""
        # 简化实现 - 实际应该基于更复杂的逻辑
        risk_weights = {
            "very_low": 0.2,
            "low": 0.3,
            "low_medium": 0.4,
            "medium": 0.5,
            "medium_high": 0.6,
            "high": 0.7,
            "very_high": 0.8
        }
        
        risk_level = subclass_info.get("risk", "medium")
        weight = risk_weights.get(risk_level, 0.5)
        
        return min(total_ratio * weight, 0.3)  # 限制单个子类别最大比例
    
    def _get_suitable_investors(self, risk_level: str) -> List[str]:
        """获取适合的投资者类型"""
        risk_mapping = {
            "very_low": [RiskTolerance.CONSERVATIVE.value],
            "low": [RiskTolerance.CONSERVATIVE.value, RiskTolerance.MODERATE.value],
            "low_medium": [RiskTolerance.MODERATE.value],
            "medium": [RiskTolerance.MODERATE.value, RiskTolerance.AGGRESSIVE.value],
            "medium_high": [RiskTolerance.AGGRESSIVE.value],
            "high": [RiskTolerance.AGGRESSIVE.value, RiskTolerance.VERY_AGGRESSIVE.value],
            "very_high": [RiskTolerance.VERY_AGGRESSIVE.value]
        }
        
        return risk_mapping.get(risk_level, [RiskTolerance.MODERATE.value])
    
    def _generate_investment_suggestions(self, allocation: Dict[str, float],
                                       risk_tolerance: str,
                                       time_horizon: str) -> Dict[str, Any]:
        """生成具体投资建议"""
        
        # 选择投资策略
        strategy = self._select_investment_strategy(risk_tolerance, time_horizon)
        
        # 生成具体产品建议
        product_suggestions = self._generate_product_suggestions(allocation, risk_tolerance)
        
        return {
            "recommended_strategy": strategy,
            "product_suggestions": product_suggestions,
            "implementation_tips": self._generate_implementation_tips(strategy, time_horizon),
            "monitoring_schedule": self._generate_monitoring_schedule(time_horizon)
        }
    
    def _select_investment_strategy(self, risk_tolerance: str, time_horizon: str) -> Dict[str, Any]:
        """选择投资策略"""
        suitable_strategies = []
        
        for strategy_key, strategy_info in self.investment_strategies.items():
            if risk_tolerance in strategy_info.get("suitable_for", []):
                suitable_strategies.append({
                    "strategy": strategy_key,
                    "name": strategy_info["name"],
                    "description": strategy_info["description"],
                    "risk_level": strategy_info["risk_level"]
                })
        
        # 选择最适合的策略
        if suitable_strategies:
            # 简化选择逻辑 - 选择第一个合适的策略
            selected = suitable_strategies[0]
        else:
            # 默认策略
            selected = {
                "strategy": "index_investing",
                "name": "指数投资",
                "description": "通过指数基金实现市场平均回报",
                "risk_level": "与市场同步"
            }
        
        return selected
    
    def _generate_product_suggestions(self, allocation: Dict[str, float], 
                                    risk_tolerance: str) -> List[Dict]:
        """生成具体产品建议"""
        suggestions = []
        
        for asset_class, ratio in allocation.items():
            if ratio > 0.01:  # 只对比例大于1%的资产类别提供建议
                asset_suggestions = self._get_asset_class_products(asset_class, ratio, risk_tolerance)
                suggestions.extend(asset_suggestions)
        
        return suggestions
    
    def _get_asset_class_products(self, asset_class: str, ratio: float, 
                                risk_tolerance: str) -> List[Dict]:
        """获取资产类别的具体产品建议"""
        product_templates = {
            "stocks": [
                {
                    "type": "ETF",
                    "examples": ["沪深300ETF", "标普500ETF", "MSCI中国ETF"],
                    "advantages": ["分散风险", "低成本", "流动性好"],
                    "suggested_allocation": ratio * 0.7
                },
                {
                    "type": "主动管理基金",
                    "examples": ["优质成长基金", "价值投资基金"],
                    "advantages": ["专业管理", "超额收益潜力"],
                    "suggested_allocation": ratio * 0.3
                }
            ],
            "bonds": [
                {
                    "type": "国债ETF",
                    "examples": ["国债ETF", "地方政府债ETF"],
                    "advantages": ["信用风险低", "稳定性高"],
                    "suggested_allocation": ratio * 0.6
                },
                {
                    "type": "企业债基金",
                    "examples": ["高等级企业债基金", "可转债基金"],
                    "advantages": ["收益较高", "分散配置"],
                    "suggested_allocation": ratio * 0.4
                }
            ],
            "cash": [
                {
                    "type": "货币基金",
                    "examples": ["余额宝", "银行货币基金"],
                    "advantages": ["流动性强", "风险极低"],
                    "suggested_allocation": ratio
                }
            ],
            "real_estate": [
                {
                    "type": "REITs",
                    "examples": ["房地产信托基金", "商业地产REITs"],
                    "advantages": ["分散投资", "稳定分红"],
                    "suggested_allocation": ratio
                }
            ]
        }
        
        return product_templates.get(asset_class, [])
    
    def _generate_implementation_tips(self, strategy: Dict, time_horizon: str) -> List[str]:
        """生成实施建议"""
        tips = [
            "分批建仓，避免一次性投入",
            "定期定额投资，降低择时风险",
            "保持投资纪律，避免情绪化操作"
        ]
        
        if time_horizon == InvestmentHorizon.LONG_TERM.value:
            tips.append("长期持有，享受复利效应")
            tips.append("定期再平衡，维持目标配置")
        
        if strategy["risk_level"] == "高":
            tips.append("设置止损点，控制下行风险")
            tips.append("密切关注市场变化，及时调整")
        
        return tips
    
    def _generate_monitoring_schedule(self, time_horizon: str) -> Dict[str, str]:
        """生成监控计划"""
        schedules = {
            InvestmentHorizon.SHORT_TERM.value: {
                "portfolio_review": "每月",
                "rebalancing": "每季度",
                "performance_evaluation": "每月"
            },
            InvestmentHorizon.MEDIUM_TERM.value: {
                "portfolio_review": "每季度", 
                "rebalancing": "每半年",
                "performance_evaluation": "每季度"
            },
            InvestmentHorizon.LONG_TERM.value: {
                "portfolio_review": "每半年",
                "rebalancing": "每年", 
                "performance_evaluation": "每年"
            }
        }
        
        return schedules.get(time_horizon, schedules[InvestmentHorizon.MEDIUM_TERM.value])
    
    def _calculate_expected_performance(self, allocation: Dict[str, float],
                                     risk_profile: Dict) -> Dict[str, Any]:
        """计算预期表现"""
        
        # 计算预期回报
        expected_return = 0
        for asset_class, ratio in allocation.items():
            asset_info = self.asset_classes.get(asset_class, {})
            asset_return = asset_info.get("expected_return", 0.03)
            expected_return += ratio * asset_return
        
        # 计算预期波动率（简化计算）
        expected_volatility = risk_profile.get("volatility_tolerance", 0.1)
        
        # 计算夏普比率（假设无风险利率2%）
        risk_free_rate = 0.02
        sharpe_ratio = (expected_return - risk_free_rate) / expected_volatility if expected_volatility > 0 else 0
        
        return {
            "expected_annual_return": round(expected_return, 4),
            "expected_volatility": round(expected_volatility, 4),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown_expectation": risk_profile.get("max_drawdown_tolerance", 0.2),
            "probability_of_loss": self._calculate_loss_probability(expected_return, expected_volatility),
            "best_case_scenario": round(expected_return + expected_volatility, 4),
            "worst_case_scenario": round(expected_return - expected_volatility, 4)
        }
    
    def _calculate_loss_probability(self, expected_return: float, volatility: float) -> float:
        """计算亏损概率（简化计算）"""
        # 使用正态分布假设
        if volatility == 0:
            return 0.0 if expected_return >= 0 else 1.0
        
        z_score = -expected_return / volatility
        # 简化概率计算
        if z_score <= 0:
            return 0.3  # 保守估计
        elif z_score <= 1:
            return 0.4
        else:
            return 0.5
    
    def _generate_risk_management_plan(self, risk_tolerance: str, time_horizon: str) -> Dict[str, Any]:
        """生成风险管理计划"""
        risk_plans = {
            RiskTolerance.CONSERVATIVE.value: {
                "stop_loss_level": 0.95,  # 5%止损
                "diversification_requirement": "高度分散",
                "liquidity_requirement": "高流动性",
                "hedging_suggestions": ["国债", "黄金ETF"]
            },
            RiskTolerance.MODERATE.value: {
                "stop_loss_level": 0.90,  # 10%止损
                "diversification_requirement": "适度分散", 
                "liquidity_requirement": "中等流动性",
                "hedging_suggestions": ["债券配置", "防御性股票"]
            },
            RiskTolerance.AGGRESSIVE.value: {
                "stop_loss_level": 0.80,  # 20%止损
                "diversification_requirement": "基本分散",
                "liquidity_requirement": "可接受较低流动性",
                "hedging_suggestions": ["期权策略", "多空对冲"]
            }
        }
        
        base_plan = risk_plans.get(risk_tolerance, risk_plans[RiskTolerance.MODERATE.value])
        
        # 根据投资期限调整
        if time_horizon == InvestmentHorizon.SHORT_TERM.value:
            base_plan["liquidity_requirement"] = "高流动性"
            base_plan["stop_loss_level"] = min(base_plan["stop_loss_level"] + 0.05, 0.98)
        
        return base_plan
    
    def _generate_rebalancing_strategy(self, time_horizon: str) -> Dict[str, Any]:
        """生成再平衡策略"""
        strategies = {
            InvestmentHorizon.SHORT_TERM.value: {
                "frequency": "季度",
                "trigger_threshold": 0.05,  # 5%偏离触发再平衡
                "method": "阈值再平衡",
                "considerations": ["交易成本", "税收影响"]
            },
            InvestmentHorizon.MEDIUM_TERM.value: {
                "frequency": "半年",
                "trigger_threshold": 0.08,
                "method": "定期+阈值再平衡", 
                "considerations": ["市场周期", "资产相关性"]
            },
            InvestmentHorizon.LONG_TERM.value: {
                "frequency": "年度",
                "trigger_threshold": 0.10,
                "method": "定期再平衡",
                "considerations": ["长期趋势", "复利效应"]
            }
        }
        
        return strategies.get(time_horizon, strategies[InvestmentHorizon.MEDIUM_TERM.value])
    
    def _generate_tax_considerations(self, investment_goal: str) -> List[str]:
        """生成税务考虑"""
        base_considerations = [
            "利用税收优惠账户（如养老金账户）",
            "长期持有享受资本利得税优惠",
            "注意股息收入的税务处理"
        ]
        
        if investment_goal == InvestmentGoal.INCOME_GENERATION.value:
            base_considerations.append("考虑免税债券以优化税后收益")
            base_considerations.append("合理安排分红再投资时间")
        
        return base_considerations
    
    def assess_investment_suitability(self, 
                                    risk_tolerance: str,
                                    investment_amount: float, 
                                    time_horizon: str,
                                    age: int,
                                    financial_situation: Dict[str, Any]) -> Dict[str, Any]:
        """评估投资适宜性"""
        
        suitability_score = 0
        warnings = []
        recommendations = []
        
        # 评估风险承受能力与投资期限匹配度
        horizon_risk_mapping = {
            InvestmentHorizon.SHORT_TERM.value: [RiskTolerance.CONSERVATIVE.value, RiskTolerance.MODERATE.value],
            InvestmentHorizon.MEDIUM_TERM.value: [RiskTolerance.MODERATE.value, RiskTolerance.AGGRESSIVE.value],
            InvestmentHorizon.LONG_TERM.value: [RiskTolerance.AGGRESSIVE.value, RiskTolerance.VERY_AGGRESSIVE.value]
        }
        
        suitable_risks = horizon_risk_mapping.get(time_horizon, [])
        if risk_tolerance not in suitable_risks:
            warnings.append(f"投资期限({time_horizon})与风险偏好({risk_tolerance})可能不匹配")
            suitability_score -= 20
        
        # 评估投资金额适宜性
        emergency_fund_ratio = financial_situation.get("emergency_fund_ratio", 0)
        if emergency_fund_ratio < 0.3:
            warnings.append("应急储备金不足，建议先建立3-6个月生活费的应急基金")
            suitability_score -= 15
        
        # 评估年龄因素
        if age < 25 and risk_tolerance == RiskTolerance.CONSERVATIVE.value:
            recommendations.append("年轻投资者可考虑更积极的投资策略")
        elif age > 60 and risk_tolerance == RiskTolerance.VERY_AGGRESSIVE.value:
            warnings.append("临近退休年龄，建议降低投资风险")
            suitability_score -= 10
        
        # 评估负债情况
        debt_to_income = financial_situation.get("debt_to_income_ratio", 0)
        if debt_to_income > 0.4:
            warnings.append("负债率较高，建议优先偿还高息债务")
            suitability_score -= 15
        
        # 计算适宜性评分
        suitability_score = max(0, 100 + suitability_score)
        
        return {
            "suitability_score": suitability_score,
            "suitability_level": self._get_suitability_level(suitability_score),
            "warnings": warnings,
            "recommendations": recommendations,
            "assessment_criteria": {
                "risk_horizon_match": risk_tolerance in suitable_risks,
                "adequate_emergency_fund": emergency_fund_ratio >= 0.3,
                "appropriate_risk_for_age": self._check_age_risk_appropriateness(age, risk_tolerance),
                "manageable_debt": debt_to_income <= 0.4
            }
        }
    
    def _get_suitability_level(self, score: float) -> str:
        """获取适宜性等级"""
        if score >= 90:
            return "非常适宜"
        elif score >= 75:
            return "适宜"
        elif score >= 60:
            return "基本适宜"
        elif score >= 40:
            return "需要调整"
        else:
            return "不适宜"
    
    def _check_age_risk_appropriateness(self, age: int, risk_tolerance: str) -> bool:
        """检查年龄与风险偏好是否匹配"""
        if age < 30:
            return risk_tolerance in [RiskTolerance.MODERATE.value, RiskTolerance.AGGRESSIVE.value, RiskTolerance.VERY_AGGRESSIVE.value]
        elif age < 50:
            return risk_tolerance in [RiskTolerance.MODERATE.value, RiskTolerance.AGGRESSIVE.value]
        else:
            return risk_tolerance in [RiskTolerance.CONSERVATIVE.value, RiskTolerance.MODERATE.value]


class PortfolioOptimizer:
    """投资组合优化器"""
    
    def __init__(self):
        self.optimization_methods = ["markowitz", "black_litterman", "risk_parity"]
    
    def optimize_portfolio(self, 
                         assets: List[Dict],
                         risk_tolerance: str,
                         method: str = "markowitz") -> Dict[str, Any]:
        """优化投资组合"""
        
        if method not in self.optimization_methods:
            return {"error": f"不支持的优化方法: {method}"}
        
        if method == "markowitz":
            return self._markowitz_optimization(assets, risk_tolerance)
        elif method == "risk_parity":
            return self._risk_parity_optimization(assets)
        else:
            return self._black_litterman_optimization(assets, risk_tolerance)
    
    def _markowitz_optimization(self, assets: List[Dict], risk_tolerance: str) -> Dict[str, Any]:
        """马科维茨均值-方差优化"""
        # 简化实现 - 实际应该使用真实的期望收益和协方差矩阵
        try:
            # 提取资产信息
            returns = [asset.get('expected_return', 0.05) for asset in assets]
            volatilities = [asset.get('volatility', 0.15) for asset in assets]
            
            # 简化优化 - 基于风险偏好分配权重
            risk_weights = {
                "conservative": [0.6, 0.3, 0.1],  # 低风险资产权重高
                "moderate": [0.4, 0.4, 0.2],      # 平衡分配
                "aggressive": [0.2, 0.5, 0.3]     # 高风险资产权重高
            }
            
            weights = risk_weights.get(risk_tolerance, risk_weights["moderate"])
            
            # 调整权重数量匹配资产数量
            if len(weights) > len(assets):
                weights = weights[:len(assets)]
            elif len(weights) < len(assets):
                weights.extend([0.1] * (len(assets) - len(weights)))
            
            # 标准化权重
            total_weight = sum(weights)
            optimized_weights = [w/total_weight for w in weights]
            
            # 计算优化后指标
            portfolio_return = sum(w * r for w, r in zip(optimized_weights, returns))
            portfolio_volatility = math.sqrt(sum(
                (w * v) ** 2 for w, v in zip(optimized_weights, volatilities)
            ))
            
            return {
                "method": "markowitz",
                "optimized_weights": optimized_weights,
                "expected_return": portfolio_return,
                "expected_volatility": portfolio_volatility,
                "sharpe_ratio": portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0,
                "efficient_frontier": self._generate_efficient_frontier(assets)
            }
            
        except Exception as e:
            return {"error": f"优化计算错误: {str(e)}"}
    
    def _risk_parity_optimization(self, assets: List[Dict]) -> Dict[str, Any]:
        """风险平价优化"""
        # 简化实现
        volatilities = [asset.get('volatility', 0.15) for asset in assets]
        
        # 风险平价：权重与波动率成反比
        risk_contributions = [1/v if v > 0 else 0 for v in volatilities]
        total_risk_contribution = sum(risk_contributions)
        
        if total_risk_contribution > 0:
            optimized_weights = [rc/total_risk_contribution for rc in risk_contributions]
        else:
            optimized_weights = [1/len(assets)] * len(assets)
        
        returns = [asset.get('expected_return', 0.05) for asset in assets]
        portfolio_return = sum(w * r for w, r in zip(optimized_weights, returns))
        portfolio_volatility = math.sqrt(sum(
            (w * v) ** 2 for w, v in zip(optimized_weights, volatilities)
        ))
        
        return {
            "method": "risk_parity",
            "optimized_weights": optimized_weights,
            "expected_return": portfolio_return,
            "expected_volatility": portfolio_volatility,
            "risk_contribution": "均衡",
            "sharpe_ratio": portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
        }
    
    def _black_litterman_optimization(self, assets: List[Dict], risk_tolerance: str) -> Dict[str, Any]:
        """Black-Litterman模型优化"""
        # 简化实现
        return self._markowitz_optimization(assets, risk_tolerance)
    
    def _generate_efficient_frontier(self, assets: List[Dict]) -> List[Dict]:
        """生成有效前沿（简化版本）"""
        frontier = []
        
        for target_return in np.linspace(0.02, 0.15, 10):
            frontier_point = {
                "target_return": target_return,
                "min_volatility": target_return * 1.5,  # 简化计算
                "optimal_weights": [1/len(assets)] * len(assets)  # 简化权重
            }
            frontier.append(frontier_point)
        
        return frontier


# 使用示例和演示函数
def investment_advisor_demo():
    """投资顾问演示"""
    print("投资顾问系统演示")
    print("=" * 50)
    
    advisor = InvestmentAdvisor()
    optimizer = PortfolioOptimizer()
    
    # 创建投资组合
    print("\n1. 创建个性化投资组合:")
    print("-" * 30)
    
    portfolio = advisor.create_investment_portfolio(
        risk_tolerance=RiskTolerance.MODERATE.value,
        investment_amount=100000,
        investment_goal=InvestmentGoal.GROWTH.value,
        time_horizon=InvestmentHorizon.LONG_TERM.value,
        age=35
    )
    
    print(f"风险偏好: {portfolio['portfolio_summary']['risk_tolerance']}")
    print(f"投资金额: {portfolio['portfolio_summary']['investment_amount']:,.2f}")
    print(f"投资目标: {portfolio['portfolio_summary']['investment_goal']}")
    
    print("\n资产配置:")
    for asset, ratio in portfolio['asset_allocation'].items():
        amount = portfolio['allocation_breakdown']['allocations'][asset]['amount']
        print(f"  {asset}: {ratio:.1%} (¥{amount:,.2f})")
    
    # 预期表现
    performance = portfolio['expected_performance']
    print(f"\n预期表现:")
    print(f"  年化回报: {performance['expected_annual_return']:.1%}")
    print(f"  波动率: {performance['expected_volatility']:.1%}")
    print(f"  夏普比率: {performance['sharpe_ratio']:.2f}")
    
    # 适宜性评估
    print("\n2. 投资适宜性评估:")
    print("-" * 30)
    
    financial_situation = {
        "emergency_fund_ratio": 0.4,
        "debt_to_income_ratio": 0.3,
        "monthly_income": 20000
    }
    
    suitability = advisor.assess_investment_suitability(
        risk_tolerance=RiskTolerance.MODERATE.value,
        investment_amount=50000,
        time_horizon=InvestmentHorizon.MEDIUM_TERM.value,
        age=35,
        financial_situation=financial_situation
    )
    
    print(f"适宜性评分: {suitability['suitability_score']}/100")
    print(f"适宜性等级: {suitability['suitability_level']}")
    
    if suitability['warnings']:
        print("警告:")
        for warning in suitability['warnings']:
            print(f"  - {warning}")
    
    # 组合优化演示
    print("\n3. 投资组合优化:")
    print("-" * 30)
    
    sample_assets = [
        {"name": "股票", "expected_return": 0.08, "volatility": 0.18},
        {"name": "债券", "expected_return": 0.04, "volatility": 0.06},
        {"name": "现金", "expected_return": 0.02, "volatility": 0.01}
    ]
    
    optimization = optimizer.optimize_portfolio(
        assets=sample_assets,
        risk_tolerance=RiskTolerance.MODERATE.value,
        method="markowitz"
    )
    
    if "error" not in optimization:
        print(f"优化方法: {optimization['method']}")
        print(f"预期回报: {optimization['expected_return']:.1%}")
        print(f"预期波动: {optimization['expected_volatility']:.1%}")
        print(f"夏普比率: {optimization['sharpe_ratio']:.2f}")


if __name__ == "__main__":
    investment_advisor_demo()