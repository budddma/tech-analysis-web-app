import top_indicators as ti
from class_ta import TechAnalysis
import pandas as pd
import pandas_ta as ta
import pytest


@pytest.fixture
def test_data():
    test = TechAnalysis('BTCUSDT')
    test.init_candle_df('1d')
    return test.get_candle_df()

def test_sma(test_data):
    close = test_data['close']
    expected_output = ta.sma(close)
    output = ti.sma(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)

def test_ema(test_data):
    close = test_data['close']
    expected_output = ta.ema(close)
    output = ti.ema(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)

def test_rsi(test_data):
    close = test_data['close']
    expected_output = ta.rsi(close)
    output = ti.rsi(close)
    pd.testing.assert_series_equal(output, expected_output, check_names=False)

def test_stoch(test_data):
    high, low, close = test_data['high'], test_data['low'], test_data['close']
    expected_output = ta.stoch(high, low, close)
    output = ti.stoch(high, low, close)
    pd.testing.assert_frame_equal(output, expected_output, check_names=False)

def test_macd(test_data):
    close = test_data['close']
    expected_output = ta.macd(close)
    output = ti.macd(close)
    pd.testing.assert_frame_equal(output, expected_output, check_names=False)
