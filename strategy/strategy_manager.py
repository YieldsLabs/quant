import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Final, List, Any, Type

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.portfolio import PortfolioPerformance, PortfolioPerformanceEvent
from core.events.strategy import GoLong, GoShort
from strategy.abstract_strategy import AbstractStrategy


@dataclass
class SymbolData:
    events: deque


class StrategyManager(AbstractEventManager):
    OHLCV_COLUMNS: Final = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
    MIN_LOOKBACK = 100

    def __init__(self, strategies_classes: List[Type[AbstractStrategy]]):
        super().__init__()

        self.strategies = [cls() for cls in strategies_classes]
        self.window_size = max([getattr(strategy, "lookback", self.MIN_LOOKBACK) for strategy in self.strategies])

        self.window_data = {}
        self.window_data_lock = asyncio.Lock()

        self.poor_strategies = set()
        self.poor_strategies_lock = asyncio.Lock()

        self.executor = ThreadPoolExecutor()

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
                self.window_data[event_id] = SymbolData(events=deque(maxlen=self.window_size))

            symbol_data = self.window_data[event_id]

            symbol_data.events.append(event.ohlcv)

            if len(symbol_data.events) < self.window_size:
                return

            window_events = list(symbol_data.events)

        valid_strategies = [strategy for strategy in self.strategies if f"{event_id}{str(strategy)}" not in self.poor_strategies]

        await self.process_strategies(valid_strategies, window_events, event)

    async def process_strategies(self, strategies: List, window_events: List, event: OHLCVEvent) -> None:
        strategy_tasks = [
            self.process_strategy(strategy, window_events, event)
            for strategy in strategies
        ]

        await asyncio.gather(*strategy_tasks)

    async def process_strategy(self, strategy: AbstractStrategy, window_events: List[Any], event: OHLCVEvent) -> None:
        strategy_name = str(strategy)
        entry = event.ohlcv.close
        lookback = strategy.lookback

        events_for_strategy = pd.DataFrame([data.to_dict() for data in window_events[-lookback:]], columns=self.OHLCV_COLUMNS)

        entry_long_signal, entry_short_signal, stop_loss, take_profit = await asyncio.get_event_loop().run_in_executor(self.executor, self.calculate_signals, strategy, events_for_strategy, entry)

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
