from dataclasses import asdict, dataclass

from shared.order_side import OrderSide


@dataclass
class Order:
    timestamp: int
    side: OrderSide
    entry_price: float
    exit_price: float
    stop_loss: float
    take_profit: float
    pnl: float
    id: str = None

    def to_dict(self):
        return asdict(self)
