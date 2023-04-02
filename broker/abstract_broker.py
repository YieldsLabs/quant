from abc import ABC, abstractmethod
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode

class AbstractBroker(ABC):
    @abstractmethod
    def set_leverage(self, symbol, leverage=3):
        raise NotImplementedError

    @abstractmethod
    def set_position_mode(self, symbol, mode=PositionMode):
        raise NotImplementedError

    @abstractmethod
    def set_margin_mode(self, symbol, mode=MarginMode, leverage=1):
        raise NotImplementedError

    @abstractmethod
    def get_account_balance(self):
        raise NotImplementedError

    @abstractmethod
    def get_symbol_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_open_position(self, symbol):
       raise NotImplementedError

    @abstractmethod
    def get_symbols(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_historical_data(self, symbol, timeframe, lookback=1000):
        raise NotImplementedError

    @abstractmethod
    def place_market_order(self, side, symbol, position_size, stop_loss_price=None, take_profit_price=None):
        raise NotImplementedError
    
    @abstractmethod
    def place_limit_order(self, side, symbol, price, position_size, stop_loss_price=None, take_profit_price=None):
        raise NotImplementedError

    @abstractmethod
    def update_stop_loss(self, order_id, symbol, side, stop_loss_price):
        raise NotImplementedError

    @abstractmethod
    def has_open_position(self, symbol):
        raise NotImplementedError

    @abstractmethod
    def close_position(self, symbol):
        raise NotImplementedError

    @abstractmethod
    def close_order(self, order_id, symbol):
        raise NotImplementedError
