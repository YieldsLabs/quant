from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.models.exchange import ExchangeType
from core.models.ws import WSType
from exchange._bybit_ws import BybitWS


class WSFactory(AbstractExchangeFactory):
    _type = {WSType.BYBIT: BybitWS}

    def __init__(self, secret: AbstractSecretService):
        super().__init__()
        self.secret = secret

    def create(self, type: ExchangeType) -> AbstractExchange:
        if type not in self._type:
            raise ValueError(f"Unknown Exchange: {type}")

        ws = self._type.get(type)
        wss = self.secret.get_wss(type.name)

        return ws(wss)
