from typing import Type

from core.interfaces.abstract_broker import AbstractBroker
from core.interfaces.abstract_trader import AbstractTrader

from .live_trader import LiveTrader
from .paper_trader import PaperTrader


def create_trader(broker: Type[AbstractBroker], slippage: float = 0.001, live_trading: bool = False) -> AbstractTrader:
    if live_trading:
        return LiveTrader(broker)
    else:
        return PaperTrader(slippage)
