import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from functools import cached_property
from typing import List, Optional, Tuple

import numpy as np

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .risk import Risk
from .risk_type import RiskType
from .side import PositionSide, SignalSide
from .signal import Signal


@dataclass(frozen=True)
class Position:
    initial_size: float
    signal: Signal
    risk: Risk
    orders: Tuple[Order] = ()
    expiration: int = field(default_factory=lambda: 900000)  # 15min
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_factor: float = field(default_factory=lambda: np.random.uniform(0.13, 0.3))
    second_factor: float = field(default_factory=lambda: np.random.uniform(0.32, 0.5))
    third_factor: float = field(default_factory=lambda: np.random.uniform(0.55, 1.0))
    trailed: bool = False
    _tp: Optional[int] = None
    _sl: Optional[int] = None

    @property
    def side(self) -> PositionSide:
        if self.signal.side == SignalSide.BUY:
            return PositionSide.LONG

        if self.signal.side == SignalSide.SELL:
            return PositionSide.SHORT

    @cached_property
    def first_take_profit(self):
        p = self.signal.symbol.price_precision
        entry_price = self.entry_price
        stop_loss = self.signal.stop_loss
        dist = self.first_factor * abs(entry_price - stop_loss)
        dist = round(dist, p)

        if self.side == PositionSide.LONG:
            return entry_price + dist
        if self.side == PositionSide.SHORT:
            return entry_price - dist

    @cached_property
    def second_take_profit(self):
        p = self.signal.symbol.price_precision
        entry_price = self.entry_price
        stop_loss = self.signal.stop_loss
        dist = self.second_factor * abs(entry_price - stop_loss)
        dist = round(dist, p)

        if self.side == PositionSide.LONG:
            return entry_price + dist
        if self.side == PositionSide.SHORT:
            return entry_price - dist

    @cached_property
    def third_take_profit(self):
        p = self.signal.symbol.price_precision
        entry_price = self.entry_price
        stop_loss = self.signal.stop_loss
        dist = self.third_factor * abs(entry_price - stop_loss)
        dist = round(dist, p)

        if self.side == PositionSide.LONG:
            return entry_price + dist
        if self.side == PositionSide.SHORT:
            return entry_price - dist

    @property
    def take_profit(self) -> float:
        p = self.signal.symbol.price_precision
        tp = self.second_take_profit if not self._tp else self._tp
        return round(tp, p)

    @property
    def stop_loss(self) -> float:
        p = self.signal.symbol.price_precision
        sl = self.signal.stop_loss if not self._sl else self._sl
        return round(sl, p)

    @property
    def open_timestamp(self) -> int:
        return self.signal.ohlcv.timestamp

    @property
    def close_timestamp(self) -> int:
        return self.risk.last_bar.timestamp

    @property
    def signal_bar(self) -> OHLCV:
        return self.signal.ohlcv

    @property
    def risk_bar(self) -> OHLCV:
        return self.risk.last_bar

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

        order_diff = self._average_size(self.open_orders) - self._average_size(
            self.closed_orders
        )

        return order_diff <= 0

    @property
    def has_break_even(self) -> bool:
        if self.side == PositionSide.LONG:
            return self.stop_loss >= self.entry_price
        if self.side == PositionSide.SHORT:
            return self.stop_loss <= self.entry_price

        return False

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
    def curr_pnl(self) -> float:
        factor = -1 if self.side == PositionSide.SHORT else 1
        pnl = factor * (self.curr_price - self.entry_price) * self.size

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
    def curr_price(self) -> float:
        last_bar = self.risk_bar
        p = self.signal.symbol.price_precision

        return round((last_bar.high + last_bar.low + last_bar.close) / 3, p)

    @property
    def is_valid(self) -> bool:
        if self.closed:
            return self.size != 0 and self.open_timestamp < self.close_timestamp

        if self.side == PositionSide.LONG:
            return self.take_profit > self.stop_loss

        if self.side == PositionSide.SHORT:
            return self.take_profit < self.stop_loss

        return False

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
        size = self._average_size(self.open_orders) - self._average_size(
            self.closed_orders
        )
        price = self.risk.exit_price(self.side, self.take_profit, self.stop_loss)

        return Order(
            status=OrderStatus.PENDING,
            price=price,
            size=size,
        )

    def fill_order(self, order: Order) -> "Position":
        if self.closed:
            return self

        if order.status == OrderStatus.PENDING:
            return self

        execution_time = datetime.now().timestamp()

        orders = (*self.orders, order)

        if order.status == OrderStatus.EXECUTED:
            return replace(
                self,
                orders=orders,
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

        gap = ohlcv.timestamp - self.risk_bar.timestamp

        print(f"SIDE: {self.side}, TS: {ohlcv.timestamp}, GAP: {gap}")

        next_position = replace(self, risk=self.risk.next(ohlcv))
        next_sl = self.stop_loss
        next_tp = self.take_profit

        next_tp = next_position.risk.tp_low(self.side, self.take_profit)
        next_sl = next_position.risk.sl_low(self.side, self.stop_loss)

        next_risk = next_position.risk.assess(
            self.side,
            next_tp,
            next_sl,
            self.open_timestamp,
            self.expiration,
        )

        print(f"RISK: {next_risk}, TP: {next_tp}, SL: {next_sl}, PnL: {self.curr_pnl}")

        return replace(
            next_position,
            risk=next_risk,
            _tp=next_tp,
            _sl=next_sl,
        )

    def break_even(self) -> float:
        curr_price = self.curr_price
        curr_sl = self.stop_loss

        first_break_even = self.first_take_profit
        second_break_even = self.second_take_profit
        third_break_even = self.third_take_profit

        if self.side == PositionSide.LONG:
            if curr_price >= first_break_even:
                curr_sl = max(curr_sl, self.entry_price)

            if curr_price >= second_break_even:
                curr_sl = max(curr_sl, first_break_even)

            if curr_price >= third_break_even:
                curr_sl = max(curr_sl, second_break_even)

        if self.side == PositionSide.SHORT:
            if curr_price <= first_break_even:
                curr_sl = min(curr_sl, self.entry_price)

            if curr_price <= second_break_even:
                curr_sl = min(curr_sl, first_break_even)

            if curr_price <= third_break_even:
                curr_sl = min(curr_sl, second_break_even)

        return curr_sl


    def force_exit(self, price: float) -> "Position":
        if self.side == PositionSide.LONG and price > self.entry_price:
            return replace(self, _tp=price)

        if self.side == PositionSide.SHORT and price < self.entry_price:
            return replace(self, _tp=price)

        return self

    def trail(self, price: Optional[float] = None) -> "Position":
        if self.trailed:
            return self

        if not price:
            return replace(self, trailed=True)

        if self.side == PositionSide.LONG and price > self.first_take_profit:
            return replace(self, _tp=price, trailed=True)

        if self.side == PositionSide.SHORT and price < self.first_take_profit:
            return replace(self, _tp=price, trailed=True)

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
            "break_even": self.has_break_even,
            "ff": self.first_factor,
            "sf": self.second_factor,
            "tf": self.third_factor,
            "ft": self.first_take_profit,
            "st": self.second_take_profit,
            "tt": self.third_take_profit,
            "trailed": self.trailed,
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
        return f"Position(signal={self.signal}, risk={self.risk.type}, open_ohlcv={self.signal_bar}, close_ohlcv={self.risk_bar}, side={self.side}, size={self.size}, entry_price={self.entry_price}, exit_price={self.exit_price}, tp={self.take_profit}, sl={self.stop_loss}, pnl={self.pnl}, trade_time={self.trade_time}, closed={self.closed}, valid={self.is_valid})"
