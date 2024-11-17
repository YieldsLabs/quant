from dataclasses import field, replace
from typing import List, Tuple

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import MinMaxScaler

from core.models.risk_type import PositionRiskType
from core.models.side import PositionSide
from core.models.ta import TechAnalysis

from ._base import Entity
from .ohlcv import OHLCV

TIME_THRESHOLD = 10000
LOOKBACK = 6


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

        sscore = silhouette_score(X, kmeans.labels_)
        cscore = calinski_harabasz_score(X, kmeans.labels_)
        db_score = davies_bouldin_score(X, kmeans.labels_)

        score = (sscore + cscore - db_score) / 3

        if score > best_score:
            best_score = score
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


def smooth_savgol(*arrays: np.ndarray) -> List[np.ndarray]:
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


def smooth_spline(*arrays: np.ndarray, s: float = 1.0, k: int = 3) -> List[np.ndarray]:
    return [
        (
            UnivariateSpline(
                np.arange(len(array)), array, s=s, k=min(k, len(array) - 1)
            )(np.arange(len(array)))
            if len(array) > k
            else array
        )
        for array in arrays
    ]


class TaMixin:
    @staticmethod
    def _ats(closes: List[float], atr: List[float]) -> List[float]:
        period = min(len(closes), len(atr))
        stop_prices = np.zeros(period)

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


@Entity
class Risk(TaMixin):
    ohlcv: List = field(default_factory=lambda: [])
    side: PositionSide = None
    tp: float = field(default_factory=lambda: 0.0)
    sl: float = field(default_factory=lambda: 0.0)
    duration: int = field(default_factory=lambda: 900)
    trail_factor: float = field(default_factory=lambda: np.random.uniform(1.1, 1.8))

    @property
    def curr_bar(self):
        return self.ohlcv[-1]

    @property
    def time_points(self):
        return [o.timestamp for o in self.ohlcv]

    @property
    def has_risk(self) -> bool:
        high, low = self.curr_bar.high, self.curr_bar.low
        risk_type = PositionRiskType.NONE
        expired = (
            self.curr_bar.timestamp - self.ohlcv[0].timestamp
        ) // 1e3 - self.duration

        if expired >= 0:
            risk_type = PositionRiskType.TIME

        if self.side == PositionSide.LONG:
            if low < self.sl:
                risk_type = PositionRiskType.SL
            if high > self.tp:
                risk_type = PositionRiskType.TP

        if self.side == PositionSide.SHORT:
            if high > self.sl:
                risk_type = PositionRiskType.SL
            if low < self.tp:
                risk_type = PositionRiskType.TP

        return risk_type != PositionRiskType.NONE

    def next(self, bar: OHLCV) -> "Risk":
        ohlcv = self.ohlcv.copy()
        ohlcv.append(bar)

        return replace(self, ohlcv=ohlcv)

    def sl_low(self, ta: TechAnalysis) -> "float":
        timestamps = np.array(self.time_points)
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return self.sl

        max_lookback = max(len(timestamps), LOOKBACK)

        trend = ta.trend

        ll = np.array(trend.ll)[-max_lookback:]
        hh = np.array(trend.hh)[-max_lookback:]
        volatility = np.array(ta.volatility.yz)[-max_lookback:]
        res = np.array(trend.resistance)[-max_lookback:]
        sup = np.array(trend.support)[-max_lookback:]

        min_length = min(len(ll), len(hh), len(volatility), len(timestamps))

        if min_length < 1:
            return self.sl

        ll_smooth, hh_smooth, volatility_smooth = smooth_savgol(ll, hh, volatility)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if self.side == PositionSide.LONG:
            return max(self.sl, np.max(sup), np.max(ll_atr))

        if self.side == PositionSide.SHORT:
            return min(self.sl, np.min(res), np.min(hh_atr))

        return self.sl

    def tp_low(self, ta: TechAnalysis) -> "float":
        timestamps = np.array(self.time_points)
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return self.tp

        max_lookback = max(len(timestamps), LOOKBACK)

        trend = ta.trend

        ll = np.array(trend.ll)[-max_lookback:]
        hh = np.array(trend.hh)[-max_lookback:]
        volatility = np.array(ta.volatility.yz)[-max_lookback:]
        res = np.array(trend.resistance)[-max_lookback:]
        sup = np.array(trend.support)[-max_lookback:]

        min_length = min(len(ll), len(hh), len(volatility), len(timestamps))

        if min_length < 1:
            return self.tp

        ll_smooth, hh_smooth, volatility_smooth = smooth_savgol(ll, hh, volatility)

        ll_smooth = ll_smooth[-min_length:]
        hh_smooth = hh_smooth[-min_length:]
        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]

        ll_atr = ll_smooth - volatility_smooth
        hh_atr = hh_smooth + volatility_smooth

        if self.side == PositionSide.LONG:
            return min(np.min(res), np.min(hh_atr))
        elif self.side == PositionSide.SHORT:
            return max(np.max(sup), np.max(ll_atr))

        return self.tp

    def sl_ats(self, ta: TechAnalysis) -> "float":
        timestamps = np.array(self.time_points)
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return self.sl

        max_lookback = max(len(timestamps), LOOKBACK)

        close = np.array([candle.close for candle in self._ohlcv])
        low = np.array([candle.low for candle in self._ohlcv])
        high = np.array([candle.high for candle in self._ohlcv])
        volatility = np.array(ta.volatility.gkyz)[-max_lookback:]

        min_length = min(len(close), len(volatility), len(high), len(low))

        if min_length < 3:
            return self.sl

        def anomaly(series):
            return (series - np.mean(series)) / np.std(series)

        close_anomaly = anomaly(close[-min_length:])

        if abs(close_anomaly[-1]) > 2:
            return self.sl

        close_smooth, volatility_smooth, high_smooth, low_smooth = smooth_savgol(
            close, volatility, high, low
        )

        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]
        close_smooth = close_smooth[-min_length:]

        ats = self._ats(close_smooth, volatility_smooth)

        rising_low = low[-1] > low[-2] and low[-2] > low[-3]
        failing_high = high[-1] < high[-2] and high[-2] < high[-3]

        bullish = rising_low and (ta.trend.dmi[-1] > 0.0 or ta.momentum.cci[-1] > 100.0)
        bearish = failing_high and (
            ta.trend.dmi[-1] <= 0.0 or ta.momentum.cci[-1] < -100.0
        )

        if self.side == PositionSide.LONG:
            l_constr = min(low[-1], low[-2])
            adjusted_sl = (
                min(l_constr, np.max(ats)) if bullish else min(l_constr, ats[-1])
            )
            atr_stop = l_constr - volatility_smooth[-1]

            return max(self.sl, max(atr_stop, adjusted_sl))

        if self.side == PositionSide.SHORT:
            h_constr = max(high[-1], high[-2])
            adjusted_sl = (
                max(h_constr, np.min(ats)) if bearish else max(h_constr, ats[-1])
            )
            atr_stop = h_constr + volatility_smooth[-1]

            return min(self.sl, min(atr_stop, adjusted_sl))

        return self.sl
