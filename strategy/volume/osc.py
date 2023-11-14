from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.volume.base import BaseVolume, VolumeType


@dataclass(frozen=True)
class OSCVolume(BaseVolume):
    type: VolumeType = VolumeType.Osc
    short_period: Parameter = StaticParameter(5.0)
    long_period: Parameter = StaticParameter(10.0)
