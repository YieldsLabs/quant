from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position
from core.models.risk import Risk
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
        risk = Risk().next(signal.ohlcv)

        return Position(
            signal=signal,
            risk=risk,
            initial_size=size,
            expiration=self.config["trade_duration"] * 1000,
        )
