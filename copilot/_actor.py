from typing import Any

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.models.risk_type import SignalRiskType

system_prompt = "You are an effective quantitative analysis assistant. Your job is to help interpret data, perform statistical analyses, technical analyses and provide insights based on numerical information."
signal_risk_prompt = """
Candlestick data provided: Type=BULLISH, Open=9.609, High=9.638, Low=9.609, Close=9.634, Real_Body=0.02500000, Upper_Shadow=0.00400000, Lower_Shadow=0.00000000
Make a decision about Risk Level based on the candlestick data. Choose from: NONE, LOW, MODERATE, or HIGH.
Return only the decision about the Risk Level.
"""

CopilotEvent = Any


class CopilotActor(BaseActor):
    _EVENTS = []

    def __init__(self, repository: AbstractMarketRepository, llm: AbstractLLMService):
        super().__init__()
        self.llm = llm
        self.repository = repository

    async def on_receive(self, msg: CopilotEvent):
        answer = self.llm.call(system_prompt, signal_risk_prompt)
        risk_level_enum = SignalRiskType.from_string(answer)

        print(risk_level_enum)
