from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position
from core.models.position_risk import PositionRisk
from core.models.profit_target import ProfitTarget
from core.models.signal import Signal
from core.models.signal_risk import SignalRisk
from core.models.ta import TechAnalysis


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
        signal_risk: SignalRisk,
        ta: TechAnalysis,
    ) -> Position:
        size = await self.size_strategy.calculate(signal)
        position_risk = PositionRisk().next(signal.ohlcv)
        profit_target = ProfitTarget(
            signal.side, signal.ohlcv.close, ta.volatility.yz[-1]
        )

        return Position(
            signal=signal,
            signal_risk=signal_risk,
            position_risk=position_risk,
            initial_size=size,
            profit_target=profit_target,
            expiration=self.config["trade_duration"] * 1000,
        )
