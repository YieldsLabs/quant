from .abstract_take_profit_finder import AbstractTakeProfit


class RiskRewardTakeProfitFinder(AbstractTakeProfit):
    NAME = 'RSKRWRD'

    def __init__(self, risk_reward_ratio=1.5):
        super().__init__()
        self.risk_reward_ratio = risk_reward_ratio

    def next(self, entry, stop_loss):
        risk = entry - stop_loss

        return entry + self.risk_reward_ratio * risk
