from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MaTestingGroundSignal(Signal):
    type: SignalType = SignalType.MaTestingGround
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = StaticParameter(100.0)
