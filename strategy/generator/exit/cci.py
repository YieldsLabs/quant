from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class CciExit(Exit):
    type: ExitType = ExitType.Cci
    source_type: Parameter = StaticParameter(SourceType.HLC3)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(8.0)
    factor: Parameter = StaticParameter(0.015)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
