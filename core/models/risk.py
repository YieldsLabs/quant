from dataclasses import dataclass, field, replace
from typing import List

import numpy as np

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide


@dataclass(frozen=True)
class Risk:
    ohlcv: List[OHLCV] = field(default_factory=list)
    type: RiskType = RiskType.NONE
    trail_factor: float = field(default_factory=lambda: np.random.uniform(1.2, 1.8))

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
        tp: float,
        sl: float,
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

        return replace(self, type=RiskType.NONE)

    def trail(self, side: PositionSide) -> "float":
        last_bar = self.last_bar
        atr = self._ema(self._true_ranges(self.ohlcv), 8)
        atr_mul = self.trail_factor * atr[-1]

        if side == PositionSide.LONG:
            return last_bar.low - atr_mul

        if side == PositionSide.SHORT:
            return last_bar.high + atr_mul

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

    @staticmethod
    def _true_ranges(ohlcvs: List[OHLCV]) -> List[float]:
        highs, lows, closes = (
            np.array([ohlcv.high for ohlcv in ohlcvs]),
            np.array([ohlcv.low for ohlcv in ohlcvs]),
            np.array([ohlcv.close for ohlcv in ohlcvs]),
        )

        prev_closes = np.roll(closes, 1)

        true_ranges = np.maximum(
            highs - lows, np.abs(highs - prev_closes), np.abs(lows - prev_closes)
        )

        return true_ranges

    @staticmethod
    def _ema(values: List[float], period: int) -> List[float]:
        ema = [np.mean(values[:period])]

        alpha = 2 / (period + 1)

        for i in range(period, len(values)):
            ema.append((values[i] - ema[-1]) * alpha + ema[-1])

        return np.array(ema)

    def to_dict(self):
        return {
            "type": self.type,
            "ohlcv": self.last_bar.to_dict(),
        }

    def __str__(self):
        return f"Risk(type={self.type}, ohlcv={self.last_bar})"
