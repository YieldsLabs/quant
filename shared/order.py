from trader.order_side import OrderSide


class Order:
    def __init__(self, timestamp: int, side: OrderSide, entry_price: float, exit_price: float, stop_loss: float, take_profit: float, pnl: float):
        self.id = None
        self.timestamp = timestamp
        self.side = side
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.pnl = pnl

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
