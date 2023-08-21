from abc import ABC

from ..event_decorators import eda


@eda
class AbstractEventManager(ABC):
    pass
