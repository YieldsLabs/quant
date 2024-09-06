from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class KstSignalLineSignal(Signal):
    type: SignalType = SignalType.KstSignalLine
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    roc_period_first: Parameter = StaticParameter(10.0)
    roc_period_second: Parameter = StaticParameter(15.0)
    roc_period_third: Parameter = StaticParameter(20.0)
    roc_period_fouth: Parameter = StaticParameter(30.0)
    period_first: Parameter = StaticParameter(10.0)
    period_second: Parameter = StaticParameter(10.0)
    period_third: Parameter = StaticParameter(10.0)
    period_fouth: Parameter = StaticParameter(15.0)
    signal_period: Parameter = StaticParameter(9.0)
