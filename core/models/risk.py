from dataclasses import dataclass, field, replace

import numpy as np

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide


@dataclass(frozen=True)
class Risk:
    ohlcv: OHLCV
    type: RiskType = RiskType.NONE
    first_target: float = field(default_factory=lambda: np.random.uniform(0.2, 0.5))
    take_profit_price: float = field(default_factory=lambda: 0.0000001)
    stop_loss_price: float = field(default_factory=lambda: 0.0000001)
    expiration: float = field(default_factory=lambda: 0.0)

    def assess(self, side: PositionSide, open_timestamp: int, bar: OHLCV) -> "Risk":
        if side == PositionSide.LONG:
            if bar.high > self.take_profit_price:
                return replace(self, type=RiskType.TP, ohlcv=bar)
            if bar.low < self.stop_loss_price:
                return replace(self, type=RiskType.SL, ohlcv=bar)

        if side == PositionSide.SHORT:
            if bar.low < self.take_profit_price:
                return replace(self, type=RiskType.TP, ohlcv=bar)
            if bar.high > self.stop_loss_price:
                return replace(self, type=RiskType.SL, ohlcv=bar)

        if bar.timestamp - open_timestamp - self.expiration >= 0:
            if side == PositionSide.LONG:
                return replace(
                    self, type=RiskType.TIME, take_profit_price=bar.high, ohlcv=bar
                )
            if side == PositionSide.SHORT:
                return replace(
                    self, type=RiskType.TIME, take_profit_price=bar.low, ohlcv=bar
                )

        return replace(self, ohlcv=bar)

    def target(self, side: PositionSide, execution_price: float) -> "Risk":
        take_profit_price = execution_price

        if side == PositionSide.LONG:
            take_profit_price = execution_price + self.first_target * (
                execution_price - self.stop_loss_price
            )

        if side == PositionSide.SHORT:
            take_profit_price = execution_price - self.first_target * (
                self.stop_loss_price - execution_price
            )

        return replace(self, take_profit_price=take_profit_price)

    def trail(self, side: PositionSide, execution_price: float) -> "Risk":
        return self

    def exit_price(self, side: PositionSide) -> "float":
        if side == PositionSide.LONG:
            if self.ohlcv.low <= self.stop_loss_price:
                return self.ohlcv.low

            if self.ohlcv.high >= self.take_profit_price:
                return self.ohlcv.high

        if side == PositionSide.SHORT:
            if self.ohlcv.high >= self.stop_loss_price:
                return self.ohlcv.high

            if self.ohlcv.low <= self.take_profit_price:
                return self.ohlcv.low

        return self.ohlcv.close

    def to_dict(self):
        return {
            "type": self.type,
            "stop_loss_price": self.stop_loss_price,
            "take_profit_price": self.take_profit_price,
            "ohlcv": self.ohlcv.to_dict(),
        }
