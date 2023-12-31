from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide


class PositionRiskBreakEvenStrategy(AbstractPositionRiskStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")

    def next(
        self,
        side: PositionSide,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcv: OHLCV,
    ) -> float:
        current_price = self._weighted_typical_price(ohlcv)

        distance = abs(take_profit_price - current_price) * self.config["tsl_distance"]

        next_stop_loss = stop_loss_price
        next_take_profit = take_profit_price

        if side == PositionSide.LONG:
            next_stop_loss = max(stop_loss_price, current_price - distance)

        if side == PositionSide.SHORT:
            next_stop_loss = min(stop_loss_price, current_price + distance)

        next_take_profit = (
            self.config["risk_reward_ratio"] * (current_price - next_stop_loss)
            + current_price
        )

        return next_stop_loss, next_take_profit

    @staticmethod
    def _weighted_typical_price(ohlcv: OHLCV) -> float:
        return (ohlcv.high + ohlcv.low + (ohlcv.close * 2.0)) / 4.0
