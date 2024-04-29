from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class AstExit(Exit):
    type: ExitType = ExitType.Ast
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    atr_period: Parameter = StaticParameter(12.0)
    factor: Parameter = StaticParameter(3.0)
