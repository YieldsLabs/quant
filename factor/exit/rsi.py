from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class RsiExit(Exit):
    type: ExitType = ExitType.Rsi
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    period: Parameter = StaticParameter(8.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
