from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.source import SourceType

from .base import BaseLine, BaseLineType


@dataclass(frozen=True)
class MaBaseLine(BaseLine):
    type: BaseLineType = BaseLineType.Ma
    source: Parameter = StaticParameter(SourceType.CLOSE)
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(12.0, 16.0)
