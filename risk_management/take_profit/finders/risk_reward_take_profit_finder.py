from .abstract_take_profit_finder import AbstractTakeProfit


class RiskRewardTakeProfitFinder(AbstractTakeProfit):
    def __init__(self, risk_reward_ratio=1.5):
        super().__init__()
        self.risk_reward_ratio = risk_reward_ratio

    def next(self, entry, stop_loss):
        return self.risk_reward_ratio * (entry - stop_loss) + entry
