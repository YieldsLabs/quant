import asyncio
from typing import List

from core.event_dispatcher import register_handler
from core.events.portfolio import PortfolioPerformanceUpdated
from labels.parse_label import parse_meta_label

from .abstract_optimization import AbstractOptimization
from .kmeans_inference import KMeansInference


class Optimization(AbstractOptimization):
    TRADE_COUNT_THRESHOLD = 10
    DRAWDAWN_CLUSTER = 1

    def __init__(self):
        super().__init__()
        self.strategies = {}
        self.lock = asyncio.Lock()

        self.cluster_analysis = KMeansInference(
            './optimization/model/kmeans_model.pkl',
            './optimization/model/scaler.pkl'
        )

    @register_handler(PortfolioPerformanceUpdated)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceUpdated):
        async with self.lock:
            strategy_id = event.strategy_id
            strategy_performance = event.performance

            if strategy_performance.total_trades < self.TRADE_COUNT_THRESHOLD:
                return

            label = parse_meta_label(strategy_id)
            symbol = label[0]

            existing_strategy = self.strategies.setdefault(symbol, (label, strategy_performance))

            if strategy_performance.sharpe_ratio > existing_strategy[1].sharpe_ratio:
                self.strategies[symbol] = (label, strategy_performance)

    async def get_top_strategies(self, num: int = 5) -> List[str]:
        async with self.lock:
            sorted_strategies = sorted(self.strategies.values(), key=lambda x: x[1].sharpe_ratio, reverse=True)
            top5_strategies = sorted_strategies[:num]

            return [strategy[0] for strategy in top5_strategies]

    async def get_all_strategies(self) -> List[str]:
        async with self.lock:
            return [strategy[0] for strategy in self.strategies.values()]
