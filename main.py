import requests
import pandas as pd
import ta
import matplotlib.pyplot as plt
import sys

class TickerAnalysis:
    def __init__(self, ticker):
        self.base_url = 'https://api.binance.com'
        self.ticker = ticker

    def load_candle_data(self, timeframe='1d'):
        end_point = '/api/v3/klines'
        url = self.base_url + end_point

        params = {
            'symbol': self.ticker,
            'interval': timeframe
        }
        req = requests.get(url, params=params)

        if req.status_code == 200:
            df = pd.DataFrame(req.json())
            df = df.iloc[:, :6]
            df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
            # candle_df.set_index('open_time', inplace=True)
            candle_df = df.iloc[:, 1:6].astype(float)
            candle_df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            self.candle_df = candle_df
        else:
            raise Exception()  # TODO: Add exception

    def calculate_indicators(self, indicators):
        indicators_df = pd.DataFrame()
        for indicator in indicators:
            if indicator == 'SMA':
                indicators_df[indicator] = ta.trend.sma_indicator(self.candle_df['close'])
            elif indicator == 'AI':
                indicators_df[indicator] = ta.trend.aroon_down(self.candle_df['close'])
            elif indicator == 'EMA':
                indicators_df[indicator] = ta.trend.ema_indicator(self.candle_df['close'])
            elif indicator == 'WMA':
                indicators_df[indicator] = ta.trend.wma_indicator(self.candle_df['close'])
            elif indicator == 'MACD':
                indicators_df[indicator] = ta.trend.macd(self.candle_df['close'])
            elif indicator == 'KST':
                indicators_df[indicator] = ta.trend.kst(self.candle_df['close'])
            elif indicator == 'KAMA':
                indicators_df[indicator] = ta.momentum.kama(self.candle_df['close'])
            elif indicator == 'PPO':
                indicators_df[indicator] = ta.momentum.ppo(self.candle_df['close'])
            elif indicator == 'RSI':
                indicators_df[indicator] = ta.momentum.rsi(self.candle_df['close'])
            elif indicator == 'ROC':
                indicators_df[indicator] = ta.momentum.roc(self.candle_df['close'])
            elif indicator == 'ADI':
                indicators_df[indicator] = ta.volume.acc_dist_index(self.candle_df['high'], self.candle_df['low'],
                                                                    self.candle_df['close'], self.candle_df['volume'])
            elif indicator == 'CMF':
                indicators_df[indicator] = ta.volume.chaikin_money_flow(self.candle_df['high'], self.candle_df['low'],
                                                                        self.candle_df['close'],
                                                                        self.candle_df['volume'])
            elif indicator == 'FI':
                indicators_df[indicator] = ta.volume.force_index(self.candle_df['close'], self.candle_df['volume'])
            elif indicator == 'ATR':
                indicators_df[indicator] = ta.volatility.average_true_range(self.candle_df['high'],
                                                                            self.candle_df['low'],
                                                                            self.candle_df['volume'])
            elif indicator == 'BB':
                indicators_df[indicator] = ta.volatility.bollinger_hband(self.candle_df['close'])
        self.indindicators_df = indicators_df

    def plot_chart(self):
        fig, ax = plt.subplots(figsize=(15, 7))

        ax.plot(self.candle_df['open_time'], self.candle_df['open'], label='Цена открытия')

        for indicator in self.indindicators_df.columns:
            ax.plot(self.candle_df['open_time'], self.indindicators_df[indicator], label=indicator)

        ax.legend()
        ax.set_title(f'Цена {self.ticker} с индикаторами')  # TODO Add names
        ax.set_xlabel('Дата')
        ax.set_ylabel('Цена')

        plt.show()

if __name__ == "__main__":

    # Пример ввода из консоли:
    # python main.py BTCUSDT SMA AI EMA WMA MACD
    
    args = sys.argv
    ticker = args[1]
    indicators = list(args[2:])

    ticker_info = TickerAnalysis(ticker)
    ticker_info.load_candle_data()
    ticker_info.calculate_indicators(indicators)
    ticker_info.plot_chart()
