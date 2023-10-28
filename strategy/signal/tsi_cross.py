from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TSICrossSignal(BaseSignal):
    type: SignalType = SignalType.TsiCross
    long_period: Parameter = StaticParameter(25.0)
    short_period: Parameter = StaticParameter(13.0)
    signal_period: Parameter = StaticParameter(13.0)
