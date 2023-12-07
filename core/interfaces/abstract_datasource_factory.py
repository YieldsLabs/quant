from abc import ABC, abstractmethod
from typing import Union

from core.interfaces.abstract_datasource import AbstractDataSource
from core.models.exchange import ExchangeType
from core.models.ws import WSType

DataSourceType = Union[ExchangeType, WSType]


class AbstractDataSourceFactory(ABC):
    @abstractmethod
    def create(self, type: DataSourceType) -> AbstractDataSource:
        pass
