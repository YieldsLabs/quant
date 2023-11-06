from core.interfaces.abstract_datasource import AbstractDataSource
from core.interfaces.abstract_datasource_factory import AbstractDataSourceFactory
from core.models.datasource import DataSourceType
from datasource.exchange_datasource import ExchangeDataSource


class DataSourceFactory(AbstractDataSourceFactory):
    _datasource_type = {
        DataSourceType.EXCHANGE: ExchangeDataSource,
    }

    def __init__(self):
        super().__init__()

    def create(self, type: DataSourceType, *args, **kwargs) -> AbstractDataSource:
        if type not in self._datasource_type:
            raise ValueError(f"Unknown DataSource: {type}")

        datasource_class = self._datasource_type.get(type)

        return datasource_class(*args, **kwargs)
