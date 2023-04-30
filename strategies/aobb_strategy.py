from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.alerts.mfi_alerts import MoneyFlowIndexAlert
from ta.volatility.bbands import BollingerBands
from ta.momentum.aosc import AwesomeOscillator


class AwesomeOscillatorBollingerBands(BaseStrategy):
    NAME = "AOBB"

    def __init__(self, ao_short_period=5, ao_long_period=34, sma_period=25, stdev_multi=2, mfi_period=14, oversold=40, overbought=60, atr_multi=1.3, risk_reward_ratio=1.5):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (AwesomeOscillator(ao_short_period, ao_long_period), AwesomeOscillator.NAME),
            (MoneyFlowIndexAlert(period=mfi_period, overbought=overbought, oversold=oversold),
                (MoneyFlowIndexAlert.buy_column(), MoneyFlowIndexAlert.sell_column())),
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            ATRStopLossFinder(atr_multi=atr_multi)
        )

    def _generate_buy_signal(self, data):
        close = data['close']
        lower_band = data['lower_band']
        ao = data[AwesomeOscillator.NAME]
        mfi_buy_column = data[MoneyFlowIndexAlert.buy_column()]

        price_change = close.shift() < close
        ao_change = ao.shift() > ao
        price_touch_lower_band = close <= lower_band

        buy_signal = price_change & ao_change & price_touch_lower_band & mfi_buy_column

        return buy_signal

    def _generate_sell_signal(self, data):
        close = data['close']
        upper_band = data['upper_band']
        ao = data[AwesomeOscillator.NAME]
        mfi_sell_column = data[MoneyFlowIndexAlert.sell_column()]

        price_change = close.shift() > close
        ao_change = ao.shift() < ao
        price_touch_upper_band = close >= upper_band

        sell_signal = price_change & ao_change & price_touch_upper_band & mfi_sell_column

        return sell_signal

    def _generate_buy_exit(self, data):
        close = data['close']
        upper_band = data['upper_band']

        cross_upper_band = close >= upper_band

        re_enter_band = cross_upper_band.shift(1) & (close < upper_band)

        buy_exit_signal = re_enter_band

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        lower_band = data['lower_band']

        cross_lower_band = close <= lower_band

        re_enter_band = cross_lower_band.shift(1) & (close > lower_band)

        sell_exit_signal = re_enter_band

        return sell_exit_signal
