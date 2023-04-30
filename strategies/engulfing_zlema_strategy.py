from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.overlap.zlma import ZeroLagEMA
from ta.patterns.engulfing import Engulfing
from ta.patterns.harami import Harami
from ta.volatility.bbands import BollingerBands


class EngulfingZLMA(BaseStrategy):
    NAME = "EZLMA"

    def __init__(self, slow_sma_period=100, oversold=20, overbought=80, tolerance=0.002, retracement_pct=0.05, atr_multi=1.3, risk_reward_ratio=1.5):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME),
            (MoneyFlowIndexAlert(overbought, oversold), (MoneyFlowIndexAlert.buy_column(), MoneyFlowIndexAlert.sell_column())),
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column())),
            (Harami(), (Harami.bullish_column(), Harami.bearish_column())),
            (BollingerBands(), ('upper_band', 'middle_band', 'lower_band')),
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            ATRStopLossFinder(atr_multi=atr_multi)
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
        upper_band = data['upper_band']

        cross_upper_band = close >= upper_band
        buy_exit_signal = cross_upper_band.shift(1) & (close < upper_band)

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        lower_band = data['lower_band']

        cross_lower_band = close <= lower_band
        sell_exit_signal = cross_lower_band.shift(1) & (close > lower_band)

        return sell_exit_signal
