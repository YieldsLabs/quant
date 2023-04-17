from collections import deque
from typing import Final, List

import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.strategy import GoLong, GoShort
from strategy.abstract_strategy import AbstractStrategy

OHLCV_COLUMNS: Final = ('timestamp', 'open', 'high', 'low', 'close', 'volume')

class StrategyManager(AbstractEventManager):
    def __init__(self, strategies: List[AbstractStrategy]):
        super().__init__()
        self.strategies = strategies
        self.window_size = max([getattr(strategy, "lookback", 100) for strategy in self.strategies])
        self.window_data = {}
    
    def get_id(self, event: OHLCVEvent):
        return f'{event.symbol}_{event.timeframe}'

    @register_handler(OHLCVEvent)
    def _on_market(self, event: OHLCVEvent):
        event_id = self.get_id(event)

        if event_id not in self.window_data:
            self.window_data[event_id] = {'events': deque(maxlen=self.window_size)}

        symbol_data = self.window_data[event_id]
        symbol_data['events'].append(event.ohlcv)

        if len(symbol_data['events']) == self.window_size:
            window_events = list(symbol_data['events'])

            for strategy in self.strategies:
                entry = event.ohlcv.close
                lookback = strategy.lookback
                required_events = pd.DataFrame([data.to_dict() for data in window_events[-lookback:]], columns=OHLCV_COLUMNS)
                entry_long_signal, entry_short_signal = strategy.entry(required_events)
                stop_loss, take_profit = strategy.stop_loss_and_take_profit(entry, required_events)
                strategy_name = str(strategy)

                if entry_long_signal:
                    stop_loss_price, take_profit_price = stop_loss[0], take_profit[0]
   
                    self.dispatcher.dispatch(
                        GoLong(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=entry, stop_loss=stop_loss_price, take_profit=take_profit_price))
                elif entry_short_signal:
                    stop_loss_price, take_profit_price = stop_loss[1],  take_profit[1]

                    self.dispatcher.dispatch(
                        GoShort(symbol=event.symbol, strategy=strategy_name, timeframe=event.timeframe, entry=entry, stop_loss=stop_loss_price, take_profit=take_profit_price))
