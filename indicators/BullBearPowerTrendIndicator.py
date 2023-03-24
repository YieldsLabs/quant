import pandas as pd
from ta.volatility import AverageTrueRange

class BullBearPowerTrendIndicator:
    def __init__(self, atr_period=5, lookback_high_low=50, lookback_trend=8):
        self.atr_period = atr_period
        self.lookback_high_low = lookback_high_low
        self.lookback_trend = lookback_trend

    def bull_and_bear(self, data):
        atr = AverageTrueRange(data['high'], data['low'], data['close'], self.atr_period).average_true_range()
        lowest_low = data['low'].rolling(window=self.lookback_high_low).min()
        highest_high = data['high'].rolling(window=self.lookback_high_low).max()

        bull_trend = (data['close'] - lowest_low) / atr
        bear_trend = (highest_high - data['close']) / atr
        bear_trend2 = -1 * bear_trend

        trend = bull_trend - bear_trend

        x = pd.Series(range(len(data)))
        y = pd.Series(trend)
        x_ = x.rolling(window=self.lookback_trend).mean()
        y_ = y.rolling(window=self.lookback_trend).mean()

        mx = x.rolling(window=self.lookback_trend).std()
        my = y.rolling(window=self.lookback_trend).std()
        c = x.rolling(window=self.lookback_trend).corr(y)

        slope = c * (my / mx)
        inter = y_ - slope * x_
        reg_trend = x * slope + inter

        return bull_trend, bear_trend, bear_trend2, reg_trend
