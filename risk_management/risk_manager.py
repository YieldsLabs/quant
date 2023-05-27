from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV
from core.events.position import PositionSide
from core.events.risk import RiskEvaluate, RiskExit, RiskType

from .abstract_risk_manager import AbstractRiskManager
from .stop_loss.strategy.break_even import BreakEvenStopLossStrategy
from .take_profit.finders.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder


class RiskManager(AbstractRiskManager):
    def __init__(self, risk_type: RiskType = RiskType.BREAK_EVEN):
        super().__init__()
        self.risk_type = risk_type
        self.break_even_strategy = BreakEvenStopLossStrategy()

    @register_handler(RiskEvaluate)
    async def _on_risk(self, event: RiskEvaluate):
        symbol, timeframe, position_side, position_size, entry_price, stop_loss_price, risk_reward_ratio, risk_per_trade, ohlcv, strategy = self._unpack_event(event)
        take_profit_price = self._calculate_take_profit_price(risk_reward_ratio, entry_price, stop_loss_price)

        if self.risk_type == RiskType.BREAK_EVEN and stop_loss_price is not None:
            stop_loss_price = await self._calculate_break_even_stop_loss(symbol, timeframe, position_side, position_size, stop_loss_price, entry_price, ohlcv, risk_per_trade)

        if self._should_exit(position_side, stop_loss_price, take_profit_price, ohlcv):
            await self._process_exit(symbol, timeframe, position_side, strategy, ohlcv, take_profit_price, stop_loss_price)

    async def _calculate_break_even_stop_loss(self, symbol, timeframe, position_side, position_size, stop_loss_price, entry_price, ohlcv, risk_per_trade):
        return await self.break_even_strategy.next(symbol, timeframe, position_side, position_size, stop_loss_price, entry_price, ohlcv.low, ohlcv.high, risk_per_trade)

    def _calculate_take_profit_price(self, risk_reward_ratio, entry_price, stop_loss_price):
        return RiskRewardTakeProfitFinder(risk_reward_ratio).next(entry_price, stop_loss_price)

    async def _process_exit(self, symbol, timeframe, position_side, strategy, ohlcv, take_profit_price, stop_loss_price):
        await self.break_even_strategy.reset(symbol, timeframe, position_side)

        exit_price = self._calculate_exit_price(position_side, ohlcv.close, take_profit_price, stop_loss_price)

        await self.dispatcher.dispatch(RiskExit(symbol=symbol, timeframe=timeframe, side=position_side, strategy=strategy, exit=exit_price))

    def _unpack_event(self, event: RiskEvaluate):
        return event.symbol, event.timeframe, event.side, event.size, event.entry, event.stop_loss, event.risk_reward_ratio, event.risk_per_trade, event.ohlcv, event.strategy

    def _should_exit(self, position_side: PositionSide, stop_loss_price: float | None, take_profit_price: float | None, ohlcv: OHLCV):
        if position_side == PositionSide.LONG:
            return self._long_exit_conditions(stop_loss_price, take_profit_price, ohlcv.low, ohlcv.high)
        elif position_side == PositionSide.SHORT:
            return self._short_exit_conditions(stop_loss_price, take_profit_price, ohlcv.low, ohlcv.high)

    @staticmethod
    def _calculate_exit_price(position_side: PositionSide, current_close: float, take_profit_price: float | None, stop_loss_price: float | None):
        exit_price = current_close

        if position_side == PositionSide.LONG:
            exit_price = max(min(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        elif position_side == PositionSide.SHORT:
            exit_price = min(max(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        return exit_price

    @staticmethod
    def _long_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float):
        return (stop_loss_price is not None and low <= stop_loss_price) or \
               (take_profit_price is not None and high >= take_profit_price)

    @staticmethod
    def _short_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float):
        return (stop_loss_price is not None and high >= stop_loss_price) or \
               (take_profit_price is not None and low <= take_profit_price)
