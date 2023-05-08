from src.market_data import MarketData
from src.indicators.top_indicators import sma, ema, rsi, stoch, macd
import pandas as pd
import pandas_ta as ta
import pytest


@pytest.fixture
def test_df():
    test_data = MarketData(("BTC", "USDT"))
    test_data.init_candle_df("1d")
    return test_data.get_candle_df()


def test_sma(test_df):
    close = test_df["close"]
    expected_output = ta.sma(close)
    output = sma(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)


def test_ema(test_df):
    close = test_df["close"]
    expected_output = ta.ema(close)
    output = ema(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)


def test_rsi(test_df):
    close = test_df["close"]
    expected_output = ta.rsi(close)
    output = rsi(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)


def test_stoch(test_df):
    high, low, close = test_df["high"], test_df["low"], test_df["close"]
    expected_output = ta.stoch(high, low, close)
    output = stoch(high, low, close)
    pd.testing.assert_frame_equal(output, expected_output, check_names=False)


def test_macd(test_df):
    close = test_df["close"]
    expected_output = ta.macd(close)
    output = macd(close)
    pd.testing.assert_frame_equal(output, expected_output, check_names=False)
