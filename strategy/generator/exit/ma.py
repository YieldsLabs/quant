from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
)

from .base import Exit, ExitType


@dataclass(frozen=True)
class MaExit(Exit):
    type: ExitType = ExitType.Ma
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(15.0, 40.0, 5.0)