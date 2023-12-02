from dataclasses import dataclass
from enum import Enum, auto

import orjson as json

from .indicator import Indicator
from .parameter import Parameter


class StrategyType(Enum):
    TREND = auto()


class StrategyOptimizationType(Enum):
    GENETIC = auto()


@dataclass(frozen=True)
class Strategy:
    type: StrategyType
    entry: Indicator
    filter: Indicator
    pulse: Indicator
    baseline: Indicator
    stop_loss: Indicator
    exit: Indicator

    @property
    def parameters(self):
        signal_data = json.dumps(self.entry.to_dict())
        filter_data = json.dumps(self.filter.to_dict())
        pulse_data = json.dumps(self.pulse.to_dict())
        baseline_data = json.dumps(self.baseline.to_dict())
        stoploss_data = json.dumps(self.stop_loss.to_dict())
        exit_data = json.dumps(self.exit.to_dict())

        return (
            signal_data,
            filter_data,
            pulse_data,
            baseline_data,
            stoploss_data,
            exit_data,
        )

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
        entry_ = f"_SGNL{self.entry.type}:{self._format_parameters(self.entry)}"
        filter_ = f"_FLTR{self.filter.type}:{self._format_parameters(self.filter)}"
        pulse_ = f"_PLS{self.pulse.type}:{self._format_parameters(self.pulse)}"
        baseline_ = (
            f"_BSLN{self.baseline.type}:{self._format_parameters(self.baseline)}"
        )
        stop_loss = (
            f"_STPLSS{self.stop_loss.type}:{self._format_parameters(self.stop_loss)}"
        )
        exit_ = f"_EXT{self.exit.type}:{self._format_parameters(self.exit)}"

        return entry_ + filter_ + pulse_ + baseline_ + stop_loss + exit_
