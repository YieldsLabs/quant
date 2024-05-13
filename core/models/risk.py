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
    trail_factor: float = field(default_factory=lambda: np.random.uniform(1.5, 3.5))

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
        curr_bar = self.last_bar

        expiration = curr_bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            if side == PositionSide.LONG:
                return replace(self, type=RiskType.TIME)
            if side == PositionSide.SHORT:
                return replace(self, type=RiskType.TIME)

        if side == PositionSide.LONG:
            if curr_bar.high >= tp:
                return replace(self, type=RiskType.TP)
            if curr_bar.low <= sl:
                return replace(self, type=RiskType.SL)

        if side == PositionSide.SHORT:
            if curr_bar.low <= tp:
                return replace(self, type=RiskType.TP)
            if curr_bar.high >= sl:
                return replace(self, type=RiskType.SL)

        return self.reset()

    def sl_low(self, side: PositionSide, sl: float) -> "float":
        period = 2

        low = self._ll(self.ohlcv, period)
        atr = self._ema(self._true_ranges(self.ohlcv), period)

        if len(low) < period:
            return sl

        if side == PositionSide.LONG:
            return max(sl, max(low - atr[-1]))
        if side == PositionSide.SHORT:
            return min(sl, min(low - atr[-1]))

    def sl_ats(self, side: PositionSide, sl: float) -> "float":
        period = 5

        atr = self._ema(self._true_ranges(self.ohlcv), period)
        ats = self._ats(self.ohlcv, atr, self.trail_factor)

        if ats[-1] == 0:
            return sl

        if side == PositionSide.LONG:
            return max(sl, ats[-1])
        if side == PositionSide.SHORT:
            return min(sl, ats[-1])

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

    def reset(self):
        return replace(self, type=RiskType.NONE)

    @staticmethod
    def _ats(ohlcvs: List[OHLCV], atr: List[OHLCV], factor: float) -> "float":
        close_prices = np.array([ohlcv.close for ohlcv in ohlcvs])
        stop_prices = np.zeros_like(close_prices)
        period = min(len(close_prices), len(atr))

        for i in range(1, period):
            stop = factor * atr[i]
            cond_one = (
                close_prices[i] > close_prices[i - 1]
                and close_prices[i - 1] > stop_prices[i - 1]
            )
            cond_two = (
                close_prices[i] < close_prices[i - 1]
                and close_prices[i - 1] < stop_prices[i - 1]
            )
            cond_three = (
                close_prices[i] > close_prices[i - 1]
                and close_prices[i - 1] < stop_prices[i - 1]
            )
            cond_four = (
                close_prices[i] < close_prices[i - 1]
                and close_prices[i - 1] > stop_prices[i - 1]
            )

            if cond_one:
                stop_prices[i] = max(stop_prices[i - 1], close_prices[i] - stop)
            elif cond_two:
                stop_prices[i] = min(stop_prices[i - 1], close_prices[i] + stop)
            elif cond_three:
                stop_prices[i] = close_prices[i] - stop
            elif cond_four:
                stop_prices[i] = close_prices[i] + stop

        return stop_prices

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

    @staticmethod
    def _hh(ohlcvs: List[OHLCV], period: int) -> List[float]:
        highs = np.array([ohlcv.high for ohlcv in ohlcvs])
        hh = np.maximum.reduce([np.roll(highs, i) for i in range(period)])
        return hh.tolist()

    @staticmethod
    def _ll(ohlcvs: List[OHLCV], period: int) -> List[float]:
        lows = np.array([ohlcv.low for ohlcv in ohlcvs])
        ll = np.minimum.reduce([np.roll(lows, i) for i in range(period)])
        return ll.tolist()

    def to_dict(self):
        return {
            "type": self.type,
            "ohlcv": self.last_bar.to_dict(),
        }

    def __str__(self):
        return f"Risk(type={self.type}, ohlcv={self.last_bar})"
