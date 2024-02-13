from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, RandomParameter

from .base import BaseLine, BaseLineType


@dataclass(frozen=True)
class MaBaseLine(BaseLine):
    type: BaseLineType = BaseLineType.Ma
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(5.0, 40.0, 5.0)
