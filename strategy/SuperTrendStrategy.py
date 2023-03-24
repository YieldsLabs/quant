from indicators.SuperTrendIndicator import SuperTrendIndicator
from strategy.AbstractStrategy import AbstractStrategy

class SuperTrendStrategy(AbstractStrategy):
    def __init__(self, atr_period=10, multiplier=3):
        super().__init__()
        self.supertrend_indicator = SuperTrendIndicator(atr_period, multiplier)
        # self.slope_threshold = slope_threshold

    def add_indicators(self, data):
        data = data.copy()
        data['supertrend'] = self.supertrend_indicator.supertrend(data)
        return data

    def supertrend_slope(self, data):
        data['supertrend_slope'] = data['supertrend'].diff()
        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
        data = self.supertrend_slope(data)
        current_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        buy_signal = (
            previous_row['close'] <= previous_row['supertrend'] and
            current_row['close'] > current_row['supertrend']
        )
        sell_signal = (
            previous_row['close'] >= previous_row['supertrend'] and
            current_row['close'] < current_row['supertrend']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'SupertrendStrategy'
