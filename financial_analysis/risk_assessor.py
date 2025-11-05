import numpy as np
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime

class RiskAssessor:
    """风险评估器"""
    
    def __init__(self):
        self.risk_levels = {
            "conservative": {"max_stock_ratio": 0.3, "volatility_tolerance": 0.1},
            "moderate": {"max_stock_ratio": 0.6, "volatility_tolerance": 0.15},
            "aggressive": {"max_stock_ratio": 0.8, "volatility_tolerance": 0.25}
        }
    
    def assess_investment_risk(self, symbol: str, historical_data: pd.DataFrame, 
                             investment_amount: float, time_horizon: str) -> Dict[str, Any]:
        """评估投资风险"""
        if historical_data.empty:
            return {"error": "历史数据为空"}
        
        # 计算风险指标
        volatility_risk = self._calculate_volatility_risk(historical_data)
        drawdown_risk = self._calculate_drawdown_risk(historical_data)
        liquidity_risk = self._assess_liquidity_risk(historical_data)
        
        # 时间 horizon 调整
        time_factor = self._get_time_factor(time_horizon)
        
        # 综合风险评分
        total_risk_score = (volatility_risk + drawdown_risk + liquidity_risk) * time_factor
        
        risk_level = self._determine_risk_level(total_risk_score)
        
        return {
            "symbol": symbol,
            "investment_amount": investment_amount,
            "time_horizon": time_horizon,
            "risk_breakdown": {
                "volatility_risk": volatility_risk,
                "drawdown_risk": drawdown_risk,
                "liquidity_risk": liquidity_risk,
                "time_adjustment": time_factor
            },
            "total_risk_score": round(total_risk_score, 2),
            "risk_level": risk_level,
            "risk_description": self._get_risk_description(risk_level),
            "recommendation": self._generate_risk_recommendation(total_risk_score, investment_amount),
            "warning_level": self._get_warning_level(risk_level)
        }
    
    def _calculate_volatility_risk(self, data: pd.DataFrame) -> float:
        """计算波动率风险"""
        returns = data['close'].pct_change().dropna()
        
        if len(returns) < 2:
            return 5.0
        
        volatility = returns.std() * np.sqrt(252)  # 年化波动率
        
        # 将波动率转换为风险分数 (0-10)
        if volatility > 0.4:
            return 9.0
        elif volatility > 0.3:
            return 7.0
        elif volatility > 0.2:
            return 5.0
        elif volatility > 0.1:
            return 3.0
        else:
            return 1.0
    
    def _calculate_drawdown_risk(self, data: pd.DataFrame) -> float:
        """计算回撤风险"""
        prices = data['close']
        peak = prices.expanding().max()
        drawdown = (prices - peak) / peak
        
        max_drawdown = drawdown.min()
        
        # 将最大回撤转换为风险分数
        if max_drawdown < -0.5:
            return 10.0
        elif max_drawdown < -0.3:
            return 8.0
        elif max_drawdown < -0.2:
            return 6.0
        elif max_drawdown < -0.1:
            return 4.0
        else:
            return 2.0
    
    def _assess_liquidity_risk(self, data: pd.DataFrame) -> float:
        """评估流动性风险"""
        if 'volume' not in data.columns:
            return 3.0
        
        avg_volume = data['volume'].mean()
        volume_volatility = data['volume'].std() / avg_volume if avg_volume > 0 else 1.0
        
        # 基于平均交易量和波动性评估流动性风险
        if avg_volume < 1000000:  # 低交易量
            liquidity_risk = 7.0
        elif avg_volume < 5000000:  # 中等交易量
            liquidity_risk = 5.0
        else:  # 高交易量
            liquidity_risk = 3.0
        
        # 考虑交易量波动性
        if volume_volatility > 0.5:
            liquidity_risk += 2.0
        
        return min(liquidity_risk, 10.0)
    
    def _get_time_factor(self, time_horizon: str) -> float:
        """获取时间因子"""
        factors = {
            "短期": 1.2,   # 短期投资风险更高
            "中期": 1.0,   # 中期投资风险适中
            "长期": 0.8    # 长期投资风险较低
        }
        return factors.get(time_horizon, 1.0)
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """确定风险等级"""
        if risk_score >= 8:
            return "极高风险"
        elif risk_score >= 6:
            return "高风险"
        elif risk_score >= 4:
            return "中风险"
        elif risk_score >= 2:
            return "低风险"
        else:
            return "极低风险"
    
    def _get_risk_description(self, risk_level: str) -> str:
        """获取风险描述"""
        descriptions = {
            "极低风险": "投资相对安全，波动性很小",
            "低风险": "投资较为安全，有一定波动性",
            "中风险": "投资有中等风险，可能面临一定波动",
            "高风险": "投资风险较高，可能面临较大波动",
            "极高风险": "投资风险很高，可能面临巨大波动"
        }
        return descriptions.get(risk_level, "风险等级未知")
    
    def _generate_risk_recommendation(self, risk_score: float, amount: float) -> str:
        """生成风险建议"""
        if risk_score >= 8:
            return f"风险极高，建议投资不超过{amount * 0.1:.0f}元，或考虑其他投资品种"
        elif risk_score >= 6:
            return f"风险较高，建议投资不超过{amount * 0.3:.0f}元"
        elif risk_score >= 4:
            return f"风险适中，建议投资{amount * 0.6:.0f}元"
        elif risk_score >= 2:
            return f"风险较低，建议投资{amount * 0.8:.0f}元"
        else:
            return f"风险极低，适合投资{amount:.0f}元"
    
    def _get_warning_level(self, risk_level: str) -> str:
        """获取警告级别"""
        warnings = {
            "极低风险": "info",
            "低风险": "info",
            "中风险": "warning",
            "高风险": "danger",
            "极高风险": "critical"
        }
        return warnings.get(risk_level, "info")
    
    def portfolio_risk_assessment(self, portfolio: Dict[str, float], 
                                historical_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """投资组合风险评估"""
        total_value = sum(portfolio.values())
        weighted_risk = 0
        component_risks = {}
        
        for symbol, value in portfolio.items():
            if symbol in historical_data:
                data = historical_data[symbol]
                risk_score = self.assess_investment_risk(symbol, data, value, "中期")["total_risk_score"]
                weight = value / total_value
                weighted_risk += risk_score * weight
                component_risks[symbol] = {
                    "risk_score": risk_score,
                    "weight": weight,
                    "contribution": risk_score * weight
                }
        
        overall_risk_level = self._determine_risk_level(weighted_risk)
        
        return {
            "portfolio_value": total_value,
            "weighted_risk_score": round(weighted_risk, 2),
            "overall_risk_level": overall_risk_level,
            "component_risks": component_risks,
            "diversification_benefit": self._assess_diversification(component_risks),
            "recommendation": self._generate_portfolio_recommendation(weighted_risk, component_risks)
        }
    
    def _assess_diversification(self, component_risks: Dict) -> str:
        """评估分散化效益"""
        if len(component_risks) <= 1:
            return "分散化不足"
        
        risk_scores = [comp["risk_score"] for comp in component_risks.values()]
        risk_range = max(risk_scores) - min(risk_scores)
        
        if risk_range > 5:
            return "分散化良好"
        elif risk_range > 3:
            return "分散化一般"
        else:
            return "分散化不足"
    
    def _generate_portfolio_recommendation(self, weighted_risk: float, 
                                         component_risks: Dict) -> str:
        """生成投资组合建议"""
        if weighted_risk >= 7:
            return "投资组合风险偏高，建议减少高风险资产配置"
        elif weighted_risk >= 5:
            return "投资组合风险适中，建议保持当前配置"
        else:
            return "投资组合风险较低，可考虑适当增加收益性资产"