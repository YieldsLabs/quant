import asyncio
from typing import List, Tuple, Type

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.strategy import LongExit, ShortExit, LongGo, ShortGo
from .abstract_strategy import AbstractStrategy


class StrategyProcessor(AbstractEventManager):
    def __init__(self, strategy: Type[AbstractStrategy]):
        super().__init__()
        self.strategy = strategy

    async def process(self, window_events: List[OHLCV], event: OHLCVEvent):
        relevant_events = window_events[-self.strategy.lookback:]
        signals = self.calculate_signals(relevant_events, event.ohlcv.close)

        await self.dispatch_signals(signals, event)

    def calculate_signals(self, events: List[OHLCV], entry: float) -> Tuple[bool, bool, bool, bool, float, float]:
        df_events = self._events_to_dataframe(events)

        return (
            *self.strategy.entry(df_events),
            *self.strategy.exit(df_events),
            *self.strategy.stop_loss(entry, df_events)
        )

    async def dispatch_signals(self, signals, event):
        entry_long_signal, entry_short_signal, exit_long_signal, exit_short_signal, stop_loss_long, stop_loss_short = signals
        strategy_name = str(self.strategy)
        tasks = []

        if entry_long_signal:
            tasks.append(self.dispatcher.dispatch(
                LongGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=event.ohlcv.close, stop_loss=stop_loss_long, risk_reward_ratio=self.strategy.risk_reward_ratio)))
        elif entry_short_signal:
            tasks.append(self.dispatcher.dispatch(
                ShortGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=event.ohlcv.close, stop_loss=stop_loss_short, risk_reward_ratio=self.strategy.risk_reward_ratio)))
        elif exit_long_signal:
            tasks.append(self.dispatcher.dispatch(
                LongExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=event.ohlcv.close)))
        elif exit_short_signal:
            tasks.append(self.dispatcher.dispatch(
                ShortExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=event.ohlcv.close)))

        await asyncio.gather(*tasks)

    @staticmethod
    def _events_to_dataframe(events: List[OHLCV]) -> pd.DataFrame:
        ohlcv_columns: tuple = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
        column_types = {column: float for column in ohlcv_columns[1:]}
        return pd.DataFrame.from_records((e.to_dict() for e in events), columns=ohlcv_columns).astype(column_types)
