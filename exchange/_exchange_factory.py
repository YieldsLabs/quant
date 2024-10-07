from cachetools import LRUCache

from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.exchange import ExchangeType

from ._bybit import Bybit


class ExchangeFactory(AbstractExchangeFactory):
    _exchange_type = {ExchangeType.BYBIT: Bybit}

    def __init__(self, secret: AbstractSecretService, cache_size: int = 10):
        super().__init__()
        self.secret = secret
        self._cache = LRUCache(maxsize=cache_size)

    def create(self, exchange_type: ExchangeType) -> AbstractExchange:
        if exchange_type not in self._exchange_type:
            raise ValueError(f"Unknown Exchange: {exchange_type}")

        exchange = self._exchange_type.get(exchange_type)

        api_key = self.secret.get_api_key(exchange_type.name)
        api_secret = self.secret.get_secret(exchange_type.name)

        if exchange_type in self._cache:
            return self._cache[exchange_type]

        exchange_inst = exchange(api_key, api_secret)
        self._cache[exchange_type] = exchange_inst
        return exchange_inst
