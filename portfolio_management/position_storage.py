import asyncio
from typing import List, Optional

from core.events.portfolio import AdvancedPortfolioPerformance, BasicPortfolioPerformance
from core.position import Order, Position
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

    async def add_closed_position(self, position: Position, exit_price: float):
        async with self._closed_positions_data['lock']:
            position.close_position(exit_price)
            self._closed_positions_data['data'].setdefault(position.closed_key, position)

    def _get_positions_for_strategy(self, strategy_id: str) -> List[Position]:
        return [position for position in self._closed_positions_data['data'].values() if position.strategy_id == strategy_id]
    
    async def filter_positions_by_strategy(self, strategy: str) -> List[Position]:
        async with self._closed_positions_data['lock']:
            return self._get_positions_for_strategy(strategy)

    def basic_performance(self, closed_positions: List[Position], initial_account_size: int, risk_per_trade: int) -> BasicPortfolioPerformance:
        return self.basic.next(closed_positions, initial_account_size, risk_per_trade)

    def advanced_performance(self, closed_positions: List[Position], initial_account_size: int) -> AdvancedPortfolioPerformance:
        return self.advanced.next(closed_positions, initial_account_size)

    async def get_top_strategies(self, initial_account_size: int, num: int = 5) -> List[str]:
        async with self._closed_positions_data['lock']:
            unique_strategies = list(set([pos.strategy_id for pos in self._closed_positions_data['data'].values()]))

            strategy_performances = [
                (strategy, self.advanced_performance(self._get_positions_for_strategy(strategy), initial_account_size))
                for strategy in unique_strategies
            ]

            sorted_strategies = sorted(strategy_performances, key=lambda x: x[1].sharpe_ratio, reverse=True)
            top_strategies = sorted_strategies[:num]

            return [parse_meta_label(strategy[0]) for strategy in top_strategies]
