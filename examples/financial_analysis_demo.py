#!/usr/bin/env python3
"""
金融分析助手演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from financial_analysis.stock_analyzer import StockAnalyzer
from financial_analysis.investment_advisor import InvestmentAdvisor
from financial_analysis.risk_assessor import RiskAssessor

def generate_sample_stock_data(symbol: str, days: int = 100) -> pd.DataFrame:
    """生成示例股票数据"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    np.random.seed(42)  # 固定随机种子以便重现
    
    # 生成价格数据
    prices = [100]
    for i in range(1, days):
        change = np.random.normal(0, 2)  # 日均波动约2%
        new_price = prices[-1] * (1 + change / 100)
        prices.append(max(new_price, 1))  # 确保价格不为负
    
    data = pd.DataFrame({
        'date': dates,
        'open': [p * (1 + np.random.normal(0, 0.01)) for p in prices],
        'high': [p * (1 + abs(np.random.normal(0, 0.02))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.02))) for p in prices],
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, days)
    })
    
    return data

def demo_financial_analysis():
    """金融分析演示"""
    print("=" * 50)
    print("金融分析助手演示")
    print("=" * 50)
    
    # 初始化组件
    analyzer = StockAnalyzer()
    advisor = InvestmentAdvisor()
    risk_assessor = RiskAssessor()
    
    # 生成示例数据
    sample_data = generate_sample_stock_data("EXAMPLE", 100)
    
    # 1. 股票分析演示
    print("\n1. 股票分析演示")
    print("-" * 30)
    
    analysis = analyzer.analyze_stock("EXAMPLE", sample_data)
    
    print(f"股票代码: {analysis['symbol']}")
    print(f"当前价格: {analysis['current_price']:.2f}")
    print(f"分析日期: {analysis['analysis_date']}")
    
    indicators = analysis['technical_indicators']
    print(f"技术指标 - MA20: {indicators['MA20']:.2f}, RSI: {indicators['RSI']:.2f}")
    print(f"趋势: {indicators['trend']}")
    
    trend = analysis['trend_analysis']
    print(f"趋势分析 - 短期: {trend['short_term']}, 波动率: {trend['volatility']}%")
    
    risk = analysis['risk_assessment']
    print(f"风险评估 - 等级: {risk['risk_level']}/10, 最大回撤: {risk['max_drawdown']}%")
    
    recommendation = analysis['recommendation']
    print(f"投资建议: {recommendation['action']} (置信度: {recommendation['confidence']})")
    
    # 2. 投资组合演示
    print("\n2. 投资组合建议")
    print("-" * 30)
    
    risk_profiles = ["conservative", "moderate", "aggressive"]
    investment_amount = 100000
    
    for profile in risk_profiles:
        portfolio = advisor.create_portfolio(profile, investment_amount)
        print(f"\n{profile} 风险偏好:")
        print(f"  股票: {portfolio['allocation']['stocks']}%")
        print(f"  债券: {portfolio['allocation']['bonds']}%")
        print(f"  现金: {portfolio['allocation']['cash']}%")
        print(f"  预期收益: {portfolio['expected_return']['min']}%-{portfolio['expected_return']['max']}%")
    
    # 3. 风险评估演示
    print("\n3. 风险评估演示")
    print("-" * 30)
    
    risk_assessment = risk_assessor.assess_investment_risk(
        "EXAMPLE", sample_data, 50000, "中期"
    )
    
    print(f"投资标的: {risk_assessment['symbol']}")
    print(f"投资金额: {risk_assessment['investment_amount']}")
    print(f"时间周期: {risk_assessment['time_horizon']}")
    print(f"综合风险评分: {risk_assessment['total_risk_score']}/10")
    print(f"风险等级: {risk_assessment['risk_level']}")
    print(f"风险描述: {risk_assessment['risk_description']}")
    print(f"投资建议: {risk_assessment['recommendation']}")
    
    # 显示风险分解
    breakdown = risk_assessment['risk_breakdown']
    print(f"风险分解 - 波动率: {breakdown['volatility_risk']:.1f}, "
          f"回撤: {breakdown['drawdown_risk']:.1f}, "
          f"流动性: {breakdown['liquidity_risk']:.1f}")

if __name__ == "__main__":
    demo_financial_analysis()