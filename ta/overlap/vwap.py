from shared.meta_label import meta_label
from ta.base.abstract_indicator import AbstractIndicator


@meta_label
class VolumeWeightedAveragePrice(AbstractIndicator):
    NAME = 'VWAP'

    def __init__(self, window=20):
        super().__init__()
        self.window = window

    def call(self, data):
        volume = data['volume'].values
        price = (data['high'] + data['low'] + data['close']) / 3
        vwap = (price * volume).rolling(window=self.window).sum() / \
            data['volume'].rolling(window=self.window).sum()
        return vwap
