from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from strategy.signal.base import BaseSignal


@dataclass(frozen=True)
class SupertrendFlipSignal(BaseSignal):
    atr_period: Parameter = RandomParameter(15.0, 25.0, 5.0)
    factor: Parameter = RandomParameter(2.0, 5.0, 1.0)

    @property
    def parameters(self):
        return [self.atr_period, self.factor]
