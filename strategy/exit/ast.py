from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.exit.base import BaseExit, ExitType


@dataclass(frozen=True)
class AstExit(BaseExit):
    type: ExitType = ExitType.Ast
    atr_period: Parameter = StaticParameter(12.0)
    multi: Parameter = StaticParameter(3.0)
