from abc import ABC, abstractmethod

from core.models.broker import MarginMode, PositionMode
from core.models.entity.position import PositionSide
from core.models.lookback import Lookback
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractRestExchange(ABC):
    @abstractmethod
    def update_symbol_settings(
        self,
        symbol: Symbol,
        position_mode: PositionMode,
        margin_mode: MarginMode,
        leverage: int,
    ):
        pass

    @abstractmethod
    def fetch_account_balance(self, currency: str):
        pass

    @abstractmethod
    def fetch_future_symbols(self):
        pass

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        in_sample: Lookback,
        out_sample: Lookback,
        batch_size: int,
    ):
        pass

    @abstractmethod
    def fetch_position(self, symbol: Symbol, side: PositionSide):
        pass

    @abstractmethod
    def fetch_trade(self, symbol: Symbol, side: PositionSide, since: int, size: float):
        pass

    @abstractmethod
    def create_market_order(self, symbol: Symbol, side: PositionSide, size: float):
        pass

    @abstractmethod
    def create_limit_order(
        symbol: Symbol, side: PositionSide, size: float, price: float
    ):
        pass

    @abstractmethod
    def create_reduce_order(
        symbol: Symbol, side: PositionSide, size: float, price: float
    ):
        pass

    @abstractmethod
    def has_filled_order(self, order_id: str, symbol: Symbol):
        pass

    @abstractmethod
    def has_open_orders(self, symbol: Symbol, side: PositionSide, is_reduced: bool):
        pass

    @abstractmethod
    def fetch_all_open_orders(
        self,
    ):
        pass

    @abstractmethod
    def cancel_order(self, order_id: str, symbol: Symbol):
        pass

    @abstractmethod
    def fetch_order_book(self, symbol: Symbol, depth: int):
        pass

    @abstractmethod
    def close_full_position(self, symbol: Symbol, side: PositionSide):
        pass

    @abstractmethod
    def close_half_position(self, symbol: Symbol, side: PositionSide):
        pass


class AbstractWSExchange(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def auth(self):
        pass

    @abstractmethod
    def subscribe(self, topic: str):
        pass

    @abstractmethod
    def get_message(self, topic: str):
        pass

    @abstractmethod
    def unsubscribe(self, topic: str):
        pass

    @abstractmethod
    def kline_topic(self, timeframe: Timeframe, symbol: Symbol):
        pass

    @abstractmethod
    def order_book_topic(self, symbol: Symbol, depth: int):
        pass

    @abstractmethod
    def liquidation_topic(self, symbol: Symbol):
        pass

    @abstractmethod
    def order_topic(self):
        pass

    @abstractmethod
    def position_topic(self):
        pass
