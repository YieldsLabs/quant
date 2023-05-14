import asyncio
from core.event_dispatcher import register_handler
from core.events.position import PositionSide
from core.events.risk import RiskEvaluate, RiskExit
from risk_management.abstract_risk_manager import AbstractRiskManager
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder


class RiskManager(AbstractRiskManager):
    def __init__(self, break_even=True):
        super().__init__()
        self.break_even = break_even
        self.break_even_stop_loss_prices = {}
        self.stop_loss_lock = asyncio.Lock()

    @register_handler(RiskEvaluate)
    async def _on_check_exit_conditions(self, event: RiskEvaluate):
        symbol, timeframe, position_side, position_size, entry_price, stop_loss_price, risk_reward_ratio, risk_per_trade, ohlcv, strategy = self._unpack_event(event)
        take_profit_price = None

        async with self.stop_loss_lock:
            if stop_loss_price:
                take_profit_price = RiskRewardTakeProfitFinder(risk_reward_ratio).next(entry_price, stop_loss_price)

            if symbol not in self.break_even_stop_loss_prices:
                self._initialize_symbol_data(symbol)

            if self.break_even:
                stop_loss_price = self._update_break_even_stop_loss(symbol, position_side, position_size, stop_loss_price, entry_price, ohlcv.low, ohlcv.high, risk_per_trade)

        if not self._should_exit(position_side, stop_loss_price, take_profit_price, ohlcv.low, ohlcv.high):
            return

        async with self.stop_loss_lock:
            self._reset_break_even_stop_loss_data(symbol, position_side)

        exit_price = self._calculate_exit_price(position_side, ohlcv.close, take_profit_price, stop_loss_price)

        await self.dispatcher.dispatch(RiskExit(symbol=symbol, timeframe=timeframe, side=position_side, strategy=strategy, exit=exit_price))

    def _initialize_symbol_data(self, symbol):
        self.break_even_stop_loss_prices[symbol] = {PositionSide.LONG: None, PositionSide.SHORT: None}

    def _reset_break_even_stop_loss_data(self, symbol, position_side):
        self.break_even_stop_loss_prices[symbol][position_side] = None

    def _unpack_event(self, event: RiskEvaluate):
        return event.symbol, event.timeframe, event.side, event.size, event.entry, event.stop_loss, event.risk_reward_ratio, event.risk_per_trade, event.ohlcv, event.strategy

    def _should_exit(self, position_side, stop_loss_price, take_profit_price, low, high):
        if position_side == PositionSide.LONG:
            return self._long_exit_conditions(stop_loss_price, take_profit_price, low, high)
        elif position_side == PositionSide.SHORT:
            return self._short_exit_conditions(stop_loss_price, take_profit_price, low, high)

    def _update_break_even_stop_loss(self, symbol, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade):
        if not self.break_even_stop_loss_prices[symbol][position_side]:
            self.break_even_stop_loss_prices[symbol][position_side] = stop_loss_price

        if position_side == PositionSide.LONG:
            new_stop_loss_price = high - (high - stop_loss_price) * risk_per_trade

            if new_stop_loss_price > self.break_even_stop_loss_prices[symbol][position_side]:
                self.break_even_stop_loss_prices[symbol][position_side] = new_stop_loss_price

                if self.break_even_stop_loss_prices[symbol][position_side] - entry_price >= risk_per_trade * position_size:
                    self.break_even_stop_loss_prices[symbol][position_side] = entry_price

        elif position_side == PositionSide.SHORT:
            new_stop_loss_price = low + (stop_loss_price - low) * risk_per_trade

            if new_stop_loss_price < self.break_even_stop_loss_prices[symbol][position_side]:
                self.break_even_stop_loss_prices[symbol][position_side] = new_stop_loss_price

                if entry_price - self.break_even_stop_loss_prices[symbol][position_side] >= risk_per_trade * position_size:
                    self.break_even_stop_loss_prices[symbol][position_side] = entry_price

        return self.break_even_stop_loss_prices[symbol][position_side]

    @staticmethod
    def _calculate_exit_price(position_side, current_close, take_profit_price, stop_loss_price):
        exit_price = current_close

        if position_side == PositionSide.LONG:
            exit_price = max(min(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        elif position_side == PositionSide.SHORT:
            exit_price = min(max(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        return exit_price

    @staticmethod
    def _long_exit_conditions(stop_loss_price, take_profit_price, low, high):
        return (stop_loss_price is not None and low <= stop_loss_price) or \
               (take_profit_price is not None and high >= take_profit_price)

    @staticmethod
    def _short_exit_conditions(stop_loss_price, take_profit_price, low, high):
        return (stop_loss_price is not None and high >= stop_loss_price) or \
               (take_profit_price is not None and low <= take_profit_price)
