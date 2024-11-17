from typing import Tuple, Union

from coral import DataSourceFactory
from core.actors import BaseActor
from core.commands.factor import EnvolveGeneration, InitGeneration
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.timeframe import Timeframe
from core.queries.broker import GetSymbols
from core.queries.factor import GetGeneration

from .generator import PopulationGenerator

FactorEvent = Union[InitGeneration, GetGeneration, EnvolveGeneration]


class FactorActor(BaseActor, EventHandlerMixin):
    def __init__(self, datasource: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.datasource = datasource
        self.config = config_service.get("factor")
        self.population = []
        self.generation = 0

    async def on_receive(self, event: FactorEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(InitGeneration, self._init_generation)
        self.register_handler(GetGeneration, self._get_generation)
        self.register_handler(EnvolveGeneration, self._envolve_generation)

    async def _init_generation(self, msg: InitGeneration):
        self.population = []
        self.generation = 0

        symbols = await self.ask(GetSymbols(msg.datasource, msg.cap))

        timeframes = [
            Timeframe.from_raw(timeframe)
            for timeframe in self.config.get("timeframes", ["15m"])
        ]

        generator = PopulationGenerator(
            symbols, timeframes, self.config.get("n_samples", 2)
        )
        
        for individual in generator:
            self.population.append(individual)

    async def _get_generation(self, _msg: GetGeneration) -> Tuple[list, float]:
        population = [(i.symbol, i.timeframe, i.strategy) for i in self.population]

        return (population, self.generation)

    async def _envolve_generation(self, _msg: EnvolveGeneration):
        self.generation += 1
