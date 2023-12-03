from abc import ABC, abstractmethod

from core.interfaces.abstract_datasource import AbstractDataSource
from core.models.exchange import ExchangeType


class AbstractDataSourceFactory(ABC):
    @abstractmethod
    def create(self, type: ExchangeType) -> AbstractDataSource:
        pass
