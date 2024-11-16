from dataclasses import dataclass

from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.models.datasource_type import DataSourceType
from infrastructure.config import ConfigService


@dataclass(frozen=True)
class SystemContext:
    signal_factory: AbstractSignalActorFactory
    position_factory: AbstractPositionActorFactory
    risk_factory: AbstractRiskActorFactory
    executor_factory: AbstractExecutorActorFactory
    feed_factory: AbstractFeedActorFactory
    datasource: DataSourceType
    config_service: ConfigService
