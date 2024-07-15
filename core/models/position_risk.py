from dataclasses import dataclass, field, replace
from typing import List, Tuple

import numpy as np
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

from .ohlcv import OHLCV
from .risk_type import PositionRiskType
from .side import PositionSide
from .ta import TechAnalysis

TIME_THRESHOLD = 35000
LOOKBACK = 12


def optimize_params(
    data: np.ndarray, n_clusters_range: Tuple[int, int] = (2, 10)
) -> int:
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    X = scaler.fit_transform(data)

    best_score = float("-inf")
    best_centroids = []

    for n_clusters in range(*n_clusters_range):
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=None)
        kmeans.fit(X)

        if len(np.unique(kmeans.labels_)) < n_clusters:
            continue

        silhouette_avg = silhouette_score(X, kmeans.labels_)

        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_centroids = scaler.inverse_transform(kmeans.cluster_centers_).flatten()

    return int(round(np.mean(best_centroids))) if len(best_centroids) > 1 else 2


def optimize_window_polyorder(data: np.ndarray) -> Tuple[int, int]:
    window_length = optimize_params(data)

    if window_length % 2 == 0:
        window_length += 1

    window_length = min(window_length, len(data))

    polyorder_range = (2, window_length - 1 if window_length > 2 else 2)
    polyorder = optimize_params(data, n_clusters_range=polyorder_range)

    polyorder = min(polyorder, window_length - 1)

    return window_length, polyorder


def smooth(*arrays: np.ndarray) -> List[np.ndarray]:
    all_data = np.concatenate(arrays)
    window_length, polyorder = optimize_window_polyorder(all_data)
    return [
        savgol_filter(
            array,
            min(window_length, len(array)),
            min(polyorder, min(window_length, len(array)) - 1),
        )
        for array in arrays
    ]


class TaMixin:
    @staticmethod
    def _ats(closes: List[float], atr: List[float]) -> List[float]:
        stop_prices = np.zeros_like(closes)
        period = min(len(closes), len(atr))

        stop_prices[0] = closes[0] - atr[0]

        for i in range(1, period):
            stop = atr[i]

            long_stop = closes[i] - stop
            short_stop = closes[i] + stop

            prev_stop = stop_prices[i - 1]
            prev_close = closes[i - 1]

            if closes[i] > prev_stop and prev_close > prev_stop:
                stop_prices[i] = max(prev_stop, long_stop)
            elif closes[i] < prev_stop and prev_close < prev_stop:
                stop_prices[i] = min(prev_stop, short_stop)
            elif closes[i] > prev_stop:
                stop_prices[i] = long_stop
            else:
                stop_prices[i] = short_stop

        return stop_prices


@dataclass(frozen=True)
class PositionRisk(TaMixin):
    ohlcv: List[OHLCV] = field(default_factory=list)
    type: PositionRiskType = PositionRiskType.NONE
    trail_factor: float = field(default_factory=lambda: np.random.uniform(1.682, 2.382))

    @property
    def curr_bar(self):
        return self.ohlcv[-1]

    def next(self, bar: OHLCV):
        ohlcv = self.ohlcv + [bar]
        ohlcv.sort(key=lambda x: x.timestamp)
        return replace(self, ohlcv=ohlcv)

    def reset(self):
        return replace(self, type=PositionRiskType.NONE)

    def assess(
        self,
        side: PositionSide,
        tp: float,
        sl: float,
        open_timestamp: float,
        expiration: float,
    ) -> "PositionRisk":
        expiration = self.curr_bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            return replace(self, type=PositionRiskType.TIME)

        high, low = self.curr_bar.high, self.curr_bar.low

        if side == PositionSide.LONG:
            tp, sl = max(tp, sl), min(tp, sl)

            if high > tp:
                return replace(self, type=PositionRiskType.TP)
            if low < sl:
                return replace(self, type=PositionRiskType.SL)

        if side == PositionSide.SHORT:
            tp, sl = min(tp, sl), max(tp, sl)

            if low < tp:
                return replace(self, type=PositionRiskType.TP)
            if high > sl:
                return replace(self, type=PositionRiskType.SL)

        return replace(self, type=PositionRiskType.NONE)

    def exit_price(self, side: PositionSide, tp: float, sl: float) -> "float":
        high, low, close = self.curr_bar.high, self.curr_bar.low, self.curr_bar.close

        if self.type == PositionRiskType.TP:
            return min(tp, high) if side == PositionSide.LONG else max(tp, low)

        elif self.type == PositionRiskType.SL:
            return (
                max(min(sl, high), low)
                if side == PositionSide.LONG
                else min(max(sl, low), high)
            )

        return close

    def sl_low(self, side: PositionSide, ta: TechAnalysis, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        max_lookback = max(len(timestamps), LOOKBACK)

        trend = ta.trend

        ll = np.array(trend.ll)[-max_lookback:]
        hh = np.array(trend.hh)[-max_lookback:]
        volatility = np.array(ta.volatility.yz)[-max_lookback:]
        res = np.array(trend.resistance)[-max_lookback:]
        sup = np.array(trend.support)[-max_lookback:]

        min_length = min(len(ll), len(hh), len(volatility), len(timestamps))

        if min_length < 1:
            return sl

        ll_smooth, hh_smooth, volatility_smooth = smooth(ll, hh, volatility)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if side == PositionSide.LONG:
            return max(sl, np.max(sup), np.max(ll_atr))

        if side == PositionSide.SHORT:
            return min(sl, np.min(res), np.min(hh_atr))

        return sl

    def tp_low(self, side: PositionSide, ta: TechAnalysis, tp: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return tp

        max_lookback = max(len(timestamps), LOOKBACK)

        trend = ta.trend

        ll = np.array(trend.ll)[-max_lookback:]
        hh = np.array(trend.hh)[-max_lookback:]
        volatility = np.array(ta.volatility.yz)[-max_lookback:]
        res = np.array(trend.resistance)[-max_lookback:]
        sup = np.array(trend.support)[-max_lookback:]

        min_length = min(len(ll), len(hh), len(volatility), len(timestamps))

        if min_length < 1:
            return tp

        ll_smooth, hh_smooth, volatility_smooth = smooth(ll, hh, volatility)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if side == PositionSide.LONG:
            return min(np.min(res), np.min(hh_atr))
        elif side == PositionSide.SHORT:
            return max(np.max(sup), np.max(ll_atr))

        return tp

    def sl_ats(
        self, side: PositionSide, curr_price: float, ta: TechAnalysis, sl: float
    ) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        max_lookback = max(len(timestamps), LOOKBACK)

        close = np.array([candle.close for candle in self.ohlcv])
        volatility = np.array(ta.volatility.yz)[-max_lookback:]

        min_length = min(len(close), len(volatility))

        if min_length < 3:
            return sl

        close_smooth, volatility_smooth = smooth(close, volatility)

        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]
        close_smooth = close_smooth[-min_length:]

        ats = self._ats(close_smooth, volatility_smooth)

        low = np.array([candle.low for candle in self.ohlcv])
        high = np.array([candle.high for candle in self.ohlcv])

        rising_low = low[-1] > low[-2] and low[-2] > low[-3]
        failing_high = high[-1] < high[-2] and high[-2] < high[-3]

        bullish = rising_low and (ta.trend.dmi[-1] > 0.0 or ta.momentum.cci[-1] > 100.0)
        bearish = failing_high and (
            ta.trend.dmi[-1] <= 0.0 or ta.momentum.cci[-1] < -100.0
        )

        if side == PositionSide.LONG:
            if bullish:
                print("BULLLLLISHHHHHH-------------------------->")
                return min(curr_price, max(sl, np.max(ats)))

            return min(curr_price, max(sl, ats[-1]))

        if side == PositionSide.SHORT:
            if bearish:
                print("BEARISHHHHHHHHH-------------------------->")
                return max(curr_price, min(sl, np.min(ats)))

            return max(curr_price, min(sl, ats[-1]))

        return sl

    def to_dict(self):
        return {
            "type": self.type,
            "trail_factor": self.trail_factor,
            "ohlcv": self.curr_bar.to_dict(),
        }

    def __str__(self):
        return f"type={self.type}, ohlcv={self.curr_bar}"

    def __repr__(self):
        return f"PositionRisk({self})"
