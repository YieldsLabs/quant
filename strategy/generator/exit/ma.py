from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, RandomParameter
from strategy.generator.exit.base import Exit, ExitType


@dataclass(frozen=True)
class MaExit(Exit):
    type: ExitType = ExitType.Ma
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(5.0, 13.0, 2.0)
