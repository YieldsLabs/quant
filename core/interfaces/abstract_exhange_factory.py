from abc import ABC, abstractmethod

from core.interfaces.abstract_exchange import AbstractExchange
from core.models.exchange import ExchangeType


class AbstractExchangeFactory(ABC):
    @abstractmethod
    def create(self, type: ExchangeType) -> AbstractExchange:
        pass
