import asyncio

from core.actors import Actor
from core.commands.feed import StartHistoricalFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.bar import Bar
from core.models.lookback import Lookback
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AsyncHistoricalData:
    def __init__(
        self,
        exchange: AbstractExchange,
        symbol: Symbol,
        timeframe: Timeframe,
        in_sample: Lookback,
        out_sample: Lookback,
        batch_size: int,
    ):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.in_sample = in_sample
        self.out_sample = out_sample
        self.batch_size = batch_size
        self.iterator = None
        self.sentinel = object()
        self.last_row = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._init_iterator()

        next_item = await self._fetch_next_item()
        if next_item is self.sentinel:
            raise StopAsyncIteration

        self.last_row = next_item
        return next_item

    def _init_iterator(self) -> None:
        if self.iterator is None:
            self.iterator = self.exchange.fetch_ohlcv(
                self.symbol,
                self.timeframe,
                self.in_sample,
                self.out_sample,
                self.batch_size,
            )

    async def _fetch_next_item(self):
        return await asyncio.to_thread(self._next_item_or_end)

    def _next_item_or_end(self):
        try:
            return Bar(OHLCV.from_list(next(self.iterator)), True)
        except StopIteration:
            return self.sentinel

    def get_last_bar(self):
        return self.last_row


class HistoricalActor(Actor):
    _EVENTS = [StartHistoricalFeed]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        exchange: AbstractExchange,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.exchange = exchange
        self.config_service = config_service.get("backtest")
        self.last_bar = None

    def pre_receive(self, msg: StartHistoricalFeed):
        return self._symbol == msg.symbol and self._timeframe == msg.timeframe

    async def on_receive(self, msg: StartHistoricalFeed):
        symbol, timeframe = msg.symbol, msg.timeframe

        stream = AsyncHistoricalData(
            self.exchange,
            symbol,
            timeframe,
            msg.in_sample,
            msg.out_sample,
            self.config_service["batch_size"],
        )

        async for bar in stream:
            await self.tell(
                NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
            )

        self.last_bar = stream.get_last_bar()
