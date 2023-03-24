from strategy.AbstractStrategy import AbstractStrategy
from indicators.FalseBreakoutIndicator import FalseBreakoutIndicator

class FalseBreakoutStrategy(AbstractStrategy):
    def __init__(self, breakout_period=20, min_period=5, max_period=5, ma_type="ema", smoothing_length=10, aggressive=False):
        self.false_breakout_indicator = FalseBreakoutIndicator(
            breakout_period=breakout_period,
            min_period=min_period,
            max_period=max_period,
            ma_type=ma_type,
            smoothing_length=smoothing_length,
            aggressive=aggressive
        )

    def add_indicators(self, ohlcv):
        data = ohlcv.copy()
        false_breakout_up, false_breakout_down = self.false_breakout_indicator.false_breakout(data)

        data['buy_signal'] = false_breakout_down
        data['sell_signal'] = false_breakout_up

        return data
    
    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
        last_row = data.iloc[-1]

        return last_row['buy_signal'], last_row['sell_signal']

    def __str__(self) -> str:
        return 'FalseBreakoutStrategy'
