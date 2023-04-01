from abc import ABC, abstractmethod
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode

class AbstractBroker(ABC):
    @abstractmethod
    def set_leverage(self, symbol, leverage=3):
        pass

    @abstractmethod
    def set_position_mode(self, symbol, mode=PositionMode):
        pass

    @abstractmethod
    def set_margin_mode(self, symbol, mode=MarginMode, leverage=1):
        pass

    @abstractmethod
    def get_account_balance(self):
        pass

    @abstractmethod
    def get_symbol_info(self):
        pass

    @abstractmethod
    def get_open_positions(self, symbol):
       pass

    @abstractmethod
    def get_symbols(self):
        pass
    
    @abstractmethod
    def get_historical_data(self, symbol, timeframe, limit=1000):
        pass

    @abstractmethod
    def place_market_order(self, side, symbol, position_size, stop_loss_price=None, take_profit_price=None):
        pass
    
    @abstractmethod
    def place_limit_order(self, side, symbol, price, position_size, stop_loss_price=None, take_profit_price=None):
        pass

    @abstractmethod
    def has_open_position(self, symbol):
        pass

    @abstractmethod
    def close_position(self, symbol):
        pass
