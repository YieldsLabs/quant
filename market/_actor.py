from typing import Union

from core.actors import BaseActor
from core.commands.market import IngestMarketData
from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.mixins import EventHandlerMixin
from core.models.entity.ohlcv import OHLCV
from core.models.ta import TechAnalysis
from core.queries.ohlcv import TA, BackNBars, BatchBars, NextBar, PrevBar

MarketEvent = Union[IngestMarketData, NextBar, PrevBar, TA, BackNBars, BatchBars]


class MarketActor(BaseActor, EventHandlerMixin):
    def __init__(self, ts: AbstractTimeSeriesService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.ts = ts

    async def on_receive(self, event: MarketEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(IngestMarketData, self._ingest_market_data)
        self.register_handler(NextBar, self._handle_next_bar)
        self.register_handler(PrevBar, self._handle_prev_bar)
        self.register_handler(BatchBars, self._handle_batch_bars)
        self.register_handler(BackNBars, self._handle_back_n_bars)
        self.register_handler(TA, self._handle_ta)

    async def _ingest_market_data(self, event: IngestMarketData) -> None:
        if event.bar.closed:
            await self.ts.upsert(event.symbol, event.timeframe, event.bar.ohlcv)

    async def _handle_next_bar(self, event: NextBar) -> OHLCV:
        return await self.ts.next_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_prev_bar(self, event: PrevBar) -> OHLCV:
        return await self.ts.prev_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_batch_bars(self, event: BatchBars) -> list[OHLCV]:
        prev_bar = event.ohlcv
        n_bars = int(event.n)
        bars = [prev_bar]

        for _ in range(n_bars - 1):
            next_bar = await self.ts.next_bar(event.symbol, event.timeframe, prev_bar)

            if next_bar is None:
                break

            bars.append(next_bar)
            prev_bar = next_bar

        bars = sorted(bars, key=lambda x: x.timestamp)

        while len(bars) < n_bars:
            first_valid_bar = bars[0]
            prev_bar = await self.ts.prev_bar(
                event.symbol, event.timeframe, first_valid_bar
            )

            if prev_bar is None:
                break

            bars.insert(0, prev_bar)

        bars = sorted(bars, key=lambda x: x.timestamp)

        return bars

    async def _handle_back_n_bars(self, event: BackNBars) -> OHLCV:
        return await self.ts.back_n_bars(
            event.symbol, event.timeframe, event.ohlcv, event.n
        )

    async def _handle_ta(self, event: TA) -> TechAnalysis:
        return await self.ts.ta(event.symbol, event.timeframe, event.ohlcv)
