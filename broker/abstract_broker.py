from abc import ABC, abstractmethod

from core.position import OrderSide

from .margin_mode import MarginMode
from .position_mode import PositionMode


class AbstractBroker(ABC):
    @abstractmethod
    def set_settings(self, symbol: str, leverage: int, position_mode: PositionMode, margin_mode: MarginMode):
        pass

    @abstractmethod
    def get_account_balance(self):
        pass

    @abstractmethod
    def get_symbol_info(self, symbol: str):
        pass

    @abstractmethod
    def get_open_position(self, symbol: str):
        pass

    @abstractmethod
    def get_symbols(self):
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, lookback=1000):
        pass

    @abstractmethod
    def place_market_order(self, order_side: OrderSide, symbol: str, position_size: float, stop_loss_price=None, take_profit_price=None):
        pass

    @abstractmethod
    def place_limit_order(self, order_side: OrderSide, symbol: str, entry_price: float, position_size: float, stop_loss_price=None, take_profit_price=None):
        pass

    @abstractmethod
    def update_stop_loss(self, order_id, symbol: str, order_side: OrderSide, stop_loss_price: float):
        pass

    @abstractmethod
    def has_open_position(self, symbol: str):
        pass

    @abstractmethod
    def close_position(self, symbol: str):
        pass

    @abstractmethod
    def close_order(self, order_id: str, symbol: str):
        pass
