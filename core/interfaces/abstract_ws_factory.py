from abc import ABC, abstractmethod

from core.interfaces.abstract_exchange import AbstractExchange
from core.models.exchange import ExchangeType
from core.models.wss_type import WSType


class AbstractWSFactory(ABC):
    @abstractmethod
    def create(self, exchange: ExchangeType, wss: WSType) -> AbstractExchange:
        pass
