import logging
import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import List, Optional, Tuple

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .position_risk import PositionRisk
from .profit_target import ProfitTarget
from .risk_type import PositionRiskType, SessionRiskType
from .side import PositionSide, SignalSide
from .signal import Signal
from .signal_risk import SignalRisk
from .ta import TechAnalysis

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Position:
    initial_size: float
    signal: Signal
    signal_risk: SignalRisk
    position_risk: PositionRisk
    profit_target: ProfitTarget
    orders: Tuple[Order] = ()
    expiration: int = field(default_factory=lambda: 900000)  # 15min
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _tp: Optional[float] = None
    _sl: Optional[float] = None

    @property
    def side(self) -> PositionSide:
        if self.signal.side == SignalSide.BUY:
            return PositionSide.LONG

        if self.signal.side == SignalSide.SELL:
            return PositionSide.SHORT

    @property
    def take_profit(self) -> float:
        p = self.signal.symbol.price_precision

        if self._tp:
            return round(self._tp, p)

        if self.signal_risk.tp:
            if (
                self.side == PositionSide.LONG
                and self.signal_risk.tp > self.stop_loss
                and self.signal_risk.tp <= self.profit_target.last
            ) or (
                self.side == PositionSide.SHORT
                and self.signal_risk.tp < self.stop_loss
                and self.signal_risk.tp >= self.profit_target.last
            ):
                return round(self.signal_risk.tp, p)

        return round(self.profit_target.last, p)

    @property
    def stop_loss(self) -> float:
        p = self.signal.symbol.price_precision

        if self._sl:
            return round(self._sl, p)

        return round(self.signal.stop_loss, p)

    @property
    def open_timestamp(self) -> int:
        return self.signal.ohlcv.timestamp

    @property
    def close_timestamp(self) -> int:
        return self.position_risk.curr_bar.timestamp

    @property
    def signal_bar(self) -> OHLCV:
        return self.signal.ohlcv

    @property
    def risk_bar(self) -> OHLCV:
        return self.position_risk.curr_bar

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
        return self.position_risk.type != PositionRiskType.NONE

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

        factor = -1.0 if self.side == PositionSide.SHORT else 1
        pnl = factor * (self.exit_price - self.entry_price) * self.size

        return pnl

    @property
    def curr_pnl(self) -> float:
        factor = -1.0 if self.side == PositionSide.SHORT else 1
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
        pr = self.signal.symbol.price_precision

        return round((last_bar.high + last_bar.low + 2.0 * last_bar.close) / 4, pr)

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
        price = self.position_risk.exit_price(
            self.side, self.take_profit, self.stop_loss
        )

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

    def next(
        self, ohlcv: OHLCV, ta: TechAnalysis, session_risk: SessionRiskType
    ) -> "Position":
        if self.closed or ohlcv.timestamp <= self.risk_bar.timestamp:
            return self

        gap = ohlcv.timestamp - self.risk_bar.timestamp
        pnl_perc = (self.curr_pnl / self.curr_price) * 100

        next_risk = self.position_risk.next(ohlcv)
        next_position = replace(self, position_risk=next_risk)

        next_position = next_position.break_even()

        if (
            self.side == PositionSide.LONG
            and self.curr_price > self.profit_target.first
        ) or (
            self.side == PositionSide.SHORT
            and self.curr_price < self.profit_target.first
        ):
            next_position = next_position.trail(ta)

        if session_risk == SessionRiskType.EXIT and pnl_perc <= 0.0:
            next_position = next_position.trail(ta)

        next_tp = next_position.take_profit
        next_sl = next_position.stop_loss
        dstp = abs(self.curr_price - self.take_profit)

        if session_risk == SessionRiskType.EXIT:
            if self.curr_pnl > 2.5 * self.fee:
                print(
                    f"TRAILLL prev TP: {next_position.take_profit}, prev SL: {next_position.stop_loss}"
                )
                next_tp = next_risk.tp_low(self.side, ta, dstp, next_tp)
                print(f"TRAILLL next TP: {next_tp}, next SL: {next_sl}")

        next_risk = next_risk.assess(
            self.side,
            next_tp,
            next_sl,
            self.open_timestamp,
            self.expiration,
        )

        logger.info(
            f"SIDE: {self.side}, TS: {ohlcv.timestamp}, GAP: {gap}ms, ENTRY: {self.entry_price}, SL: {self.stop_loss}, TP: {self.take_profit}, PnL%: {pnl_perc}, BREAK EVEN: {self.has_break_even}"
        )

        return replace(
            next_position,
            position_risk=next_risk,
            _tp=next_tp,
            _sl=next_sl,
            last_modified=datetime.now().timestamp(),
        )

    def break_even(self) -> "Position":
        curr_price = self.curr_price
        curr_sl = self.stop_loss

        if self.side == PositionSide.LONG:
            if curr_price > self.profit_target.first:
                curr_sl = min(curr_sl, self.entry_price)

            if curr_price > self.profit_target.second:
                curr_sl = min(curr_sl, self.profit_target.first)

            if curr_price > self.profit_target.third:
                curr_sl = min(curr_sl, self.profit_target.second)

            if curr_price > self.profit_target.fourth:
                curr_sl = min(curr_sl, self.profit_target.third)

        if self.side == PositionSide.SHORT:
            if curr_price < self.profit_target.first:
                curr_sl = max(curr_sl, self.entry_price)

            if curr_price < self.profit_target.second:
                curr_sl = max(curr_sl, self.profit_target.first)

            if curr_price < self.profit_target.third:
                curr_sl = max(curr_sl, self.profit_target.second)

            if curr_price < self.profit_target.fourth:
                curr_sl = max(curr_sl, self.profit_target.third)

        return replace(self, _sl=curr_sl, last_modified=datetime.now().timestamp())

    def trail(self, ta: TechAnalysis) -> "Position":
        prev_sl = self.stop_loss
        next_sl = self.position_risk.sl_ats(self.side, ta, self.stop_loss)

        logger.info(
            f"<---- &&&&&&TRAIL&&&&& -->>> prevSL: {prev_sl}, nextSL: {next_sl}"
        )

        return replace(self, _sl=next_sl, last_modified=datetime.now().timestamp())

    def theo_taker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.taker_fee

    def theo_maker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.maker_fee

    def take_profit_level(self, factor: float):
        entry_price = self.entry_price
        stop_loss = self.signal.stop_loss
        dist = factor * abs(entry_price - stop_loss)
        dist = round(dist, self.signal.symbol.price_precision)

        if self.side == PositionSide.LONG:
            return entry_price + dist
        if self.side == PositionSide.SHORT:
            return entry_price - dist

    @staticmethod
    def _average_size(orders: List[Order]) -> float:
        total_size = sum(order.size for order in orders)
        return total_size / len(orders) if orders else 0.0

    @staticmethod
    def _average_price(orders: List[Order]) -> float:
        total_price = sum(order.price for order in orders)
        return total_price / len(orders) if orders else 0.0

    def to_dict(self):
        return {
            "signal": self.signal.to_dict(),
            "signal_risk": self.signal_risk.to_dict(),
            "position_risk": self.position_risk.to_dict(),
            "profit_target": self.profit_target.to_dict(),
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
        }

    def __str__(self):
        return f"signal={self.signal}, signal_risk={self.signal_risk.type}, position_risk={self.position_risk.type}, open_ohlcv={self.signal_bar}, close_ohlcv={self.risk_bar}, side={self.side}, size={self.size}, entry_price={self.entry_price}, exit_price={self.exit_price}, tp={self.take_profit}, sl={self.stop_loss}, pnl={self.pnl}, trade_time={self.trade_time}, closed={self.closed}, valid={self.is_valid}, break_even={self.has_break_even}"

    def __repr__(self):
        return f"Position({self})"
