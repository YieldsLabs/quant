from abc import ABC, abstractmethod

from core.models.broker import MarginMode, PositionMode
from core.models.lookback import Lookback
from core.models.position import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractExchange(ABC):
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
    def fetch_position(self, symbol: Symbol):
        pass

    @abstractmethod
    def fetch_trade(self, symbol: Symbol):
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
    def fetch_order(self, order_id: str, symbol: Symbol):
        pass

    @abstractmethod
    def has_order(self, order_id: str, symbol: Symbol):
        pass

    @abstractmethod
    def fetch_order_book(self, symbol: Symbol):
        pass

    @abstractmethod
    def close_position(self, symbol: Symbol):
        pass
