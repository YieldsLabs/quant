import asyncio
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from typing import Dict, Tuple

from core.models.symbol import Symbol
from core.models.strategy import Strategy
from core.models.timeframe import Timeframe

class StrategyStorage:
    def __init__(self, n_clusters=3):
        self.kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
        self.scaler = MinMaxScaler()
        self.data: Dict[Tuple(Symbol, Timeframe, Strategy), Tuple[np.array, int]] = {}
        self.lock = asyncio.Lock()

    async def next(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy,  metrics: np.array):
        async with self.lock:
            key = (symbol, timeframe, strategy)
           
            self.data[key] = (metrics, -1)

            if len(self.data.keys()) < self.kmeans.n_clusters:
                return

            data_matrix = np.array([item[0] for item in self.data.values()])

            normalized_data = self.scaler.fit_transform(data_matrix)
            cluster_indices = self.kmeans.fit_predict(normalized_data)

            for idx, key in enumerate(self.data.keys()):
                current_metrics = self.data[key][0]
                self.data[key] = (current_metrics, cluster_indices[idx])


    async def get_top(self, num: int = 10):
        async with self.lock:
            sorted_strategies = sorted(self.data.keys(), key=lambda key: (self.data[key][1], self.data[key][0][0]), reverse=True)
            
            return sorted_strategies[:num]
