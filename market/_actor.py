from typing import Union

from core.actors import BaseActor
from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.mixins import EventHandlerMixin
from core.models.ohlcv import OHLCV
from core.models.ta import TechAnalysis
from core.queries.ohlcv import TA, BackNBars, NextBar, PrevBar

MarketEvent = Union[NextBar, PrevBar, TA, BackNBars]


class MarketActor(BaseActor, EventHandlerMixin):
    def __init__(self, ts: AbstractTimeSeriesService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.ts = ts

    async def on_receive(self, event: MarketEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(NextBar, self._handle_next_bar)
        self.register_handler(PrevBar, self._handle_prev_bar)
        self.register_handler(BackNBars, self._handle_back_n_bars)
        self.register_handler(TA, self._handle_ta)

    async def _handle_next_bar(self, event: NextBar) -> OHLCV:
        return await self.ts.next_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_prev_bar(self, event: PrevBar) -> OHLCV:
        return await self.ts.prev_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_back_n_bars(self, event: BackNBars) -> OHLCV:
        return await self.ts.back_n_bars(
            event.symbol, event.timeframe, event.ohlcv, event.n
        )

    async def _handle_ta(self, event: TA) -> TechAnalysis:
        return await self.ts.ta(event.symbol, event.timeframe, event.ohlcv)
