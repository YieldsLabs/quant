import asyncio
from typing import List, Optional

from core.models.portfolio import AdvancedPortfolioPerformance, BasicPortfolioPerformance
from core.models.position import Order, Position
from labels.parse_label import parse_meta_label

from .portfolio_advanced_performance import PortfolioAdvancedPerformance
from .portfolio_basic_performance import PortfolioBasicPerformance


class PositionStorage:
    def __init__(self):
        self._active_positions_data = {'data': {}, 'lock': asyncio.Lock()}
        self._closed_positions_data = {'data': {}, 'lock': asyncio.Lock()}

        self.basic = PortfolioBasicPerformance()
        self.advanced = PortfolioAdvancedPerformance()

    async def add_active_position(self, symbol: str, position: Position):
        async with self._active_positions_data['lock']:
            self._active_positions_data['data'][symbol] = position

    async def remove_active_position(self, symbol: str):
        async with self._active_positions_data['lock']:
            self._active_positions_data['data'].pop(symbol, None)

    async def get_active_position(self, symbol: str) -> Optional[Position]:
        async with self._active_positions_data['lock']:
            return self._active_positions_data['data'].get(symbol)

    async def add_order(self, symbol: str, order: Order):
        async with self._active_positions_data['lock']:
            position = self._active_positions_data['data'].get(symbol)
            if position:
                position.add_order(order)
                position.update_prices(order.price)
                self._active_positions_data['data'][symbol] = position

    async def close_position(self, symbol: str, exit_price: float):
        active_position = await self._get_and_remove_active_position(symbol)
        if active_position:
            await self._mark_position_as_closed(active_position, exit_price)

    async def _get_and_remove_active_position(self, symbol: str):
        async with self._active_positions_data['lock']:
            return self._active_positions_data['data'].pop(symbol, None)

    async def _mark_position_as_closed(self, active_position, exit_price: float):
        active_position.close_position(exit_price)

        async with self._closed_positions_data['lock']:
            self._closed_positions_data['data'].setdefault(active_position.closed_key, active_position)

    def _get_positions_for_strategy(self, strategy: str) -> List[Position]:
        return [position for position in self._closed_positions_data['data'].values() if position.strategy == strategy]

    def _get_unique_strategies(self):
        return list(set([pos.strategy for pos in self._closed_positions_data['data'].values()]))

    async def filter_positions_by_strategy(self, strategy: str) -> List[Position]:
        async with self._closed_positions_data['lock']:
            return self._get_positions_for_strategy(strategy)

    async def total_pnl(self) -> float:
        async with self._closed_positions_data['lock']:
            unique_strategies = self._get_unique_strategies()

            return sum([
                position.pnl
                for strategy in unique_strategies
                for position in self._get_positions_for_strategy(strategy)
            ])

    def basic_performance(self, closed_positions: List[Position], initial_account_size: int, risk_per_trade: int) -> BasicPortfolioPerformance:
        return self.basic.next(closed_positions, initial_account_size, risk_per_trade)

    def advanced_performance(self, closed_positions: List[Position], initial_account_size: int) -> AdvancedPortfolioPerformance:
        return self.advanced.next(closed_positions, initial_account_size)

    async def get_top_strategies(self, initial_account_size: int, num: int = 5) -> List[str]:
        async with self._closed_positions_data['lock']:
            unique_strategies = self._get_unique_strategies()

            strategy_performances = [
                (strategy, self.advanced_performance(self._get_positions_for_strategy(strategy), initial_account_size))
                for strategy in unique_strategies
            ]

            sorted_strategies = sorted(strategy_performances, key=lambda x: x[1].sharpe_ratio, reverse=True)
            top_strategies = sorted_strategies[:num]

            return [parse_meta_label(strategy[0]) for strategy in top_strategies]
