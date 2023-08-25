from abc import ABC, abstractmethod

from .abstract_actor import AbstractActor
from ..models.position import Position


class AbstractPositionRiskActorFactory(ABC):
    @abstractmethod
    def create_actor(self, position: Position) -> AbstractActor:
        pass
