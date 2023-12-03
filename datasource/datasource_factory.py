from core.interfaces.abstract_datasource import AbstractDataSource
from core.interfaces.abstract_datasource_factory import AbstractDataSourceFactory
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.exchange import ExchangeType
from datasource.exchange_datasource import ExchangeDataSource


class DataSourceFactory(AbstractDataSourceFactory):
    def __init__(self, exchange_factory: AbstractExchangeFactory):
        super().__init__()
        self.exchange_factory = exchange_factory

    def create(self, type: ExchangeType, *args, **kwargs) -> AbstractDataSource:
        if not isinstance(type, ExchangeType):
            raise ValueError("Invalid datasource type provided")

        exchange = self.exchange_factory.create(type)
        return ExchangeDataSource(exchange, *args, **kwargs)
