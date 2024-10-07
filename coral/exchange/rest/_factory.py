from typing import Optional, Type

from cachetools import LRUCache

from core.interfaces.abstract_datasource_factory import (
    AbstractDataSourceFactory,
    DataSource,
)
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.datasource_type import DataSourceType

from ._bybit import Bybit


class RestDataSourceFactory(AbstractDataSourceFactory):
    def __init__(self, secret_service: AbstractSecretService):
        super().__init__()
        self.secret_service = secret_service
        self._bucket = LRUCache(maxsize=10)
        self._default_map = {
            DataSourceType.BYBIT: Bybit,
        }

    def register(
        self,
        datasource: DataSourceType,
        exchange_class: Optional[Type[DataSource]] = None,
    ) -> None:
        if exchange_class is None:
            exchange_class = self._default_map.get(datasource)

        self._bucket[datasource] = exchange_class

    def create(self, datasource: DataSourceType, **kwargs) -> DataSource:
        if datasource not in self._bucket:
            raise ValueError(f"Class for {datasource} is not registered.")

        api_key = self.secret_service.get_api_key(datasource.name)
        api_secret = self.secret_service.get_secret(datasource.name)

        return self._bucket[datasource](api_key, api_secret)
