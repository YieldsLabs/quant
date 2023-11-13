from typing import Optional

from core.interfaces.abstract_position_size_strategy import AbstractPositionSizeStrategy


class PositionFixedSizeStrategy(AbstractPositionSizeStrategy):
    def __init__(self, risk_per_trade: float):
        super().__init__()
        self.risk_per_trade = risk_per_trade

    def calculate(
        self,
        account_size: float,
        entry_price: float,
        stop_loss_price: Optional[float] = None,
    ) -> float:
        risk_amount = self.risk_per_trade * account_size

        if stop_loss_price is not None and entry_price is not None:
            price_difference = abs(entry_price - stop_loss_price)
        else:
            raise ValueError("Both entry_price and stop_loss_price must be provided.")

        if price_difference == 0:
            raise ValueError("Price difference cannot be zero.")

        position_size = risk_amount / price_difference

        return position_size
