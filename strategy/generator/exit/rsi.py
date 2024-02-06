from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth

from .base import Exit, ExitType


@dataclass(frozen=True)
class RsiExit(Exit):
    type: ExitType = ExitType.Rsi
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    period: Parameter = RandomParameter(14.0, 30.0, 1.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
