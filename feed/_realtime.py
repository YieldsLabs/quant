import logging
from typing import List

from coral import DataSourceFactory
from core.actors import FeedActor
from core.actors.decorators import Consumer, Producer
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.models.datasource_type import DataSourceType
from core.models.entity.bar import Bar
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.wss_type import WSType
from core.tasks.feed import StartRealtimeFeed

from .streams.base import AsyncRealTimeData
from .streams.strategy import (
    KlineStreamStrategy,
    LiquidationStreamStrategy,
    OrderBookStreamStrategy,
    OrderStreamStrategy,
    PositionStreamStrategy,
)

logger = logging.getLogger(__name__)


class RealtimeActor(FeedActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        datasource: DataSourceType,
        datasource_factory: DataSourceFactory,
    ):
        super().__init__(symbol, timeframe, datasource)
        self.datasource_factory = datasource_factory
        self.depth = 50

    async def on_receive(self, msg: StartRealtimeFeed):
        await self.collector.start(msg)

    @Producer
    async def _kline_producer(self, msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.datasource_factory.create(
                msg.datasource, ProtocolType.WS, WSType.PUBLIC
            ),
            KlineStreamStrategy(self.timeframe, self.symbol),
        ) as stream:
            async for bars in stream:
                yield bars

    @Producer
    async def _ob_producer(self, msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.datasource_factory.create(
                msg.datasource, ProtocolType.WS, WSType.PUBLIC
            ),
            OrderBookStreamStrategy(self.symbol, self.depth),
        ) as stream:
            async for orders in stream:
                yield orders

    @Producer
    async def _liquidation_producer(self, msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.datasource_factory.create(
                msg.datasource, ProtocolType.WS, WSType.PUBLIC
            ),
            LiquidationStreamStrategy(self.symbol),
        ) as stream:
            async for liquidations in stream:
                yield liquidations

    @Producer
    async def _order_producer(self, msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.datasource_factory.create(
                msg.datasource, ProtocolType.WS, WSType.PRIVATE
            ),
            OrderStreamStrategy(self.symbol),
        ) as stream:
            async for order in stream:
                yield order

    @Producer
    async def _position_producer(self, msg: StartRealtimeFeed):
        async with AsyncRealTimeData(
            self.datasource_factory.create(
                msg.datasource, ProtocolType.WS, WSType.PRIVATE
            ),
            PositionStreamStrategy(self.symbol),
        ) as stream:
            async for position in stream:
                yield position

    @Consumer
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
