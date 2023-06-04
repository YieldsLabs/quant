import asyncio
from typing import List, NamedTuple, Tuple, Type
import pandas as pd

from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.strategy import LongExit, ShortExit, LongGo, ShortGo

from .abstract_strategy import AbstractStrategy


class SignalResult(NamedTuple):
    entry_long_signal: bool
    entry_short_signal: bool
    exit_long_signal: bool
    exit_short_signal: bool
    stop_loss_long: float
    stop_loss_short: float


class StrategyProcessor(AbstractEventManager):
    def __init__(self, strategy: Type[AbstractStrategy]):
        super().__init__()
        self.strategy = strategy

    async def process(self, window_events: List[OHLCV], event: OHLCVEvent):
        relevant_events = window_events[-self.strategy.lookback:]
        signals = self.calculate_signals(relevant_events, event.ohlcv.close)

        await self.dispatch_signals(signals, event)

    def calculate_signals(self, events: List[OHLCV], entry: float) -> SignalResult:
        df_events = self._events_to_dataframe(events)

        return SignalResult(
            *self.strategy.entry(df_events),
            *self.strategy.exit(df_events),
            *self.strategy.stop_loss(entry, df_events)
        )

    async def dispatch_signals(self, signals: SignalResult, event: OHLCVEvent):
        strategy_name = str(self.strategy)
        tasks = []

        if signals.entry_long_signal:
            tasks.append(self.dispatcher.dispatch(
                LongGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=event.ohlcv.close, stop_loss=signals.stop_loss_long, risk_reward_ratio=self.strategy.risk_reward_ratio)))
        elif signals.entry_short_signal:
            tasks.append(self.dispatcher.dispatch(
                ShortGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=event.ohlcv.close, stop_loss=signals.stop_loss_short, risk_reward_ratio=self.strategy.risk_reward_ratio)))
        elif signals.exit_long_signal:
            tasks.append(self.dispatcher.dispatch(
                LongExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=event.ohlcv.close)))
        elif signals.exit_short_signal:
            tasks.append(self.dispatcher.dispatch(
                ShortExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=event.ohlcv.close)))

        await asyncio.gather(*tasks)

    @staticmethod
    def _events_to_dataframe(events: List[OHLCV]) -> pd.DataFrame:
        ohlcv_columns: tuple = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
        column_types = {column: float for column in ohlcv_columns[1:]}
        return pd.DataFrame.from_records((e.to_dict() for e in events), columns=ohlcv_columns).astype(column_types)
