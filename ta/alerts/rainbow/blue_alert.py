from alerts.abstract_alert import AbstractAlert
from ta.indicators.rsi_indicator import RSIIndicator


class BlueAlert(AbstractAlert):
    def __init__(self, lookback=21, lookback_rsi=21):
        super().__init__()
        self.lookback = lookback
        self.rsi = RSIIndicator(period=lookback_rsi)

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
