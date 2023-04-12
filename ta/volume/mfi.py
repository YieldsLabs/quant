from ta.base.abstract_indicator import AbstractIndicator


class MoneyFlowIndex(AbstractIndicator):
    NAME = 'MFI'

    def __init__(self, period=14):
        super().__init__()
        self.period = period

    def call(self, ohlcv):
        high = ohlcv['high']
        low = ohlcv['low']
        close = ohlcv['close']
        volume = ohlcv['volume']

        typical_price = (high + low + close) / 3

        money_flow = typical_price * volume
        money_flow_positive = money_flow.where(typical_price > typical_price.shift(1), 0)
        money_flow_negative = money_flow.where(typical_price < typical_price.shift(1), 0)

        money_flow_positive_sum = money_flow_positive.rolling(window=self.period).sum()
        money_flow_negative_sum = money_flow_negative.rolling(window=self.period).sum()

        money_flow_ratio = money_flow_positive_sum / money_flow_negative_sum

        mfi = 100 - (100 / (1 + money_flow_ratio))

        return mfi
