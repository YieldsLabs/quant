from alerts.abstract_alert import AbstractAlert
from ta.atr_indicator import ATRIndicator
from ta.rsi_indicator import RSIIndicator

class UTBotAlerts(AbstractAlert):
    def __init__(self, atr_period=10, sensitivity=2, ema_period=1):
        super().__init__()
        self.atr_period = atr_period
        self.sensitivity = sensitivity
        self.ema_period = ema_period
        self.atr_indicator = ATRIndicator(period=atr_period)
        self.rsi_indicator = RSIIndicator(period=ema_period)

    def alert(self, ohlcv):
        data = ohlcv.copy()

        data['atr'] = self.atr_indicator.atr(ohlcv)
        nloss = self.sensitivity * data['atr']

        data['slope'] = (data['close'] - data['close'].shift(self.ema_period)) / self.ema_period
        data['rsi'] = self.rsi_indicator.rsi(data, 'slope')

        buy = (
            (data['rsi'] > 30) &
            (data['rsi'].shift(1) < 30) &
            (data['rsi'] < 35) &
            (data['close'] - data['close'].shift(1) > nloss)
        )

        sell = (
            (data['rsi'] < 70) &
            (data['rsi'].shift(1) > 70) &
            (data['rsi'] > 65) &
            (data['close'].shift(1) - data['close'] > nloss)
        )

        return buy, sell
