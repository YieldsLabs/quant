from cachetools import LRUCache

from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.interfaces.abstract_ws_factory import AbstractWSFactory
from core.models.exchange import ExchangeType
from core.models.wss_type import WSType

from ._bybit_ws import BybitWS


class WSFactory(AbstractWSFactory):
    _type = {ExchangeType.BYBIT: BybitWS}

    def __init__(self, secret: AbstractSecretService, cache_size: int = 30):
        super().__init__()
        self.secret = secret
        self._cache = LRUCache(maxsize=cache_size)

    def create(self, exchange_type: ExchangeType, ws_type: WSType) -> AbstractExchange:
        if exchange_type not in self._type:
            raise ValueError(f"Unknown Exchange: {exchange_type}")

        ws = self._type.get(exchange_type)

        wss = {
            WSType.PUBLIC: self.secret.get_wss_public(exchange_type.name),
            WSType.PRIVATE: self.secret.get_wss_private(exchange_type.name),
            WSType.ORDER: self.secret.get_wss_order(exchange_type.name),
        }

        wss_url = wss.get(ws_type, self.secret.get_wss_public(exchange_type.name))

        if ws_type in {WSType.PRIVATE, WSType.ORDER}:
            cache_key = (exchange_type, ws_type)

            api_key = self.secret.get_api_key(exchange_type.name)
            api_secret = self.secret.get_secret(exchange_type.name)

            if cache_key in self._cache:
                return self._cache[cache_key]

            ws_instance = ws(wss_url, api_key, api_secret)
            self._cache[cache_key] = ws_instance
            return ws_instance
        else:
            return ws(wss_url, "", "")
