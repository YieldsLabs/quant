from dataclasses import dataclass
import re
from typing import Any, Tuple


@dataclass(frozen=True)
class Strategy:
    name: str
    parameters: Tuple[Any, ...]
    stop_loss_type: str
    stop_loss_parameters: Tuple[Any, ...]

    @property
    def hyperparameters(self):
        return list(self.parameters + self.stop_loss_parameters)

    @classmethod
    def from_label(cls, label: str) -> 'Strategy':
        def parse_params(params_str: str):
            return tuple([float(p) if '.' in p else int(p) for p in params_str.split(':')])

        pattern = r"_STRTG([A-Z]+)_([\d:.]+)_STPLSS([A-Z]+)_([\d:.]+)"
        matches = re.match(pattern, label)

        if not matches:
            raise ValueError(f"Label '{label}' does not match expected pattern")

        strategy_name = matches.group(1)
        strategy_params = parse_params(matches.group(2))

        stop_loss_type = matches.group(3)
        stop_loss_params = parse_params(matches.group(4))

        return cls(
            strategy_name.lower(),
            strategy_params,
            stop_loss_type,
            stop_loss_params
        )

    def __str__(self) -> str:
        strategy_name = self.name.upper()
        strategy_parameters = ':'.join(map(str, self.parameters))
        stop_loss_name = self.stop_loss_type.upper()
        sl_parameters = ':'.join(map(str, self.stop_loss_parameters))

        return f"_STRTG{strategy_name}_{strategy_parameters}_STPLSS{stop_loss_name}_{sl_parameters}"