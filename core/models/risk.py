from dataclasses import dataclass, field, replace
from typing import List

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide


@dataclass(frozen=True)
class Risk:
    ohlcv: List[OHLCV] = field(default_factory=list)
    type: RiskType = RiskType.NONE

    @property
    def last_bar(self):
        return self.ohlcv[-1]

    def next(self, bar: OHLCV):
        self.ohlcv.append(bar)
        ohlcv = sorted(self.ohlcv, key=lambda x: x.timestamp)

        return replace(self, ohlcv=ohlcv)

    def assess(
        self,
        side: PositionSide,
        sl: float,
        tp: float,
        open_timestamp: float,
        expiration: float,
    ) -> "Risk":
        bar = self.last_bar

        if side == PositionSide.LONG:
            if bar.high > tp:
                return replace(self, type=RiskType.TP)
            if bar.low < sl:
                return replace(self, type=RiskType.SL)

        if side == PositionSide.SHORT:
            if bar.low < tp:
                return replace(self, type=RiskType.TP)
            if bar.high > sl:
                return replace(self, type=RiskType.SL)

        expiration = bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            if side == PositionSide.LONG:
                return replace(self, type=RiskType.TIME)
            if side == PositionSide.SHORT:
                return replace(self, type=RiskType.TIME)

        return self

    def trail(self, side: PositionSide) -> "float":
        last_bar = self.last_bar

        if side == PositionSide.LONG:
            return last_bar.low

        if side == PositionSide.SHORT:
            return last_bar.high

    def exit_price(self, side: PositionSide, sl: float, tp: float) -> "float":
        last_bar = self.last_bar

        if side == PositionSide.LONG:
            if last_bar.low <= sl:
                return last_bar.low

            if last_bar.high >= tp:
                return last_bar.high

        if side == PositionSide.SHORT:
            if last_bar.high >= sl:
                return last_bar.high

            if last_bar.low <= tp:
                return last_bar.low

        return last_bar.close

    def to_dict(self):
        return {
            "type": self.type,
            "ohlcv": self.last_bar.to_dict(),
        }
