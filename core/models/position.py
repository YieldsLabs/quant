import logging
import uuid
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import List, Optional, Tuple

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .position_risk import PositionRisk
from .profit_target import ProfitTarget
from .risk_type import PositionRiskType, SessionRiskType, SignalRiskType
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
        if self._tp:
            return self._tp

        return self.profit_target.last

    @property
    def stop_loss(self) -> float:
        if self._sl:
            return self._sl

        return self.signal.stop_loss

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
            return self.stop_loss > self.entry_price
        if self.side == PositionSide.SHORT:
            return self.stop_loss < self.entry_price

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

        return (last_bar.close + last_bar.high + last_bar.low) / 3.0

    @property
    def curr_target(self) -> float:
        targets = self.profit_target.targets
        curr_price = self.curr_price
        idx = 0

        if self.side == PositionSide.LONG:
            for i, target in enumerate(targets):
                if curr_price > target:
                    idx = i
                    break

        elif self.side == PositionSide.SHORT:
            for i, target in enumerate(targets):
                if curr_price < target:
                    idx = i
                    break

        return targets[idx]

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
                profit_target=replace(self.profit_target, entry=order.price),
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
            print("Wrong update")
            return self

        gap = ohlcv.timestamp - self.risk_bar.timestamp

        if gap > 300000:
            print("NOOOOOOOOOOO________>>>>>>>>>>>>")

        next_risk = self.position_risk.next(ohlcv)
        next_position = replace(self, position_risk=next_risk)

        next_position = next_position.break_even(ta)

        if next_position.signal_risk.type == SignalRiskType.NONE:
            trail_target = next_position.profit_target.targets[3]
        else:
            stp = next_position.signal_risk.tp
            index = next(
                (
                    i
                    for i, target in enumerate(next_position.profit_target.targets)
                    if target >= stp
                ),
                -1,
            )
            tidx = max(0, index)

            trail_target = next_position.profit_target.targets[tidx]

        print(next_position.profit_target.targets)
        print(f"Trail target: {trail_target}")

        if (
            next_position.side == PositionSide.LONG
            and next_position.curr_price > trail_target
        ) or (
            next_position.side == PositionSide.SHORT
            and next_position.curr_price < trail_target
        ):
            print("Target traillllllllll")
            next_position = next_position.trail(ta)

        pnl_perc = (next_position.curr_pnl / next_position.curr_price) * 100
        exit_target = next_position.profit_target.targets[4]

        if session_risk == SessionRiskType.EXIT:
            if (
                next_position.side == PositionSide.LONG
                and next_position.curr_price > exit_target
            ) or (
                next_position.side == PositionSide.SHORT
                and next_position.curr_price < exit_target
            ):
                print(
                    f"TRAILLL PREV SL: {next_position.stop_loss}, CURR PRICE: {next_position.risk_bar.close}"
                )
                next_position = next_position.trail(ta)
                print(
                    f"TRAILLL NEXT SL: {next_position.stop_loss}, CURR PRICE: {next_position.risk_bar.close}"
                )

        next_tp = next_position.take_profit
        next_sl = next_position.stop_loss

        next_risk = next_risk.assess(
            next_position.side,
            next_tp,
            next_sl,
            next_position.open_timestamp,
            next_position.expiration,
        )

        if next_risk.type == PositionRiskType.TP:
            next_risk = next_risk.reset()

        next_position = replace(
            next_position,
            position_risk=next_risk,
            _tp=next_tp,
            _sl=next_sl,
            last_modified=datetime.now().timestamp(),
        )

        logger.info(
            f"SIDE: {next_position.side}, TS: {ohlcv.timestamp}, GAP: {gap}ms, ENTRY: {next_position.entry_price}, CURR: {next_position.curr_price}, HIGH: {next_position.risk_bar.high}, LOW: {next_position.risk_bar.low}, PT: {next_position.curr_target}, SL: {next_position.stop_loss}, TP: {next_position.take_profit}, LLM_TP: {next_position.signal_risk.tp}, PnL%: {pnl_perc}, BREAK EVEN: {next_position.has_break_even}, RISK: {next_position.has_risk}"
        )

        return next_position

    def break_even(self, ta: TechAnalysis) -> "Position":
        curr_price = self.curr_price
        curr_sl = self.stop_loss
        volatility = ta.volatility.yz[-1]
        duration = self.trade_time / 100000 // len(self.position_risk.ohlcv)
        factor = volatility * duration
        targets = self.profit_target.targets[2:]

        if self.side == PositionSide.LONG:
            for i, target in enumerate(targets):
                if curr_price > target:
                    curr_sl = max(
                        curr_sl,
                        (self.entry_price if i == 0 else targets[i - 1]),
                    )
                    break

        elif self.side == PositionSide.SHORT:
            for i, target in enumerate(targets):
                if curr_price < target:
                    curr_sl = min(
                        curr_sl,
                        (self.entry_price if i == 0 else targets[i - 1]),
                    )
                    break

        if curr_sl != self.stop_loss:
            print(f"BREAK EVEEEEENNNNN: {factor}")

        return replace(self, _sl=curr_sl, last_modified=datetime.now().timestamp())

    def trail(self, ta: TechAnalysis) -> "Position":
        prev_sl = self.stop_loss
        next_sl = self.position_risk.sl_ats(self.side, self.curr_price, ta, prev_sl)

        logger.info(
            f"<---- &&&&&&TRAIL&&&&& -->>> prevSL: {prev_sl}, nextSL: {next_sl}"
        )

        return replace(self, _sl=next_sl, last_modified=datetime.now().timestamp())

    def theo_taker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.taker_fee

    def theo_maker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.maker_fee

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
            "curr_target": self.curr_target,
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
