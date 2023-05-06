from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy_management.base_strategy import BaseStrategy
from ta.momentum.rsi import RelativeStrengthIndex


class ContrarianNeutralityPullBack(BaseStrategy):
    NAME = "CONTRARIANNEUTRALITYPULLBACK"

    def __init__(self, lookback=50, period=14, oversold=20, overbought=80, atr_multi=1.2, risk_reward_ratio=3):
        indicators = [
            (RelativeStrengthIndex(period=period), ('rsi')),
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            ATRStopLossFinder(atr_multi=atr_multi)
        )
        self.oversold = oversold
        self.overbought = overbought
        self.lookback = lookback

    def _generate_buy_entry(self, data):
        rsi = data['rsi']

        buy_entry = (rsi >= 50) & (rsi > rsi.shift(1)) & (rsi.shift(1) > 50) & (rsi.shift(1) < rsi.shift(2)) & (rsi.shift(2) < 53) & (rsi.shift(2) > 50) & (rsi.shift(13) < 50) & (rsi < 55)

        return buy_entry

    def _generate_sell_entry(self, data):
        rsi = data['rsi']

        sell_entry = (rsi <= 50) & (rsi < rsi.shift(1)) & (rsi.shift(1) < 50) & (rsi.shift(1) > rsi.shift(2)) & (rsi.shift(2) > 47) & (rsi.shift(2) < 50) & (rsi.shift(13) > 50) & (rsi > 45)

        return sell_entry

    def _generate_buy_exit(self, data):
        rsi = data['rsi']

        buy_exit_signal = rsi > self.overbought

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        rsi = data['rsi']

        sell_exit_signal = rsi < self.oversold

        return sell_exit_signal
