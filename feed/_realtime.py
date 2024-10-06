import asyncio
import logging
from typing import List

from core.actors import StrategyActor
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.tasks.feed import StartRealtimeFeed

from .streams.base import AsyncRealTimeData
from .streams.collector import DataCollector
from .streams.strategy.kline import KlineStreamStrategy

logger = logging.getLogger(__name__)


class RealtimeActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        ws: AbstractWS,
    ):
        super().__init__(symbol, timeframe)
        self.ws = ws
        self.collector = DataCollector()

        self.collector.add_producer(self._kline_producer)
        self.collector.add_consumer(self._consumer)

    def on_stop(self):
        asyncio.run(self.collector.stop())

    async def on_receive(self, msg: StartRealtimeFeed):
        await self.collector.start(msg)

    async def _kline_producer(self, _msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.ws, KlineStreamStrategy(self.ws, self.timeframe, self.symbol)
        ) as stream:
            async for bars in stream:
                yield bars

    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_bars(data)

    async def _process_bars(self, bars: List[Bar]):
        for bar in bars:
            await self.ask(IngestMarketData(self.symbol, self.timeframe, bar))
            await self.tell(NewMarketDataReceived(self.symbol, self.timeframe, bar))

            if bar.closed:
                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")
