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
    def fetch_symbols(self):
        pass

    @abstractmethod
    def fetch_ohlcv(
        self, symbol: Symbol, timeframe: Timeframe, lookback: Lookback, batch_size: int
    ):
        pass

    @abstractmethod
    def fetch_position(self, symbol: Symbol):
        pass

    @abstractmethod
    def open_market_position(self, symbol: Symbol, side: PositionSide, size: float):
        pass

    @abstractmethod
    def close_position(self, symbol: Symbol):
        pass
