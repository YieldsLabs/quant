from dataclasses import dataclass, field, replace
from typing import List

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide

FIRST_TARGET = 0.5


@dataclass(frozen=True)
class Risk:
    ohlcv: OHLCV
    type: RiskType = RiskType.NONE
    take_profit_price: float = field(default_factory=lambda: 0.0000001)
    stop_loss_price: float = field(default_factory=lambda: 0.0000001)
    expiration: float = field(default_factory=lambda: 0.0)

    def assess(
        self, side: PositionSide, entry: float, open_ts: float, ohlcv: List[OHLCV]
    ) -> "Risk":
        last_candle = ohlcv[-1]

        if side == PositionSide.LONG:
            if last_candle.high > self.take_profit_price:
                return replace(self, type=RiskType.TP, ohlcv=last_candle)
            if last_candle.low < self.stop_loss_price:
                return replace(self, type=RiskType.SL, ohlcv=last_candle)

        if side == PositionSide.SHORT:
            if last_candle.low < self.take_profit_price:
                return replace(self, type=RiskType.TP, ohlcv=last_candle)
            if last_candle.high > self.stop_loss_price:
                return replace(self, type=RiskType.SL, ohlcv=last_candle)

        if open_ts + self.expiration - last_candle.timestamp <= 0:
            if (side == PositionSide.LONG and last_candle.high > entry) or (
                side == PositionSide.SHORT and last_candle.low < entry
            ):
                return replace(self, type=RiskType.TIME, ohlcv=last_candle)

        return replace(self, ohlcv=last_candle)

    def target(self, side: PositionSide, execution_price: float) -> "Risk":
        take_profit_price = execution_price

        if side == PositionSide.LONG:
            take_profit_price = execution_price + FIRST_TARGET * (
                execution_price - self.stop_loss_price
            )

        if side == PositionSide.SHORT:
            take_profit_price = execution_price - FIRST_TARGET * (
                self.stop_loss_price - execution_price
            )

        return replace(self, take_profit_price=take_profit_price)

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
