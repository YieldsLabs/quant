from shared.meta_label import meta_label
from ta.base.abstract_indicator import AbstractIndicator


@meta_label
class MoneyFlowIndex(AbstractIndicator):
    NAME = 'MFI'

    def __init__(self, period=14):
        super().__init__()
        self.period = period

    def call(self, ohlcv):
        data = ohlcv.copy()

        data['typical_price'] = (data['high'] + data['low'] + data['close']) / 3
        data['money_flow'] = data['typical_price'] * data['volume']
        data['money_flow_positive'] = data['money_flow'].where(data['typical_price'] > data['typical_price'].shift(1), 0)
        data['money_flow_negative'] = data['money_flow'].where(data['typical_price'] < data['typical_price'].shift(1), 0)

        money_flow_positive_sum = data['money_flow_positive'].rolling(window=self.period).sum()
        money_flow_negative_sum = data['money_flow_negative'].rolling(window=self.period).sum()

        money_flow_ratio = money_flow_positive_sum / money_flow_negative_sum
        mfi = 100 - (100 / (1 + money_flow_ratio))

        return mfi
