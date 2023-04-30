from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.overlap.zlma import ZeroLagEMA
from ta.patterns.engulfing import Engulfing
from ta.patterns.harami import Harami


class EngulfingZLMA(BaseStrategy):
    NAME = "EZLMA"

    def __init__(self, slow_sma_period=100, oversold=20, overbought=80, tolerance=0.002, retracement_pct=0.05, risk_reward_ratio=1.5):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME),
            (MoneyFlowIndexAlert(overbought, oversold), (MoneyFlowIndexAlert.buy_column(), MoneyFlowIndexAlert.sell_column())),
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column())),
            (Harami(), (Harami.bullish_column(), Harami.bearish_column())),
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
            LowHighStopLossFinder()
        )
        self.tolerance = tolerance
        self.retracement_pct = retracement_pct

    def _generate_buy_signal(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        bullish_column = data[Engulfing.bullish_column()] | data[Harami.bullish_column()]
        mfi_buy_column = data[MoneyFlowIndexAlert.buy_column()]

        buy_confirmation = (close.shift() > zlema) & (abs(close.shift() - zlema) / zlema <= self.tolerance)

        buy_signal = buy_confirmation & bullish_column & mfi_buy_column & (close >= zlema * (1 - self.retracement_pct))

        return buy_signal

    def _generate_sell_signal(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        bearish_column = data[Engulfing.bearish_column()] | data[Harami.bearish_column()]
        mfi_sell_column = data[MoneyFlowIndexAlert.sell_column()]

        sell_confirmation = (close.shift() < zlema) & (abs(close.shift() - zlema) / zlema <= self.tolerance)

        sell_signal = sell_confirmation & bearish_column & mfi_sell_column & (close <= zlema * (1 + self.retracement_pct))

        return sell_signal

    def _generate_buy_exit(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        bearish_column = data[Engulfing.bearish_column()] | data[Harami.bearish_column()]

        buy_exit_signal = (close >= zlema) | bearish_column

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]
        bullish_column = data[Engulfing.bullish_column()] | data[Harami.bullish_column()]

        sell_exit_signal = (close <= zlema) | bullish_column

        return sell_exit_signal
