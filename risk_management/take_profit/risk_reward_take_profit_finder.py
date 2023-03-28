from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.trade_type import TradeType

class RiskRewardTakeProfitFinder(AbstractTakeProfit):
    def __init__(self, risk_reward_ratio=1.5):
        super().__init__()
        self.risk_reward_ratio = risk_reward_ratio

    def next(self, trade_type, entry_price, stop_loss_price):
        risk = abs(entry_price - stop_loss_price)

        if trade_type.value == TradeType.LONG.value:
            take_profit_price = entry_price + self.risk_reward_ratio * risk
        elif trade_type.value == TradeType.SHORT.value:
            take_profit_price = entry_price - self.risk_reward_ratio * risk

        return take_profit_price
    
    def __str__(self) -> str:
        return f'RiskRewardTakeProfitFinder(risk_reward_ratio={self.risk_reward_ratio})'