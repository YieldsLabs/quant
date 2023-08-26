import asyncio
from collections import namedtuple

from core.commands.actor import PositionRiskActorStart, PositionRiskActorStop, SignalActorStart, SignalActorStop
from core.event_decorators import command_handler
from core.interfaces.abstract_event_manager import AbstractEventManager

from .position_risk_actor_factory import PositionRiskActorFactory
from .signal_actor_factory import SignalActorFactory

ActorKey = namedtuple('ActorKey', ['symbol', 'timeframe'])

class Supervisor(AbstractEventManager):
    def __init__(self, 
                 signal_factory: SignalActorFactory,
                 position_risk_factory: PositionRiskActorFactory
        ):
        super().__init__()
        self.signal_factory = signal_factory
        self.position_risk_factory = position_risk_factory
        self.signal_lock = asyncio.Lock()
        self.risk_lock = asyncio.Lock()
        self.signal_actors = {}
        self.risk_actors = {}

    @command_handler(SignalActorStart)
    async def _create_signal_actor(self, command: SignalActorStart):
        key = ActorKey(command.symbol, command.timeframe)

        async with self.signal_lock:
            if key in self.signal_actors:
                print("Actor for this symbol and timeframe is already running.")
                return
            
            actor = self.signal_factory.create_actor(command.symbol, command.timeframe, command.wasm_path, command.strategy_name, command.strategy_parameters)

            await actor.start()

            print('Signal actor start')
            
            self.signal_actors[key] = actor

    @command_handler(PositionRiskActorStart)
    async def _create_position_risk_actor(self, command: PositionRiskActorStart):
        key = ActorKey(command.position.signal.symbol, command.position.signal.timeframe)

        async with self.risk_lock:
            if key in self.risk_actors:
                print("Actor for this position is already running.")
                return
            
            actor = self.position_risk_factory.create_actor(command.position)

            await actor.start()

            self.risk_actors[key] = actor

    @command_handler(SignalActorStop)
    async def _stop_signal_actor(self, command: SignalActorStop):
        key = ActorKey(command.symbol, command.timeframe)

        async with self.signal_lock:
            actor = self.signal_actors.get(key)
            
            if actor:
                if await actor.running:
                    await actor.stop()
                del self.signal_actors[key]

                print('Signal actor stop')

    @command_handler(PositionRiskActorStop)
    async def _handle_stop_position_risk_actor(self, command: PositionRiskActorStop):      
        key = ActorKey(command.position.signal.symbol, command.position.signal.timeframe)
        
        async with self.risk_lock:
            actor = self.risk_actors.get(key)
            
            if actor:
                if await actor.running:
                    await actor.stop()
                
                del self.risk_actors[key]


