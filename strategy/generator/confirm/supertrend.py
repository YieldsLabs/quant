from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class SupertrendConfirm(Confirm):
    type: Confirm = ConfirmType.Sup
    source_type: Parameter = StaticParameter(SourceType.HL2)
    atr_period: Parameter = StaticParameter(10.0)
    factor: Parameter = StaticParameter(3.0)
