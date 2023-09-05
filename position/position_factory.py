from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.ohlcv import OHLCV
from core.models.position import Position, PositionSide
from core.models.signal import Signal, SignalSide

from .position_risk_break_even import BreakEvenStrategy
from .position_take_profit_rr import PositionRRTakeProfit
from .position_sizer import PositionSizer


class PositionFactory(AbstractPositionFactory):
    def __init__(self, leverage: float, risk_per_trade: float, risk_reward_ratio: float):
        super().__init__()
        self.leverage = leverage
        self.risk_per_trade = risk_per_trade
        self.risk_reward_ratio = risk_reward_ratio

    def create_position(self, signal: Signal, ohlcv: OHLCV, account_size: float, entry_price: float, stop_loss_price: float | None) -> Position:
        symbol = signal.symbol
        
        stop_loss_price = round(stop_loss_price, symbol.price_precision) if stop_loss_price else None
        entry_price = round(entry_price, symbol.price_precision)

        position_size = PositionSizer.calculate(
            account_size,
            entry_price,
            symbol.fee,
            symbol.min_position_size,
            symbol.position_precision,
            self.leverage,
            stop_loss_price,
            self.risk_per_trade
        )

        position_side = PositionSide.LONG if signal.side == SignalSide.BUY else PositionSide.SHORT
        risk_strategy = BreakEvenStrategy()
        take_profit_strategy = PositionRRTakeProfit(self.risk_reward_ratio)

        return Position(
            signal,
            position_side,
            position_size,
            entry_price,
            risk_strategy,
            take_profit_strategy,
            open_timestamp=ohlcv.timestamp,
            stop_loss_price=stop_loss_price
        )

    