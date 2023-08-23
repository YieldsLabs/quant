from dataclasses import dataclass
import re
from typing import Any, List

from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class Strategy:
    symbol: str
    timeframe: Timeframe
    name: str
    parameters: List[Any]
    stop_loss_type: str
    stop_loss_parameters: List[Any]

    @property
    def hyperparameters(self) -> List[Any]:
        return self.parameters + [self.stop_loss_type] + [self.stop_loss_parameters]

    @classmethod
    def from_label(cls, label: str) -> 'Strategy':
        def parse_params(params_str: str):
            return [float(p) if '.' in p else int(p) for p in params_str.split(':')]
    
        def parse_timeframe(input_string):
            for timeframe in Timeframe:
                if str(timeframe) == input_string:
                    return timeframe

        pattern = r"([A-Z\d]+)_(\d+[smhd])_STRTG([A-Z]+)_([\d:.]+)_STPLSS([A-Z]+)_([\d:.]+)"
        matches = re.match(pattern, label)

        symbol = matches.group(1)
        timeframe = matches.group(2)

        strategy_name = matches.group(3)
        strategy_params = parse_params(matches.group(4))

        stop_loss_type = matches.group(5)
        stop_loss_params = parse_params(matches.group(6))

        return cls(
            symbol,
            parse_timeframe(timeframe),
            strategy_name.lower(),
            strategy_params,
            stop_loss_type,
            stop_loss_params
        )
    
    def __hash__(self):
        return hash((self.symbol, self.timeframe, self.name, tuple(self.parameters), self.stop_loss_type, tuple(self.stop_loss_parameters)))
    
    def __str__(self) -> str:
        strategy_name = self.name.upper()
        strategy_parameters = ':'.join(map(str, self.parameters))
        stop_loss_name = self.stop_loss_type.upper()
        sl_parameters = ':'.join(map(str, self.stop_loss_parameters))

        return f"{self.symbol}_{self.timeframe}_STRTG{strategy_name}_{strategy_parameters}_STPLSS{stop_loss_name}_{sl_parameters}"
