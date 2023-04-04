from abc import ABC, abstractmethod

from shared.position_side import PositionSide


class AbstractRiskManager(ABC):
    @abstractmethod
    def calculate_position_size(self, account_size: float, entry_price=None, stop_loss_price=None):
        raise NotImplementedError

    @abstractmethod
    def check_exit_conditions(self, position_side: PositionSide, entry_price: float, current_row):
        raise NotImplementedError

    @abstractmethod
    def calculate_entry(self, position_side: PositionSide, account_size: float, entry_price: float):
        raise NotImplementedError

    @abstractmethod
    def calculate_prices(self, position_side: PositionSide, entry_price: float):
        raise NotImplementedError

    @abstractmethod
    def calculate_profit(self, position_side: PositionSide, position_size: float, entry_price: float, current_close: float, take_profit_price: float, stop_loss_price: float):
        raise NotImplementedError
