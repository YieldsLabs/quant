from dataclasses import dataclass
from typing import Any, Tuple

from .indicator import Indicator


@dataclass(frozen=True)
class Strategy:
    name: str
    signal: Indicator
    filter: Indicator
    stop_loss: Indicator

    @property
    def parameters(self):
        signal_parameters = ([self.signal.type.value] if hasattr(self.signal.type, 'value') and self.signal.type.value else []) + list(self.signal.parameters)
        filter_parameters = ([self.filter.type.value] if hasattr(self.filter.type, 'value') and self.filter.type.value else []) + list(self.filter.parameters)
        stop_loss_parameters = ([self.stop_loss.type.value] if hasattr(self.stop_loss.type, 'value') and self.stop_loss.type.value else []) + list(self.stop_loss.parameters)
    
        return (signal_parameters, filter_parameters, list(self.stop_loss.parameters))

    def __str__(self) -> str:
        strategy_name = self.name.upper()
        
        indicator_params = [str(self.signal.type)] if hasattr(self.signal.type, 'value') else [] + self.signal.parameters
        strategy_parameters = ':'.join(map(str, indicator_params))

        filter_name = "NONE" if isinstance(self.filter.type, type(Any)) else str(self.filter.type)
        filter_parameters = ':'.join(map(str, self.filter.parameters))
        filter_parameters = '_' + filter_parameters if len(filter_parameters) > 0 else ''
        
        stop_loss_name = str(self.stop_loss.type)
        stop_loss_parameters = ':'.join(map(str, self.stop_loss.parameters))

        return f"_STRTG{strategy_name}_{strategy_parameters}_FLTR{filter_name}{filter_parameters}_STPLSS{stop_loss_name}_{stop_loss_parameters}"
    
    def __hash__(self) -> int:
        return hash(str(self))