from dataclasses import dataclass
from enum import Enum

from .indicator import Indicator
from .parameter import Parameter


@dataclass(frozen=True)
class Strategy:
    name: str
    signal: Indicator
    filter: Indicator
    stop_loss: Indicator

    @property
    def parameters(self):
        def process_parameters(param):
            if isinstance(param, Enum):
                return float(param.value)
            if isinstance(param, Parameter):
                return float(param.value)

        def serialize_parameters(obj):
            return [process_parameters(p) for p in obj.parameters]

        signal_parameters = serialize_parameters(self.signal)
        filter_parameters = serialize_parameters(self.filter)
        stop_loss_parameters = serialize_parameters(self.stop_loss)

        return (signal_parameters, filter_parameters, stop_loss_parameters[1:])

    def __str__(self) -> str:
        def process_parameters(param):
            if isinstance(param, Enum):
                return str(param)
            if isinstance(param, Parameter):
                if param.value.is_integer():
                    return int(param.value)
                return float(param.value)

        def serialize_parameters(obj):
            return [process_parameters(p) for p in obj.parameters]

        strategy_name = self.name.upper()

        signal = serialize_parameters(self.signal)
        signal_parameters = ":".join(map(str, signal))

        filter = serialize_parameters(self.filter)

        filter_name = filter[0] if len(filter) > 0 else "NONE"
        filter_parameters = ":".join(map(str, filter[1:]))
        filter_parameters = (
            "_" + filter_parameters if len(filter_parameters) > 0 else ""
        )

        stop_loss = serialize_parameters(self.stop_loss)
        stop_loss_name = stop_loss[0]
        stop_loss_parameters = ":".join(map(str, stop_loss[1:]))

        return f"_STRTG{strategy_name}_{signal_parameters}_FLTR{filter_name}{filter_parameters}_STPLSS{stop_loss_name}_{stop_loss_parameters}"
