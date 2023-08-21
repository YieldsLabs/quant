from abc import abstractmethod
from typing import Union

from .abstract_event_manager import AbstractEventManager

from ..events.position import LongPositionOpened, ShortPositionOpened


class AbstractTrader(AbstractEventManager):
    @abstractmethod
    def trade(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        pass
