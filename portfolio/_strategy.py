import asyncio
from typing import Dict, List, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
from sklearn.metrics import calinski_harabasz_score
from sklearn.preprocessing import MinMaxScaler

from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class StrategyStorage:
    def __init__(self, n_neighbors=3, max_data_size=1000):
        self.scaler = MinMaxScaler()
        self.imputer = KNNImputer(n_neighbors=n_neighbors)
        self.data: Dict[Tuple[Symbol, Timeframe, Strategy], Tuple[np.array, int]] = {}
        self.lock = asyncio.Lock()
        self.max_data_size = max_data_size

    async def next(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        metrics: np.array,
    ):
        async with self.lock:
            key = (symbol, timeframe, strategy)
            self.data[key] = (metrics, -1)

            if len(self.data) > self.max_data_size:
                oldest_key = next(iter(self.data))
                self.data.pop(oldest_key)

            if len(self.data) >= 2:
                self._update_clusters()

    async def reset(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        async with self.lock:
            self.data.pop((symbol, timeframe, strategy), None)

    async def reset_all(self):
        async with self.lock:
            self.data = {}

    async def get_top(self, num: int = 10) -> List[Tuple[Symbol, Timeframe, Strategy]]:
        async with self.lock:
            sorted_strategies = sorted(
                self.data.keys(), key=self._sorting_key, reverse=True
            )
            return sorted_strategies[:num]

    def _update_clusters(self):
        if len(self.data) < 3:
            return

        data_keys = list(self.data.keys())
        data_matrix = np.array([self.data[key][0] for key in data_keys])

        imputed_data = self.imputer.fit_transform(data_matrix)
        normalized_data = self.scaler.fit_transform(imputed_data)
        optimal_clusters = self._determine_optimal_clusters(normalized_data)
        kmeans = KMeans(n_clusters=optimal_clusters, n_init="auto", random_state=1337)
        cluster_indices = kmeans.fit_predict(normalized_data)

        for key, idx in zip(data_keys, cluster_indices):
            self.data[key] = (
                self.data[key][0],
                idx,
            )

    def _determine_optimal_clusters(self, data: np.array) -> int:
        max_clusters = min(len(data) - 1, 10)
        min_clusters = min(2, max_clusters)
        best_score = float("-inf")
        optimal_clusters = 0

        for k in range(min_clusters, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, n_init="auto", random_state=None)
            kmeans.fit_predict(data)

            if len(np.unique(kmeans.labels_)) < k:
                continue

            score = calinski_harabasz_score(data, kmeans.labels_)

            if score > best_score:
                best_score = score
                optimal_clusters = k

        return optimal_clusters

    def _sorting_key(self, key):
        return self.data[key][1], self.data[key][0][0]
