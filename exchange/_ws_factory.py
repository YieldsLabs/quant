from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.interfaces.abstract_ws_factory import AbstractWSFactory
from core.models.exchange import ExchangeType
from core.models.wss_type import WSType

from ._bybit_ws import BybitWS


class WSFactory(AbstractWSFactory):
    _type = {ExchangeType.BYBIT: BybitWS}

    def __init__(self, secret: AbstractSecretService):
        super().__init__()
        self.secret = secret

    def create(self, type: ExchangeType, ws_type: WSType) -> AbstractExchange:
        if type not in self._type:
            raise ValueError(f"Unknown Exchange: {type}")

        ws = self._type.get(type)
        wss = {
            WSType.PUBLIC: self.secret.get_wss_public(type.name),
            WSType.PRIVATE: self.secret.get_wss_private(type.name),
            WSType.ORDER: self.secret.get_wss_order(type.name),
        }

        wss = wss.get(ws_type, self.secret.get_wss_public(type.name))

        api_key = self.secret.get_api_key(type.name)
        api_secret = self.secret.get_secret(type.name)

        return ws(wss, api_key, api_secret)
