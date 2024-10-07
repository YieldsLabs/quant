from typing import Optional, Type

from cachetools import LRUCache

from core.interfaces.abstract_datasource_factory import (
    AbstractDataSourceFactory,
    DataSource,
)
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.exchange import ExchangeType

from ._bybit import Bybit


class RestDataSourceFactory(AbstractDataSourceFactory):
    def __init__(self, secret_service: AbstractSecretService):
        super().__init__()
        self.secret_service = secret_service
        self._bucket = LRUCache(maxsize=10)
        self._default_map = {
            ExchangeType.BYBIT: Bybit,
        }

    def register(
        self,
        exchange_type: ExchangeType,
        exchange_class: Optional[Type[DataSource]] = None,
    ) -> None:
        if exchange_class is None:
            exchange_class = self._default_map.get(exchange_type)

        self._bucket[exchange_type] = exchange_class

    def create(self, exchange_type: ExchangeType, **kwargs) -> DataSource:
        if exchange_type not in self._bucket:
            raise ValueError(f"Class for {exchange_type} is not registered.")

        api_key = self.secret_service.get_api_key(exchange_type.name)
        api_secret = self.secret_service.get_secret(exchange_type.name)

        return self._bucket[exchange_type](api_key, api_secret)
