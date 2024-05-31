from dataclasses import dataclass
from typing import Optional

from core.models.risk_type import SignalRiskType


@dataclass(frozen=True)
class SignalRisk:
    type: SignalRiskType = SignalRiskType.NONE
    tp: Optional[float] = None
    sl: Optional[float] = None

    def to_dict(self):
        return {
            "type": self.type,
            "tp": self.tp,
            "sl": self.sl,
        }

    def __str__(self):
        return f"type={self.type}, tp={self.tp}, sl={self.sl}"

    def __repr__(self):
        return f"SignalRisk({self})"
