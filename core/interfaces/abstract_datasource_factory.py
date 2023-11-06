from abc import ABC, abstractmethod

from core.interfaces.abstract_datasource import AbstractDataSource
from core.models.datasource import DataSourceType


class AbstractDataSourceFactory(ABC):
    @abstractmethod
    def create(self, type: DataSourceType) -> AbstractDataSource:
        pass
