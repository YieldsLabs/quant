from typing import Optional, Type

from cachetools import LRUCache

from core.interfaces.abstract_datasource_factory import (
    AbstractDataSourceFactory,
    DataSource,
)
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.exchange import ExchangeType

from ._bybit import BybitWS


class WSDataSourceFactory(AbstractDataSourceFactory):
    def __init__(self, secret_service: AbstractSecretService):
        super().__init__()
        self.secret_service = secret_service
        self._bucket = LRUCache(maxsize=10)
        self._default_map = {
            ExchangeType.BYBIT: BybitWS,
        }

    def register(
        self, exchange_type: ExchangeType, ws_class: Optional[Type[DataSource]] = None
    ) -> None:
        if ws_class is None:
            ws_class = self._default_map.get(exchange_type)

        self._bucket[exchange_type] = ws_class

    def create(self, exchange_type: ExchangeType, **kwargs) -> DataSource:
        if exchange_type not in self._bucket:
            raise ValueError(f"WebSocket class for {exchange_type} is not registered.")

        wss_url = self.secret_service.get_wss_public(exchange_type.name)
        api_key = self.secret_service.get_api_key(exchange_type.name)
        api_secret = self.secret_service.get_secret(exchange_type.name)

        return self._bucket[exchange_type](wss_url, api_key, api_secret)
