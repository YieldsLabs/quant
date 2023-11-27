from dataclasses import dataclass

from core.interfaces.abstract_broker_factory import AbstractBrokerFactory
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_squad_factory import AbstractSquadFactory
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.exchange import ExchangeType
from core.models.lookback import Lookback
from core.models.strategy import StrategyType


@dataclass(frozen=True)
class SystemContext:
    broker_factory: AbstractBrokerFactory
    exchange_factory: AbstractExchangeFactory
    squad_factory: AbstractSquadFactory
    executor_factory: AbstractExecutorActorFactory
    strategy_generator_factory: AbstractStrategyGeneratorFactory
    strategy_optimizer_factory: AbstractStrategyOptimizerFactory
    strategy_type: StrategyType
    exchange_type: ExchangeType
    in_sample: Lookback
    out_sample: Lookback
    active_strategy_num: int
    parallel_num: int
    leverage: int
    is_live: bool
