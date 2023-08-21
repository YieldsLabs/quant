from core.event_decorators import register_handler
from core.events.backtest import BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed
from core.models.timeframe import Timeframe
from core.models.ohlcv import OHLCV
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK
from core.interfaces.abstract_backtest import AbstractBacktest


class Backtest(AbstractBacktest):
    def __init__(self):
        super().__init__()

    @register_handler(BacktestStarted)
    async def _on_backtest(self, event: BacktestStarted):
        actor = event.actor
        symbol = actor.symbol
        timeframe = actor.timeframe

        self._ensure_actor_state(actor)

        iterator = event.datasource.fetch(symbol, timeframe, TIMEFRAMES_TO_LOOKBACK[(event.lookback, timeframe)])

        async for data in iterator:
            await self._process_historical_data(symbol, timeframe, data)

        last_row = iterator.get_last_row()

        if last_row:
            last_close = last_row[-2]
            await self.dispatcher.dispatch(PositionClosed(symbol, timeframe, last_close))

        if actor.running:
            actor.stop()

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, data):
        ohlcv = OHLCV.from_raw(data)

        await self.dispatcher.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv))

    def _ensure_actor_state(self, actor):
        if actor.running:
            actor.stop()

        actor.start()
