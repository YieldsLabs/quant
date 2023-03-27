from tradetype import TradeType


class SimpleTakeProfitFinder:
    def __init__(self, take_profit_pct=0.03):
        self.take_profit_pct = take_profit_pct

    def calculate_take_profit_price(self, trade_type, entry_price, stop_loss_price=0):
        if trade_type.value == TradeType.LONG.value :
            take_profit_price = entry_price * (1.0 + self.take_profit_pct)
        elif trade_type.value == TradeType.SHORT.value :
            take_profit_price = entry_price * (1.0 - self.take_profit_pct)
        
        return take_profit_price
    
    def __str__(self) -> str:
        return f'SimpleTakeProfitFinder(take_profit_pct={self.take_profit_pct})'
    

class EmptyTakeProfitFinder:
    def calculate_take_profit_price(self, trade_type, entry_price, stop_loss_price=0):
        return None
    
    def __str__(self) -> str:
        return f'EmptyTakeProfitFinder()'
    

class RiskRewardTakeProfitFinder:
    def __init__(self, risk_reward_ratio=1.5):
        self.risk_reward_ratio = risk_reward_ratio

    def calculate_take_profit_price(self, trade_type, entry_price, stop_loss_price):
        risk = abs(entry_price - stop_loss_price)

        if trade_type.value == TradeType.LONG.value:
            take_profit_price = entry_price + self.risk_reward_ratio * risk
        elif trade_type.value == TradeType.SHORT.value:
            take_profit_price = entry_price - self.risk_reward_ratio * risk

        return take_profit_price
    
    def __str__(self) -> str:
        return f'RiskRewardTakeProfitFinder(risk_reward_ratio={self.risk_reward_ratio})'