from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter

from .base import Exit, ExitType


@dataclass(frozen=True)
class MfiExit(Exit):
    type: ExitType = ExitType.Mfi
    period: Parameter = StaticParameter(14.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
