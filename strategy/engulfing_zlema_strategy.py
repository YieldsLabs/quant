from .base.base_strategy import BaseStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.overlap.zlma import ZeroLagEMA
from ta.patterns.engulfing import Engulfing
from ta.patterns.harami import Harami


class EngulfingZLMA(BaseStrategy):
    NAME = "EZLMA"

    def __init__(self, slow_sma_period=200, oversold=20, overbought=80, tolerance=0.002, retracement_pct=0.05,):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME),
            (MoneyFlowIndexAlert(overbought, oversold), (MoneyFlowIndexAlert.buy_column(), MoneyFlowIndexAlert.sell_column())),
        ]
        patterns = [
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column())),
            (Harami(), (Harami.bullish_column(), Harami.bearish_column())),
        ]
        super().__init__(indicators, patterns)
        self.tolerance = tolerance
        self.retracement_pct = retracement_pct

    def _check_confirmation_candle(self, current_row, previous_row):
        close_diff = abs(previous_row["close"] - current_row[ZeroLagEMA.NAME])
        sma_slow_ratio = close_diff / current_row[ZeroLagEMA.NAME]

        buy_confirmation = (
            previous_row["close"] > current_row[ZeroLagEMA.NAME] and sma_slow_ratio <= self.tolerance
        )

        sell_confirmation = (
            previous_row["close"] < current_row[ZeroLagEMA.NAME] and sma_slow_ratio <= self.tolerance
        )

        return buy_confirmation, sell_confirmation

    def _generate_buy_signal(self, data):
        current_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        buy_confirmation, _ = self._check_confirmation_candle(current_row, previous_row)

        buy_signal = (
            buy_confirmation
            and (current_row[Engulfing.bullish_column()] or current_row[Harami.bullish_column()])
            and current_row[MoneyFlowIndexAlert.buy_column()]
            and (
                current_row["close"]
                >= current_row[ZeroLagEMA.NAME] * (1 - self.retracement_pct)
            )
        )

        return buy_signal

    def _generate_sell_signal(self, data):
        current_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        _, sell_confirmation = self._check_confirmation_candle(current_row, previous_row)

        sell_signal = (
            sell_confirmation
            and (current_row[Engulfing.bearish_column()] or current_row[Harami.bearish_column()])
            and current_row[MoneyFlowIndexAlert.sell_column()]
            and (
                current_row["close"]
                <= current_row[ZeroLagEMA.NAME] * (1 + self.retracement_pct)
            )
        )

        return sell_signal
