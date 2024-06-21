import asyncio
import logging
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


def fisher_transform(prices, lookback=10):
    import numpy as np

    prices = np.array(prices)
    high = np.max(prices[-lookback:])
    low = np.min(prices[-lookback:])

    if high != low:
        value = 2 * ((prices - low) / (high - low)) - 1
    else:
        value = 0

    value = np.clip(value, -0.99, 0.99)
    fisher = 0.5 * np.log((1 + value) / (1 - value))
    return fisher


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
        ta = msg.ta

        curr_bar = signal.ohlcv
        prev_bar = msg.prev_bar
        side = "LONG" if signal.side == SignalSide.BUY else "SHORT"
        risk = SignalRisk(
            type=SignalRiskType.NONE,
        )

        # cci = np.array(ta.momentum.cci[-LOOKBACK:])
        # bbp = np.array(ta.volatility.bbp[-LOOKBACK:])
        # tr = np.array(ta.volatility.tr[-LOOKBACK:])
        # fast_rsi = np.array(ta.oscillator.frsi[-LOOKBACK:])
        # slow_rsi = np.array(ta.oscillator.srsi[-LOOKBACK:])
        # macd = np.array(ta.trend.macd[-LOOKBACK:])
        # ppo = np.array(ta.trend.ppo[-LOOKBACK:])
        # stoch_k = np.array(ta.oscillator.k[-LOOKBACK:])
        # nvol = np.array(ta.volume.nvol[-LOOKBACK:])
        # slow_ema = np.array(ta.trend.sma[-LOOKBACK:])
        # fast_ema = np.array(ta.trend.fma[-LOOKBACK:])

        # features = np.column_stack(
        #     (
        #         cci,
        #         bbp,
        #         macd,
        #         slow_rsi,
        #         ppo,
        #         stoch_k,
        #         slow_ema,
        #         tr,
        #         nvol,
        #     )
        # )
        # features = MinMaxScaler().fit_transform(features)
        # kmeans = CustomKMeans(n_clusters=N_CLUSTERS, random_state=1337).fit(features)
        # cluster_counts = np.bincount(kmeans.labels_)
        # most_common_cluster = np.argmax(cluster_counts)
        # least_common_cluster = np.argmin(cluster_counts)

        # logger.info(
        #     f"Common cluster: {most_common_cluster}, Least Common: {least_common_cluster}"
        # )

        # prompt = signal_risk_prompt.format(
        #     curr_bar=curr_bar,
        #     prev_bar=prev_bar,
        #     side=side,
        #     timeframe=signal.timeframe,
        #     # macd_histogram=trend.macd[-LOOKBACK:],
        #     # rsi=osc.srsi[-LOOKBACK:],
        #     # k=osc.k[-LOOKBACK:],
        #     # bbp=volatility.bbp[-LOOKBACK:],
        #     # ema=trend.sma[-LOOKBACK:],
        #     # cci=momentum.cci[-LOOKBACK:]
        # )

        # logger.info(f"Signal Prompt: {prompt}")

        # answer = await self.llm.call(system_prompt, prompt)

        # logger.info(f"LLM Answer: {answer}")

        # match = re.search(signal_risk_pattern, answer)

        # if not match:
        #     risk = SignalRisk(
        #         type=SignalRiskType.NONE,
        #     )
        # else:
        #     risk = SignalRisk(
        #         type=SignalRiskType.from_string(match.group(1)),
        #         tp=float(match.group(2)),
        #         sl=float(match.group(3)),
        #     )

        # logger.info(f"Signal Risk: {risk}")
        # tp = ta.trend.hh[-1] if signal.side == SignalSide.BUY else ta.trend.ll[-1]
        # sl = ta.trend.ll[-1] if signal.side == SignalSide.BUY else ta.trend.hh[-1]
        # risk_type = (
        #     SignalRiskType.LOW
        #     if (most_common_cluster == 1 and least_common_cluster == 0)
        #     else SignalRiskType.HIGH
        # )

        # if risk_type == SignalRiskType.HIGH:
        #     risk = SignalRisk(
        #         type=risk_type,
        #         tp=tp,
        #         sl=sl,
        #     )

        return risk

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        async with self._lock:
            ta = msg.ta
            bars = pad_bars(msg.session, LOOKBACK)

            ema = np.array(ta.trend.sma[-LOOKBACK:])
            support = np.array(ta.trend.support[-LOOKBACK:])
            resistance = np.array(ta.trend.resistance[-LOOKBACK:])

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

            features = MinMaxScaler(feature_range=(-1, 1)).fit_transform(features)
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

            prev_long, prev_short = self.prev_txn

            should_exit = False

            if (
                msg.side == PositionSide.LONG
                and prev_long
                and (
                    (int(prev_long[0]) == 2 and int(knn_transaction[0]) == 4)
                    or (int(prev_long[0]) == 1 and int(knn_transaction[0]) == 4)
                    or (int(prev_long[0]) == 1 and int(knn_transaction[0]) == 2)
                    or (int(prev_long[0]) == 2 and int(knn_transaction[0]) == 1)
                    or (int(prev_long[0]) == 4 and int(knn_transaction[0]) == 2)
                )
            ):
                should_exit = True

            if (
                msg.side == PositionSide.SHORT
                and prev_short
                and (
                    (int(prev_short[0]) == 4 and int(knn_transaction[0]) == 2)
                    or (int(prev_short[0]) == 4 and int(knn_transaction[0]) == 3)
                    or (int(prev_short[0]) == 1 and int(knn_transaction[0]) == 4)
                    or (int(prev_short[0]) == 2 and int(knn_transaction[0]) == 4)
                    or (int(prev_short[0]) == 3 and int(knn_transaction[0]) == 2)
                    or (int(prev_short[0]) == 1 and int(knn_transaction[0]) == 2)
                )
            ):
                should_exit = True

            if msg.side == PositionSide.LONG:
                if not should_exit:
                    prev_long = knn_transaction
                else:
                    prev_long = None
            else:
                if not should_exit:
                    prev_short = knn_transaction
                else:
                    prev_short = None

            self.prev_txn = (prev_long, prev_short)

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
