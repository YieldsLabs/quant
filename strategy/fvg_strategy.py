from strategy.abstract_strategy import AbstractStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlerts
from ta.indicators.zlema_indicator import ZeroLagEMAIndicator
from ta.smc.fair_value_gap import FairValueGapIndicator


class FairValueGapStrategy(AbstractStrategy):
    def __init__(self, lookback=40, overbought=70, oversold=30, fair_value=0.5, slow_sma_period=100, tolerance=0.02):
        super().__init__()
        self.lookback = lookback
        self.fair_value = fair_value
        self.tolerance = tolerance

        self.fvg_indicator = FairValueGapIndicator(lookback)
        self.zlema = ZeroLagEMAIndicator(window=slow_sma_period)
        self.mfi = MoneyFlowIndexAlerts(overbought_level=overbought, oversold_level=oversold)

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
        if len(ohlcv) < self.lookback:
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
        pass

    def __str__(self) -> str:
        return f'FairValueGapStrategy(lookback={self.lookback}, fair_value={self.fair_value})'
