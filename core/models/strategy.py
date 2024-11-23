from dataclasses import dataclass
from enum import Enum, auto

from .indicator import Indicator
from .parameter import Parameter


class StrategyOptimizationType(Enum):
    GENETIC = auto()


@dataclass(frozen=True)
class Strategy:
    signal: Indicator
    confirm: Indicator
    pulse: Indicator
    baseline: Indicator
    exit: Indicator

    @property
    def parameters(self):
        return (
            self.signal.to_dict(),
            self.confirm.to_dict(),
            self.pulse.to_dict(),
            self.baseline.to_dict(),
            self.exit.to_dict(),
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
        signal_ = f"_SGNL{self.signal.type}:{self._format_parameters(self.signal)}"
        confirm_ = f"_CNFRM{self.confirm.type}:{self._format_parameters(self.confirm)}"
        pulse_ = f"_PLS{self.pulse.type}:{self._format_parameters(self.pulse)}"
        baseline_ = (
            f"_BSLN{self.baseline.type}:{self._format_parameters(self.baseline)}"
        )
        exit_ = f"_EXT{self.exit.type}:{self._format_parameters(self.exit)}"

        return f"{signal_}{confirm_}{pulse_}{baseline_}{exit_}"

    def __hash__(self) -> int:
        return hash(str(self))
