from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import SmoothATR
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class AstExit(Exit):
    type: ExitType = ExitType.Ast
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(12.0)
    factor: Parameter = StaticParameter(3.0)
