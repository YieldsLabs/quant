from typing import Optional

from core.models.risk_type import SignalRiskType

from ._base import Entity


@Entity
class SignalRisk:
    type: SignalRiskType = SignalRiskType.NONE
    tp: Optional[float] = None
    sl: Optional[float] = None
