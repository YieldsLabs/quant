import numpy as np
from risk_management.stop_loss.finders.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.finders.simple_stop_loss_finder import SimpleStopLossFinder
from ta.volatility.atr import AverageTrueRange


class ATRStopLossFinder(AbstractStopLoss):
    NAME = 'ATR'

    def __init__(self, period=14, atr_multi=1.5, stop_loss_pct=0.02):
        super().__init__()
        self.atr_indicator = AverageTrueRange(period)
        self.base_stop_loss_finder = SimpleStopLossFinder(stop_loss_pct=stop_loss_pct)
        self.atr_multi = atr_multi
        self.period = period

    def next(self, entry, ohlcv):
        atr_value = self.atr_indicator.call(ohlcv)
        atr_value = atr_value.iloc[-1]

        if np.isnan(atr_value):
            return self.base_stop_loss_finder.next(entry, ohlcv)

        atr = atr_value * self.atr_multi

        return entry - atr, entry + atr
