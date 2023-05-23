from core.events.position import PositionSide


class BreakEvenStopLossStrategy:
    def __init__(self):
        self.data = {}

    def _init(self, symbol: str):
        self.data[symbol] = {PositionSide.LONG: None, PositionSide.SHORT: None}

    def next(self, symbol: str, position_side: PositionSide, position_size: float, stop_loss_price: float, entry_price: float, low: float, high: float, risk_per_trade: float) -> float:
        if symbol not in self.data:
            self._init(symbol)

        if not self.data[symbol][position_side]:
            self.data[symbol][position_side] = stop_loss_price

        if position_side == PositionSide.LONG:
            new_stop_loss_price = high - (high - stop_loss_price) * risk_per_trade

            if new_stop_loss_price > self.data[symbol][position_side]:
                self.data[symbol][position_side] = new_stop_loss_price
                if self.data[symbol][position_side] - entry_price >= risk_per_trade * position_size:
                    self.data[symbol][position_side] = entry_price

        elif position_side == PositionSide.SHORT:
            new_stop_loss_price = low + (stop_loss_price - low) * risk_per_trade

            if new_stop_loss_price < self.data[symbol][position_side]:
                self.data[symbol][position_side] = new_stop_loss_price
                if entry_price - self.data[symbol][position_side] >= risk_per_trade * position_size:
                    self.data[symbol][position_side] = entry_price

        next_stop_loss_price = self.data[symbol][position_side]

        return next_stop_loss_price

    def reset(self, symbol: str, position_side: PositionSide):
        self.data[symbol][position_side] = None
