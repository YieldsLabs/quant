from ta.ma_indicator import MovingAverageIndicator


class BBIndicator:
    def __init__(self, sma_period=20, multiplier=2):
        self.ma = MovingAverageIndicator(sma_period)
        self.multiplier = multiplier
        self.sma_period = sma_period

    def bb(self, data):
        sma = self.ma.sma(data['close'])
        std_dev = data['close'].rolling(window=self.sma_period).std()
        upper_band = sma + (std_dev * self.multiplier)
        lower_band = sma - (std_dev * self.multiplier)
        return upper_band, lower_band
