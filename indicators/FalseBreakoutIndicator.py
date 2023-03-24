import numpy as np
from ta.MovingAverageIndicator import MovingAverageIndicator

class FalseBreakoutIndicator:
    def __init__(self, breakout_period=20, min_period=5, max_period=5, ma_type="ema", smoothing_length=10, aggressive=False):
        self.breakout_period = breakout_period
        self.min_period = min_period
        self.max_period = max_period
        self.ma_type = ma_type
        self.smoothing_length = smoothing_length
        self.aggressive = aggressive
        self.ma_indicator = MovingAverageIndicator(window=smoothing_length)

    def apply_smoothing(self, data):
        if self.ma_type == "ema":
            return self.ma_indicator.ema(data)
        elif self.ma_type == "wma":
            return self.ma_indicator.wma(data)
        else:
            return data

    def false_breakout(self, ohlcv):
        data = ohlcv.copy()

        hi = self.apply_smoothing(data['high'].rolling(window=self.breakout_period).max())
        lo = self.apply_smoothing(data['low'].rolling(window=self.breakout_period).min())

        if self.aggressive:
            hi = self.apply_smoothing(data['low'].rolling(window=self.breakout_period).max())
            lo = self.apply_smoothing(data['high'].rolling(window=self.breakout_period).min())

        data['new_high'] = (hi > hi.shift(1)) & (hi.shift(1) <= hi.shift(2))
        data['new_low'] = (lo < lo.shift(1)) & (lo.shift(1) >= lo.shift(2))

        data['count'] = np.where(data['new_high'], -1, np.where(data['new_low'], 1, 0)).cumsum()
        data['index'] = data.index

        min_bars = data['index'] - data['index'].shift(self.min_period) > 0
        max_valid = (data['index'] - data['index'].shift(-self.max_period)) <= 0

        data['breakdown'] = data['close'].shift(1) > hi.shift(1)
        data['breakup'] = data['close'].shift(1) < lo.shift(1)

        data['false_breakout_up'] = (data['count'] < -1) & data['breakdown'] & max_valid & min_bars
        data['false_breakout_down'] = (data['count'] > 1) & data['breakup'] & max_valid & min_bars

        return data['false_breakout_up'], data['false_breakout_down']
