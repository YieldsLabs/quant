from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union

from .abstract_exchange import AbstractRestExchange, AbstractWSExchange

DataSource = Union[AbstractRestExchange, AbstractWSExchange]


class AbstractDataSourceFactory(ABC):
    @abstractmethod
    def register(self, source_type: Any, source_class: Optional[Type] = None) -> None:
        pass

    @abstractmethod
    def create(self, source_type: Any, **kwargs) -> DataSource:
        pass
