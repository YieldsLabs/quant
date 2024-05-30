import logging
from typing import TYPE_CHECKING, Optional

from core.actors import StrategyActor
from core.actors.policy.signal import SignalPolicy
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_signal_service import AbstractSignalService
from core.mixins import EventHandlerMixin
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.wasm_type import WasmType

if TYPE_CHECKING:
    from core.models.strategy_ref import StrategyRef

logger = logging.getLogger(__name__)


class SignalActor(StrategyActor, EventHandlerMixin):
    _EVENTS = [NewMarketDataReceived]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        wasm_type: WasmType,
        service: AbstractSignalService,
    ):
        super().__init__(symbol, timeframe)
        self._strategy = strategy
        self._wasm_type = wasm_type
        self.service = service
        self.strategy_ref: Optional[StrategyRef] = None

    @property
    def strategy(self):
        return self._strategy

    def on_start(self):
        self.service.load_instance(self._wasm_type)
        self.strategy_ref = self.service.register(self.strategy, self._wasm_type)

    def on_stop(self):
        self.strategy_ref.unregister()
        self.strategy_ref = None

    def pre_receive(self, event: NewMarketDataReceived):
        return SignalPolicy.should_process(self, event)

    async def on_receive(self, event: NewMarketDataReceived):
        signal_event = self.strategy_ref.next(
            self.symbol, self.timeframe, self.strategy, event.ohlcv
        )

        if signal_event:
            logger.debug(signal_event)

            await self.tell(signal_event)
