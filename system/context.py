from dataclasses import dataclass

from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_squad_factory import AbstractSquadFactory
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.exchange import ExchangeType
from core.models.strategy import StrategyType
from infrastructure.config import ConfigService


@dataclass(frozen=True)
class SystemContext:
    squad_factory: AbstractSquadFactory
    executor_factory: AbstractExecutorActorFactory
    strategy_generator_factory: AbstractStrategyGeneratorFactory
    strategy_optimizer_factory: AbstractStrategyOptimizerFactory
    exchange_type: ExchangeType
    strategy_type: StrategyType
    config_service: ConfigService
