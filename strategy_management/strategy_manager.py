import asyncio
from typing import List, Type
from core.abstract_event_manager import AbstractEventManager

from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from strategy_management.strategy_processor import StrategyProcessor
from .symbol_data import SymbolData
from .abstract_strategy import AbstractStrategy


class StrategyManager(AbstractEventManager):
    def __init__(self, strategies: List[Type[AbstractStrategy]]):
        super().__init__()
        self.strategies = [StrategyProcessor(strategy) for strategy in strategies]

        self.window_size = max([getattr(strategy, "lookback", 50) for strategy in self.strategies])
        self.window_data = {}
        self.window_data_lock = asyncio.Lock()

    @register_handler(OHLCVEvent)
    async def _on_ohlcv(self, event: OHLCVEvent) -> None:
        event_id = self._create_event_id(event)

        async with self.window_data_lock:
            if event_id not in self.window_data:
                self.window_data[event_id] = SymbolData(self.window_size)

        symbol_data = self.window_data[event_id]

        await symbol_data.append(event.ohlcv)

        if symbol_data.count < self.window_size:
            return

        window_events = await symbol_data.get_window()

        await self.process_strategies(window_events, event)

    async def process_strategies(self, window_events: List[OHLCV], event: OHLCVEvent) -> None:
        tasks = [strategy.process(window_events, event) for strategy in self.strategies]

        await asyncio.gather(*tasks)

    @staticmethod
    def _create_event_id(event: OHLCVEvent) -> str:
        return f'{event.symbol}_{event.timeframe}'
