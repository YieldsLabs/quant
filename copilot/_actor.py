import logging
from typing import Union

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import check_random_state

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import SignalSide
from core.models.signal_risk import SignalRisk
from core.queries.copilot import EvaluateSession, EvaluateSignal

CopilotEvent = Union[EvaluateSignal, EvaluateSession]

logger = logging.getLogger(__name__)
LOOKBACK = 5
N_CLUSTERS = 3


def lorentzian_distance(u, v):
    return np.log(1 + np.sum(np.abs(u - v)))


class CustomKMeans(KMeans):
    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4, random_state=None):
        super().__init__(
            n_clusters=n_clusters, max_iter=max_iter, tol=tol, random_state=random_state
        )
        self.n_clusters = n_clusters

    def _e_step(self, X):
        """E-step implementation to assign clusters using Lorentzian distance."""
        distances = cdist(X, self.cluster_centers_, metric=lorentzian_distance)
        labels = distances.argmin(axis=1)
        return labels, distances

    def fit(self, X, y=None):
        """Overriding the fit method to use the custom _e_step."""
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

        cci = np.array(ta.momentum.cci[-LOOKBACK:])
        bbp = np.array(ta.volatility.bbp[-LOOKBACK:])
        tr = np.array(ta.volatility.tr[-LOOKBACK:])
        fast_rsi = np.array(ta.oscillator.frsi[-LOOKBACK:])
        slow_rsi = np.array(ta.oscillator.srsi[-LOOKBACK:])
        macd = np.array(ta.trend.macd[-LOOKBACK:])
        ppo = np.array(ta.trend.ppo[-LOOKBACK:])
        stoch_k = np.array(ta.oscillator.k[-LOOKBACK:])
        nvol = np.array(ta.volume.nvol[-LOOKBACK:])
        slow_ema = np.array(ta.trend.sma[-LOOKBACK:])
        fast_ema = np.array(ta.trend.fma[-LOOKBACK:])

        features = np.column_stack(
            (
                cci,
                bbp,
                macd,
                slow_rsi,
                ppo,
                stoch_k,
                slow_ema,
                tr,
                nvol,
            )
        )
        features = MinMaxScaler().fit_transform(features)
        kmeans = CustomKMeans(n_clusters=N_CLUSTERS, random_state=1337).fit(features)
        cluster_counts = np.bincount(kmeans.labels_)
        most_common_cluster = np.argmax(cluster_counts)
        least_common_cluster = np.argmin(cluster_counts)

        logger.info(
            f"Common cluster: {most_common_cluster}, Least Common: {least_common_cluster}"
        )

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
        tp = ta.trend.hh[-1] if signal.side == SignalSide.BUY else ta.trend.ll[-1]
        sl = ta.trend.ll[-1] if signal.side == SignalSide.BUY else ta.trend.hh[-1]
        risk_type = (
            SignalRiskType.LOW
            if (most_common_cluster == 1 and least_common_cluster == 0)
            else SignalRiskType.HIGH
        )

        if risk_type == SignalRiskType.HIGH:
            risk = SignalRisk(
                type=risk_type,
                tp=tp,
                sl=sl,
            )

        return risk

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        ta = msg.ta

        cci = np.array(ta.momentum.cci[-LOOKBACK:])
        bbp = np.array(ta.volatility.bbp[-LOOKBACK:])
        slow_rsi = np.array(ta.oscillator.srsi[-LOOKBACK:])
        stoch_k = np.array(ta.oscillator.k[-LOOKBACK:])
        mfi = np.array(ta.volume.mfi[-LOOKBACK:])

        features = np.column_stack((cci, bbp, slow_rsi, stoch_k, mfi))
        features = MinMaxScaler().fit_transform(features)
        kmeans = CustomKMeans(n_clusters=N_CLUSTERS, random_state=1337).fit(features)
        cluster_counts = np.bincount(kmeans.labels_)
        most_common_cluster = np.argmax(cluster_counts)
        least_common_cluster = np.argmin(cluster_counts)

        body_range_ratio = msg.bar.body_range_ratio

        # fast_rsi = np.array(ta.oscillator.frsi[-LOOKBACK:])

        # exit_long = (cci < 100) | (bbp > 0.8) | ((fast_rsi > 70) & (slow_rsi > 70))
        # exit_short = (cci > -100) | (bbp < 0.2) | ((fast_rsi < 30) & (slow_rsi < 30))

        # signal_exit = exit_long[-1] if msg.side == PositionSide.LONG else exit_short[-1]
        should_exit = False

        logger.info(
            f"CCI: {cci[-1]}, "
            f"RSI SLOW: {slow_rsi[-1]}, "
            f"BB%: {bbp[-1]}, "
            f"Body Range Ratio: {body_range_ratio}, "
            # f"Signal Exit {signal_exit}, "
            f"Clusters: {kmeans.labels_}, "
            # f"Centers: {kmeans.cluster_centers_}, "
            # f"Common Cluster {most_common_cluster}, "
            # f"Anomaly Cluster {least_common_cluster}"
        )

        if should_exit:
            return SessionRiskType.EXIT

        return SessionRiskType.CONTINUE
