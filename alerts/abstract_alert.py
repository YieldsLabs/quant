from abc import ABC, abstractmethod


class AbstractAlert(ABC):
    @abstractmethod
    def alert():
        pass