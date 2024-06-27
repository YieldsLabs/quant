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
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(14.0)
    smooth_signal: Parameter = StaticParameter(Smooth.EMA)
    period_signal: Parameter = StaticParameter(7.0)
