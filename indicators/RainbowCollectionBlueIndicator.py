from ta.momentum import RSIIndicator

class RainbowCollectionBlueIndicator:
    def __init__(self, lookback=21, lookback_rsi=21):
        self.lookback = lookback
        self.lookback_rsi = lookback_rsi

    def buy_sell(self, ohlcv):
        data = ohlcv.copy()

        data['slope'] = (data['close'] - data['close'].shift(self.lookback)) / self.lookback
        data['indicator'] = RSIIndicator(data['slope'], self.lookback_rsi).rsi()

        buy = (
            (data['indicator'] > 30) &
            (data['indicator'].shift(1) < 30) &
            (data['indicator'] < 35)
        )

        sell = (
            (data['indicator'] < 70) &
            (data['indicator'].shift(1) > 70) &
            (data['indicator'] > 65)
        )

        return buy, sell