from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class RsiNeutralityConfirm(Confirm):
    type: Confirm = ConfirmType.RsiNeutrality
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    period: Parameter = StaticParameter(28.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
