from typing import Optional, Type

from core.interfaces.abstract_datasource_factory import DataSource
from core.interfaces.abstract_exchange import AbstractRestExchange, AbstractWSExchange
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.datasource_type import DataSourceType
from core.models.protocol_type import ProtocolType
from core.models.wss_type import WSType

from .exchange import ExchangeRestDataSourceFactory, ExchangeWSDataSourceFactory


class DataSourceFactory:
    def __init__(self, secret_service: AbstractSecretService):
        self._exrest = ExchangeRestDataSourceFactory(secret_service)
        self._exws = ExchangeWSDataSourceFactory(secret_service)

    def register_rest_exchange(
        self,
        datasource: DataSourceType,
        exchange_class: Optional[Type[AbstractRestExchange]] = None,
    ):
        self._exrest.register(datasource, exchange_class)

    def register_ws_exchange(
        self,
        datasource: DataSourceType,
        ws_class: Optional[Type[AbstractWSExchange]] = None,
    ):
        self._exws.register(datasource, ws_class)

    def create(
        self,
        datasource: DataSourceType,
        protocol: ProtocolType,
        ws: WSType = WSType.PUBLIC,
        **kwargs,
    ) -> DataSource:
        if protocol == ProtocolType.REST:
            return self._exrest.create(datasource, **kwargs)
        elif protocol == ProtocolType.WS:
            return self._exws.create(datasource, ws, **kwargs)
        else:
            raise ValueError(f"Unknown protocol type: {protocol}")
