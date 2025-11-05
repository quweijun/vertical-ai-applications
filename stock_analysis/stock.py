import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和图形显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class StockPredictor:
    def __init__(self):
        self.model = None
        self.data = None
        self.feature_names = None
        self.lookback_days = 30
        self.features_per_day = 19
        
    def get_stock_data(self, stock_code, period="1y"):
        """获取股票数据"""
        try:
            if stock_code.endswith('.SZ') or stock_code.endswith('.SS'):
                ticker = stock_code
            else:
                if stock_code.startswith('6'):
                    ticker = f"{stock_code}.SS"
                else:
                    ticker = f"{stock_code}.SZ"
            
            stock = yf.Ticker(ticker)
            self.data = stock.history(period=period)
            
            if self.data.empty:
                print("未找到该股票数据，请检查股票代码是否正确")
                return False
                
            print(f"成功获取 {stock_code} 的股票数据，共 {len(self.data)} 个交易日")
            return True
            
        except Exception as e:
            print(f"获取股票数据时出错: {e}")
            return False
    
    def prepare_features(self, lookback_days=30):
        """准备特征数据"""
        self.lookback_days = lookback_days
        
        if self.data is None:
            print("请先获取股票数据")
            return False
            
        # 计算技术指标
        self.data['MA_5'] = self.data['Close'].rolling(window=5).mean()
        self.data['MA_10'] = self.data['Close'].rolling(window=10).mean()
        self.data['MA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['MA_30'] = self.data['Close'].rolling(window=30).mean()
        
        # RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = self.data['Close'].ewm(span=12).mean()
        exp2 = self.data['Close'].ewm(span=26).mean()
        self.data['MACD'] = exp1 - exp2
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9).mean()
        self.data['MACD_Histogram'] = self.data['MACD'] - self.data['MACD_Signal']
        
        # 布林带
        self.data['BB_Middle'] = self.data['Close'].rolling(window=20).mean()
        bb_std = self.data['Close'].rolling(window=20).std()
        self.data['BB_Upper'] = self.data['BB_Middle'] + (bb_std * 2)
        self.data['BB_Lower'] = self.data['BB_Middle'] - (bb_std * 2)
        self.data['BB_Width'] = (self.data['BB_Upper'] - self.data['BB_Lower']) / self.data['BB_Middle']
        
        # 变化率
        self.data['Price_Change'] = self.data['Close'].pct_change()
        self.data['Volume_Change'] = self.data['Volume'].pct_change()
        self.data['Volatility'] = self.data['Close'].rolling(window=20).std()
        
        # 创建特征
        features = []
        targets = []
        
        for i in range(lookback_days, len(self.data)-1):
            feature_set = []
            for j in range(i-lookback_days, i):
                feature_set.extend([
                    self.data['Open'].iloc[j],
                    self.data['High'].iloc[j],
                    self.data['Low'].iloc[j],
                    self.data['Close'].iloc[j],
                    self.data['Volume'].iloc[j],
                    self.data['MA_5'].iloc[j],
                    self.data['MA_10'].iloc[j],
                    self.data['MA_20'].iloc[j],
                    self.data['MA_30'].iloc[j],
                    self.data['RSI'].iloc[j],
                    self.data['MACD'].iloc[j],
                    self.data['MACD_Signal'].iloc[j],
                    self.data['MACD_Histogram'].iloc[j],
                    self.data['BB_Upper'].iloc[j],
                    self.data['BB_Lower'].iloc[j],
                    self.data['BB_Width'].iloc[j],
                    self.data['Price_Change'].iloc[j],
                    self.data['Volume_Change'].iloc[j],
                    self.data['Volatility'].iloc[j]
                ])
            features.append(feature_set)
            targets.append(self.data['Close'].iloc[i+1])
        
        self.features = np.array(features)
        self.targets = np.array(targets)
        
        # 删除NaN
        valid_indices = ~np.isnan(self.features).any(axis=1) & ~np.isnan(self.targets)
        self.features = self.features[valid_indices]
        self.targets = self.targets[valid_indices]
        
        print(f"特征数据准备完成，共 {len(self.features)} 个样本")
        return True
    
    def train_model(self):
        """训练预测模型"""
        if not hasattr(self, 'features') or len(self.features) == 0:
            print("请先准备特征数据")
            return False
            
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.targets, test_size=0.2, random_state=42
        )
        
        self.model = RandomForestRegressor(
            n_estimators=100, 
            max_depth=10, 
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        print(f"模型训练完成")
        print(f"测试集均方误差(MSE): {mse:.4f}")
        print(f"测试集平均绝对误差(MAE): {mae:.4f}")
        print(f"测试集平均绝对百分比误差(MAPE): {mae:.2f}%")
        
        return True
    
    def create_feature_from_prediction(self, prediction, last_real_data):
        """根据预测值创建新的特征"""
        new_open = prediction
        new_high = prediction * 1.01
        new_low = prediction * 0.99
        new_close = prediction
        new_volume = last_real_data['Volume']
        
        new_ma_5 = (last_real_data['MA_5'] * 4 + prediction) / 5
        new_ma_10 = (last_real_data['MA_10'] * 9 + prediction) / 10
        new_ma_20 = (last_real_data['MA_20'] * 19 + prediction) / 20
        new_ma_30 = (last_real_data['MA_30'] * 29 + prediction) / 30
        
        new_rsi = last_real_data['RSI']
        new_macd = last_real_data['MACD']
        new_macd_signal = last_real_data['MACD_Signal']
        new_macd_histogram = last_real_data['MACD_Histogram']
        new_bb_upper = last_real_data['BB_Upper']
        new_bb_lower = last_real_data['BB_Lower']
        new_bb_width = last_real_data['BB_Width']
        new_price_change = (prediction - last_real_data['Close']) / last_real_data['Close']
        new_volume_change = last_real_data['Volume_Change']
        new_volatility = last_real_data['Volatility']
        
        return [
            new_open, new_high, new_low, new_close, new_volume,
            new_ma_5, new_ma_10, new_ma_20, new_ma_30,
            new_rsi, new_macd, new_macd_signal, new_macd_histogram,
            new_bb_upper, new_bb_lower, new_bb_width,
            new_price_change, new_volume_change, new_volatility
        ]
    
    def predict_future(self, days=5):
        """预测未来多天的股价"""
        if self.model is None:
            print("请先训练模型")
            return None, None, None
            
        last_real_data = {
            'Open': self.data['Open'].iloc[-1],
            'High': self.data['High'].iloc[-1],
            'Low': self.data['Low'].iloc[-1],
            'Close': self.data['Close'].iloc[-1],
            'Volume': self.data['Volume'].iloc[-1],
            'MA_5': self.data['MA_5'].iloc[-1],
            'MA_10': self.data['MA_10'].iloc[-1],
            'MA_20': self.data['MA_20'].iloc[-1],
            'MA_30': self.data['MA_30'].iloc[-1],
            'RSI': self.data['RSI'].iloc[-1],
            'MACD': self.data['MACD'].iloc[-1],
            'MACD_Signal': self.data['MACD_Signal'].iloc[-1],
            'MACD_Histogram': self.data['MACD_Histogram'].iloc[-1],
            'BB_Upper': self.data['BB_Upper'].iloc[-1],
            'BB_Lower': self.data['BB_Lower'].iloc[-1],
            'BB_Width': self.data['BB_Width'].iloc[-1],
            'Price_Change': self.data['Price_Change'].iloc[-1],
            'Volume_Change': self.data['Volume_Change'].iloc[-1],
            'Volatility': self.data['Volatility'].iloc[-1]
        }
        
        predictions = []
        confidence_scores = []
        
        last_date = self.data.index[-1]
        future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(days)]
        
        current_features = self.features[-1].copy().reshape(1, -1)
        
        for day in range(days):
            prediction = self.model.predict(current_features)[0]
            predictions.append(prediction)
            
            tree_predictions = []
            for tree in self.model.estimators_:
                tree_pred = tree.predict(current_features)[0]
                tree_predictions.append(tree_pred)
            
            confidence = 1 - (np.std(tree_predictions) / abs(prediction)) if prediction != 0 else 0
            confidence_scores.append(min(max(confidence, 0), 0.95))
            
            if day < days - 1:
                new_day_features = self.create_feature_from_prediction(prediction, last_real_data)
                current_features = np.roll(current_features, -self.features_per_day)
                start_idx = -self.features_per_day
                current_features[0, start_idx:] = new_day_features
                
                last_real_data['Close'] = prediction
                last_real_data['Open'] = new_day_features[0]
                last_real_data['High'] = new_day_features[1]
                last_real_data['Low'] = new_day_features[2]
                last_real_data['Volume'] = new_day_features[3]
        
        return predictions, confidence_scores, future_dates
    
    def plot_predictions(self, stock_code, predictions, confidence_scores, future_dates, days):
        """绘制历史价格和预测结果"""
        if self.data is None:
            print("请先获取股票数据")
            return
            
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # 历史价格（显示最近60个交易日）
        display_days = min(60, len(self.data))
        history_dates = self.data.index[-display_days:]
        history_prices = self.data['Close'].iloc[-display_days:]
        
        # 主图：价格预测
        ax1.plot(history_dates, history_prices, label='Historical Price', color='blue', linewidth=2)
        ax1.plot(future_dates, predictions, label='Predicted Price', color='red', linewidth=2, marker='o')
        ax1.plot([history_dates[-1], future_dates[0]], 
                [history_prices.iloc[-1], predictions[0]], 
                color='red', linewidth=2)
        
        # 置信区间
        for i, (pred, conf) in enumerate(zip(predictions, confidence_scores)):
            upper_bound = pred * (1 + 0.15 * (1 - conf))
            lower_bound = pred * (1 - 0.15 * (1 - conf))
            ax1.fill_between([future_dates[i]], lower_bound, upper_bound, 
                           alpha=0.2, color='red', label='Confidence Interval' if i == 0 else "")
        
        ax1.set_title(f'{stock_code} Stock Price Prediction ({days} Days)')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 置信度图
        colors = ['green' if conf > 0.7 else 'orange' if conf > 0.5 else 'red' 
                 for conf in confidence_scores]
        bars = ax2.bar(range(1, days + 1), confidence_scores, color=colors, alpha=0.7)
        ax2.set_title('Prediction Confidence')
        ax2.set_xlabel('Prediction Day')
        ax2.set_ylabel('Confidence')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3)
        
        for i, (bar, conf) in enumerate(zip(bars, confidence_scores)):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{conf:.2f}', ha='center', va='bottom', fontsize=10)
        
        # plt.figure(figsize=(12, 8))
        plt.tight_layout()
        plt.show()
        print("预测图表已显示")
    
    def plot_technical_indicators(self, stock_code):
        """绘制技术指标"""
        if self.data is None:
            print("请先获取股票数据")
            return
            
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # 只显示最近60天的数据
        display_days = min(60, len(self.data))
        display_data = self.data.iloc[-display_days:]
        
        # 价格和移动平均线
        ax1.plot(display_data.index, display_data['Close'], label='Close Price', linewidth=1.5)
        ax1.plot(display_data.index, display_data['MA_5'], label='MA5', linewidth=1)
        ax1.plot(display_data.index, display_data['MA_10'], label='MA10', linewidth=1)
        ax1.plot(display_data.index, display_data['MA_20'], label='MA20', linewidth=1)
        ax1.set_title(f'{stock_code} - Price Trend')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # RSI
        ax2.plot(display_data.index, display_data['RSI'], label='RSI', color='purple', linewidth=1.5)
        ax2.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
        ax2.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
        ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        ax2.set_title('RSI Indicator')
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # MACD
        ax3.plot(display_data.index, display_data['MACD'], label='MACD', color='blue', linewidth=1.5)
        ax3.plot(display_data.index, display_data['MACD_Signal'], label='Signal', color='red', linewidth=1.5)
        ax3.bar(display_data.index, display_data['MACD_Histogram'], 
               label='Histogram', color='gray', alpha=0.3)
        ax3.set_title('MACD Indicator')
        ax3.set_ylabel('MACD')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        print("技术指标图表已显示")
    
    def analyze_stock(self, stock_code, period="1y", predict_days=5):
        """综合分析股票"""
        print(f"开始分析股票: {stock_code}")
        print("=" * 50)
        
        # 获取数据
        if not self.get_stock_data(stock_code, period):
            return
            
        # 准备特征
        if not self.prepare_features(lookback_days=30):
            return
            
        # 训练模型
        if not self.train_model():
            return
            
        # 预测未来多天
        predictions, confidence_scores, future_dates = self.predict_future(days=predict_days)
        
        if predictions:
            current_price = self.data['Close'].iloc[-1]
            
            print(f"\n===== 分析结果 =====")
            print(f"当前股价: {current_price:.2f}")
            print(f"预测未来 {predict_days} 个交易日的股价:")
            print("-" * 60)
            
            for i, (pred, conf) in enumerate(zip(predictions, confidence_scores)):
                day_change = pred - (predictions[i-1] if i > 0 else current_price)
                day_change_pct = (day_change / (predictions[i-1] if i > 0 else current_price)) * 100
                total_change = pred - current_price
                total_change_pct = (total_change / current_price) * 100
                
                trend_icon = "↑" if day_change > 0 else "↓"
                confidence_level = "High" if conf > 0.7 else "Medium" if conf > 0.5 else "Low"
                
                print(f"{trend_icon} Day {i+1}: {pred:>8.2f} | "
                      f"Change: {day_change:>+7.2f} ({day_change_pct:>+6.2f}%) | "
                      f"Confidence: {conf:.2f} ({confidence_level})")
            
            print("-" * 60)
            final_change = predictions[-1] - current_price
            final_change_pct = (final_change / current_price) * 100
            
            if final_change_pct > 5:
                trend = "🚀 Strong Bullish"
            elif final_change_pct > 2:
                trend = "📈 Bullish"
            elif final_change_pct > -2:
                trend = "➡️ Sideways"
            elif final_change_pct > -5:
                trend = "📉 Bearish"
            else:
                trend = "🔻 Strong Bearish"
                
            print(f"Total Change: {final_change:>+8.2f} ({final_change_pct:>+6.2f}%)")
            print(f"Trend: {trend}")
            
            # 绘制图表
            try:
                self.plot_predictions(stock_code, predictions, confidence_scores, future_dates, predict_days)
                self.plot_technical_indicators(stock_code)
            except Exception as e:
                print(f"图表显示错误: {e}")
                print("尝试使用备用显示方式...")
                plt.show(block=True)

def main():
    """主函数"""
    predictor = StockPredictor()
    
    print("股票分析与预测系统")
    print("=" * 30)
    
    # 输入股票代码
    stock_code = input("请输入股票代码(例如: 000001.SZ 或 600036.SS): ").strip()
    
    # 输入预测天数
    try:
        predict_days = int(input("请输入预测天数(1-90): ").strip())
        predict_days = max(1, min(90, predict_days))
    except:
        print("输入无效，使用默认预测天数: 5")
        predict_days = 5
    
    print(f"\n开始分析股票 {stock_code}，预测未来 {predict_days} 天...")
    
    # 分析股票
    predictor.analyze_stock(stock_code, period="1y", predict_days=predict_days)

if __name__ == "__main__":
    main()