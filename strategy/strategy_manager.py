import asyncio
from collections import deque
from typing import List, Any, Type

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.portfolio import PortfolioPerformance, PortfolioPerformanceEvent
from core.events.strategy import GoLong, GoShort
from strategy.abstract_strategy import AbstractStrategy


class SymbolData:
    def __init__(self, size: int):
        self.buffer = deque(maxlen=size)
        self.count = 0
        self.lock = asyncio.Lock()

    async def append(self, event):
        async with self.lock:
            self.count += 1
            self.buffer.append(event)

    async def get_window(self):
        async with self.lock:
            return list(self.buffer)

class StrategyManager(AbstractEventManager):
    OHLCV_COLUMNS: tuple = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
    MIN_LOOKBACK = 100
    BATCH_SIZE = 10

    def __init__(self, strategies_classes: List[Type[AbstractStrategy]]):
        super().__init__()

        self.strategies = [cls() for cls in strategies_classes]
        self.window_size = max([getattr(strategy, "lookback", self.MIN_LOOKBACK) for strategy in self.strategies])

        self.window_data = {}
        self.window_data_lock = asyncio.Lock()

        self.poor_strategies = set()
        self.poor_strategies_lock = asyncio.Lock()

    @register_handler(PortfolioPerformanceEvent)
    async def _on_poor_strategy(self, event: PortfolioPerformanceEvent):
        strategy_id = event.strategy_id
        performance = event.performance

        if not self._is_poor_strategy(performance):
            return

        async with self.poor_strategies_lock:
            self.poor_strategies.add(strategy_id)

    @register_handler(OHLCVEvent)
    async def _on_ohlcv(self, event: OHLCVEvent) -> None:
        if not len(self.strategies):
            raise ValueError('Strategies should be defined')

        event_id = self.get_event_id(event)

        async with self.window_data_lock:
            if event_id not in self.window_data:
                self.window_data[event_id] = SymbolData(self.window_size)

        symbol_data = self.window_data[event_id]

        await symbol_data.append(event.ohlcv)
        
        if symbol_data.count < self.window_size:
            return
        
        window_events = await symbol_data.get_window()

        valid_strategies = [strategy for strategy in self.strategies if f"{event_id}{str(strategy)}" not in self.poor_strategies]

        await self.process_strategies(valid_strategies, window_events, event)
            
    async def process_strategies(self, strategies: list, window_events: list, event: OHLCVEvent) -> None:
        strategy_batches = [strategies[i:i + self.BATCH_SIZE] for i in range(0, len(strategies), self.BATCH_SIZE)]

        for batch in strategy_batches:
            strategy_tasks = [
                self.process_strategy(strategy, window_events, event)
                for strategy in batch
            ]

            await asyncio.gather(*strategy_tasks)

    async def process_strategy(self, strategy: AbstractStrategy, window_events: List[Any], event: OHLCVEvent) -> None:
        strategy_name = str(strategy)
        entry = event.ohlcv.close
        lookback = strategy.lookback

        events_for_strategy = pd.DataFrame([data.to_dict() for data in window_events[-lookback:]], columns=self.OHLCV_COLUMNS)
        entry_long_signal, entry_short_signal, stop_loss, take_profit = await asyncio.to_thread(self.calculate_signals, strategy, events_for_strategy, entry)

        if entry_long_signal:
            stop_loss_price, take_profit_price = stop_loss[0], take_profit[0]
            await self.dispatcher.dispatch(GoLong(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=entry, stop_loss=stop_loss_price, take_profit=take_profit_price))
        elif entry_short_signal:
            stop_loss_price, take_profit_price = stop_loss[1], take_profit[1]
            await self.dispatcher.dispatch(GoShort(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=entry, stop_loss=stop_loss_price, take_profit=take_profit_price))

    def get_event_id(self, event: OHLCVEvent) -> str:
        return f'{event.symbol}_{event.timeframe}'

    def calculate_signals(self, strategy: AbstractStrategy, required_events: pd.DataFrame, entry: float) -> tuple:
        entry_long_signal, entry_short_signal = strategy.entry(required_events)

        stop_loss, take_profit = strategy.stop_loss_and_take_profit(entry, required_events)

        return entry_long_signal, entry_short_signal, stop_loss, take_profit

    def _is_poor_strategy(self, performance: PortfolioPerformance):
        return False
