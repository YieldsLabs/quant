from dataclasses import dataclass, field, replace
from typing import List

import numpy as np
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

from .ohlcv import OHLCV
from .risk_type import PositionRiskType
from .side import PositionSide
from .ta import TechAnalysis

TIME_THRESHOLD = 15000
SL_LOOKBACK = 8
AST_LOOKBACK = 12


def optimize_params(data: np.ndarray, n_clusters_range: tuple = (2, 10)) -> int:
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    scaler = MinMaxScaler()
    X = scaler.fit_transform(data.reshape(-1, 1))

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

    return int(round(np.mean(best_centroids))) if len(best_centroids) else 2


def optimize_window_polyorder(data: np.ndarray) -> tuple:
    window_length = optimize_params(data)

    if window_length % 2 == 0:
        window_length += 1

    window_length = min(window_length, len(data))

    polyorder_range = (2, window_length - 1 if window_length > 2 else 2)
    polyorder = optimize_params(data, n_clusters_range=polyorder_range)

    polyorder = min(polyorder, window_length - 1)

    return window_length, polyorder


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
    trail_factor: float = field(default_factory=lambda: np.random.uniform(2.684, 3.382))

    @property
    def curr_bar(self):
        return self.ohlcv[-1]

    @property
    def prev_bar(self):
        return self.ohlcv[-2]

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
    ) -> "PositionRisk":
        expiration = self.curr_bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            if side == PositionSide.LONG:
                return replace(self, type=PositionRiskType.TIME)
            if side == PositionSide.SHORT:
                return replace(self, type=PositionRiskType.TIME)

        if side == PositionSide.LONG:
            if self.curr_bar.high > tp:
                return replace(self, type=PositionRiskType.TP)
            if self.curr_bar.low < sl:
                return replace(self, type=PositionRiskType.SL)

        if side == PositionSide.SHORT:
            if self.curr_bar.low < tp:
                return replace(self, type=PositionRiskType.TP)
            if self.curr_bar.high > sl:
                return replace(self, type=PositionRiskType.SL)

        return replace(self, type=PositionRiskType.NONE)

    def exit_price(self, side: PositionSide, tp: float, sl: float) -> "float":
        if self.type == PositionRiskType.TP:
            if side == PositionSide.LONG:
                return min(tp, self.curr_bar.high)
            elif side == PositionSide.SHORT:
                return max(tp, self.curr_bar.low)

        elif self.type == PositionRiskType.SL:
            if side == PositionSide.LONG:
                return max(sl, self.curr_bar.low)
            elif side == PositionSide.SHORT:
                return min(sl, self.curr_bar.high)

        return self.curr_bar.close

    def sl_low(
        self, side: PositionSide, ta: TechAnalysis, dist: float, sl: float
    ) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        ll = np.array(ta.trend.ll)[-SL_LOOKBACK:]
        hh = np.array(ta.trend.hh)[-SL_LOOKBACK:]
        volatility = np.array(ta.volatility.yz)[-SL_LOOKBACK:]

        min_length = min(len(ll), len(hh), len(volatility))

        if min_length < 3:
            return sl

        all_data = np.concatenate([ll, hh, volatility])
        window_length, polyorder = optimize_window_polyorder(all_data)

        ll_smooth = savgol_filter(ll, window_length, polyorder)
        hh_smooth = savgol_filter(hh, window_length, polyorder)
        volatility_smooth = savgol_filter(volatility, window_length, polyorder)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if side == PositionSide.LONG:
            return max(sl, np.max(ll_atr) - dist)

        if side == PositionSide.SHORT:
            return min(sl, np.min(hh_atr) + dist)

        return sl

    def tp_low(
        self, side: PositionSide, ta: TechAnalysis, dist: float, tp: float
    ) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return tp

        ll = np.array(ta.trend.ll)[-SL_LOOKBACK:]
        hh = np.array(ta.trend.hh)[-SL_LOOKBACK:]
        volatility = np.array(ta.volatility.yz)[-SL_LOOKBACK:]

        min_length = min(len(ll), len(hh), len(volatility))

        if min_length < 3:
            return tp

        all_data = np.concatenate([ll, hh, volatility])
        window_length, polyorder = optimize_window_polyorder(all_data)

        ll_smooth = savgol_filter(ll, window_length, polyorder)
        hh_smooth = savgol_filter(hh, window_length, polyorder)
        volatility_smooth = savgol_filter(volatility, window_length, polyorder)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if side == PositionSide.LONG:
            return min(tp, np.min(hh_atr) + dist)

        if side == PositionSide.SHORT:
            return max(tp, np.max(ll_atr) - dist)

        return tp

    def sl_ats(self, side: PositionSide, ta: TechAnalysis, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        close = np.array([candle.close for candle in self.ohlcv])[-AST_LOOKBACK:]
        volatility = np.array(ta.volatility.yz)[-AST_LOOKBACK:]

        min_length = min(len(close), len(volatility))

        if min_length < 3:
            return sl

        all_data = np.concatenate([close, volatility])
        window_length, polyorder = optimize_window_polyorder(all_data)

        close_smooth = savgol_filter(close, window_length, polyorder)
        volatility_smooth = savgol_filter(volatility, window_length, polyorder)

        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ats = self._ats(close_smooth, volatility_smooth)

        if side == PositionSide.LONG:
            return ats[-1]
        if side == PositionSide.SHORT:
            return ats[-1]

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
