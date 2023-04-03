from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.position_side import PositionSide

class RiskRewardTakeProfitFinder(AbstractTakeProfit):
    def __init__(self, risk_reward_ratio=1.5):
        super().__init__()
        self.risk_reward_ratio = risk_reward_ratio

    def next(self, position_side, entry_price, stop_loss_price):
        risk = abs(entry_price - stop_loss_price)

        if position_side == PositionSide.LONG:
            take_profit_price = entry_price + self.risk_reward_ratio * risk
        elif position_side == PositionSide.SHORT:
            take_profit_price = entry_price - self.risk_reward_ratio * risk

        return take_profit_price
    
    def __str__(self) -> str:
        return f'RiskRewardTakeProfitFinder(risk_reward_ratio={self.risk_reward_ratio})'