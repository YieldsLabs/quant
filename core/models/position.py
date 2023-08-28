from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple

from .ohlcv import OHLCV
from .signal import Signal
from .order import Order

from ..interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from ..interfaces.abstract_position_take_profit_strategy import AbstractPositionTakeProfitStrategy


class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Position:
    signal: Signal
    side: PositionSide
    size: float
    entry_price: float
    risk_strategy: AbstractPositionRiskStrategy
    take_profit_strategy: AbstractPositionTakeProfitStrategy
    orders: Tuple[Order] = ()
    closed: bool = False
    stop_loss_price: Optional[float] = None
    take_profit_price: Optional[float] = field(init=False)
    open_timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    closed_timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    last_modified: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    exit_price: float = field(default_factory=lambda: 0.0001)

    @property
    def closed_key(self) -> str:
        return f"{self.signal}_{self.side}_{self.closed_timestamp}"
    
    @property
    def trade_time(self) -> int:
        return int(self.closed_timestamp - self.open_timestamp)

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        if self.side == PositionSide.LONG:
            pnl = (self.exit_price - self.entry_price) * self.size
        elif self.side == PositionSide.SHORT:
            pnl = (self.entry_price - self.exit_price) * self.size

        return pnl

    def add_order(self, order: Order) -> 'Position':
        return replace(
            self,
            orders=self.orders + (order,),
            last_modified=int(datetime.now().timestamp())
        )

    def close(self) -> 'Position':
        if self.closed:
            return self

        return replace(
            self, 
            closed=True,
            last_modified=int(datetime.now().timestamp()),
            closed_timestamp=int(datetime.now().timestamp()),
        )

    def update_prices(self, execution_price: float) -> 'Position':
        last_modified = int(datetime.now().timestamp())
        
        if not self.closed:
            return replace(
                self,
                entry_price=execution_price,
                last_modified=last_modified
            )
        else:
            return replace(
                self,
                exit_price=execution_price,
                last_modified=last_modified
            )
        
    
    def next(self, ohlcv: OHLCV) -> 'Position':
        # next_stop_loss = self.risk_strategy.next(self.side, self.entry_price, self.stop_loss_price, ohlcv)
        
        return replace(
            self,
            stop_loss_price = self.stop_loss_price
        )
    
    def __post_init__(self):
        if self.stop_loss_price:
            object.__setattr__(self, 'take_profit_price', self.take_profit_strategy.next(self.entry_price, self.stop_loss_price))
    