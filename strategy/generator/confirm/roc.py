from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class RocConfirm(Confirm):
    type: Confirm = ConfirmType.Roc
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(21.0)
