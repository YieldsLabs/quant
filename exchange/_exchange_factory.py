from functools import lru_cache

from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.exchange import ExchangeType

from ._bybit import Bybit


class ExchangeFactory(AbstractExchangeFactory):
    _exchange_type = {ExchangeType.BYBIT: Bybit}

    def __init__(self, secret: AbstractSecretService):
        super().__init__()
        self.secret = secret

    @lru_cache(maxsize=None)
    def create(self, type: ExchangeType) -> AbstractExchange:
        if type not in self._exchange_type:
            raise ValueError(f"Unknown Exchange: {type}")

        exchange = self._exchange_type.get(type)

        api_key = self.secret.get_api_key(type.name)
        api_secret = self.secret.get_secret(type.name)

        return exchange(api_key, api_secret)
