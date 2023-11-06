from broker.futures_broker import FuturesBroker
from core.interfaces.abstract_broker_factory import AbstractBrokerFactory
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.broker import BrokerType


class BrokerFactory(AbstractBrokerFactory):
    _broker_type = {BrokerType.FUTURES: FuturesBroker}

    def __init__(self):
        super().__init__()

    def create(self, type: BrokerType, exchange: AbstractExchange):
        if type not in self._broker_type:
            raise ValueError(f"Unknown Broker: {type}")

        broker_class = self._broker_type.get(type)

        return broker_class(exchange)
