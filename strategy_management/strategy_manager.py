import asyncio
from typing import List, Type

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.portfolio import PortfolioPerformance, PortfolioPerformanceEvent
from core.events.strategy import LongExit, ShortExit, LongGo, ShortGo
from .symbol_data import SymbolData
from .abstract_strategy import AbstractStrategy
from .kmeans_inference import KMeansInference


class StrategyManager(AbstractEventManager):
    MIN_LOOKBACK = 100
    TOTAL_TRADES_THRESHOLD = 30
    POOR_STRATEGY_CLUSTER = 1

    def __init__(self, strategies_classes: List[Type[AbstractStrategy]], inference: Type[KMeansInference]):
        super().__init__()

        self.strategies = [cls() for cls in strategies_classes]
        self.window_size = max([getattr(strategy, "lookback", self.MIN_LOOKBACK) for strategy in self.strategies])

        self.window_data = {}
        self.window_data_lock = asyncio.Lock()

        self.inference = inference

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

        event_id = self.create_event_id(event)

        async with self.window_data_lock:
            if event_id not in self.window_data:
                self.window_data[event_id] = SymbolData(self.window_size)

        symbol_data = self.window_data[event_id]

        await symbol_data.append(event.ohlcv)

        if symbol_data.count < self.window_size:
            return

        window_events = await symbol_data.get_window()

        await self.process_strategies(event_id, window_events, event)

    async def process_strategies(self, event_id: str, window_events: List[OHLCV], event: OHLCVEvent) -> None:
        valid_strategies = [strategy for strategy in self.strategies if f"{event_id}{str(strategy)}" not in self.poor_strategies]

        for strategy in valid_strategies:
            await self.process_strategy(strategy, window_events, event)

    async def process_strategy(self, strategy: AbstractStrategy, window_events: List[OHLCV], event: OHLCVEvent) -> None:
        strategy_name = str(strategy)
        close = event.ohlcv.close
        lookback = strategy.lookback
        events = window_events[-lookback:]

        entry_long_signal, entry_short_signal, exit_long_signal, exit_short_signal, stop_loss, take_profit = await asyncio.to_thread(self.calculate_signals, strategy, events, close)

        tasks = []

        if entry_long_signal:
            tasks.append(self.dispatcher.dispatch(LongGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=close, stop_loss=stop_loss[0], take_profit=take_profit[0])))
        elif entry_short_signal:
            tasks.append(self.dispatcher.dispatch(ShortGo(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=close, stop_loss=stop_loss[1], take_profit=take_profit[1])))
        elif exit_long_signal:
            tasks.append(self.dispatcher.dispatch(LongExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=close)))
        elif exit_short_signal:
            tasks.append(self.dispatcher.dispatch(ShortExit(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, exit=close)))

        if not tasks:
            return

        await asyncio.gather(*tasks)

    def _is_poor_strategy(self, performance: PortfolioPerformance) -> bool:
        return False
        # if performance.total_trades < self.TOTAL_TRADES_THRESHOLD:
        #     return False

        # features = [
        #     performance.max_drawdown,
        #     performance.average_pnl,
        #     performance.risk_of_ruin,
        #     performance.profit_factor,
        #     performance.sharpe_ratio,
        #     performance.sortino_ratio,
        #     performance.calmar_ratio,
        #     performance.cvar,
        #     performance.ulcer_index,
        # ]

        # return (
        #     self.inference.infer(features) == self.POOR_STRATEGY_CLUSTER
        #     and performance.total_pnl < 0
        # )

    @staticmethod
    def calculate_signals(strategy: AbstractStrategy, events: List[OHLCV], entry: float) -> tuple:
        ohlcv_columns: tuple = ('timestamp', 'open', 'high', 'low', 'close', 'volume')
        column_types = {column: float for column in ohlcv_columns[1:]}
        df_events = pd.DataFrame.from_records((e.to_dict() for e in events), columns=ohlcv_columns).astype(column_types)

        entry_long_signal, entry_short_signal = strategy.entry(df_events)
        exit_long_signal, exit_short_signal = strategy.exit(df_events)
        stop_loss, take_profit = strategy.stop_loss_and_take_profit(entry, df_events)

        return entry_long_signal, entry_short_signal, exit_long_signal, exit_short_signal, stop_loss, take_profit

    @staticmethod
    def create_event_id(event: OHLCVEvent) -> str:
        return f'{event.symbol}_{event.timeframe}'
