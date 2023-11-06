import json
from dataclasses import dataclass
from enum import Enum, auto

from .indicator import Indicator
from .parameter import Parameter


class StrategyType(Enum):
    TREND = auto()


class StrategyOptimizationType(Enum):
    GENETIC = auto()


@dataclass(frozen=True)
class Strategy:
    type: StrategyType
    entry_signal: Indicator
    regime_filter: Indicator
    stop_loss: Indicator
    exit_signal: Indicator

    @property
    def parameters(self):
        signal_data = json.dumps(self.entry_signal.to_dict()).encode()
        filter_data = json.dumps(self.regime_filter.to_dict()).encode()
        stoploss_data = json.dumps(self.stop_loss.to_dict()).encode()
        exit_data = json.dumps(self.exit_signal.to_dict()).encode()

        return (signal_data, filter_data, stoploss_data, exit_data)

    def _format_parameters(self, indicator):
        formatted_values = []
        for k, v in indicator.__dict__.items():
            if k != "type":
                if (
                    isinstance(v, Parameter)
                    and isinstance(v.value, float)
                    and v.value.is_integer()
                ):
                    formatted_values.append(str(int(v.value)))
                else:
                    formatted_values.append(str(v))
        parameters = ":".join(formatted_values)
        return parameters if parameters else "NONE"

    def __str__(self) -> str:
        entry_ = f"_SGNL{self.entry_signal.type}:{self._format_parameters(self.entry_signal)}"
        filter_ = f"_FLTR{self.regime_filter.type}:{self._format_parameters(self.regime_filter)}"
        stop_loss = (
            f"_STPLSS{self.stop_loss.type}:{self._format_parameters(self.stop_loss)}"
        )
        exit_ = (
            f"_EXIT{self.exit_signal.type}:{self._format_parameters(self.exit_signal)}"
        )

        return entry_ + filter_ + stop_loss + exit_
