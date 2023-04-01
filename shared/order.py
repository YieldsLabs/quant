class Order:
    def __init__(self, timestamp, side, entry_price, exit_price, stop_loss, take_profit, profit):
        self.id = None
        self.timestamp = timestamp
        self.side = side
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.profit = profit

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'side': self.side,
            'entry': self.entry_price,
            'exit': self.exit_price,
            'profit': self.profit,
            'stop loss': self.stop_loss,
            'take profit': self.take_profit,
        }
