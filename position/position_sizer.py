from typing import Optional


class PositionSizer:
    @staticmethod
    def calculate(
        account_size: float,
        entry_price: float,
        trading_fee: float,
        min_position_size: float,
        position_precision: int,
        leverage: int = 1,
        stop_loss_price: Optional[float] = None,
        risk_per_trade: float = 0.001
    ) -> float:
        account_size *= leverage
        risk_amount = risk_per_trade * account_size

        if stop_loss_price is not None and entry_price is not None:
            price_difference = abs(entry_price - stop_loss_price) * (1 + trading_fee)
        else:
            raise ValueError("Both entry_price and stop_loss_price must be provided.")

        if price_difference == 0:
            raise ValueError("Price difference cannot be zero.")

        position_size = risk_amount / price_difference
        adjusted_position_size = max(position_size, min_position_size)
        rounded_position_size = round(adjusted_position_size, position_precision)

        return rounded_position_size
