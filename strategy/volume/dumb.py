from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.volume.base import BaseVolume, VolumeType


@dataclass(frozen=True)
class DumbVolume(BaseVolume):
    type: VolumeType = VolumeType.Dumb
    period: Parameter = StaticParameter(10.0)
