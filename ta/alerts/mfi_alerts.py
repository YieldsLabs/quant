from ta.alerts.abstract_alert import AbstractAlert
from ta.volume.mfi import MoneyFlowIndex


class MoneyFlowIndexAlert(AbstractAlert):
    NAME = 'MFI'

    def __init__(self, period=14, overbought=80, oversold=20):
        super().__init__()
        self.mfi = MoneyFlowIndex(period)
        self.overbought = overbought
        self.oversold = oversold
        # known issue with meta labels
        self.period = period

    def call(self, data):
        mfi_values = self.mfi.call(data)

        return mfi_values < self.oversold, mfi_values > self.overbought
