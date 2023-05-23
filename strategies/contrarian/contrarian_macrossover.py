from risk_management.stop_loss.finders.atr_stop_loss_finder import ATRStopLossFinder
from strategy_management.base_strategy import BaseStrategy
from ta.base.ma import MovingAverage
from ta.momentum.rsi import RelativeStrengthIndex
from ta.volume.vo import VolumeOscillator


class ContrarianMACrossover(BaseStrategy):
    NAME = "CONTRARIANMACROSSOVER"

    def __init__(self, period=8, sma_period=5, oversold=25, overbought=75, lower_exit_barrier=30, upper_exit_barrier=70, lookback=50, atr_multi=1.5, risk_reward_ratio=2):
        indicators = [
            (VolumeOscillator(), ('VO')),
            (RelativeStrengthIndex(period=period), ('rsi')),
        ]
        super().__init__(
            indicators,
            ATRStopLossFinder(atr_multi=atr_multi),
            risk_reward_ratio=risk_reward_ratio
        )
        self.ma = MovingAverage(sma_period)
        self.oversold = oversold
        self.overbought = overbought
        self.lower_exit_barrier = lower_exit_barrier
        self.upper_exit_barrier = upper_exit_barrier
        self.lookback = lookback

    def _generate_buy_entry(self, data):
        rsi = data['rsi']
        rsi_signal = self.ma.sma(rsi)
        vo = data['VO']

        buy_entry = (rsi > rsi_signal) & (rsi.shift(1) < rsi_signal.shift(1)) & (rsi < self.oversold)

        return buy_entry & (vo > 0)

    def _generate_sell_entry(self, data):
        rsi = data['rsi']
        rsi_signal = self.ma.sma(rsi)
        vo = data['VO']

        sell_entry = (rsi < rsi_signal) & (rsi.shift(1) > rsi_signal.shift(1)) & (rsi > self.overbought)

        return sell_entry & (vo < 0)

    def _generate_buy_exit(self, data):
        rsi = data['rsi']

        buy_exit_trigger = rsi > self.upper_exit_barrier
        buy_exit_signal = buy_exit_trigger & (rsi < rsi.shift(1))

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        rsi = data['rsi']

        sell_exit_trigger = rsi < self.lower_exit_barrier
        sell_exit_signal = sell_exit_trigger & (rsi > rsi.shift(1))

        return sell_exit_signal
