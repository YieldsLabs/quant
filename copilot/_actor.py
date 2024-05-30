import asyncio
import logging
from typing import Union

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import SignalSide
from core.queries.copilot import EvaluateSession, EvaluateSignal

from ._prompt import signal_risk_prompt, system_prompt

CopilotEvent = Union[EvaluateSignal, EvaluateSession]

logger = logging.getLogger(__name__)


class CopilotActor(BaseActor, EventHandlerMixin):
    _EVENTS = [EvaluateSignal, EvaluateSession]

    def __init__(self, llm: AbstractLLMService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self.llm = llm

        self.register_handler(EvaluateSignal, self._evaluate_signal)
        self.register_handler(EvaluateSession, self._evaluate_session)

    async def on_receive(self, event: CopilotEvent):
        return await self.handle_event(event)

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRiskType:
        signal = msg.signal
        side = "LONG" if signal.side == SignalSide.BUY else "SHORT"
        prompt = signal_risk_prompt.format(current_bar=str(signal.ohlcv), side=side)

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        risk_level_enum = SignalRiskType.from_string(answer)
        return risk_level_enum

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        await asyncio.sleep(0.1337)
        return SessionRiskType.CONTINUE
