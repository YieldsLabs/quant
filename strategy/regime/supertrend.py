from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class SupertrendFilter(BaseRegime):
    type: FilterType = FilterType.Supertrend
    atr_period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(3.0)
