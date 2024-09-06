from dataclasses import dataclass

from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.exchange import ExchangeType
from infrastructure.config import ConfigService


@dataclass(frozen=True)
class SystemContext:
    signal_factory: AbstractSignalActorFactory
    position_factory: AbstractPositionActorFactory
    risk_factory: AbstractRiskActorFactory
    executor_factory: AbstractExecutorActorFactory
    feed_factory: AbstractFeedActorFactory
    strategy_generator_factory: AbstractStrategyGeneratorFactory
    strategy_optimizer_factory: AbstractStrategyOptimizerFactory
    exchange_type: ExchangeType
    config_service: ConfigService
