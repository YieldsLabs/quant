from typing import Optional

from core.interfaces.abstract_position_size_strategy import AbstractPositionSizeStrategy
from core.models.signal import Signal
from core.queries.portfolio import GetEquity


class PositionFixedSizeStrategy(AbstractPositionSizeStrategy):
    def __init__(self, risk_per_trade: float):
        super().__init__()
        self.risk_per_trade = risk_per_trade

    async def calculate(
        self,
        signal: Signal,
        entry_price: float,
        stop_loss_price: Optional[float] = None,
    ) -> float:
        risk_amount = self.risk_per_trade * await self.query(GetEquity(signal))

        if stop_loss_price is not None and entry_price is not None:
            price_difference = abs(entry_price - stop_loss_price)
        else:
            raise ValueError("Both entry_price and stop_loss_price must be provided.")

        if price_difference == 0:
            raise ValueError(
                f"Price difference cannot be zero. For entry price {entry_price} and for stop loss {stop_loss_price}"
            )

        position_size = risk_amount / price_difference

        return position_size
