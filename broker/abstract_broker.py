from abc import ABC, abstractmethod
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from shared.order_side import OrderSide

class AbstractBroker(ABC):
    @abstractmethod
    def set_leverage(self, symbol: str, leverage=3):
        raise NotImplementedError

    @abstractmethod
    def set_position_mode(self, symbol: str, mode: PositionMode):
        raise NotImplementedError

    @abstractmethod
    def set_margin_mode(self, symbol: str, mode: MarginMode, leverage=1):
        raise NotImplementedError

    @abstractmethod
    def get_account_balance(self):
        raise NotImplementedError

    @abstractmethod
    def get_symbol_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_open_position(self, symbol: str):
       raise NotImplementedError

    @abstractmethod
    def get_symbols(self):
        raise NotImplementedError

    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, lookback=1000):
        raise NotImplementedError

    @abstractmethod
    def place_market_order(self, side: OrderSide, symbol: str, position_size: float, stop_loss_price=None, take_profit_price=None):
        raise NotImplementedError
    
    @abstractmethod
    def place_limit_order(self, side: OrderSide, symbol: str, price, position_size: float, stop_loss_price=None, take_profit_price=None):
        raise NotImplementedError

    @abstractmethod
    def update_stop_loss(self, order_id, symbol: str, side: OrderSide, stop_loss_price: float):
        raise NotImplementedError

    @abstractmethod
    def has_open_position(self, symbol: str):
        raise NotImplementedError

    @abstractmethod
    def close_position(self, symbol: str):
        raise NotImplementedError

    @abstractmethod
    def close_order(self, order_id: str, symbol: str):
        raise NotImplementedError
