
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class BollingerBands(AbstractIndicator):
    def __init__(self, sma_period=20, multiplier=2):
        self.ma = MovingAverage(sma_period)
        self.multiplier = multiplier

    def call(self, data):
        middle_band = self.ma.sma(data['close'])
        std_dev = data['close'].rolling(window=self.ma.window).std()
        upper_band = middle_band + (std_dev * self.multiplier)
        lower_band = middle_band - (std_dev * self.multiplier)
        
        return upper_band, middle_band, lower_band

    def __str__(self) -> str:
        return f'_BBANDS_{self.multiplier}{self.ma}'
