from typing import Any, Optional, Type

from core.interfaces.abstract_datasource_factory import DataSource
from core.interfaces.abstract_exchange import AbstractRestExchange, AbstractWSExchange
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.datasource_type import DataSourceType
from core.models.exchange import ExchangeType

from .exchange import ExchangeRestDataSourceFactory, ExchangeWSDataSourceFactory


class DataSourceFactory:
    def __init__(self, secret_service: AbstractSecretService):
        self._exrest = ExchangeRestDataSourceFactory(secret_service)
        self._exws = ExchangeWSDataSourceFactory(secret_service)

    def register_rest_exchange(
        self,
        exchange_type: ExchangeType,
        exchange_class: Optional[Type[AbstractRestExchange]] = None,
    ):
        self._exrest.register(exchange_type, exchange_class)

    def register_ws_exchange(
        self,
        exchange_type: ExchangeType,
        ws_class: Optional[Type[AbstractWSExchange]] = None,
    ):
        self._exws.register(exchange_type, ws_class)

    def create(
        self, factory_type: DataSourceType, conn_type: Any, **kwargs
    ) -> DataSource:
        if factory_type == DataSourceType.ExREST:
            return self._exrest.create(conn_type, **kwargs)
        elif factory_type == DataSourceType.ExWS:
            return self._exws.create(conn_type, **kwargs)
        else:
            raise ValueError(f"Unknown factory type: {factory_type}")
