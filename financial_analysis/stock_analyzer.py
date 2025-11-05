import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime

class StockAnalyzer:
    """股票分析器"""
    
    def __init__(self):
        pass
    
    def analyze_stock(self, symbol: str, data: pd.DataFrame = None) -> Dict[str, Any]:
        """分析股票"""
        if data is None:
            # 模拟数据
            data = self._generate_sample_data()
        
        analysis = {
            "symbol": symbol,
            "current_price": data['close'].iloc[-1],
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "technical_indicators": self._calculate_indicators(data),
            "trend_analysis": self._analyze_trend(data),
            "risk_assessment": self._assess_risk(data),
            "recommendation": self._generate_recommendation(data)
        }
        
        return analysis
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """生成示例数据"""
        dates = pd.date_range(start='2024-01-01', end='2024-03-01', freq='D')
        np.random.seed(42)
        
        data = pd.DataFrame({
            'date': dates,
            'open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'high': 100 + np.cumsum(np.random.randn(len(dates)) * 0.6),
            'low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.4),
            'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'volume': np.random.randint(1000000, 5000000, len(dates))
        })
        
        return data
    
    def _calculate_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """计算技术指标"""
        close = data['close']
        
        # 移动平均线
        ma_20 = close.rolling(20).mean().iloc[-1]
        ma_50 = close.rolling(50).mean().iloc[-1]
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        return {
            "MA20": round(ma_20, 2),
            "MA50": round(ma_50, 2),
            "RSI": round(rsi, 2),
            "trend": "上涨" if ma_20 > ma_50 else "下跌"
        }
    
    def _analyze_trend(self, data: pd.DataFrame) -> Dict[str, Any]:
        """趋势分析"""
        close = data['close']
        
        short_trend = "上涨" if close.iloc[-1] > close.iloc[-5] else "下跌"
        medium_trend = "上涨" if close.iloc[-1] > close.iloc[-20] else "下跌"
        
        return {
            "short_term": short_trend,
            "medium_term": medium_trend,
            "volatility": round(close.pct_change().std() * 100, 2)
        }
    
    def _assess_risk(self, data: pd.DataFrame) -> Dict[str, Any]:
        """风险评估"""
        returns = data['close'].pct_change().dropna()
        
        risk_score = min(10, int(returns.std() * 1000))
        
        return {
            "risk_level": risk_score,
            "volatility": round(returns.std() * 100, 2),
            "max_drawdown": round((data['close'] / data['close'].cummax() - 1).min() * 100, 2)
        }
    
    def _generate_recommendation(self, data: pd.DataFrame) -> Dict[str, Any]:
        """生成投资建议"""
        indicators = self._calculate_indicators(data)
        risk = self._assess_risk(data)
        
        if indicators['RSI'] < 30:
            recommendation = "买入"
            confidence = "高"
        elif indicators['RSI'] > 70:
            recommendation = "卖出"
            confidence = "中"
        else:
            recommendation = "持有"
            confidence = "中"
        
        return {
            "action": recommendation,
            "confidence": confidence,
            "reasoning": f"RSI指标{indicators['RSI']}，趋势{indicators['trend']}",
            "disclaimer": "投资有风险，建议仅供参考"
        }

class InvestmentAdvisor:
    """投资顾问"""
    
    def create_portfolio(self, risk_profile: str, amount: float) -> Dict[str, Any]:
        """创建投资组合"""
        profiles = {
            "conservative": {"stocks": 30, "bonds": 50, "cash": 20},
            "moderate": {"stocks": 60, "bonds": 30, "cash": 10},
            "aggressive": {"stocks": 80, "bonds": 15, "cash": 5}
        }
        
        allocation = profiles.get(risk_profile, profiles["moderate"])
        
        return {
            "risk_profile": risk_profile,
            "investment_amount": amount,
            "allocation": allocation,
            "breakdown": {
                "stocks": amount * allocation["stocks"] / 100,
                "bonds": amount * allocation["bonds"] / 100,
                "cash": amount * allocation["cash"] / 100
            },
            "expected_return": self._get_expected_return(risk_profile)
        }
    
    def _get_expected_return(self, risk_profile: str) -> Dict[str, float]:
        """获取预期收益"""
        returns = {
            "conservative": {"min": 4, "max": 7},
            "moderate": {"min": 6, "max": 10},
            "aggressive": {"min": 8, "max": 15}
        }
        return returns.get(risk_profile, {"min": 5, "max": 8})