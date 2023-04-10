from strategy.abstract_strategy import AbstractStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.overlap.zlma import ZeroLagEMA
from ta.smc.fair_value_gap import FairValueGap


class FairValueGapStrategy(AbstractStrategy):
    NAME = "FVG"

    def __init__(self, slow_sma_period=100, mfi_period=14, overbought=70, oversold=30, lookback=40, fair_value=0.5, tolerance=0.02):
        super().__init__()
        self.zlema = ZeroLagEMA(window=slow_sma_period)
        self.mfi = MoneyFlowIndexAlert(period=mfi_period, overbought_level=overbought, oversold_level=oversold)
        self.fvg_indicator = FairValueGap(lookback)
        self.fair_value = fair_value
        self.tolerance = tolerance

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['zlema'] = self.zlema.call(data)
        data['fvg'] = self.fvg_indicator.call(data)
        data['mfi_buy'], data['mfi_sell'] = self.mfi.alert(data)
        return data

    def _check_confirmation_candle(self, current_row, previous_row):
        buy_confirmation = (
            previous_row['close'] > current_row['zlema']
            and abs(previous_row['close'] - current_row['zlema']) / current_row['zlema'] <= self.tolerance
        )

        sell_confirmation = (
            previous_row['close'] < current_row['zlema']
            and abs(previous_row['close'] - current_row['zlema']) / current_row['zlema'] <= self.tolerance
        )

        return buy_confirmation, sell_confirmation

    def entry(self, ohlcv):
        if len(ohlcv) < self.fvg_indicator.ma.window:
            return False, False

        data = self._add_indicators(ohlcv)

        last_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        buy_confirmation, sell_confirmation = self._check_confirmation_candle(last_row, previous_row)

        buy_signal = (
            last_row['fvg'] < -self.fair_value
            and buy_confirmation
            and last_row['mfi_buy']
        )

        sell_signal = (
            last_row['fvg'] > self.fair_value
            and sell_confirmation
            and last_row['mfi_sell']
        )

        return buy_signal, sell_signal
    
    def exit(self, ohlcv):
        return False, False
