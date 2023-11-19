from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
)
from strategy.exit.base import BaseExit, ExitType


@dataclass(frozen=True)
class MovingAverageExit(BaseExit):
    type: ExitType = ExitType.Ma
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(15.0, 40.0, 5.0)
