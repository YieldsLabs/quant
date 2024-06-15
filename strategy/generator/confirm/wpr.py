from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class WprConfirm(Confirm):
    type: Confirm = ConfirmType.Wpr
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(14.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
