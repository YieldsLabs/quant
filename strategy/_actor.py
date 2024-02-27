import logging
from typing import TYPE_CHECKING, Optional

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_signal_service import AbstractSignalService
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

if TYPE_CHECKING:
    from core.models.strategy_ref import StrategyRef

logger = logging.getLogger(__name__)


class SignalActor(Actor):
    _EVENTS = [NewMarketDataReceived]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        service: AbstractSignalService,
    ):
        super().__init__(symbol, timeframe)

        self.strategy_ref: Optional[StrategyRef] = None
        self.service = service
        self._strategy = strategy

    def on_start(self):
        self.strategy_ref = self.service.register(self._strategy)

    def on_stop(self):
        self.strategy_ref.unregister()
        self.strategy_ref = None

    def pre_receive(self, event: NewMarketDataReceived):
        return (
            event.symbol == self._symbol
            and event.timeframe == self._timeframe
            and event.closed
        )

    async def on_receive(self, event: NewMarketDataReceived):
        signal_event = self.strategy_ref.next(
            self._symbol, self._timeframe, self._strategy, event.ohlcv
        )

        if signal_event:
            await self.tell(signal_event)
