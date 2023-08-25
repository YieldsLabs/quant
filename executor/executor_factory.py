from typing import Type

from core.interfaces.abstract_broker import AbstractBroker
from core.interfaces.abstract_executor import AbstractExecutor
from core.interfaces.abstract_executor_factory import AbstractExecutorFactory

from .live_executor import LiveExecutor
from .paper_executor import PaperExecutor

class ExecutorFactory(AbstractExecutorFactory):
    def __init__(self, broker: AbstractBroker, slippage: float):
        self.broker = broker
        self.slippage = slippage

    def create_executor(self, live: bool = False) -> AbstractExecutor:
        if live:
            return LiveExecutor(self.broker)
        else:
            return PaperExecutor(self.slippage)
