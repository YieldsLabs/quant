from typing import Type
from risk_management.abstract_risk_manager import AbstractRiskManager
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.position_side import PositionSide


class RiskManager(AbstractRiskManager):
    def __init__(self, stop_loss_finder: Type[AbstractStopLoss], take_profit_finder: Type[AbstractTakeProfit], risk_per_trade=0.01, trading_fee=0.01, price_precision=3, position_precision=2, min_position_size=0.01, trailing_stop_loss=False, max_stop_loss_adjustments=10):
        super().__init__()
        self.stop_loss_finder = stop_loss_finder
        self.take_profit_finder = take_profit_finder
        self.risk_per_trade = self._validate_risk_per_trade(risk_per_trade)
        self.trading_fee = self._validate_trading_fee(trading_fee)
        self.price_precision = self._validate_precision(price_precision)
        self.position_precision = self._validate_precision(position_precision)
        self.min_position_size = self._validate_min_position_size(
            min_position_size)
        
        self.trailing_stop_loss = trailing_stop_loss
        self.trailing_stop_loss_prices = {}
        self.max_stop_loss_adjustments = max_stop_loss_adjustments
        self.stop_loss_adjustment_count = {PositionSide.LONG: 0, PositionSide.SHORT: 0}


    def calculate_position_size(self, account_size, entry_price=None, stop_loss_price=None):
        risk_amount = self.risk_per_trade * account_size
        div = abs(entry_price - stop_loss_price) * (1 +
                                                    self.trading_fee) if stop_loss_price and entry_price else 1
        position_size = risk_amount / div if div != 0 else 1

        return round(position_size if position_size > self.min_position_size else self.min_position_size, self.price_precision)

    def check_exit_conditions(self, position_side, entry_price, current_row):
        stop_loss_price, take_profit_price = self.calculate_prices(
            position_side, entry_price)

        if self.trailing_stop_loss and self.stop_loss_adjustment_count[position_side] < self.max_stop_loss_adjustments:
            stop_loss_price = self.update_trailing_stop_loss(position_side, stop_loss_price, current_row)

        if self.should_exit(position_side, stop_loss_price, take_profit_price, current_row):
            self.trailing_stop_loss_prices[position_side] = None
            self.stop_loss_adjustment_count[position_side] = 0
            return True

        return False

    def calculate_profit(self, position_side, position_size, entry_price, current_close, take_profit_price, stop_loss_price):
        profit = 0
        exit_price = current_close

        if position_side == PositionSide.LONG:
            exit_price = min(
                exit_price, take_profit_price if take_profit_price else exit_price)
            exit_price = max(
                exit_price, stop_loss_price if stop_loss_price else exit_price)

            profit = (exit_price - entry_price) * position_size

        elif position_side == PositionSide.SHORT:
            exit_price = max(
                exit_price, take_profit_price if take_profit_price else exit_price)
            exit_price = min(
                exit_price, stop_loss_price if stop_loss_price else exit_price)

            profit = (entry_price - exit_price) * position_size

        return profit

    def calculate_prices(self, position_side, entry_price):
        stop_loss_price = self.stop_loss_finder.next(
            position_side, entry_price)
        take_profit_price = self.take_profit_finder.next(
            position_side, entry_price, stop_loss_price)

        return round(stop_loss_price, self.price_precision), round(take_profit_price, self.price_precision) if take_profit_price else None

    def calculate_entry(self, position_side, account_size, entry_price):
        stop_loss_price, take_profit_price = self.calculate_prices(position_side, entry_price)
        position_size = self.calculate_position_size(account_size, entry_price, stop_loss_price=stop_loss_price)

        return position_size, stop_loss_price, take_profit_price

    def should_exit(self, position_side, stop_loss_price, take_profit_price, current_row):
        if position_side == PositionSide.LONG:
            return self._long_exit_conditions(stop_loss_price, take_profit_price, current_row)
        elif position_side == PositionSide.SHORT:
            return self._short_exit_conditions(stop_loss_price, take_profit_price, current_row)
        
    def update_trailing_stop_loss(self, position_side, stop_loss_price, current_row):
        if position_side not in self.trailing_stop_loss_prices:
            self.trailing_stop_loss_prices[position_side] = stop_loss_price

        if position_side == PositionSide.LONG:
            new_stop_loss_price = current_row['high'] - (current_row['high'] - stop_loss_price) * self.risk_per_trade
            if new_stop_loss_price > self.trailing_stop_loss_prices[position_side]:
                self.trailing_stop_loss_prices[position_side] = new_stop_loss_price
                self.stop_loss_adjustment_count[position_side] += 1
        elif position_side == PositionSide.SHORT:
            new_stop_loss_price = current_row['low'] + (stop_loss_price - current_row['low']) * self.risk_per_trade
            if new_stop_loss_price < self.trailing_stop_loss_prices[position_side]:
                self.trailing_stop_loss_prices[position_side] = new_stop_loss_price
                self.stop_loss_adjustment_count[position_side] += 1

        return self.trailing_stop_loss_prices[position_side]

    @staticmethod
    def _long_exit_conditions(stop_loss_price, take_profit_price, current_row):
        return (stop_loss_price is not None and current_row['low'] <= stop_loss_price) or \
               (take_profit_price is not None and current_row['high'] >= take_profit_price)

    @staticmethod
    def _short_exit_conditions(stop_loss_price, take_profit_price, current_row):
        return (stop_loss_price is not None and current_row['high'] >= stop_loss_price) or \
               (take_profit_price is not None and current_row['low'] <= take_profit_price)

    def _validate_risk_per_trade(self, risk_per_trade):
        if risk_per_trade <= 0 or risk_per_trade >= 1:
            raise ValueError(
                "Risk per trade should be a positive value between 0 and 1.")
        return risk_per_trade

    def _validate_trading_fee(self, trading_fee):
        if trading_fee < 0 or trading_fee >= 1:
            raise ValueError("Trading fee should be a value between 0 and 1.")
        return trading_fee

    def _validate_precision(self, precision):
        if precision < 0 or not isinstance(precision, int):
            raise ValueError("Precision should be a non-negative integer.")
        return precision

    def _validate_min_position_size(self, min_position_size):
        if min_position_size <= 0:
            raise ValueError(
                "Minimum position size should be a positive value.")
        return min_position_size
