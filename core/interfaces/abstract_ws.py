from abc import abstractmethod

from core.interfaces.abstract_event_manager import AbstractEventManager


class AbstractWS(AbstractEventManager):
    @abstractmethod
    def run(self):
        pass
