from risk_management.stop_loss.finders.atr_stop_loss_finder import ATRStopLossFinder
from strategy.base_strategy import BaseStrategy
from ta.momentum.rsi import RelativeStrengthIndex
from ta.volume.vo import VolumeOscillator


class ContrarianReversal(BaseStrategy):
    NAME = "CONTRARIANREVERSAL"

    def __init__(self, period=5, lower_barrier=20, lower_threshold=33, upper_barrier=80, upper_threshold=67, lower_exit_barrier=70, upper_exit_barrier=30, atr_multi=1.5, risk_reward_ratio=2.2):
        indicators = [
            (VolumeOscillator(), ('VO')),
            (RelativeStrengthIndex(period=period), ('rsi')),
        ]
        super().__init__(
            indicators,
            ATRStopLossFinder(atr_multi=atr_multi),
            risk_reward_ratio=risk_reward_ratio
        )
        self.lower_barrier = lower_barrier
        self.lower_threshold = lower_threshold
        self.upper_barrier = upper_barrier
        self.upper_threshold = upper_threshold
        self.upper_exit_barrier = upper_exit_barrier
        self.lower_exit_barrier = lower_exit_barrier

    def _generate_buy_entry(self, data):
        rsi = data['rsi']
        vo = data['VO']

        buy_entry = (rsi >= self.lower_barrier) & (rsi < rsi.shift(1)) & (rsi.shift(1) > self.lower_barrier) & (rsi.shift(1) < self.lower_threshold) & (rsi.shift(2) < self.lower_barrier)

        return buy_entry & (vo > 0)

    def _generate_sell_entry(self, data):
        rsi = data['rsi']
        vo = data['VO']

        sell_entry = (rsi <= self.upper_barrier) & (rsi > rsi.shift(1)) & (rsi.shift(1) < self.upper_barrier) & (rsi.shift(1) > self.upper_threshold) & (rsi.shift(2) > self.upper_barrier)

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
