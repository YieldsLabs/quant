from dataclasses import dataclass, replace

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide


@dataclass(frozen=True)
class Risk:
    ohlcv: OHLCV
    type: RiskType = RiskType.NONE

    def assess(
        self,
        side: PositionSide,
        sl: float,
        tp: float,
        open_timestamp: float,
        expiration: float,
        bar: OHLCV,
    ) -> "Risk":
        if side == PositionSide.LONG:
            if bar.high > tp:
                return replace(self, type=RiskType.TP, ohlcv=bar)
            if bar.low < sl:
                return replace(self, type=RiskType.SL, ohlcv=bar)

        if side == PositionSide.SHORT:
            if bar.low < tp:
                return replace(self, type=RiskType.TP, ohlcv=bar)
            if bar.high > sl:
                return replace(self, type=RiskType.SL, ohlcv=bar)

        expiration = bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            if side == PositionSide.LONG:
                return replace(self, type=RiskType.TIME, ohlcv=bar)
            if side == PositionSide.SHORT:
                return replace(self, type=RiskType.TIME, ohlcv=bar)

        return replace(self, ohlcv=bar)

    def trail(self) -> "Risk":
        return self

    def exit_price(self, side: PositionSide, sl: float, tp: float) -> "float":
        if side == PositionSide.LONG:
            if self.ohlcv.low <= sl:
                return self.ohlcv.low

            if self.ohlcv.high >= tp:
                return self.ohlcv.high

        if side == PositionSide.SHORT:
            if self.ohlcv.high >= sl:
                return self.ohlcv.high

            if self.ohlcv.low <= tp:
                return self.ohlcv.low

        return self.ohlcv.close

    def to_dict(self):
        return {
            "type": self.type,
            "ohlcv": self.ohlcv.to_dict(),
        }
