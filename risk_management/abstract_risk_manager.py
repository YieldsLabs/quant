from abc import ABC, abstractmethod

class AbstractRiskManager(ABC):
    @abstractmethod
    def calculate_position_size(self, account_size, entry_price=None, stop_loss_price=None):
        pass

    @abstractmethod
    def check_exit_conditions(self, entry_trade_type, entry_price, current_row):
        pass

    @abstractmethod
    def calculate_prices(self, entry_trade_type, entry_price):
        pass
