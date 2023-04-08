from ta.base.abstract_indicator import AbstractIndicator


class VolumeAdjustedMovingAverage(AbstractIndicator):
    NAME = 'VAMA'

    def __init__(self, short_volatility=50, long_volatility=1000, alpha_factor=0.20):
        super().__init__()
        self.short_volatility = short_volatility
        self.long_volatility = long_volatility
        self.alpha_factor = alpha_factor

    def call(self, data):
        short_std = data['close'].rolling(window=self.short_volatility).std()
        long_std = data['close'].rolling(window=self.long_volatility).std()

        alpha = (short_std / long_std) * self.alpha_factor

        vama = data['close'].copy()
        vama.iloc[0] = data['close'].iloc[0]

        for i in range(1, len(data)):
            vama.iloc[i] = vama.iloc[i - 1] * (1 - alpha.iloc[i]) + data['close'].iloc[i] * alpha.iloc[i]

        return vama
