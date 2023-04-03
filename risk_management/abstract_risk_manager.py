from abc import ABC, abstractmethod

from shared.position_side import PositionSide

class AbstractRiskManager(ABC):
    @abstractmethod
    def calculate_position_size(self, account_size, entry_price=None, stop_loss_price=None):
        raise NotImplementedError

    @abstractmethod
    def check_exit_conditions(self, position_side: PositionSide, entry_price, current_row):
        raise NotImplementedError

    @abstractmethod
    def calculate_prices(self, position_side: PositionSide, entry_price):
        raise NotImplementedError
    
    @abstractmethod
    def calculate_profit(self, position_side: PositionSide, position_size, entry_price, current_close, take_profit_price, stop_loss_price):
        raise NotImplementedError
