from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position
from core.models.position_risk import PositionRisk
from core.models.risk_type import SignalRiskType
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
        signal_risk_type: SignalRiskType,
    ) -> Position:
        size = await self.size_strategy.calculate(signal)
        position_risk = PositionRisk().next(signal.ohlcv)

        return Position(
            signal=signal,
            signal_risk_type=signal_risk_type,
            position_risk=position_risk,
            initial_size=size,
            expiration=self.config["trade_duration"] * 1000,
        )
