import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.entity.ohlcv import OHLCV
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

        model, scaler = self._create_model(ta, signal.ohlcv)

        position_risk = PositionRisk(model=model, scaler=scaler).next(signal.ohlcv)
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

    @staticmethod
    def _create_model(ta: TechAnalysis, ohlcv: OHLCV):
        model = SGDRegressor(
            max_iter=1984,
            tol=None,
            warm_start=True,
            alpha=0.001,
            penalty="elasticnet",
            l1_ratio=0.69,
        )

        scaler = StandardScaler()

        hlcc4 = np.array(
            ta.trend.hlcc4 + [(ohlcv.high + ohlcv.low + 2 * ohlcv.close) / 4.0]
        )

        hlcc4_lagged_1 = np.roll(hlcc4, 1)
        hlcc4_lagged_1[0] = hlcc4[0]

        hlcc4_lagged_2 = np.roll(hlcc4, 2)
        hlcc4_lagged_2[:2] = hlcc4[:2]

        close = np.array(ta.trend.close + [ohlcv.close])

        current_tr = max(
            ohlcv.high - ohlcv.low,
            abs(ohlcv.high - ta.trend.close[-1]),
            abs(ohlcv.low - ta.trend.close[-1]),
        )

        true_range = np.array(ta.volatility.tr + [current_tr])

        true_range_lagged_1 = np.roll(true_range, 1)
        true_range_lagged_1[0] = true_range[0]

        true_range_lagged_2 = np.roll(true_range, 2)
        true_range_lagged_2[:2] = true_range[:2]

        features = np.column_stack(
            (
                hlcc4[:-2],
                hlcc4_lagged_1[:-2],
                hlcc4_lagged_2[:-2],
                true_range[:-2],
                true_range_lagged_1[:-2],
                true_range_lagged_2[:-2],
                hlcc4[2:] - hlcc4_lagged_1[2:],
                true_range[2:] - true_range_lagged_1[2:],
            )
        )

        target = close[2:]

        features_scaled = scaler.fit_transform(features)

        model.fit(features_scaled, target)

        return model, scaler
