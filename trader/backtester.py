from itertools import product
import random
from typing import List, Type
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.order import FillOrder, Order, OrderSide
from core.events.position import ClosePosition, ClosedPosition, OpenLongPosition, OpenShortPosition
from core.timeframes import Timeframes
from datasource.abstract_datasource import AbstractDatasource
from .abstract_trader import AbstractTrader

class Backtester(AbstractTrader):
    def __init__(self, datasource: Type[AbstractDatasource]):
        super().__init__()
        self.datasource = datasource

    def run(self, symbols: List[str], timeframes: List[Timeframes], lookback: int = 3000):
        symbols_and_timeframes = list(product(symbols, timeframes))
        
        random.shuffle(symbols_and_timeframes)

        for symbol, timeframe in symbols_and_timeframes:
            historical_data = self.datasource.fetch(symbol, timeframe, lookback)

            for timestamp, open, high, low, close, volume in historical_data:
                ohlcv = OHLCV(timestamp, float(open), float(high), float(low), float(close), float(volume))
                self.dispatcher.dispatch(OHLCVEvent(symbol, timeframe, ohlcv))
      
    @register_handler(OpenLongPosition)
    def _open_long_position(self, event: OpenLongPosition):
        self.trade(event)

    @register_handler(OpenShortPosition)
    def _open_short_position(self, event: OpenShortPosition):
        self.trade(event)

    @register_handler(ClosePosition)
    def _on_close_position(self, event: ClosePosition):
        self.dispatcher.dispatch(ClosedPosition(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.exit_price))
        
    def trade(self, event):
        order_side = OrderSide.BUY if isinstance(event, OpenLongPosition) else OrderSide.SELL
        
        order = Order(side=order_side, entry=event.entry, size=event.size, stop_loss=event.stop_loss, take_profit=event.take_profit)
        self.dispatcher.dispatch(FillOrder(symbol=event.symbol, timeframe=event.timeframe, order=order))
