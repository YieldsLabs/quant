from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class RsiSignalLineConfirm(Confirm):
    type: Confirm = ConfirmType.RsiSignalLine
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    period: Parameter = StaticParameter(18.0)
    smooth_signal: Parameter = StaticParameter(Smooth.HMA)
    smooth_period: Parameter = StaticParameter(10.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
