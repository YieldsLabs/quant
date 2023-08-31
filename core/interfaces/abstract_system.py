from abc import abstractmethod

from .abstract_event_manager import AbstractEventManager


class AbstractSystem(AbstractEventManager):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
