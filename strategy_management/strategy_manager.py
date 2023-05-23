import asyncio
from typing import List, Type

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.strategy import LongExit, ShortExit, LongGo, ShortGo
from .symbol_data import SymbolData
from .abstract_strategy import AbstractStrategy


class StrategyManager(AbstractEventManager):
    MIN_LOOKBACK = 50

    def __init__(self, strategies: List[Type[AbstractStrategy]]):
        super().__init__()

        self.strategies = strategies
        self.window_size = max([getattr(strategy, "lookback", self.MIN_LOOKBACK) for strategy in self.strategies])

        self.window_data = {}
        self.window_data_lock = asyncio.Lock()

    @register_handler(OHLCVEvent)
    async def _on_ohlcv(self, event: OHLCVEvent) -> None:
        if not len(self.strategies):
            raise ValueError('Strategies should be defined')

        event_id = self.create_event_id(event)

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
        for strategy in self.strategies:
            await self.process_strategy(strategy, window_events, event)

    async def process_strategy(self, strategy: Type[AbstractStrategy], window_events: List[OHLCV], event: OHLCVEvent) -> None:
        strategy_name = str(strategy)

        ohlcv = event.ohlcv

        lookback = strategy.lookback
        risk_reward_ratio = strategy.risk_reward_ratio

        events = window_events[-lookback:]
        entry_long_signal, entry_short_signal, exit_long_signal, exit_short_signal, stop_loss_long, stop_loss_short = await asyncio.to_thread(self.calculate_signals, strategy, events, ohlcv.close)

        tasks = []

        if entry_long_signal:
            tasks.append(self.dispatcher.dispatch(LongGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=ohlcv.close, stop_loss=stop_loss_long, risk_reward_ratio=risk_reward_ratio)))
        elif entry_short_signal:
            tasks.append(self.dispatcher.dispatch(ShortGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=ohlcv.close, stop_loss=stop_loss_short, risk_reward_ratio=risk_reward_ratio)))
        elif exit_long_signal:
            tasks.append(self.dispatcher.dispatch(LongExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=ohlcv.close)))
        elif exit_short_signal:
            tasks.append(self.dispatcher.dispatch(ShortExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=ohlcv.close)))

        if not tasks:
            return

        await asyncio.gather(*tasks)

    @staticmethod
    def calculate_signals(strategy: AbstractStrategy, events: List[OHLCV], entry: float) -> tuple[bool, bool, bool, bool, float, float]:
        ohlcv_columns: tuple = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
        column_types = {column: float for column in ohlcv_columns[1:]}
        df_events = pd.DataFrame.from_records((e.to_dict() for e in events), columns=ohlcv_columns).astype(column_types)

        entry_long_signal, entry_short_signal = strategy.entry(df_events)
        exit_long_signal, exit_short_signal = strategy.exit(df_events)
        stop_loss_long, stop_loss_short = strategy.stop_loss(entry, df_events)

        return entry_long_signal, entry_short_signal, exit_long_signal, exit_short_signal, stop_loss_long, stop_loss_short

    @staticmethod
    def create_event_id(event: OHLCVEvent) -> str:
        return f'{event.symbol}_{event.timeframe}'
