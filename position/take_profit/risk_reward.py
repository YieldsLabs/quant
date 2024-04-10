from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)
from core.models.side import PositionSide


class PositionRiskRewardTakeProfitStrategy(AbstractPositionTakeProfitStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")

    def next(self, side: PositionSide, entry_price: float, stop_loss_price: float):
        if side == PositionSide.LONG:
            return (
                entry_price
                + (entry_price - stop_loss_price) * self.config["risk_reward_ratio"]
            )

        return (
            entry_price
            - (stop_loss_price - entry_price) * self.config["risk_reward_ratio"]
        )
