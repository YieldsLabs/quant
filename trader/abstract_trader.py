from abc import abstractmethod
from typing import Union
from core.abstract_event_manager import AbstractEventManager
from core.events.position import LongPositionOpened, ShortPositionOpened


class AbstractTrader(AbstractEventManager):
    @abstractmethod
    def trade(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        pass
