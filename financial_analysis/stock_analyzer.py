import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    """股票分析器"""
    
    def __init__(self):
        self.technical_indicators = {}
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """获取股票数据"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            
            if hist.empty:
                return {"error": f"无法获取股票 {symbol} 的数据"}
            
            # 计算技术指标
            indicators = self._calculate_technical_indicators(hist)
            
            # 获取基本信息
            info = stock.info
            basic_info = {
                "name": info.get('longName', symbol),
                "sector": info.get('sector', '未知'),
                "industry": info.get('industry', '未知'),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0)
            }
            
            return {
                "symbol": symbol,
                "basic_info": basic_info,
                "price_data": {
                    "current_price": hist['Close'].iloc[-1],
                    "previous_close": hist['Close'].iloc[-2] if len(hist) > 1 else hist['Close'].iloc[-1],
                    "day_change": hist['Close'].iloc[-1] - hist['Close'].iloc[-2] if len(hist) > 1 else 0,
                    "day_change_percent": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100) if len(hist) > 1 else 0
                },
                "technical_indicators": indicators,
                "historical_data": self._format_historical_data(hist)
            }
            
        except Exception as e:
            return {"error": f"获取股票数据时出错: {str(e)}"}
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """计算技术指标"""
        # 移动平均线
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()
        
        # RSI
        data['RSI'] = self._calculate_rsi(data['Close'])
        
        # MACD
        macd, signal = self._calculate_macd(data['Close'])
        data['MACD'] = macd
        data['MACD_Signal'] = signal
        
        # 布林带
        data['BB_Upper'], data['BB_Lower'] = self._calculate_bollinger_bands(data['Close'])
        
        latest = data.iloc[-1]
        
        return {
            "moving_averages": {
                "MA20": latest['MA20'],
                "MA50": latest['MA50'],
                "trend": "上涨" if latest['MA20'] > latest['MA50'] else "下跌"
            },
            "rsi": {
                "value": latest['RSI'],
                "signal": "超买" if latest['RSI'] > 70 else "超卖" if latest['RSI'] < 30 else "中性"
            },
            "macd": {
                "value": latest['MACD'],
                "signal": latest['MACD_Signal'],
                "trend": "看涨" if latest['MACD'] > latest['MACD_Signal'] else "看跌"
            },
            "bollinger_bands": {
                "upper": latest['BB_Upper'],
                "lower": latest['BB_Lower'],
                "position": "上轨附近" if latest['Close'] > latest['BB_Upper'] * 0.95 else 
                           "下轨附近" if latest['Close'] < latest['BB_Lower'] * 1.05 else "中轨附近"
            }
        }
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series) -> tuple:
        """计算MACD指标"""
        exp1 = prices.ewm(span=12).mean()
        exp2 = prices.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        return macd, signal
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> tuple:
        """计算布林带"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return upper_band, lower_band
    
    def _format_historical_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """格式化历史数据"""
        return {
            "periods": {
                "1d": f"{data['Close'].iloc[-1]:.2f}",
                "1w": f"{data['Close'].iloc[-5]:.2f}" if len(data) >= 5 else "N/A",
                "1m": f"{data['Close'].iloc[-20]:.2f}" if len(data) >= 20 else "N/A",
                "3m": f"{data['Close'].iloc[-60]:.2f}" if len(data) >= 60 else "N/A",
                "1y": f"{data['Close'].iloc[0]:.2f}" if len(data) > 0 else "N/A"
            },
            "performance": {
                "week_change": f"{((data['Close'].iloc[-1] - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100):.2f}%" if len(data) >= 5 else "N/A",
                "month_change": f"{((data['Close'].iloc[-1] - data['Close'].iloc[-20]) / data['Close'].iloc[-20] * 100):.2f}%" if len(data) >= 20 else "N/A",
                "year_change": f"{((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100):.2f}%" if len(data) > 0 else "N/A"
            }
        }
    
    def generate_trading_signals(self, symbol: str) -> Dict[str, Any]:
        """生成交易信号"""
        data = self.get_stock_data(symbol)
        if "error" in data:
            return data
        
        indicators = data["technical_indicators"]
        signals = []
        confidence = 0
        
        # RSI信号
        if indicators["rsi"]["signal"] == "超卖":
            signals.append("RSI显示超卖，可能反弹")
            confidence += 25
        elif indicators["rsi"]["signal"] == "超买":
            signals.append("RSI显示超买，可能回调")
            confidence += 25
        
        # MACD信号
        if indicators["macd"]["trend"] == "看涨":
            signals.append("MACD金叉，看涨信号")
            confidence += 30
        else:
            signals.append("MACD死叉，看跌信号")
            confidence -= 20
        
        # 移动平均线信号
        if indicators["moving_averages"]["trend"] == "上涨":
            signals.append("短期均线上穿长期均线，趋势向上")
            confidence += 25
        else:
            signals.append("短期均线下穿长期均线，趋势向下")
            confidence -= 15
        
        # 总体建议
        if confidence >= 50:
            recommendation = "买入"
        elif confidence >= 20:
            recommendation = "持有"
        elif confidence >= 0:
            recommendation = "观望"
        else:
            recommendation = "卖出"
        
        return {
            "symbol": symbol,
            "signals": signals,
            "confidence_score": confidence,
            "recommendation": recommendation,
            "risk_level": "高风险" if abs(confidence) > 60 else "中风险" if abs(confidence) > 30 else "低风险",
            "disclaimer": "投资有风险，入市需谨慎。本分析仅供参考。"
        }

class InvestmentAdvisor:
    """投资顾问"""
    
    def __init__(self):
        self.risk_profiles = {
            "conservative": {
                "stocks": 20,
                "bonds": 50,
                "cash": 30,
                "description": "保守型 - 注重本金安全"
            },
            "moderate": {
                "stocks": 50,
                "bonds": 30,
                "cash": 20,
                "description": "稳健型 - 平衡风险与收益"
            },
            "aggressive": {
                "stocks": 80,
                "bonds": 15,
                "cash": 5,
                "description": "进取型 - 追求高收益"
            }
        }
    
    def create_portfolio(self, risk_profile: str, investment_amount: float) -> Dict[str, Any]:
        """创建投资组合"""
        if risk_profile not in self.risk_profiles:
            return {"error": "无效的风险偏好"}
        
        profile = self.risk_profiles[risk_profile]
        
        portfolio = {
            "risk_profile": risk_profile,
            "investment_amount": investment_amount,
            "allocation": profile,
            "detailed_allocation": {
                "stocks": {
                    "amount": investment_amount * profile["stocks"] / 100,
                    "suggestions": self._get_stock_suggestions(risk_profile)
                },
                "bonds": {
                    "amount": investment_amount * profile["bonds"] / 100,
                    "suggestions": ["国债", "企业债", "地方政府债"]
                },
                "cash": {
                    "amount": investment_amount * profile["cash"] / 100,
                    "suggestions": ["货币基金", "定期存款", "活期存款"]
                }
            },
            "expected_return": self._calculate_expected_return(risk_profile),
            "risk_warning": self._get_risk_warning(risk_profile)
        }
        
        return portfolio
    
    def _get_stock_suggestions(self, risk_profile: str) -> List[str]:
        """获取股票建议"""
        if risk_profile == "conservative":
            return ["蓝筹股", "公用事业股", "消费必需品"]
        elif risk_profile == "moderate":
            return ["蓝筹股", "成长股", "科技股"]
        else:  # aggressive
            return ["科技股", "新兴行业", "小盘股"]
    
    def _calculate_expected_return(self, risk_profile: str) -> Dict[str, float]:
        """计算预期收益"""
        returns = {
            "conservative": {"min": 3, "max": 6},
            "moderate": {"min": 6, "max": 10},
            "aggressive": {"min": 10, "max": 15}
        }
        return returns.get(risk_profile, {"min": 0, "max": 0})
    
    def _get_risk_warning(self, risk_profile: str) -> str:
        """获取风险警告"""
        warnings = {
            "conservative": "低风险，但收益有限",
            "moderate": "中等风险，适合长期投资",
            "aggressive": "高风险，可能面临较大波动"
        }
        return warnings.get(risk_profile, "未知风险")

class RiskAssessor:
    """风险评估器"""
    
    def assess_investment_risk(self, symbol: str, investment_amount: float, 
                             time_horizon: str) -> Dict[str, Any]:
        """评估投资风险"""
        analyzer = StockAnalyzer()
        stock_data = analyzer.get_stock_data(symbol)
        
        if "error" in stock_data:
            return stock_data
        
        # 计算波动率风险
        volatility_risk = self._calculate_volatility_risk(stock_data)
        
        # 计算基本面风险
        fundamental_risk = self._assess_fundamental_risk(stock_data)
        
        # 时间 horizon 风险调整
        time_risk = self._adjust_time_risk(time_horizon)
        
        # 总体风险评分
        total_risk = (volatility_risk + fundamental_risk) * time_risk
        
        risk_level = "低风险" if total_risk < 3 else "中风险" if total_risk < 7 else "高风险"
        
        return {
            "symbol": symbol,
            "investment_amount": investment_amount,
            "time_horizon": time_horizon,
            "risk_breakdown": {
                "volatility_risk": volatility_risk,
                "fundamental_risk": fundamental_risk,
                "time_adjustment": time_risk
            },
            "total_risk_score": total_risk,
            "risk_level": risk_level,
            "recommendation": self._generate_risk_recommendation(total_risk, investment_amount)
        }
    
    def _calculate_volatility_risk(self, stock_data: Dict) -> float:
        """计算波动率风险"""
        # 简化实现 - 基于价格变化幅度
        try:
            price_data = stock_data["price_data"]
            change_percent = abs(price_data["day_change_percent"])
            if change_percent > 5:
                return 8
            elif change_percent > 3:
                return 5
            elif change_percent > 1:
                return 3
            else:
                return 1
        except:
            return 5
    
    def _assess_fundamental_risk(self, stock_data: Dict) -> float:
        """评估基本面风险"""
        try:
            basic_info = stock_data["basic_info"]
            pe_ratio = basic_info.get("pe_ratio", 0)
            
            if pe_ratio == 0:
                return 6
            elif pe_ratio > 50:
                return 8
            elif pe_ratio > 30:
                return 5
            elif pe_ratio > 15:
                return 3
            else:
                return 2
        except:
            return 5
    
    def _adjust_time_risk(self, time_horizon: str) -> float:
        """调整时间风险"""
        time_factors = {
            "短期": 1.2,
            "中期": 1.0,
            "长期": 0.8
        }
        return time_factors.get(time_horizon, 1.0)
    
    def _generate_risk_recommendation(self, risk_score: float, amount: float) -> str:
        """生成风险建议"""
        if risk_score < 3:
            return f"风险较低，适合投资{amount}元"
        elif risk_score < 7:
            return f"风险适中，建议投资{amount * 0.7:.0f}元"
        else:
            return f"风险较高，建议投资不超过{amount * 0.3:.0f}元"