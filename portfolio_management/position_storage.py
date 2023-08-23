import asyncio
from collections import namedtuple
from typing import List, Optional

from core.interfaces.abstract_position_storage import AbstractPositionStorage
from core.models.portfolio import AdvancedPortfolioPerformance, BasicPortfolioPerformance
from core.models.position import Order, Position
from core.models.strategy import Strategy

from .portfolio_advanced_performance import PortfolioAdvancedPerformance
from .portfolio_basic_performance import PortfolioBasicPerformance

ActivePositions = namedtuple("ActivePositions", ["positions"])
ClosedPositions = namedtuple("ClosedPositions", ["positions"])

class PositionStorage(AbstractPositionStorage):
    def __init__(self):
        self.active = ActivePositions({})
        self.closed = ClosedPositions({})
        
        self._active_positions_lock = asyncio.Lock()
        self._closed_positions_lock = asyncio.Lock()

        self.basic = PortfolioBasicPerformance()
        self.advanced = PortfolioAdvancedPerformance()

    async def add_active_position(self, symbol: str, position: Position) -> None:
        async with self._active_positions_lock:
            updated_positions = dict(self.active.positions)
            updated_positions[symbol] = position
            self.active = ActivePositions(updated_positions)

    def _remove(self, symbol, positions):
        try:
            del positions[symbol]
        except KeyError:
            pass
        return positions
    
    async def remove_active_position(self, symbol: str) -> None:
        async with self._active_positions_lock:
            updated_positions = self._remove(symbol, dict(self.active.positions))
            self.active = ActivePositions(updated_positions)

    async def has_active_position(self, symbol: str) -> bool:
        async with self._active_positions_lock:
            return symbol in self.active.positions

    async def get_all_active_positions(self) -> List[Position]:
        async with self._active_positions_lock:
            return list(self.active.positions.values())

    async def get_active_position(self, symbol: str) -> Optional[Position]:
        async with self._active_positions_lock:
            return self.active.positions.get(symbol)

    async def add_order(self, symbol: str, order: Order) -> None:
        position = await self._get_and_remove_active_position(symbol)
        
        if position:
            position = position.add_order(order)
            position = position.update_prices(order.price)
            await self.add_active_position(symbol, position)

    async def close_position(self, symbol: str, exit_price: float) -> None:
        active_position = await self._get_and_remove_active_position(symbol)
       
        if active_position:
            await self._mark_position_as_closed(active_position, exit_price)

    async def _get_and_remove_active_position(self, symbol: str) -> Optional[Position]:
        position = await self.get_active_position(symbol)
        
        if position:
            await self.remove_active_position(symbol)
        
        return position

    async def _mark_position_as_closed(self, active_position: Position, exit_price: float) -> None:
        async with self._closed_positions_lock:
            updated_positions = dict(self.closed.positions)
            position = active_position.close_position(exit_price)
            updated_positions[active_position.closed_key] = position
            self.closed = ClosedPositions(updated_positions)

    def _get_positions_for_strategy(self, strategy: Strategy) -> List[Position]:
        return [position for position in self.closed.positions.values() if position.strategy == strategy]

    def _get_unique_strategies(self) -> List[str]:
        return list(set(pos.strategy for pos in self.closed.positions.values()))

    async def get_closed_positions(self, strategy: Strategy) -> List[Position]:
        async with self._closed_positions_lock:
            return self._get_positions_for_strategy(strategy)

    async def total_pnl(self) -> float:
        async with self._closed_positions_lock:
            return sum(position.pnl for position in self.closed.positions.values())

    async def basic_performance(self, closed_positions: List[Position], initial_account_size: int, risk_per_trade: int) -> BasicPortfolioPerformance:
        async with self._closed_positions_lock:
            return self.basic.next(closed_positions, initial_account_size, risk_per_trade)

    async def advanced_performance(self, closed_positions: List[Position], initial_account_size: int) -> AdvancedPortfolioPerformance:
        async with self._closed_positions_lock:
            return self.advanced.next(closed_positions, initial_account_size)

    async def get_top_strategies(self, initial_account_size: int, num: int = 5) -> List[str]:
        async with self._closed_positions_lock:
            unique_strategies = self._get_unique_strategies()

            strategy_performances = [
                (strategy, self.advanced.next(self._get_positions_for_strategy(strategy), initial_account_size))
                for strategy in unique_strategies
            ]

            sorted_strategies = sorted(strategy_performances, key=lambda x: x[1].sharpe_ratio, reverse=True)
            top_strategies = sorted_strategies[:num]

            return [strategy[0] for strategy in top_strategies]
