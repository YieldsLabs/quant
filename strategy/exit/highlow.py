from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.exit.base import BaseExit, ExitType


@dataclass(frozen=True)
class HighLowExit(BaseExit):
    type: ExitType = ExitType.HighLow
    period: Parameter = StaticParameter(5.0)
