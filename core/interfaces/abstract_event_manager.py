from abc import ABC

from core.event_decorators import eda


@eda
class AbstractEventManager(ABC):
    pass
