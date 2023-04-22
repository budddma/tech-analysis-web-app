import requests
import pandas as pd
import ta
import plotly.graph_objects as go
import streamlit as st


class TechAnalysis:
    def __init__(self, pair):
        self.__base_url = 'https://api.binance.com'
        self.__pair = pair
        self.__cndl_df = None
        self.__ind_df = None

    def init_candle_df(self, timeframe='1d'):  # todo добавить timeframe (def value)
        end_point = '/api/v3/klines'

        # Формируем путь для задания запроса
        url = self.__base_url + end_point
        params = {
            'symbol': self.__pair,
            'interval': timeframe,
            'limit': 300
        }

        # Отправляем запрос о тикере
        req = requests.get(url, params=params)

        if req.status_code == 200:
            cndl_df = pd.DataFrame(req.json()).iloc[:, :6]
            cndl_df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
            cndl_df['open_time'] = pd.to_datetime(cndl_df['open_time'], unit='ms')
            cndl_df.iloc[:, 1:6] = cndl_df.iloc[:, 1:6].astype(float)
            self.__cndl_df = cndl_df
        else:
            raise Exception(f"Binance API request ended with error {req.status_code}")  # todo st.error

    def init_indicators_df(self, indicators):
        ind_df = pd.DataFrame()
        for ind in indicators:
            if ind == 'SMA':
                ind_df[ind] = ta.trend.sma_indicator(self.__cndl_df['close'])
            elif ind == 'AI':
                ind_df[ind] = ta.trend.aroon_down(self.__cndl_df['close'])
            elif ind == 'EMA':
                ind_df[ind] = ta.trend.ema_indicator(self.__cndl_df['close'])
            elif ind == 'WMA':
                ind_df[ind] = ta.trend.wma_indicator(self.__cndl_df['close'])
            elif ind == 'MACD':
                ind_df[ind] = ta.trend.macd(self.__cndl_df['close'])
            elif ind == 'KST':
                ind_df[ind] = ta.trend.kst(self.__cndl_df['close'])
            elif ind == 'KAMA':
                ind_df[ind] = ta.momentum.kama(self.__cndl_df['close'])
            elif ind == 'PPO':
                ind_df[ind] = ta.momentum.ppo(self.__cndl_df['close'])
            elif ind == 'RSI':
                ind_df[ind] = ta.momentum.rsi(self.__cndl_df['close'])
            elif ind == 'ROC':
                ind_df[ind] = ta.momentum.roc(self.__cndl_df['close'])
            elif ind == 'ADI':
                ind_df[ind] = ta.volume.acc_dist_index(self.__cndl_df['high'], self.__cndl_df['low'],
                                                       self.__cndl_df['close'], self.__cndl_df['volume'])
            elif ind == 'CMF':
                ind_df[ind] = ta.volume.chaikin_money_flow(self.__cndl_df['high'], self.__cndl_df['low'],
                                                           self.__cndl_df['close'],
                                                           self.__cndl_df['volume'])
            elif ind == 'FI':
                ind_df[ind] = ta.volume.force_index(self.__cndl_df['close'], self.__cndl_df['volume'])
            elif ind == 'ATR':
                ind_df[ind] = ta.volatility.average_true_range(self.__cndl_df['high'],
                                                               self.__cndl_df['low'],
                                                               self.__cndl_df['volume'])
            elif ind == 'BB':
                ind_df[ind] = ta.volatility.bollinger_hband(self.__cndl_df['close'])
        self.__ind_df = ind_df

    def plot_chart(self):
        # объявляем фигуру
        fig = go.Figure()

        # добавляем свечи
        fig.add_trace(go.Candlestick(x=self.__cndl_df['open_time'],
                                     open=self.__cndl_df['open'], high=self.__cndl_df['high'],
                                     low=self.__cndl_df['low'], close=self.__cndl_df['close'], name='Свечи')
                      )

        # добавляем индикаторы
        for ind in self.__ind_df.columns:
            fig.add_trace(go.Scatter(x=self.__cndl_df['open_time'], y=self.__ind_df[ind], name=ind))

        str_indicators = ', '.join(self.__ind_df.columns.to_list())

        # свойства фигуры
        fig.update_layout(
            height=600, width=800,
            title_text=f'Цена {self.__pair} и индикаторы {str_indicators}',  # todo нормальные подписи
            title_font_size=20,
            yaxis_title='Стоимость',
            xaxis_rangeslider_visible=False)

        st.plotly_chart(fig)


if __name__ == "__main__":
    # Пример ввода из консоли:
        # streamlit run main.py
    # BTCUSDT

    # todo ЗАГОЛОВОК: ТЕХ АНАЛИЗ КРИПТОВАЛЮТ ИСПОЛЬЗУЯ БИНАНС

    pair = st.text_input('Введите тикер криптовалют в чароноприёмник')  # todo можно отдельно вводить EUR И USD
    ticker_info = TechAnalysis(pair)
    ticker_info.init_candle_df()
    indicators = st.multiselect(
        'Выберите не более 5 индикаторов',
        ['AI', 'PPO', 'RSI', 'SMA'], max_selections=5)
    ticker_info.init_indicators_df(indicators)
    ticker_info.plot_chart()

#   TODO: Добавить комменты по коду с помощью copilot и удалить из README
#   TODO добавить в readme пример графика
#   TODO разделить на файлы main handwritten_indicators tech_analysis
