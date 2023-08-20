import asyncio
from typing import Dict, List, Optional
from core.events.portfolio import AdvancedPortfolioPerformance, BasicPortfolioPerformance

from core.position import Order, Position
from labels.parse_label import parse_meta_label

from .portfolio_advanced_performance import PortfolioAdvancedPerformance
from .portfolio_basic_performance import PortfolioBasicPerformance


class PositionStorage:
    def __init__(self):
        self.active_positions: Dict[str, Position] = {}
        self.active_positions_lock = asyncio.Lock()
        self.closed_positions: Dict[str, Position] = {}
        self.closed_positions_lock = asyncio.Lock()
        
        self.basic = PortfolioBasicPerformance()
        self.advanced = PortfolioAdvancedPerformance()

    async def add_active_position(self, symbol: str, position: Position):
        async with self.active_positions_lock:
            self.active_positions[symbol] = position

    async def remove_active_position(self, symbol: str):
        async with self.active_positions_lock:
            self.active_positions.pop(symbol, None)

    async def get_active_position(self, symbol: str) -> Optional[Position]:
        async with self.active_positions_lock:
            return self.active_positions.get(symbol)

    async def add_order(self, symbol: str, order: Order):
        async with self.active_positions_lock:
            position = self.active_positions.get(symbol)

            position.add_order(order)
            position.update_prices(order.price)

            self.active_positions[symbol] = position

    async def add_closed_position(self, position: Position, exit_price: float):
        async with self.closed_positions_lock:
            position.close_position(exit_price)

            if position.closed_key not in self.closed_positions:
                self.closed_positions[position.closed_key] = position

    async def filter_closed_positions_by_strategy(self, strategy_id: str) -> List[Position]:
        async with self.closed_positions_lock:
            return [position for position in self.closed_positions.values() if position.strategy_id == strategy_id]
        
    async def basic_performance(self, strategy_id: str, initial_account_size: int, risk_per_trade: int) -> BasicPortfolioPerformance:
        closed_positions = await self.filter_closed_positions_by_strategy(strategy_id)

        return self.basic.next(closed_positions, initial_account_size, risk_per_trade)
    
    async def advanced_performance(self, strategy_id: str, initial_account_size: int) -> AdvancedPortfolioPerformance:
        closed_positions = await self.filter_closed_positions_by_strategy(strategy_id)

        return self.advanced.next(closed_positions, initial_account_size)
    
    async def get_top_strategies(self, initial_account_size: int, num: int = 5) -> List[str]:
        async with self.closed_positions_lock:
            unique_strategies = list(set([pos.strategy_id for pos in self.closed_positions.values()]))

            strategy_performances = []
            
            for strategy in unique_strategies:
                closed_positions = [position for position in self.closed_positions.values() if position.strategy_id == strategy]
                performance = self.advanced.next(closed_positions, initial_account_size)
                strategy_performances.append((strategy, performance))

            sorted_strategies = sorted(strategy_performances, key=lambda x: x[1].sharpe_ratio, reverse=True)
            top_strategies = sorted_strategies[:num]

            return [parse_meta_label(strategy[0]) for strategy in top_strategies]
