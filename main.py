from class_ta import TechAnalysis
import streamlit as st


if __name__ == "__main__":

    st.set_page_config(layout='wide')
    st.title('Технический анализ криптовалют с помощью Binance ')

    ticker1 = st.text_input('Введите тикер **базовой** валюты в чароноприёмник 😛', placeholder='BTC')
    ticker2 = st.text_input('Введите тикер **котируемой** валюты в чароноприёмник 😛', placeholder='USDT')

    if ticker1 and ticker2:
        tech_analysis = TechAnalysis(ticker1 + ticker2)

        timeframe = st.selectbox('Выберите таймфрейм', ('1 минута', '1 час', '1 день', '1 неделя', '1 месяц'))
        time_dict = {'1 минута': '1m', '1 час': '1h', '1 день': '1d', '1 неделя': '1w', '1 месяц': '1M'}
        if timeframe:
            tech_analysis.init_candle_df(time_dict[timeframe])

            indicators = st.multiselect(
                'Выберите до 5 индикаторов',
                ['SMA', 'EMA', 'RSI', 'SO', 'MACD', 'WMA', 'KST', 'KAMA', 'PPO', 'ROC', 'AD', 'CMF', 'CFO', 'ATR',
                 'BB'],
                max_selections=5)

            if indicators:
                tech_analysis.init_indicators_df(indicators)
                tech_analysis.plot_chart()
