
from abc import ABC

from core.event_dispatcher import eda

@eda
class AbstractEventManager(ABC):
    pass