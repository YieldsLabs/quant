from typing import Optional, Type

from cachetools import LRUCache

from core.interfaces.abstract_datasource_factory import (
    AbstractDataSourceFactory,
    DataSource,
)
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.datasource_type import DataSourceType
from core.models.wss_type import WSType

from ._bybit import BybitWS


class WSDataSourceFactory(AbstractDataSourceFactory):
    def __init__(self, secret_service: AbstractSecretService):
        super().__init__()
        self.secret_service = secret_service
        self._bucket = LRUCache(maxsize=10)
        self._default_map = {
            DataSourceType.BYBIT: BybitWS,
        }
        self._cache = LRUCache(maxsize=10)

    def register(
        self, datasource: DataSourceType, ws_class: Optional[Type[DataSource]] = None
    ) -> None:
        if ws_class is None:
            ws_class = self._default_map.get(datasource)

        self._bucket[datasource] = ws_class

    def create(self, datasource: DataSourceType, ws: WSType, **kwargs) -> DataSource:
        cache_key = (datasource, ws)

        if ws == WSType.PRIVATE:
            if cache_key in self._cache:
                return self._cache[cache_key]

        if datasource not in self._bucket:
            raise ValueError(f"WebSocket class for {datasource} is not registered.")

        wss = {
            WSType.PUBLIC: self.secret_service.get_wss_public(datasource.name),
            WSType.PRIVATE: self.secret_service.get_wss_private(datasource.name),
            WSType.ORDER: self.secret_service.get_wss_order(datasource.name),
        }

        wss_url = wss.get(ws, self.secret_service.get_wss_public(datasource.name))
        api_key = self.secret_service.get_api_key(datasource.name)
        api_secret = self.secret_service.get_secret(datasource.name)

        instance = self._bucket[datasource](wss_url, api_key, api_secret)

        if ws == WSType.PRIVATE:
            self._cache[cache_key] = instance

        return instance
