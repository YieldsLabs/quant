from dataclasses import dataclass

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
        return {
            'timestamp': self.timestamp,
            'side': self.side,
            'entry': self.entry_price,
            'exit': self.exit_price,
            'pnl': self.pnl,
            'stop loss': self.stop_loss,
            'take profit': self.take_profit,
        }
