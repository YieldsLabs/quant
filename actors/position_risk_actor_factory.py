from core.interfaces.abstract_position_risk_actor_factory import AbstractPositionRiskActorFactory
from core.models.position import Position

from .position_risk_actor import PositionRiskActor


class PositionRiskActorFactory(AbstractPositionRiskActorFactory):
    def __init__(self, risk_buffer: float, event_cooldown: float):
        self.risk_buffer = risk_buffer
        self.event_cooldown = event_cooldown
    
    def create_actor(self, position: Position):
        return PositionRiskActor(
            position,
            self.risk_buffer,
            self.event_cooldown,
        )
        
