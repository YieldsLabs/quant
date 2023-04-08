from shared.meta_label import meta_label
from ta.alerts.abstract_alert import AbstractAlert
from ta.volume.mfi import MoneyFlowIndex


@meta_label
class MoneyFlowIndexAlert(AbstractAlert):
    NAME = 'MFI'

    def __init__(self, period=14, overbought_level=80, oversold_level=20):
        super().__init__()
        self.mfi = MoneyFlowIndex(period)
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level

    def alert(self, data):
        data['mfi'] = self.mfi.call(data)

        return data['mfi'] < self.oversold_level, data['mfi'] > self.overbought_level
