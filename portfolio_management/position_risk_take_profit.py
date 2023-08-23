class PositionTakeProfit:
    @staticmethod
    def calculate(entry: float, stop_loss: float, risk_reward_ratio: float):
        return risk_reward_ratio * (entry - stop_loss) + entry
