from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position
from core.models.signal import Signal


class PositionFactory(AbstractPositionFactory):
    def __init__(
        self,
        config_service: AbstractConfig,
        size_strategy: AbstractOrderSizeStrategy,
    ):
        super().__init__()
        self.size_strategy = size_strategy
        self.config = config_service.get("position")

    async def create(
        self,
        signal: Signal,
    ) -> Position:
        size = await self.size_strategy.calculate(signal)

        return Position.from_signal(
            signal,
            size,
            self.config["trade_duration"] * 1000,
        )
