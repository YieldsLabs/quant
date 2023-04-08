from alerts.abstract_alert import AbstractAlert
from shared.meta_label import meta_label
from ta.momentum.rsi import RelativeStrengthIndex


@meta_label
class GreenAlert(AbstractAlert):
    NAME = "GREEN"

    def __init__(self, period=13, lookback=5):
        super().__init__()
        self.rsi = RelativeStrengthIndex(period=period)
        self.lookback = lookback

    def alert(self, ohlcv):
        data = ohlcv.copy()

        data['rsi'] = self.rsi.rsi(data)
        data['rsi_slope'] = (
            data['rsi'] - data['rsi'].shift(self.lookback)) / self.lookback

        buy = (
            data['rsi_slope'] > 0
            and data['rsi_slope'].shift(1) < 0
            and data['rsi'] < 25
        )

        sell = (
            data['rsi_slope'] < 0
            and data['rsi_slope'].shift(1) > 0
            and data['rsi'] > 75
        )

        return buy, sell

    def __str__(self):
        return f'{super().__str__()}'
