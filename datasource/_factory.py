from core.interfaces.abstract_datasource import AbstractDataSource
from core.interfaces.abstract_datasource_factory import (
    AbstractDataSourceFactory,
    DataSourceType,
)
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.exchange import ExchangeType
from core.models.ws import WSType
from datasource._exchange import ExchangeDataSource
from datasource._ws import WSDataSource


class DataSourceFactory(AbstractDataSourceFactory):
    def __init__(
        self,
        exchange_factory: AbstractExchangeFactory,
        ws_factory: AbstractExchangeFactory,
    ):
        super().__init__()
        self.exchange_factory = exchange_factory
        self.ws_factory = ws_factory

    def create(self, type: DataSourceType, *args, **kwargs) -> AbstractDataSource:
        if not isinstance(type, DataSourceType):
            raise ValueError("Invalid datasource type provided")

        if isinstance(type, ExchangeType):
            exchange = self.exchange_factory.create(type)
            return ExchangeDataSource(exchange, *args, **kwargs)

        if isinstance(type, WSType):
            ws = self.ws_factory.create(type)
            return WSDataSource(ws, *args, **kwargs)
