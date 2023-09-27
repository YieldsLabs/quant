from abc import abstractmethod
from typing import Any

from .abstract_event_manager import AbstractEventManager


class AbstractBroker(AbstractEventManager):
    @abstractmethod
    def set_settings(self, command: Any):
        pass

    @abstractmethod
    def open_position(self, command: Any):
        pass

    @abstractmethod
    def close_position(self, command: Any):
        pass

    @abstractmethod
    def get_account_balance(self, command: Any):
        pass

    @abstractmethod
    def get_symbols(self, command: Any):
        pass

    @abstractmethod
    def get_symbol(self, command: Any):
        pass

    @abstractmethod
    def get_historical_data(
        self, symbol: str, timeframe: str, lookback: int, batch_size: int
    ):
        pass
