from dataclasses import dataclass, field, replace
from typing import List

import numpy as np

from .ohlcv import OHLCV
from .risk_type import RiskType
from .side import PositionSide

TIME_THRESHOLD = 25000


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

        return self

    def sl_low(self, side: PositionSide, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        period = 3
        atr_period = 2

        if len(self.ohlcv) < period:
            return sl

        lows = np.array([candle.low for candle in self.ohlcv])
        highs = np.array([candle.high for candle in self.ohlcv])
        closes = np.array([candle.close for candle in self.ohlcv])

        ll = self._min(lows, period)
        hh = self._max(highs, period)

        ll_ema = self._ema(ll, period)
        hh_ema = self._ema(hh, period)

        atr = self.trail_factor * self._ema(
            self._true_ranges(highs, lows, closes), atr_period
        )

        min_length = min(len(ll_ema), len(hh_ema), len(atr))

        ll_ema = ll_ema[-min_length:]
        hh_ema = hh_ema[-min_length:]
        atr = atr[-min_length:]

        ll_atr = ll_ema - atr
        hh_atr = hh_ema + atr

        if side == PositionSide.LONG:
            return max(sl, np.max(ll_atr))

        if side == PositionSide.SHORT:
            return min(sl, np.min(hh_atr))

    def tp_low(self, side: PositionSide, tp: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return tp

        period = 3
        atr_period = 2

        if len(self.ohlcv) < period:
            return tp

        lows = np.array([candle.low for candle in self.ohlcv])
        highs = np.array([candle.high for candle in self.ohlcv])
        closes = np.array([candle.close for candle in self.ohlcv])

        ll = self._min(lows, period)
        hh = self._max(highs, period)

        ll_ema = self._ema(ll, period)
        hh_ema = self._ema(hh, period)

        atr = self.trail_factor * self._ema(
            self._true_ranges(highs, lows, closes), atr_period
        )

        min_length = min(len(ll_ema), len(hh_ema), len(atr))

        ll_ema = ll_ema[-min_length:]
        hh_ema = hh_ema[-min_length:]
        atr = atr[-min_length:]

        ll_atr = ll_ema - atr
        hh_atr = hh_ema + atr

        if side == PositionSide.LONG:
            return min(tp, np.min(hh_atr))

        if side == PositionSide.SHORT:
            return max(tp, np.max(ll_atr))

    def sl_ats(self, side: PositionSide, sl: float) -> "float":
        period = 5

        if len(self.ohlcv) < period:
            return sl

        lows = np.array([candle.low for candle in self.ohlcv])
        highs = np.array([candle.high for candle in self.ohlcv])
        closes = np.array([candle.close for candle in self.ohlcv])

        atr = self._ema(self._true_ranges(highs, lows, closes), period)
        ats = self._ats(closes, atr, self.trail_factor)

        if side == PositionSide.LONG:
            return max(sl, ats[-1])
        if side == PositionSide.SHORT:
            return min(sl, ats[-1])

    def exit_price(self, side: PositionSide, tp: float, sl: float) -> "float":
        last_bar = self.last_bar

        if self.type == RiskType.TP:
            if side == PositionSide.LONG:
                return min(tp, last_bar.high)
            elif side == PositionSide.SHORT:
                return max(tp, last_bar.low)

        elif self.type == RiskType.SL:
            if side == PositionSide.LONG:
                return max(sl, last_bar.low)
            elif side == PositionSide.SHORT:
                return min(sl, last_bar.high)

        return last_bar.close

    @staticmethod
    def _ats(closes: List[float], atr: List[float], factor: float) -> "float":
        stop_prices = np.zeros_like(closes)
        period = min(len(closes), len(atr))

        for i in range(1, period):
            stop = factor * atr[i]
            cond_one = closes[i] > closes[i - 1] and closes[i - 1] > stop_prices[i - 1]
            cond_two = closes[i] < closes[i - 1] and closes[i - 1] < stop_prices[i - 1]
            cond_three = (
                closes[i] > closes[i - 1] and closes[i - 1] < stop_prices[i - 1]
            )
            cond_four = closes[i] < closes[i - 1] and closes[i - 1] > stop_prices[i - 1]

            if cond_one:
                stop_prices[i] = max(stop_prices[i - 1], closes[i] - stop)
            elif cond_two:
                stop_prices[i] = min(stop_prices[i - 1], closes[i] + stop)
            elif cond_three:
                stop_prices[i] = closes[i] - stop
            elif cond_four:
                stop_prices[i] = closes[i] + stop

        return stop_prices

    @staticmethod
    def _true_ranges(
        highs: List[float], lows: List[float], closes: List[float]
    ) -> List[float]:
        prev_close = np.roll(closes, shift=1)
        prev_close[0] = closes[0]

        tr1 = highs - lows
        tr2 = np.abs(highs - prev_close)
        tr3 = np.abs(lows - prev_close)

        return np.maximum(tr1, np.maximum(tr2, tr3))

    @staticmethod
    def _ema(data: List[float], period: int) -> List[float]:
        ema = np.zeros_like(data)
        alpha = 2 / (period + 1)
        ema[0] = data[0]

        for i in range(1, len(data)):
            ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]

        return ema

    @staticmethod
    def _min(data: List[float], period: int) -> List[float]:
        return np.array(
            [np.min(data[i : i + period]) for i in range(len(data) - period + 1)]
        )

    @staticmethod
    def _max(data: List[float], period: int) -> List[float]:
        return np.array(
            [np.max(data[i : i + period]) for i in range(len(data) - period + 1)]
        )

    def to_dict(self):
        return {
            "type": self.type,
            "ohlcv": self.last_bar.to_dict(),
        }

    def __str__(self):
        return f"Risk(type={self.type}, ohlcv={self.last_bar})"
