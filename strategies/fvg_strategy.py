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
            RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
            LowHighStopLossFinder()
        )
        self.fair_value = fair_value
        self.tolerance = tolerance

    def _generate_buy_signal(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        mfi_buy_column = data[MoneyFlowIndexAlert.buy_column()]
        fair_value_gap_column = data[FairValueGap.NAME]

        buy_confirmation = (close.shift() > zlema) & (abs(close.shift() - zlema) / zlema <= self.tolerance)

        buy_signal = buy_confirmation & (fair_value_gap_column < -self.fair_value) & mfi_buy_column

        return buy_signal

    def _generate_sell_signal(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        mfi_sell_column = data[MoneyFlowIndexAlert.sell_column()]
        fair_value_gap_column = data[FairValueGap.NAME]

        sell_confirmation = (close.shift() < zlema) & (abs(close.shift() - zlema) / zlema <= self.tolerance)

        sell_signal = sell_confirmation & (fair_value_gap_column > self.fair_value) & mfi_sell_column

        return sell_signal
    
    def _generate_buy_exit(self, data):
        close = data['close']
        fair_value_gap_column = data[FairValueGap.NAME]
        
        buy_exit_signal = (close > close.shift()) & (fair_value_gap_column >= -self.fair_value)
        
        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        fair_value_gap_column = data[FairValueGap.NAME]
        
        sell_exit_signal = (close < close.shift()) & (fair_value_gap_column <= self.fair_value)
        
        return sell_exit_signal
