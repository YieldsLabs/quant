from ta.alerts.abstract_alert import AbstractAlert
from ta.volume.mfi import MoneyFlowIndex


class MoneyFlowIndexAlert(AbstractAlert):
    NAME = 'MFI'

    def __init__(self, period=14, overbought_level=80, oversold_level=20):
        super().__init__()
        self.mfi = MoneyFlowIndex(period)
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level

    def call(self, data):
        mfi_values = self.mfi.call(data)

        oversold = mfi_values < self.oversold_level
        overbought = mfi_values > self.overbought_level

        return oversold, overbought