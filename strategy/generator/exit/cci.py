from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth

from .base import Exit, ExitType


@dataclass(frozen=True)
class CciExit(Exit):
    type: ExitType = ExitType.Cci
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(0.015)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
