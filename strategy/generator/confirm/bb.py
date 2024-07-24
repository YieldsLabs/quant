from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class BbConfirm(Confirm):
    type: Confirm = ConfirmType.BbC
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(2.0)