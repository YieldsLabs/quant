import logging
import typing
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Union

if typing.TYPE_CHECKING:
    from wasmtime import Instance, Store

from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.models.action import Action
from core.models.entity.ohlcv import OHLCV
from core.models.entity.signal import Signal
from core.models.side import SignalSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

SignalEvent = Union[
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StrategyRef:
    id: int
    instance_ref: "Instance"
    store_ref: "Store"

    @cached_property
    def exports(self):
        return self.instance_ref.exports(self.store_ref)

    def unregister(self):
        self.exports["strategy_unregister"](self.store_ref, self.id)
        self.store_ref.gc()

    def next(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy, ohlcv: OHLCV
    ) -> Optional[SignalEvent]:
        strategy_args = [
            self.store_ref,
            self.id,
            ohlcv.timestamp,
            ohlcv.open,
            ohlcv.high,
            ohlcv.low,
            ohlcv.close,
            ohlcv.volume,
        ]

        raw_action, price = self.exports["strategy_next"](*strategy_args)

        action = Action.from_raw(raw_action)

        side = SignalSide.BUY if action in Action.GO_LONG else SignalSide.SELL

        action_event_map = {
            Action.GO_LONG: GoLongSignalReceived(
                signal=Signal(
                    symbol,
                    timeframe,
                    strategy,
                    side,
                    ohlcv,
                    entry=price,
                ),
            ),
            Action.GO_SHORT: GoShortSignalReceived(
                signal=Signal(
                    symbol,
                    timeframe,
                    strategy,
                    side,
                    ohlcv,
                    entry=price,
                ),
            ),
        }

        return action_event_map.get(action)
