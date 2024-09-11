from dataclasses import dataclass, field, replace
from typing import List, Tuple

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from .ohlcv import OHLCV
from .risk_type import PositionRiskType
from .side import PositionSide
from .ta import TechAnalysis

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
        UnivariateSpline(np.arange(len(array)), array, s=s, k=min(k, len(array) - 1))(
            np.arange(len(array))
        )
        if len(array) > k
        else array
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


@dataclass(frozen=True)
class PositionRisk(TaMixin):
    model: SGDRegressor
    scaler: StandardScaler
    ohlcv: List[OHLCV] = field(default_factory=list)
    type: PositionRiskType = PositionRiskType.NONE
    trail_factor: float = field(default_factory=lambda: np.random.uniform(1.8, 2.2))

    @property
    def curr_bar(self):
        return self.ohlcv[-1]

    def update_model(self):
        if len(self.ohlcv) < 3:
            return

        last_ohlcv = self.ohlcv[-3:]

        close = [ohlcv.close for ohlcv in last_ohlcv]
        high = [ohlcv.high for ohlcv in last_ohlcv]
        low = [ohlcv.low for ohlcv in last_ohlcv]

        hlcc4 = [(high[i] + low[i] + 2 * close[i]) / 4.0 for i in range(3)]
        hlcc4_lagged_1 = [hlcc4[0]] + hlcc4[:-1]
        hlcc4_lagged_2 = [hlcc4[0], hlcc4[1]] + hlcc4[:-2]

        true_range = [
            max(
                high[i] - low[i],
                abs(high[i] - close[i - 1]),
                abs(low[i] - close[i - 1]),
            )
            for i in range(1, 3)
        ]
        true_range.insert(0, true_range[0])

        true_range_lagged_1 = [true_range[0]] + true_range[:-1]
        true_range_lagged_2 = [true_range[0], true_range[1]] + true_range[:-2]

        hlcc4_diff = hlcc4[-1] - hlcc4_lagged_1[-1]
        true_range_diff = true_range[-1] - true_range_lagged_1[-1]

        features = np.array(
            [
                [
                    hlcc4[-1],
                    hlcc4_lagged_1[-1],
                    hlcc4_lagged_2[-1],
                    true_range[-1],
                    true_range_lagged_1[-1],
                    true_range_lagged_2[-1],
                    hlcc4_diff,
                    true_range_diff,
                ]
            ]
        )
        target = np.array([close[-1]])

        features_scaled = self.scaler.transform(features)

        self.model.partial_fit(features_scaled, target)

    def forecast(self, steps: int = 3):
        if len(self.ohlcv) < 1:
            return []

        self.update_model()

        last_ohlcv = self.ohlcv[-1]

        last_hlcc4 = (last_ohlcv.high + last_ohlcv.low + 2 * last_ohlcv.close) / 4.0
        last_true_range = max(
            last_ohlcv.high - last_ohlcv.low,
            abs(last_ohlcv.high - self.ohlcv[-2].close),
            abs(last_ohlcv.low - self.ohlcv[-2].close),
        )

        last_hlcc4_lagged_1 = last_hlcc4
        last_hlcc4_lagged_2 = last_hlcc4
        last_true_range_lagged_1 = last_true_range
        last_true_range_lagged_2 = last_true_range

        hlcc4_diff = last_hlcc4 - last_hlcc4_lagged_1
        true_range_diff = last_true_range - last_true_range_lagged_1

        predictions = []

        for _ in range(steps):
            X = np.array(
                [
                    [
                        last_hlcc4,
                        last_hlcc4_lagged_1,
                        last_hlcc4_lagged_2,
                        last_true_range,
                        last_true_range_lagged_1,
                        last_true_range_lagged_2,
                        hlcc4_diff,
                        true_range_diff,
                    ]
                ]
            )

            X_scaled = self.scaler.transform(X)

            forecast = self.model.predict(X_scaled)[0]
            predictions.append(forecast)

            last_hlcc4_lagged_2 = last_hlcc4_lagged_1
            last_hlcc4_lagged_1 = last_hlcc4
            last_hlcc4 = forecast

            last_true_range_lagged_2 = last_true_range_lagged_1
            last_true_range_lagged_1 = last_true_range
            last_true_range = max(
                forecast - last_ohlcv.close,
                abs(forecast - self.ohlcv[-2].close),
                abs(last_ohlcv.low - self.ohlcv[-2].close),
            )

        return predictions

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
        high, low = self.curr_bar.high, self.curr_bar.low
        expiration = self.curr_bar.timestamp - open_timestamp - expiration

        if expiration >= 0:
            return replace(self, type=PositionRiskType.TIME)

        if side == PositionSide.LONG:
            if low < sl:
                return replace(self, type=PositionRiskType.SL)
            if high > tp:
                return replace(self, type=PositionRiskType.TP)

        if side == PositionSide.SHORT:
            if high > sl:
                return replace(self, type=PositionRiskType.SL)
            if low < tp:
                return replace(self, type=PositionRiskType.TP)

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

        ll_smooth, hh_smooth, volatility_smooth = smooth_savgol(ll, hh, volatility)

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

        ll_smooth, hh_smooth, volatility_smooth = smooth_savgol(ll, hh, volatility)

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

    def sl_ats(self, side: PositionSide, ta: TechAnalysis, sl: float) -> "float":
        timestamps = np.array([candle.timestamp for candle in self.ohlcv])
        ts_diff = np.diff(timestamps)

        if ts_diff.sum() < TIME_THRESHOLD:
            return sl

        max_lookback = max(len(timestamps), LOOKBACK)

        close = np.array([candle.close for candle in self.ohlcv])
        low = np.array([candle.low for candle in self.ohlcv])
        high = np.array([candle.high for candle in self.ohlcv])
        volatility = np.array(ta.volatility.gkyz)[-max_lookback:]

        min_length = min(len(close), len(volatility), len(high), len(low))

        if min_length < 3:
            return sl

        close_smooth, volatility_smooth, high_smooth, low_smooth = smooth_savgol(
            close, volatility, high, low
        )

        volatility_smooth = self.trail_factor * volatility_smooth[-min_length:]
        close_smooth = close_smooth[-min_length:]

        ats = self._ats(close_smooth, volatility_smooth)

        rising_low = low_smooth[-1] > low_smooth[-2] and low_smooth[-2] > low_smooth[-3]
        failing_high = (
            high_smooth[-1] < high_smooth[-2] and high_smooth[-2] < high_smooth[-3]
        )

        bullish = rising_low and (ta.trend.dmi[-1] > 0.0 or ta.momentum.cci[-1] > 100.0)
        bearish = failing_high and (
            ta.trend.dmi[-1] <= 0.0 or ta.momentum.cci[-1] < -100.0
        )

        if side == PositionSide.LONG:
            l_constr = low_smooth[-1] - volatility_smooth[-1]
            adjusted_sl = (
                min(l_constr, np.max(ats)) if bullish else min(l_constr, ats[-1])
            )

            return max(sl, adjusted_sl)

        if side == PositionSide.SHORT:
            h_constr = high_smooth[-1] + volatility_smooth[-1]
            adjusted_sl = (
                max(h_constr, np.min(ats)) if bearish else max(h_constr, ats[-1])
            )

            return min(sl, adjusted_sl)

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
