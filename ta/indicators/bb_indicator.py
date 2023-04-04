
from ta.indicators.base.abstract_indicator import AbstractIndicator

from ta.indicators.base.ma import MovingAverage


class BBIndicator(AbstractIndicator):
    def __init__(self, sma_period=20, multiplier=2):
        self.ma = MovingAverage(sma_period)
        self.multiplier = multiplier
        self.sma_period = sma_period

    def call(self, data):
        middle_band = self.ma.sma(data['close'])
        std_dev = data['close'].rolling(window=self.sma_period).std()
        upper_band = middle_band + (std_dev * self.multiplier)
        lower_band = middle_band - (std_dev * self.multiplier)
        return upper_band, middle_band, lower_band
    
    def __str__(self) -> str:
        return f'BBIndicator(multiplier={self.multiplier}, sma_period={self.sma_period})'
