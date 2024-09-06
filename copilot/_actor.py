import asyncio
import logging
import re
from typing import Union

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.utils import check_random_state
from sklearn.decomposition import KernelPCA, PCA
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.mixture import BayesianGaussianMixture
from sklearn.neighbors import LocalOutlierFactor

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import PositionSide, SignalSide
from core.models.signal_risk import SignalRisk
from core.queries.copilot import EvaluateSession, EvaluateSignal

from ._prompt import (
    signal_contrarian_risk_prompt,
    signal_risk_pattern,
    signal_trend_risk_prompt,
    system_prompt,
)

CopilotEvent = Union[EvaluateSignal, EvaluateSession]

logger = logging.getLogger(__name__)
LOOKBACK = 8
N_CLUSTERS = 5


def binary_strings(n):
    def backtrack(current):
        if len(current) == n:
            results.append(current)
            return

        backtrack(current + "0")
        backtrack(current + "1")

    results = []
    backtrack("")
    return results


def pad_bars(bars, length):
    if len(bars) < length:
        padding = [None] * (length - len(bars))
        return padding + bars
    else:
        return bars[-length:]


def lorentzian_distance(u, v):
    return np.log(1 + np.sum(np.abs(u - v)))


class CustomKMeans(KMeans):
    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4, random_state=None):
        super().__init__(
            n_clusters=n_clusters, max_iter=max_iter, tol=tol, random_state=random_state
        )

    def _e_step(self, X):
        distances = cdist(X, self.cluster_centers_, metric=lorentzian_distance)
        labels = distances.argmin(axis=1)
        return labels, distances

    def fit(self, X, y=None):
        random_state = check_random_state(self.random_state)
        X = self._validate_data(X, accept_sparse="csr", reset=True)

        self.cluster_centers_ = self._init_centroids(X, random_state)

        for i in range(self.max_iter):
            self.labels_, distances = self._e_step(X)

            new_centers = np.array(
                [
                    X[self.labels_ == j].mean(axis=0)
                    if len(X[self.labels_ == j]) > 0
                    else self.cluster_centers_[j]
                    for j in range(self.n_clusters)
                ]
            )

            if np.all(np.abs(new_centers - self.cluster_centers_) <= self.tol):
                break

            self.cluster_centers_ = new_centers

        self.inertia_ = np.sum((distances.min(axis=1)) ** 2)
        self.n_iter_ = i + 1
        return self

    def _init_centroids(self, X, random_state):
        n_samples, n_features = X.shape
        centers = np.empty((self.n_clusters, n_features), dtype=X.dtype)

        center_id = random_state.randint(n_samples)
        centers[0] = X[center_id]

        closest_dist_sq = np.full(n_samples, np.inf)
        closest_dist_sq = np.minimum(
            closest_dist_sq, np.sum((X - centers[0]) ** 2, axis=1)
        )

        for c in range(1, self.n_clusters):
            probabilities = closest_dist_sq / closest_dist_sq.sum()
            new_center_id = random_state.choice(n_samples, p=probabilities)
            centers[c] = X[new_center_id]

            new_dist_sq = np.sum((X - centers[c]) ** 2, axis=1)
            closest_dist_sq = np.minimum(closest_dist_sq, new_dist_sq)

        return centers


class CopilotActor(BaseActor, EventHandlerMixin):
    _EVENTS = [EvaluateSignal, EvaluateSession]

    def __init__(self, llm: AbstractLLMService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

        self.llm = llm
        self.prev_txn = (None, None)
        self._lock = asyncio.Lock()
        self.anomaly = set(binary_strings(8))
        self.bars_n = 3
        self.horizon = 3

    async def on_receive(self, event: CopilotEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(EvaluateSignal, self._evaluate_signal)
        self.register_handler(EvaluateSession, self._evaluate_session)

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRisk:
        signal = msg.signal
        curr_bar = signal.ohlcv

        prev_bar = msg.prev_bar
        ta = msg.ta

        trend = ta.trend
        volume = ta.volume
        osc = ta.oscillator
        momentum = ta.momentum
        volatility = ta.volatility

        side = (
            PositionSide.LONG if signal.side == SignalSide.BUY else PositionSide.SHORT
        )
        risk_type = SignalRiskType.NONE

        risk = SignalRisk(
            type=risk_type,
        )

        bar = sorted(prev_bar + [curr_bar], key=lambda x: x.timestamp)
        strategy_type = "Contrarian" if "SUP" not in str(signal.strategy) else "Trend" 

        template = (
            signal_contrarian_risk_prompt
            if strategy_type == "Contrarian"
            else signal_trend_risk_prompt
        )

        prompt = template.format(
            side=side,
            strategy_type=strategy_type,
            entry=curr_bar.close,
            horizon=self.horizon,
            timeframe=signal.timeframe,
            bar=bar[-self.bars_n :],
            trend=trend.sma[-self.bars_n :],
            macd=trend.macd[-self.bars_n :],
            rsi=osc.srsi[-self.bars_n :],
            cci=momentum.cci[-self.bars_n :],
            roc=momentum.sroc[-self.bars_n :],
            nvol=volume.nvol[-self.bars_n :],
            support=trend.support[-self.bars_n :]
            if side == PositionSide.SHORT
            else trend.resistance[-self.bars_n :],
            resistance=trend.resistance[-self.bars_n :]
            if side == PositionSide.SHORT
            else trend.support[-self.bars_n :],
            vwap=volume.vwap[-self.bars_n :],
            upper_bb=volatility.upb[-self.bars_n :],
            lower_bb=volatility.lwb[-self.bars_n :],
            true_range=volatility.tr[-self.bars_n :],
        )

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        match = re.search(signal_risk_pattern, answer)
        # match = None

        if not match:
            risk = SignalRisk(type=risk_type)
        else:
            risk_type = SignalRiskType.from_string(match.group(1))
            _tp, _sl = match.group(2).split("."), match.group(3).split(".")

            tp, sl = float(f"{_tp[0]}.{_tp[1]}"), float(f"{_sl[0]}.{_sl[1]}")

            unknow_risk = tp > curr_bar.close and side == PositionSide.SHORT or tp < curr_bar.close and side == PositionSide.LONG

            if unknow_risk:
                logger.warn(f"Risk is unknown TP/SL")
                # risk_type = SignalRiskType.UNKNOWN

            risk = SignalRisk(type=risk_type, tp=tp, sl=sl)

        logger.info(f"Entry: {curr_bar.close}, Signal Risk: {risk}")

        return risk

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        async with self._lock:
            ta = msg.ta
            bars = pad_bars(msg.session, LOOKBACK)

            ema = np.array(ta.trend.sma[-LOOKBACK:])
            support = np.array(ta.trend.support[-LOOKBACK:])
            resistance = np.array(ta.trend.resistance[-LOOKBACK:])
            dmi = np.array(ta.trend.dmi[-LOOKBACK:])
            macd = np.array(ta.trend.macd[-LOOKBACK:])
            cci = np.array(ta.momentum.cci[-LOOKBACK:])
            ebb = np.array(ta.volatility.ebb[-LOOKBACK:])
            ekch = np.array(ta.volatility.ekch[-LOOKBACK:])
            rsi = np.array(ta.oscillator.srsi[-LOOKBACK:])
            stoch_k = np.array(ta.oscillator.k[-LOOKBACK:])
            mfi = np.array(ta.volume.mfi[-LOOKBACK:])
            roc = np.array(ta.momentum.sroc[-LOOKBACK:])
            vwap = np.array(ta.volume.vwap[-LOOKBACK:])
            nvol = np.array(ta.volume.nvol[-LOOKBACK:])
            volatility = np.array(ta.volatility.yz[-LOOKBACK:])
            tr = np.array(ta.volatility.tr[-LOOKBACK:])

            brr = np.array(
                [
                    bar.body_range_ratio if bar is not None else 0.0
                    for bar in bars[-LOOKBACK:]
                ]
            )
            close = np.array(
                [bar.close if bar is not None else 0.0 for bar in bars[-LOOKBACK:]]
            )

            features = np.column_stack(
                (
                    ema,
                    support,
                    resistance,
                    dmi,
                    macd,
                    brr,
                    cci,
                    rsi,
                    stoch_k,
                    mfi,
                    ebb,
                    ekch,
                    volatility,
                    roc,
                    vwap,
                    tr,
                    nvol,
                )
            )

            features = StandardScaler().fit_transform(features)
            features = MinMaxScaler(feature_range=(-1, 1)).fit_transform(features)

            features = PCA(n_components=5).fit_transform(features)
            features = KernelPCA(n_components=2, kernel='rbf').fit_transform(features)

            n_neighbors = len(features) - 1
            max_clusters = min(n_neighbors, 10)
            min_clusters = min(2, max_clusters)
            k_best_score = float("-inf")
            k_best_labels = None

            for k in range(min_clusters, max_clusters + 1):
                kmeans = CustomKMeans(n_clusters=k, random_state=None).fit(features)

                if len(np.unique(kmeans.labels_)) < k:
                    continue

                score = calinski_harabasz_score(features, kmeans.labels_)
                sil_score = silhouette_score(features, kmeans.labels_)
                db_score = davies_bouldin_score(features, kmeans.labels_)

                combined_score = (score + sil_score - db_score) / 3
    
                if combined_score > k_best_score:
                    k_best_score = combined_score
                    k_best_labels = kmeans.labels_
   
            k_cluster_labels = k_best_labels.reshape(-1, 1)

            features_with_clusters = np.hstack((features, k_cluster_labels))

            iso_forest = IsolationForest(contamination=0.01, random_state=1337).fit(features_with_clusters)
            iso_anomaly = iso_forest.predict(features_with_clusters) == -1

            lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=0.01)
            lof_anomaly = lof.fit_predict(features_with_clusters) == -1

            one_class_svm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.01)
            svm_anomaly = one_class_svm.fit_predict(features_with_clusters) == -1

            iso_scores = iso_forest.decision_function(features_with_clusters)
            lof_scores = -lof.negative_outlier_factor_
            svm_score = one_class_svm.decision_function(features_with_clusters)
            
            anomaly_scores = 0.3 * iso_scores + 0.2 * lof_scores + 0.5 * svm_score

            bgmm = BayesianGaussianMixture(n_components=2, covariance_type='full', random_state=1337)
            bgmm.fit(anomaly_scores.reshape(-1, 1))

            dynamic_threshold = np.percentile(bgmm.means_, 5)
            knn_transaction = "".join(map(str, kmeans.labels_))

            should_exit = False

            confidence_scores = {
                'knn_transaction': 0.4 if knn_transaction in self.anomaly else 0,
                'anomaly_score': 0.2 if anomaly_scores[-1] < dynamic_threshold else 0,
                'iso_anomaly': 0.3 if iso_anomaly[-1] else 0,
                'lof_anomaly': 0.05 if lof_anomaly[-1] else 0,
                'svm_anomaly': 0.05 if svm_anomaly[-1] else 0,
            }

            if sum(confidence_scores.values()) > 0.5:
                should_exit = True

            logger.info(
                f"SIDE: {msg.side}, "
                f"Close: {close[-1]}, "
                f"Exit: {should_exit}"
            )

            if should_exit:
                return SessionRiskType.EXIT

            return SessionRiskType.CONTINUE
