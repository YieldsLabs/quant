import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import List, Tuple

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .risk import Risk
from .risk_type import RiskType
from .side import PositionSide, SignalSide
from .signal import Signal


@dataclass(frozen=True)
class Position:
    signal: Signal
    risk: Risk
    initial_size: float
    orders: Tuple[Order] = ()
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def side(self) -> PositionSide:
        if self.signal.side == SignalSide.BUY:
            return PositionSide.LONG

        if self.signal.side == SignalSide.SELL:
            return PositionSide.SHORT

    @property
    def take_profit(self) -> float:
        return self.risk.take_profit_price

    @property
    def stop_loss(self) -> float:
        return self.risk.stop_loss_price

    @property
    def open_timestamp(self) -> int:
        return self.signal.ohlcv.timestamp

    @property
    def close_timestamp(self) -> int:
        return self.risk.ohlcv.timestamp

    @property
    def signal_bar(self) -> OHLCV:
        return self.signal.ohlcv

    @property
    def risk_bar(self) -> OHLCV:
        return self.risk.ohlcv

    @property
    def trade_time(self) -> int:
        return abs(self.close_timestamp - self.open_timestamp)

    @property
    def closed(self) -> bool:
        if not self.orders:
            return False

        if self.rejected_orders:
            return True

        if not self.closed_orders:
            return False

        return len(self.closed_orders) >= len(self.open_orders)

    @property
    def has_risk(self) -> bool:
        return self.risk.type != RiskType.NONE

    @property
    def adj_count(self) -> int:
        return max(
            0,
            len(self.open_orders) - 1,
        )

    @property
    def size(self) -> float:
        if self.closed_orders:
            return self._average_size(self.closed_orders)

        if self.open_orders:
            return self._average_size(self.open_orders)

        return 0.0

    @property
    def open_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.EXECUTED]

    @property
    def closed_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.CLOSED]

    @property
    def rejected_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.FAILED]

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        factor = -1 if self.side == PositionSide.SHORT else 1
        pnl = factor * (self.exit_price - self.entry_price) * self.size

        return pnl

    @property
    def fee(self) -> float:
        return sum([order.fee for order in self.open_orders]) + sum(
            [order.fee for order in self.closed_orders]
        )

    @property
    def entry_price(self) -> float:
        return self._average_price(self.open_orders)

    @property
    def exit_price(self) -> float:
        return self._average_price(self.closed_orders)

    @property
    def is_valid(self) -> bool:
        if self.closed:
            return self.size != 0 and self.open_timestamp < self.close_timestamp

        if self.side == PositionSide.LONG:
            return self.take_profit > self.stop_loss

        if self.side == PositionSide.SHORT:
            return self.take_profit < self.stop_loss

        return False

    @classmethod
    def from_signal(
        cls,
        signal: Signal,
        initial_size: float,
        expiration: float,
    ) -> "Position":
        risk = Risk(
            ohlcv=signal.ohlcv,
            stop_loss_price=signal.stop_loss,
            expiration=expiration,
        )

        return cls(signal=signal, risk=risk, initial_size=initial_size)

    def entry_order(self) -> Order:
        price = round(self.signal.entry, self.signal.symbol.price_precision)
        size = round(
            max(self.initial_size, self.signal.symbol.min_position_size),
            self.signal.symbol.position_precision,
        )

        return Order(
            status=OrderStatus.PENDING,
            price=price,
            size=size,
        )

    def exit_order(self) -> Order:
        price = self.risk.exit_price(self.side)

        return Order(
            status=OrderStatus.PENDING,
            price=price,
            size=self.size,
        )

    def fill_order(self, order: Order) -> "Position":
        if self.closed:
            return self

        if order.status == OrderStatus.PENDING:
            return self

        execution_time = datetime.now().timestamp()

        orders = (*self.orders, order)

        if order.status == OrderStatus.EXECUTED:
            risk = self.risk.target(self.side, order.price)

            return replace(
                self,
                orders=orders,
                risk=risk,
                last_modified=execution_time,
            )

        if order.status == OrderStatus.CLOSED:
            return replace(
                self,
                orders=orders,
                last_modified=execution_time,
            )

        if order.status == OrderStatus.FAILED:
            return replace(
                self,
                orders=orders,
                last_modified=execution_time,
            )

    def next(self, ohlcv: OHLCV) -> "Position":
        if self.closed:
            return self

        if ohlcv.timestamp <= self.risk_bar.timestamp:
            return self

        gap = ohlcv.timestamp - self.risk.ohlcv.timestamp

        print(f"SIDE: {self.side}, TS: {ohlcv.timestamp}, GAP: {gap}")

        risk = self.risk.assess(
            self.side,
            self.open_timestamp,
            ohlcv,
        )

        # print(f"RISK: {risk}")

        return replace(
            self,
            risk=risk,
        )

    def trail(self, entry_price: float) -> "Position":
        return replace(self, risk=self.risk.trail(self.side, entry_price))

    def theo_taker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.taker_fee

    def theo_maker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.maker_fee

    def to_dict(self):
        return {
            "signal": self.signal.to_dict(),
            "risk": self.risk.to_dict(),
            "side": str(self.side),
            "size": self.size,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "closed": self.closed,
            "valid": self.is_valid,
            "pnl": self.pnl,
            "fee": self.fee,
            "take_profit": self.take_profit,
            "stop_loss": self.stop_loss,
            "trade_time": self.trade_time,
        }

    @staticmethod
    def _average_size(orders: List[Order]) -> float:
        total_size = sum(order.size for order in orders)
        return total_size / len(orders) if orders else 0.0

    @staticmethod
    def _average_price(orders: List[Order]) -> float:
        total_price = sum(order.price for order in orders)
        return total_price / len(orders) if orders else 0.0

    def __str__(self):
        return f"Position(signal={self.signal}, open_ohlcv={self.signal.ohlcv}, close_ohlcv={self.risk.ohlcv}, side={self.side}, size={self.size}, entry_price={self.entry_price}, tp={self.take_profit}, sl={self.stop_loss}, exit_price={self.exit_price}, trade_time={self.trade_time}, closed={self.closed}, valid={self.is_valid})"
