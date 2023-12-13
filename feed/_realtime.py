import asyncio
import logging

from core.actors import Actor
from core.commands.feed import StartRealtimeFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_ws import AbstractWS
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

logger = logging.getLogger(__name__)


class AsyncRealTimeData:
    def __init__(
        self,
        ws: AbstractWS,
        symbol: Symbol,
        timeframe: Timeframe,
    ):
        self.ws = ws
        self.symbol = symbol
        self.timeframe = timeframe
        self.iterator = None

        self.task = asyncio.create_task(self._initialize())

    async def _initialize(self):
        await self.ws.run()
        await self.ws.subscribe(self.symbol, self.timeframe)

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.task.cancel()
        await self.ws.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.ws.receive(self.symbol, self.timeframe)
            return data
        except StopAsyncIteration:
            await self.ws.close()
            raise


class RealtimeActor(Actor):
    _EVENTS = [StartRealtimeFeed]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        ws: AbstractWS,
    ):
        super().__init__(symbol, timeframe, strategy)
        self.ws = ws

    def pre_receive(self, msg: StartRealtimeFeed):
        return self._symbol == msg.symbol and self._timeframe == msg.timeframe

    async def on_receive(self, msg: StartRealtimeFeed):
        asyncio.create_task(self._run_realtime_feed(msg))

    async def _run_realtime_feed(self, msg: StartRealtimeFeed):
        symbol, timeframe = msg.symbol, msg.timeframe

        stream = AsyncRealTimeData(self.ws, symbol, timeframe)

        async for bar in stream:
            if bar:
                await self.tell(
                    NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
                )

            if bar and bar.closed:
                logger.info(f"Tick: {symbol}_{timeframe}:{bar}")