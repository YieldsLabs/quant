import logging
from typing import List

from coral import DataSourceFactory
from core.actors import FeedActor
from core.actors.decorators import Consumer, Producer
from core.commands.market import IngestMarketData
from core.events.market import NewMarketDataReceived, NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.entity.bar import Bar
from core.models.entity.order import Order
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
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe, datasource)
        self.datasource_factory = datasource_factory
        self.config = config_service.get("feed")

    async def on_receive(self, msg: StartRealtimeFeed):
        await self.collector.start(msg)
        await self.collector.wait_for_completion()

    @Producer
    async def _kline_producer(self, msg: StartRealtimeFeed):
        async for bars in self._stream_producer(
            KlineStreamStrategy(self.timeframe, self.symbol),
            ProtocolType.WS,
            WSType.PUBLIC,
            msg,
        ):
            yield bars

    @Producer
    async def _ob_producer(self, msg: StartRealtimeFeed):
        async for orders in self._stream_producer(
            OrderBookStreamStrategy(self.symbol, self.config.get("dom", 15)),
            ProtocolType.WS,
            WSType.PUBLIC,
            msg,
        ):
            yield orders

    @Producer
    async def _liquidation_producer(self, msg: StartRealtimeFeed):
        async for liquidations in self._stream_producer(
            LiquidationStreamStrategy(self.symbol),
            ProtocolType.WS,
            WSType.PUBLIC,
            msg,
        ):
            yield liquidations

    @Producer
    async def _order_producer(self, msg: StartRealtimeFeed):
        async for order in self._stream_producer(
            OrderStreamStrategy(self.symbol),
            ProtocolType.WS,
            WSType.PRIVATE,
            msg,
        ):
            yield order

    @Producer
    async def _position_producer(self, msg: StartRealtimeFeed):
        async for position in self._stream_producer(
            PositionStreamStrategy(self.symbol),
            ProtocolType.WS,
            WSType.PRIVATE,
            msg,
        ):
            yield position

    @Consumer
    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_bars(data)

            case [Order(), *_]:
                await self._process_orders(data)

    async def _process_bars(self, bars: List[Bar]):
        for bar in bars:
            await self.ask(
                IngestMarketData(self.symbol, self.timeframe, self.datasource, bar)
            )
            await self.tell(
                NewMarketDataReceived(self.symbol, self.timeframe, self.datasource, bar)
            )

            if bar.closed:
                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")

    async def _process_orders(self, orders: List[Order]):
        for order in orders:
            await self.tell(
                NewMarketOrderReceived(
                    self.symbol, self.timeframe, self.datasource, order
                )
            )
            logger.info(f"{self.symbol}_{self.timeframe}:{order}")

    async def _stream_producer(self, strategy, protocol_type, ws_type, msg):
        async with AsyncRealTimeData(
            self.datasource_factory.create(msg.datasource, protocol_type, ws_type),
            strategy,
        ) as stream:
            async for data in stream:
                yield data
