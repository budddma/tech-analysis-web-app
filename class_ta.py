import requests
import pandas as pd
import top_indicators
import pandas_ta as ta
import plotly.graph_objects as go
import streamlit as st


class TechAnalysis:
    def __init__(self, pair):
        self.__base_url = 'https://api.binance.com'
        self.__pair = pair
        self.__cndl_df = None
        self.__ind_df = None

    def init_candle_df(self, timeframe):
        end_point = '/api/v3/klines'

        url = self.__base_url + end_point
        params = {
            'symbol': self.__pair,
            'interval': timeframe,
            'limit': 300
        }

        req = requests.get(url, params=params)

        if req.status_code == 200:
            cndl_df = pd.DataFrame(req.json()).iloc[:, :6]
            cndl_df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
            cndl_df['open_time'] = pd.to_datetime(cndl_df['open_time'], unit='ms')
            cndl_df[cndl_df.columns[1:6]] = cndl_df[cndl_df.columns[1:6]].astype(float)
            self.__cndl_df = cndl_df
        else:
            raise Exception(f'🚨 Binance API request ended with error {req.status_code}')

    def get_candle_df(self):
        return self.__cndl_df

    def init_indicators_df(self, indicators):
        ind_df = pd.DataFrame()
        ind_dict = {
            'SMA': top_indicators.sma,  # close
            'EMA': top_indicators.ema,  # close
            'RSI': top_indicators.rsi,  # close
            'SO': top_indicators.stoch,  # high low close
            'MACD': top_indicators.macd,  # close
            'WMA': ta.wma,  # close
            'KST': ta.kst,  # close
            'KAMA': ta.kama,  # close
            'PPO': ta.ppo,  # close
            'ROC': ta.roc,  # close
            'AD': ta.ad,  # high low close volume
            'CMF': ta.cmf,  # high low close
            'CFO': ta.cfo,  # close
            'ATR': ta.atr,  # high low close
            'BB': ta.bbands  # close
        }

        for ind in indicators:
            ind_func = ind_dict[ind]
            if ind in {'SO', 'ATR'}:
                ind_args = [self.__cndl_df['high'], self.__cndl_df['low'], self.__cndl_df['close']]
            elif ind in {'AD', 'CMF'}:
                ind_args = [self.__cndl_df['high'], self.__cndl_df['low'], self.__cndl_df['close'],
                            self.__cndl_df['volume']]
            else:
                ind_args = [self.__cndl_df['close']]

            fuc_out = ind_func(*ind_args)
            if isinstance(fuc_out, pd.DataFrame):
                for col in fuc_out.columns:
                    ind_df[col] = fuc_out[col]
            else:
                ind_df[ind] = ind_func(*ind_args)

        self.__ind_df = ind_df

    def plot_chart(self):

        fig = go.Figure()

        min_price, max_price = 0, float('INF')

        fig.add_trace(go.Candlestick(x=self.__cndl_df['open_time'],
                                     open=self.__cndl_df['open'], high=self.__cndl_df['high'],
                                     low=self.__cndl_df['low'], close=self.__cndl_df['close'], name='Свеча')
                      )

        for ind in self.__ind_df.columns:
            fig.add_trace(go.Scatter(x=self.__cndl_df['open_time'], y=self.__ind_df[ind], name=ind))
            min_price = min(self.__ind_df[ind].min(), min_price, self.__cndl_df['low'].min())
            max_price = max(self.__ind_df[ind].max(), max_price, self.__cndl_df['high'].max())

        str_indicators = ', '.join(self.__ind_df.columns.to_list())

        fig.update_layout(
            title_text=f'{self.__pair} и индикаторы {str_indicators}',
            title_font_size=20,
            yaxis_title='Стоимость',
            xaxis_rangeslider_visible=False)

        fig.update_yaxes(
            range=[min_price, max_price]
        )

        st.plotly_chart(fig, use_container_width=True)
