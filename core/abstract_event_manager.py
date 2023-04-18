from abc import ABC

from .event_dispatcher import eda

@eda
class AbstractEventManager(ABC):
    pass