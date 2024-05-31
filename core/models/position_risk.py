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

TIME_THRESHOLD = 25000


def optimize_params(data: np.ndarray, n_clusters_range: tuple = (2, 10)) -> int:
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data.reshape(-1, 1))

    best_score = float("-inf")
    best_centroids = []

    for n_clusters in range(*n_clusters_range):
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=None)
        kmeans.fit(data_scaled)

        if len(np.unique(kmeans.labels_)) < n_clusters:
            continue

        silhouette_avg = silhouette_score(data_scaled, kmeans.labels_)

        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_centroids = scaler.inverse_transform(kmeans.cluster_centers_).flatten()

    return int(round(np.mean(best_centroids))) if len(best_centroids) else 2


def optimize_window_polyorder(
    ll_data: np.ndarray, hh_data: np.ndarray, atr_data: np.ndarray
) -> tuple:
    all_data = np.concatenate([ll_data, hh_data, atr_data])

    window_length = optimize_params(all_data)
    polyorder_range = (2, window_length - 1 if window_length > 2 else 2)
    polyorder = optimize_params(all_data, n_clusters_range=polyorder_range)

    window_length += 1 if window_length % 2 == 0 else 0
    polyorder = min(polyorder, window_length - 1)

    return window_length, polyorder


class TaMixin:
    @staticmethod
    def _ats(closes: List[float], atr: List[float]) -> List[float]:
        stop_prices = np.zeros_like(closes)
        period = min(len(closes), len(atr))

        for i in range(1, period):
            stop = atr[i]
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
    def _ema(data: List[float], period: int) -> List[float]:
        ema = np.zeros_like(data)
        alpha = 2 / (period + 1)
        ema[0] = data[0]

        for i in range(1, len(data)):
            ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]

        return ema


@dataclass(frozen=True)
class PositionRisk(TaMixin):
    ohlcv: List[OHLCV] = field(default_factory=list)
    type: PositionRiskType = PositionRiskType.NONE
    trail_factor: float = field(default_factory=lambda: np.random.uniform(3.2, 5.8))

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
                return replace(self, type=PositionRiskType.TIME)
            if side == PositionSide.SHORT:
                return replace(self, type=PositionRiskType.TIME)

        if side == PositionSide.LONG:
            if curr_bar.high >= tp:
                return replace(self, type=PositionRiskType.TP)
            if curr_bar.low <= sl:
                return replace(self, type=PositionRiskType.SL)

        if side == PositionSide.SHORT:
            if curr_bar.low <= tp:
                return replace(self, type=PositionRiskType.TP)
            if curr_bar.high >= sl:
                return replace(self, type=PositionRiskType.SL)

        return replace(self, type=PositionRiskType.NONE)

    def exit_price(self, side: PositionSide, tp: float, sl: float) -> "float":
        last_bar = self.last_bar

        if self.type == PositionRiskType.TP:
            if side == PositionSide.LONG:
                return min(tp, last_bar.high)
            elif side == PositionSide.SHORT:
                return max(tp, last_bar.low)

        elif self.type == PositionRiskType.SL:
            if side == PositionSide.LONG:
                return max(sl, last_bar.low)
            elif side == PositionSide.SHORT:
                return min(sl, last_bar.high)

        return last_bar.close

    def sl_low(self, side: PositionSide, ta: TechAnalysis, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        ll = np.array(ta.trend.ll)
        hh = np.array(ta.trend.hh)
        tr = np.array(ta.volatility.tr)

        min_length = min(len(ll), len(hh), len(tr))

        if min_length < 3:
            return sl

        window_length, polyorder = optimize_window_polyorder(ll, hh, tr)

        ll_smooth = savgol_filter(ll, window_length, polyorder)
        hh_smooth = savgol_filter(hh, window_length, polyorder)
        atr_smooth = savgol_filter(tr, window_length, polyorder)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        atr_smooth = self.trail_factor * atr_smooth[-min_length:]

        ll_atr = ll_smooth - atr_smooth
        hh_atr = hh_smooth + atr_smooth

        if side == PositionSide.LONG:
            return max(sl, np.max(ll_atr))

        if side == PositionSide.SHORT:
            return min(sl, np.min(hh_atr))

        return sl

    def tp_low(self, side: PositionSide, ta: TechAnalysis, tp: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return tp

        ll = np.array(ta.trend.ll)
        hh = np.array(ta.trend.hh)
        tr = np.array(ta.volatility.tr)

        min_length = min(len(ll), len(hh), len(tr))

        if min_length < 3:
            return tp

        window_length, polyorder = optimize_window_polyorder(ll, hh, tr)

        ll_smooth = savgol_filter(ll, window_length, polyorder)
        hh_smooth = savgol_filter(hh, window_length, polyorder)
        atr_smooth = savgol_filter(tr, window_length, polyorder)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        atr_smooth = self.trail_factor * atr_smooth[-min_length:]

        ll_atr = ll_smooth - atr_smooth
        hh_atr = hh_smooth + atr_smooth

        if side == PositionSide.LONG:
            return min(tp, np.min(hh_atr))

        if side == PositionSide.SHORT:
            return max(tp, np.max(ll_atr))

        return tp

    def sl_ats(self, side: PositionSide, ta: TechAnalysis, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        closes = np.array([candle.close for candle in self.ohlcv])
        atr = self.trail_factor * self._ema(np.array(ta.volatility.tr), 5)

        ats = self._ats(closes, atr)

        if side == PositionSide.LONG:
            return max(sl, np.min(ats))
        if side == PositionSide.SHORT:
            return min(sl, np.max(ats))

        return sl

    def to_dict(self):
        return {
            "type": self.type,
            "trail_factor": self.trail_factor,
            "ohlcv": self.last_bar.to_dict(),
        }

    def __str__(self):
        return f"type={self.type}, ohlcv={self.last_bar}"

    def __repr__(self):
        return f"Risk({self})"
