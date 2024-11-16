from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.source import SourceType

from .base import Exit, ExitType


@dataclass(frozen=True)
class MadExit(Exit):
    type: ExitType = ExitType.Mad
    source: Parameter = StaticParameter(SourceType.CLOSE)
    period_fast: Parameter = StaticParameter(8.0)
    period_slow: Parameter = StaticParameter(23.0)
