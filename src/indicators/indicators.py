import pandas as pd


def sma(close, length=10):
    return close.rolling(window=length).mean()


def ema(close, length=10):
    close_copy = close.copy()
    sma_nth = close_copy[0:length].mean()

    close_copy[:length - 1] = 'nan'
    close_copy.iloc[length - 1] = sma_nth

    return close_copy.ewm(span=length, adjust=False).mean()


def rsi(close, length=14):
    negative = close.diff()
    positive = negative.copy()

    positive[positive < 0] = 0
    negative[negative > 0] = 0

    positive_avg = positive.ewm(alpha=(1.0 / length), min_periods=length).mean()
    negative_avg = negative.ewm(alpha=(1.0 / length), min_periods=length).mean()

    return 100 * positive_avg / (positive_avg + negative_avg.abs())


def stoch(high, low, close, k=14, d=3):
    lowest_low = low.rolling(k).min()
    highest_high = high.rolling(k).max()

    stoch = 100 * (close - lowest_low) / (highest_high - lowest_low)

    stoch_k = sma(stoch.loc[stoch.first_valid_index():, ], length=d)
    stoch_d = sma(stoch_k.loc[stoch_k.first_valid_index():, ], length=d)

    return pd.DataFrame({'STOCHk_14_3_3': stoch_k, 'STOCHd_14_3_3': stoch_d})


def macd(close, fast=12, slow=26, signal=9):
    fast_ema = ema(close, length=fast)
    slow_ema = ema(close, length=slow)

    macd_line = fast_ema - slow_ema
    signal_ema = ema(close=macd_line.loc[macd_line.first_valid_index():, ], length=signal)
    histogram = macd_line - signal_ema

    return pd.DataFrame({'MACD_12_26_9': macd_line, 'MACDh_12_26_9': histogram, 'MACDs_12_26_9': signal_ema})
