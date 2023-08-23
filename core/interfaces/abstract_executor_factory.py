from abc import ABC, abstractmethod

from .abstract_executor import AbstractExecutor


class AbstractExecutorFactory(ABC):
    @abstractmethod
    def create_executor(self, live: bool) -> AbstractExecutor:
        pass
