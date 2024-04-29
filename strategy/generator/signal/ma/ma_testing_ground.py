from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MaTestingGroundSignal(Signal):
    type: SignalType = SignalType.MaTestingGround
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = StaticParameter(100.0)
