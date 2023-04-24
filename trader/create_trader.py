from typing import Type
from broker.abstract_broker import AbstractBroker
from trader.abstract_trader import AbstractTrader
from trader.live_trader import LiveTrader
from trader.paper_trader import PaperTrader


def create_trader(broker: Type[AbstractBroker], live_trading: bool = False) -> AbstractTrader:
    if live_trading:
        return LiveTrader(broker)
    else:
        return PaperTrader()
