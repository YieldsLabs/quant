from alerts.abstract_alert import AbstractAlert
from ta.momentum.rsi import RelativeStrengthIndex


class BlueAlert(AbstractAlert):
    NAME = "BLUE"

    def __init__(self, period=21, lookback=21):
        super().__init__()
        self.rsi = RelativeStrengthIndex(period=period)
        self.lookback = lookback

    def alert(self, ohlcv):
        data = ohlcv.copy()

        data['slope'] = (data['close'] - data['close'].shift(self.lookback)) / self.lookback
        data['indicator'] = self.rsi.rsi(data, 'slope')

        buy = (
            (data['indicator'] > 30)
            & (data['indicator'].shift(1) < 30)
            & (data['indicator'] < 35)
        )

        sell = (
            (data['indicator'] < 70)
            & (data['indicator'].shift(1) > 70)
            & (data['indicator'] > 65)
        )

        return buy, sell

    def __str__(self):
        return f'{super().__str__()}'
