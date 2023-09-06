from dataclasses import dataclass
from typing import Tuple

from .indicator import Indicator


@dataclass(frozen=True)
class Strategy:
    name: str
    indicators: Tuple[Indicator, ...]
    stop_loss: Indicator

    @property
    def parameters(self):
        indicator_params = [item for indicator in self.indicators for item in [indicator.type.value, *indicator.parameters]]
        return indicator_params + list(self.stop_loss.parameters)

    def __str__(self) -> str:
        strategy_name = self.name.upper()
        indicator_params = [item for indicator in self.indicators for item in [str(indicator.type), *indicator.parameters]]
        strategy_parameters = ':'.join(map(str, indicator_params))
        stop_loss_name = str(self.stop_loss.type)
        sl_parameters = ':'.join(map(str, self.stop_loss.parameters))

        return f"_STRTG{strategy_name}_{strategy_parameters}_STPLSS{stop_loss_name}_{sl_parameters}"
    
    def __hash__(self) -> int:
        return hash(str(self))