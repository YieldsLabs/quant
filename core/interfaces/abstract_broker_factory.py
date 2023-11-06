from abc import ABC, abstractmethod

from core.interfaces.abstract_broker import AbstractBroker
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.broker import BrokerType


class AbstractBrokerFactory(ABC):
    @abstractmethod
    def create(self, type: BrokerType, exchange: AbstractExchange) -> AbstractBroker:
        pass
