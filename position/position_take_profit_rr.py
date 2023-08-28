from core.interfaces.abstract_position_take_profit_strategy import AbstractPositionTakeProfitStrategy


class PositionRRTakeProfit(AbstractPositionTakeProfitStrategy):
    def __init__(self, risk_reward_ratio: float):
        super().__init__()
        self.risk_reward_ratio = risk_reward_ratio

    def next(self, entry_price: float, stop_loss_price: float):
        return self.risk_reward_ratio * (entry_price - stop_loss_price) + entry_price