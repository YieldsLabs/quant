from abc import ABC, abstractmethod
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.events.position import OrderSide


class AbstractBroker(ABC):
    @abstractmethod
    def set_leverage(self, symbol: str, leverage=3):
        pass

    @abstractmethod
    def set_position_mode(self, symbol: str, mode: PositionMode):
        pass

    @abstractmethod
    def set_margin_mode(self, symbol: str, mode: MarginMode, leverage=1):
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
