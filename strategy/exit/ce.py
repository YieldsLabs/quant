from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.exit.base import BaseExit, ExitType


@dataclass(frozen=True)
class ChExit(BaseExit):
    type: ExitType = ExitType.Ch
    period: Parameter = StaticParameter(22.0)
    atr_period: Parameter = StaticParameter(14.0)
    multi: Parameter = StaticParameter(3.0)
