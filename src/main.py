from market_data import MarketData
import streamlit as st

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Технический анализ криптовалют")

    ticker1 = st.text_input(
        "Введите тикер **базовой** валюты в чароноприёмник 😛", placeholder="e.g. BTC"
    )
    ticker2 = st.text_input(
        "Введите тикер **котируемой** валюты в чароноприёмник 😛",
        placeholder="e.g. USDT",
    )
    pair = ticker1 + ticker2

    pairs_list = MarketData.get_possible_pairs()
    if pair in pairs_list:
        market_data = MarketData((ticker1, ticker2))

        timeframe = st.selectbox(
            "Выберите таймфрейм", ("1 минута", "1 час", "1 день", "1 неделя", "1 месяц")
        )
        time_dict = {
            "1 минута": "1m",
            "1 час": "1h",
            "1 день": "1d",
            "1 неделя": "1w",
            "1 месяц": "1M",
        }

        if timeframe:
            market_data.init_candle_df(time_dict[timeframe])

            indicators = st.multiselect(
                "Выберите до 5 индикаторов",
                [
                    "SMA",
                    "EMA",
                    "RSI",
                    "SO",
                    "MACD",
                    "WMA",
                    "KST",
                    "KAMA",
                    "PPO",
                    "ROC",
                    "AD",
                    "CMF",
                    "CFO",
                    "ATR",
                    "BB",
                ],
                max_selections=5,
            )

            if indicators:
                market_data.init_indicators_df(indicators)
                market_data.plot_chart()
