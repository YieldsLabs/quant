from risk_management.stop_loss.finders.atr_stop_loss_finder import ATRStopLossFinder
from strategy_management.base_strategy import BaseStrategy
from ta.momentum.rsi import RelativeStrengthIndex
from ta.volume.vo import VolumeOscillator


class ContrarianNeutralityPullBack(BaseStrategy):
    NAME = "CONTRARIANNEUTRALITYPULLBACK"

    def __init__(self, period=14, lower_exit_barrier=30, upper_exit_barrier=70, atr_multi=1.5, risk_reward_ratio=2.5):
        indicators = [
            (VolumeOscillator(), ('VO')),
            (RelativeStrengthIndex(period=period), ('rsi')),
        ]
        super().__init__(
            indicators,
            ATRStopLossFinder(atr_multi=atr_multi),
            risk_reward_ratio=risk_reward_ratio
        )
        self.lower_exit_barrier = lower_exit_barrier
        self.upper_exit_barrier = upper_exit_barrier

    def _generate_buy_entry(self, data):
        rsi = data['rsi']
        vo = data['VO']

        buy_entry = (rsi >= 50) & (rsi > rsi.shift(1)) & (rsi.shift(1) > 50) & (rsi.shift(1) < rsi.shift(2)) & (rsi.shift(2) < 53) & (rsi.shift(2) > 50) & (rsi.shift(13) < 50) & (rsi < 55)

        return buy_entry & (vo > 0)

    def _generate_sell_entry(self, data):
        rsi = data['rsi']
        vo = data['VO']

        sell_entry = (rsi <= 50) & (rsi < rsi.shift(1)) & (rsi.shift(1) < 50) & (rsi.shift(1) > rsi.shift(2)) & (rsi.shift(2) > 47) & (rsi.shift(2) < 50) & (rsi.shift(13) > 50) & (rsi > 45)

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
