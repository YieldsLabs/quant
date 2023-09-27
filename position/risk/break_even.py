from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide


class PositionRiskBreakEvenStrategy(AbstractPositionRiskStrategy):
    def __init__(self, break_even_percentage: float = 0.25):
        super().__init__()
        self.break_even_percentage = break_even_percentage

    def next(
        self,
        side: PositionSide,
        entry_price: float,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcv: OHLCV,
    ) -> float:
        distance_to_target = (
            abs(take_profit_price - entry_price) * self.break_even_percentage
        )
        current_price = self._weighted_typical_price(ohlcv)

        if side == PositionSide.LONG:
            if current_price >= entry_price + distance_to_target:
                return entry_price

        elif side == PositionSide.SHORT:
            if current_price <= entry_price - distance_to_target:
                return entry_price

        return stop_loss_price

    def _weighted_typical_price(self, ohlcv: OHLCV) -> float:
        return (ohlcv.high + ohlcv.low + (ohlcv.close * 2.0)) / 4.0
