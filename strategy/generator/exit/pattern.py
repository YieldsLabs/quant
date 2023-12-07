from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Exit, ExitType


@dataclass(frozen=True)
class PatternExit(Exit):
    type: ExitType = ExitType.Pattern
    period: Parameter = StaticParameter(5.0)
