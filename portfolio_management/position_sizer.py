from typing import Optional


class PositionSizer:
    @staticmethod
    def calculate_position_size(
        account_size: float,
        entry_price: float,
        trading_fee: float,
        min_position_size: float,
        price_precision: int,
        stop_loss_price: Optional[float] = None,
        risk_per_trade: float = 0.001
    ) -> float:
        risk_amount = risk_per_trade * account_size

        if stop_loss_price and entry_price:
            price_difference = abs(entry_price - stop_loss_price) * (1 + trading_fee)
        else:
            price_difference = 1

        if price_difference != 0:
            position_size = risk_amount / price_difference
        else:
            position_size = 1

        adjusted_position_size = max(position_size, min_position_size)
        
        rounded_position_size = round(adjusted_position_size, price_precision)

        return rounded_position_size