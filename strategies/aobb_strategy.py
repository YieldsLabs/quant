from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.volatility.bbands import BollingerBands
from ta.volume.mfi import MoneyFlowIndex
from ta.momentum.aosc import AwesomeOscillator


class AwesomeOscillatorBollingerBands(BaseStrategy):
    NAME = "AOBB"

    def __init__(self, ao_short_period=5, ao_long_period=34, sma_period=25, stdev_multi=2, mfi_period=14, oversold=40, overbought=60, atr_multi=1.4, risk_reward_ratio=1.5):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (AwesomeOscillator(ao_short_period, ao_long_period), AwesomeOscillator.NAME),
            (MoneyFlowIndex(period=mfi_period), MoneyFlowIndex.NAME)
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
            ATRStopLossFinder(atr_multi=atr_multi)
        )
        self.oversold = oversold
        self.overbought = overbought

    def _generate_buy_signal(self, data):
        close = data['close']
        lower_band = data['lower_band']
        ao = data[AwesomeOscillator.NAME]
        mfi = data[MoneyFlowIndex.NAME]

        price_change = close.shift() < close
        ao_change = ao.shift() > ao
        price_touch_lower_band = close <= lower_band
        oversold = mfi <= self.oversold

        buy_signal = price_change & ao_change & price_touch_lower_band & oversold

        return buy_signal

    def _generate_sell_signal(self, data):
        close = data['close']
        upper_band = data['upper_band']
        ao = data[AwesomeOscillator.NAME]
        mfi = data[MoneyFlowIndex.NAME]

        price_change = close.shift() > close
        ao_change = ao.shift() < ao
        price_touch_upper_band = close >= upper_band
        overbought = mfi >= self.overbought

        sell_signal = price_change & ao_change & price_touch_upper_band & overbought

        return sell_signal
