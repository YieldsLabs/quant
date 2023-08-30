from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide


class BreakEvenStrategy(AbstractPositionRiskStrategy):
    def __init__(self, risk_per_trade: float):
        super().__init__()
        self.risk_per_trade = risk_per_trade

    def next(self, side: PositionSide, entry_price: float, stop_loss_price: float, ohlcv: OHLCV) -> float:
        new_stop_loss_price = ohlcv.high - (ohlcv.high - stop_loss_price) * self.risk_per_trade if side == PositionSide.LONG else ohlcv.low + (stop_loss_price - ohlcv.low) * self.risk_per_trade

        if (side == PositionSide.LONG and new_stop_loss_price > entry_price) or (side == PositionSide.SHORT and new_stop_loss_price < entry_price):
            return new_stop_loss_price

        return stop_loss_price