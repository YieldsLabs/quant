import asyncio
import logging
import re
from typing import Union

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.manifold import Isomap
from sklearn.metrics import calinski_harabasz_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import check_random_state

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import PositionSide, SignalSide
from core.models.signal_risk import SignalRisk
from core.queries.copilot import EvaluateSession, EvaluateSignal

from ._prompt import signal_risk_pattern, signal_risk_prompt, system_prompt

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

    async def on_receive(self, event: CopilotEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(EvaluateSignal, self._evaluate_signal)
        self.register_handler(EvaluateSession, self._evaluate_session)

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRisk:
        signal = msg.signal

        curr_bar = signal.ohlcv
        prev_bar = msg.prev_bar

        side = (
            PositionSide.LONG if signal.side == SignalSide.BUY else PositionSide.SHORT
        )
        risk = SignalRisk(
            type=SignalRiskType.NONE,
        )

        prompt = signal_risk_prompt.format(
            bar=sorted(prev_bar + [curr_bar], key=lambda x: x.timestamp),
            side=side,
            timeframe=signal.timeframe,
        )

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        match = re.search(signal_risk_pattern, answer)
        risk_type = SignalRiskType.NONE

        if not match:
            risk = SignalRisk(type=risk_type)
        else:
            risk_type = SignalRiskType.from_string(match.group(1))

            tp = float(match.group(2))
            sl = float(match.group(3))

            if (side == PositionSide.LONG and tp < curr_bar.close) or (
                side == PositionSide.SHORT and tp > curr_bar.close
            ):
                risk_type = SignalRiskType.VERY_HIGH

            risk = SignalRisk(type=risk_type, tp=tp, sl=sl)

        logger.info(f"Signal Risk: {risk}")

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
            slow_rsi = np.array(ta.oscillator.srsi[-LOOKBACK:])
            stoch_k = np.array(ta.oscillator.k[-LOOKBACK:])
            mfi = np.array(ta.volume.mfi[-LOOKBACK:])

            volatility = np.array(ta.volatility.yz[-LOOKBACK:])

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
                    slow_rsi,
                    stoch_k,
                    mfi,
                    ebb,
                    ekch,
                    volatility,
                )
            )

            features = MinMaxScaler(feature_range=(-1.0, 1.0)).fit_transform(features)
            features = Isomap(
                n_components=2, n_neighbors=len(features) - 1
            ).fit_transform(features)

            max_clusters = min(len(features) - 1, 10)
            min_clusters = min(2, max_clusters)
            best_score = float("-inf")
            optimal_clusters = min_clusters

            for k in range(min_clusters, max_clusters + 1):
                kmeans = CustomKMeans(n_clusters=k, random_state=None).fit(features)

                if len(np.unique(kmeans.labels_)) < k:
                    continue

                score = calinski_harabasz_score(features, kmeans.labels_)

                if score > best_score:
                    best_score = score
                    optimal_clusters = k

            kmeans = CustomKMeans(n_clusters=optimal_clusters, random_state=1337).fit(
                features
            )

            knn_transaction = "".join(map(str, kmeans.labels_))

            should_exit = False

            if knn_transaction in self.anomaly:
                should_exit = True

            logger.info(
                f"SIDE: {msg.side}, "
                f"Close: {close[-1]}, "
                f"EMA: {ema[-1]}, "
                f"Support: {support[-1]}, "
                f"Resistance: {resistance[-1]}, "
                f"MACD: {macd[-1]}, "
                f"Body Range Ratio: {brr[-1]}, "
                f"DMI: {dmi[-1]}, "
                f"CCI: {cci[-1]}, "
                f"RSI: {slow_rsi[-1]}, "
                f"Stoch K: {stoch_k[-1]}, "
                f"MFI: {mfi[-1]}, "
                f"Volatility: {volatility[-1]}, "
                f"EBB: {ebb[-1]}, "
                f"EKCH: {ekch[-1]}, "
                f"KNN Transaction: {knn_transaction}, "
                f"Exit: {should_exit}"
            )

            if should_exit:
                return SessionRiskType.EXIT

            return SessionRiskType.CONTINUE
