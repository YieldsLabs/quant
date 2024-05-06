import logging
from dataclasses import dataclass
from typing import Optional, Union

from wasmtime import Instance, Store

from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.models.action import Action
from core.models.ohlcv import OHLCV
from core.models.side import SignalSide
from core.models.signal import Signal
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
    instance_ref: Instance
    store_ref: Store

    def unregister(self):
        exports = self.instance_ref.exports(self.store_ref)
        exports["unregister_strategy"](self.store_ref, self.id)
        self.store_ref.gc()

    def next(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy, ohlcv: OHLCV
    ) -> Optional[SignalEvent]:
        exports = self.instance_ref.exports(self.store_ref)

        [raw_action, price] = exports["strategy_next"](
            self.store_ref,
            self.id,
            ohlcv.timestamp,
            ohlcv.open,
            ohlcv.high,
            ohlcv.low,
            ohlcv.close,
            ohlcv.volume,
        )

        action = Action.from_raw(raw_action)

        long_stop_loss, short_stop_loss = 0.0, 0.0

        if action in (Action.GO_LONG, Action.GO_SHORT):
            [long_stop_loss, short_stop_loss] = exports["strategy_stop_loss"](
                self.store_ref, self.id
            )

        side = (
            SignalSide.BUY
            if action in (Action.GO_LONG, Action.EXIT_SHORT)
            else SignalSide.SELL
        )

        action_event_map = {
            Action.GO_LONG: GoLongSignalReceived(
                signal=Signal(
                    symbol,
                    timeframe,
                    strategy,
                    side,
                    ohlcv,
                    entry=price,
                    stop_loss=long_stop_loss,
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
                    stop_loss=short_stop_loss,
                ),
            ),
            Action.EXIT_LONG: ExitLongSignalReceived(
                signal=Signal(
                    symbol,
                    timeframe,
                    strategy,
                    side,
                    ohlcv,
                    exit=price,
                ),
            ),
            Action.EXIT_SHORT: ExitShortSignalReceived(
                signal=Signal(
                    symbol,
                    timeframe,
                    strategy,
                    side,
                    ohlcv,
                    exit=price,
                ),
            ),
        }

        return action_event_map.get(action)
