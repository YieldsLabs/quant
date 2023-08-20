from core.event_decorators import register_handler
from core.events.backtest import BacktestStarted
from core.events.ohlcv import OHLCV, NewMarketDataReceived
from core.events.position import ClosePositionPrepared
from core.timeframe import Timeframe

from .abstract_backtest import AbstractBacktest
from .lookback import TIMEFRAMES_TO_LOOKBACK


class Backtest(AbstractBacktest):
    def __init__(self):
        super().__init__()

    @register_handler(BacktestStarted)
    async def _on_backtest(self, event: BacktestStarted):
        actor = event.actor
        symbol = actor.symbol
        timeframe = actor.timeframe

        iterator = event.datasource.fetch(symbol, timeframe, TIMEFRAMES_TO_LOOKBACK[(event.lookback, timeframe)])

        if actor.running:
            actor.stop()

        actor.start()

        async for data in iterator:
            await self._process_historical_data(symbol, timeframe, data)

        last_row = iterator.get_last_row()

        if last_row:
            last_close = last_row[-2]
            await self.dispatcher.dispatch(ClosePositionPrepared(symbol, timeframe, last_close))

        if actor.running:
            actor.stop()

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, data):
        timestamp, open, high, low, close, volume = data
        ohlcv = OHLCV(timestamp, float(open), float(high), float(low), float(close), float(volume))
        await self.dispatcher.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv))
