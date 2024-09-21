from abc import ABC, abstractmethod

from core.events._base import Event
from core.interfaces.abstract_actor import AbstractActor


class EventPolicy(ABC):
    @abstractmethod
    def should_process(actor: AbstractActor, event: Event) -> bool:
        pass
