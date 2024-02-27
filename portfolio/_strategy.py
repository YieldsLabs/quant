import asyncio
from typing import Dict, Tuple

import numpy as np
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class StrategyStorage:
    def __init__(self, n_clusters=3):
        self.kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
        self.scaler = MinMaxScaler()
        self.imputer = KNNImputer(n_neighbors=2)
        self.data: Dict[Tuple[Symbol, Timeframe, Strategy], Tuple[np.array, int]] = {}
        self.lock = asyncio.Lock()

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

            if len(self.data.keys()) >= self.kmeans.n_clusters:
                self._update_clusters()

    async def reset(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        async with self.lock:
            self.data.pop((symbol, timeframe, strategy), None)

    async def reset_all(self):
        async with self.lock:
            self.data = {}

    async def get_top(self, num: int = 10):
        async with self.lock:
            sorted_strategies = sorted(
                self.data.keys(), key=self._sorting_key, reverse=True
            )
            return sorted_strategies[:num]

    def _update_clusters(self):
        data_matrix = np.array([item[0] for item in self.data.values()])
        imputed_data = self.imputer.fit_transform(data_matrix)
        normalized_data = self.scaler.fit_transform(imputed_data)
        cluster_indices = self.kmeans.fit_predict(normalized_data)

        for (symbol, timeframe, strategy), idx in zip(
            self.data.keys(), cluster_indices
        ):
            self.data[(symbol, timeframe, strategy)] = (
                self.data[(symbol, timeframe, strategy)][0],
                idx,
            )

    def _sorting_key(self, key):
        return self.data[key][1], self.data[key][0][0]
