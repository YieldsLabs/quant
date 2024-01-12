from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.interfaces.abstract_position_size_strategy import AbstractPositionSizeStrategy
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)
from core.models.ohlcv import OHLCV
from core.models.position import Position, PositionSide
from core.models.signal import Signal, SignalSide


class PositionFactory(AbstractPositionFactory):
    def __init__(
        self,
        position_size_strategy: AbstractPositionSizeStrategy,
        risk_strategy: AbstractPositionRiskStrategy,
        take_profit_strategy: AbstractPositionTakeProfitStrategy,
    ):
        super().__init__()
        self.position_size_strategy = position_size_strategy
        self.risk_strategy = risk_strategy
        self.take_profit_strategy = take_profit_strategy

    async def create_position(
        self,
        signal: Signal,
        ohlcv: OHLCV,
        entry_price: float,
        stop_loss_price: float | None,
    ) -> Position:
        symbol = signal.symbol

        stop_loss_price = (
            round(stop_loss_price, symbol.price_precision) if stop_loss_price else None
        )
        entry_price = round(entry_price, symbol.price_precision)

        take_profit_price = self.take_profit_strategy.next(entry_price, stop_loss_price)

        position_size = await self.position_size_strategy.calculate(
            signal, entry_price, stop_loss_price
        )

        adjusted_position_size = max(position_size, symbol.min_position_size)
        rounded_position_size = round(adjusted_position_size, symbol.position_precision)

        position_side = (
            PositionSide.LONG if signal.side == SignalSide.BUY else PositionSide.SHORT
        )

        return Position(
            signal,
            position_side,
            rounded_position_size,
            entry_price,
            self.risk_strategy,
            open_timestamp=ohlcv.timestamp,
            take_profit_price=take_profit_price,
            stop_loss_price=stop_loss_price,
        )
