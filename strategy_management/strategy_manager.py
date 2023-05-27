import asyncio
from typing import List, Type
from core.abstract_event_manager import AbstractEventManager

from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from .strategy_storage import StrategyStorage
from .strategy_processor import StrategyProcessor
from .abstract_strategy import AbstractStrategy


class StrategyManager(AbstractEventManager):
    MIN_LOOKBACK = 50

    def __init__(self, strategies: List[Type[AbstractStrategy]]):
        super().__init__()
        self.strategies = [StrategyProcessor(strategy) for strategy in strategies]
        self.storage = StrategyStorage(
            window_size=max(getattr(strategy, "lookback", self.MIN_LOOKBACK) for strategy in self.strategies)
        )

    @register_handler(OHLCVEvent)
    async def _on_ohlcv(self, event: OHLCVEvent) -> None:
        event_id = self._create_event_id(event)
        await self.storage.append(event_id, event.ohlcv)

        if not self.storage.can_process(event_id):
            return

        window_events = await self.storage.get_window(event_id)
        await self.process_strategies(window_events, event)

    async def process_strategies(self, window_events: List[OHLCV], event: OHLCVEvent) -> None:
        await asyncio.gather(*(strategy.process(window_events, event) for strategy in self.strategies))

    @staticmethod
    def _create_event_id(event: OHLCVEvent) -> str:
        return f'{event.symbol}_{event.timeframe}'
