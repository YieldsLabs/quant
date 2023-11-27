from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, RandomParameter
from strategy.baseline.base import BaseLine, BaseLineType


@dataclass(frozen=True)
class MaBaseLine(BaseLine):
    type: BaseLineType = BaseLineType.Ma
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(15.0, 40.0, 5.0)
