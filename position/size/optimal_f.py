from typing import Optional

from core.interfaces.abstract_position_size_strategy import AbstractPositionSizeStrategy
from core.models.signal import Signal
from core.models.size import PositionSizeType
from core.queries.portfolio import GetPositionRisk


class PositionOptimalFSizeStrategy(AbstractPositionSizeStrategy):
    def __init__(self):
        super().__init__()

    async def calculate(
        self,
        signal: Signal,
        entry_price: float,
        stop_loss_price: Optional[float] = None,
    ) -> float:
        risk_amount = await self.query(
            GetPositionRisk(signal, PositionSizeType.Optimalf)
        )

        fixed_risk_amount = await self.query(
            GetPositionRisk(signal, PositionSizeType.Fixed)
        )

        if risk_amount >= 3 * fixed_risk_amount:
            risk_amount = risk_amount * 0.033

        if stop_loss_price is not None and entry_price is not None:
            price_difference = abs(entry_price - stop_loss_price)
        else:
            raise ValueError("Both entry_price and stop_loss_price must be provided.")

        if price_difference == 0:
            raise ValueError(
                f"Price difference cannot be zero. For entry price {entry_price} and for stoploss {stop_loss_price}"
            )

        position_size = risk_amount / price_difference

        return position_size
