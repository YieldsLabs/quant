from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)


class PositionRiskRewardTakeProfitStrategy(AbstractPositionTakeProfitStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")

    def next(self, entry_price: float, stop_loss_price: float):
        return (
            self.config["risk_reward_ratio"] * (entry_price - stop_loss_price)
            + entry_price
        )
