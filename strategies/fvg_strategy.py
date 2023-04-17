from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.overlap.zlma import ZeroLagEMA
from ta.smc.fair_value_gap import FairValueGap


class FairValueGapZLMA(BaseStrategy):
    NAME = "FVGZLMA"

    def __init__(self, slow_sma_period=100, mfi_period=14, overbought=70, oversold=30, sma_period=40, fair_value=0.5, tolerance=0.02, risk_reward_ratio=1.5):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME),
            (MoneyFlowIndexAlert(period=mfi_period, overbought=overbought, oversold=oversold),
                (MoneyFlowIndexAlert.buy_column(), MoneyFlowIndexAlert.sell_column())),
            (FairValueGap(sma_period), FairValueGap.NAME)
        ]
        super().__init__(
            indicators,
            LowHighStopLossFinder(),
            RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio)
        )
        self.fair_value = fair_value
        self.tolerance = tolerance

    def _check_confirmation_candle(self, current_row, previous_row):
        buy_confirmation = (
            previous_row['close'] > current_row[ZeroLagEMA.NAME]
            and abs(previous_row['close'] - current_row[ZeroLagEMA.NAME]) / current_row[ZeroLagEMA.NAME] <= self.tolerance
        )

        sell_confirmation = (
            previous_row['close'] < current_row[ZeroLagEMA.NAME]
            and abs(previous_row['close'] - current_row[ZeroLagEMA.NAME]) / current_row[ZeroLagEMA.NAME] <= self.tolerance
        )

        return buy_confirmation, sell_confirmation

    def _generate_buy_signal(self, data):
        buy_confirmation, _ = self._check_confirmation_candle(data.iloc[-1], data.iloc[-2])

        buy_signal = (
            data.iloc[-1, data.columns.get_loc(FairValueGap.NAME)] < -self.fair_value
            and buy_confirmation
            and data.iloc[-1, data.columns.get_loc(MoneyFlowIndexAlert.buy_column())]
        )
        return buy_signal

    def _generate_sell_signal(self, data):
        _, sell_confirmation = self._check_confirmation_candle(data.iloc[-1], data.iloc[-2])

        sell_signal = (
            data.iloc[-1, data.columns.get_loc(FairValueGap.NAME)] > self.fair_value
            and sell_confirmation
            and data.iloc[-1, data.columns.get_loc(MoneyFlowIndexAlert.sell_column())]
        )
        return sell_signal
