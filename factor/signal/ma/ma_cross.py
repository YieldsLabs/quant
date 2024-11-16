from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MaCrossSignal(Signal):
    type: SignalType = SignalType.MaCross
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(10.0, 20.0, 5.0)
