from dataclasses import dataclass

from core.models.candle import CandleReversalType
from core.models.parameter import CategoricalParameter, Parameter
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CandlestickReversalSignal(Signal):
    type: SignalType = SignalType.CandlestickReversal
    candle: Parameter = CategoricalParameter(CandleReversalType)
