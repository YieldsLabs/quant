import asyncio

from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_squad_factory import AbstractSquad


class Squad(AbstractSquad):
    def __init__(self, 
                 signal_actor: AbstractActor, position_actor: AbstractActor,
                 risk_actor: AbstractActor, executor_actor: AbstractActor):
        super().__init__()
        self.signal_actor = signal_actor
        self.position_actor = position_actor
        self.risk_actor = risk_actor
        self.executor_actor = executor_actor

    @property
    def symbol(self):
        return self.signal_actor.symbol
    
    @property
    def timeframe(self):
        return self.signal_actor.timeframe
    
    @property
    def strategy(self):
        return self.signal_actor.strategy

    async def start(self):
        await asyncio.gather(*[
            self.signal_actor.start(), self.position_actor.start(), self.risk_actor.start(), self.executor_actor.start()])

    async def stop(self):
        await asyncio.gather(*[
            self.signal_actor.stop(), self.position_actor.stop(), self.risk_actor.stop(), self.executor_actor.stop()])
