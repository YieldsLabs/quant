import pandas as pd
from ta.base.abstract_indicator import AbstractIndicator


class VolumeWeightedAveragePrice(AbstractIndicator):
    NAME = 'VWAP'

    def __init__(self, window=20):
        super().__init__()
        self.window = window

    def call(self, data):
        volume = data['volume'].values
        price = (data['high'].values + data['low'].values + data['close'].values) / 3
        weighted_price = price * volume

        vwap = (
            pd.Series(weighted_price, index=data.index).rolling(window=self.window).sum()
            / data['volume'].rolling(window=self.window).sum()
        )

        return vwap
