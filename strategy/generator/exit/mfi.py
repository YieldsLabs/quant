from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter

from .base import Exit, ExitType


@dataclass(frozen=True)
class MfiExit(Exit):
    type: ExitType = ExitType.Mfi
    period: Parameter = StaticParameter(6.0)
    threshold: Parameter = RandomParameter(0.0, 2.0, 1.0)
