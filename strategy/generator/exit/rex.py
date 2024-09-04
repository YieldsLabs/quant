from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class RexExit(Exit):
    type: ExitType = ExitType.Rex
    source: Parameter = StaticParameter(SourceType.HL2)
    smooth: Parameter = StaticParameter(Smooth.LSMA)
    period: Parameter = StaticParameter(10.0)
    smooth_signal: Parameter = StaticParameter(Smooth.TEMA)
    period_signal: Parameter = StaticParameter(5.0)
