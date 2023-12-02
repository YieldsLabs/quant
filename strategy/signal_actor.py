import logging
from typing import TYPE_CHECKING, Optional

from core.actors.base import BaseActor
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_signal_service import AbstractSignalService
from core.models.strategy import Strategy
from core.models.timeframe import Timeframe

if TYPE_CHECKING:
    from core.models.strategy_ref import StrategyRef

logger = logging.getLogger(__name__)


class SignalActor(BaseActor):
    def __init__(
        self,
        symbol: str,
        timeframe: Timeframe,
        strategy: Strategy,
        service: AbstractSignalService,
    ):
        super().__init__(symbol, timeframe, strategy)

        self.strategy_ref: Optional[StrategyRef] = None
        self.service = service

    async def start(self):
        await super().start()

        self._register_strategy()

        self._dispatcher.register(
            NewMarketDataReceived, self.handle, self._filter_events
        )

    async def stop(self):
        await super().stop()

        self._unregister_strategy()

        self._dispatcher.unregister(NewMarketDataReceived, self.handle)

    async def handle(self, event: NewMarketDataReceived):
        if not await self.running:
            return

        event = self.strategy_ref.next(
            self._symbol, self._timeframe, self._strategy, event.ohlcv
        )

        if event:
            await self.dispatch(event)

    def _register_strategy(self):
        self.strategy_ref = self.service.register(self._strategy)

    def _unregister_strategy(self):
        self.strategy_ref.unregister()
        self.strategy_ref = None

    def _filter_events(self, event: NewMarketDataReceived):
        return (
            event.symbol == self._symbol
            and event.timeframe == self._timeframe
            and event.closed
        )
