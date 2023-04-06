
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class RelativeStrengthIndex(AbstractIndicator):
    def __init__(self, period=14):
        self.ma = MovingAverage(window=period)

    def call(self, data, column='close'):
        delta = data[column].diff()
        gain, loss = delta.copy(), delta.copy()
        gain[gain < 0] = 0
        loss[loss > 0] = 0
        loss = loss.abs()

        avg_gain = self.ma.sma(gain)
        avg_loss = self.ma.sma(loss)

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def __str__(self) -> str:
        return f'_RSI{self.ma}'
