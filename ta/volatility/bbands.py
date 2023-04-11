from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class BollingerBands(AbstractIndicator):
    NAME = 'BBANDS'

    def __init__(self, sma_period=20, multiplier=2):
        super().__init__()
        self.ma = MovingAverage(sma_period)
        self.multiplier = multiplier

    def call(self, data):
        closes = data['close']

        middle_band = self.ma.sma(closes)
        std_dev = closes.rolling(window=self.ma.window).std()
        
        upper_band = middle_band + (std_dev * self.multiplier)
        lower_band = middle_band - (std_dev * self.multiplier)

        return upper_band, middle_band, lower_band
