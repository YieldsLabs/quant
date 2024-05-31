import asyncio
import logging
from typing import Union

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import SignalSide
from core.queries.copilot import EvaluateSession, EvaluateSignal
from core.queries.ohlcv import PrevBar

from ._prompt import signal_risk_prompt, system_prompt

CopilotEvent = Union[EvaluateSignal, EvaluateSession]

logger = logging.getLogger(__name__)


class CopilotActor(BaseActor, EventHandlerMixin):
    _EVENTS = [EvaluateSignal, EvaluateSession]

    def __init__(self, llm: AbstractLLMService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

        self.llm = llm

    async def on_receive(self, event: CopilotEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(EvaluateSignal, self._evaluate_signal)
        self.register_handler(EvaluateSession, self._evaluate_session)

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRiskType:
        signal = msg.signal

        curr_bar = signal.ohlcv
        prev_bar = await self.ask(PrevBar(signal.symbol, signal.timeframe, curr_bar))
        side = "LONG" if signal.side == SignalSide.BUY else "SHORT"

        prompt = signal_risk_prompt.format(
            curr_bar=curr_bar, prev_bar=prev_bar, side=side, timeframe=signal.timeframe
        )

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        risk_level_enum = SignalRiskType.from_string(answer)
        return risk_level_enum

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        await asyncio.sleep(0.1337)
        return SessionRiskType.CONTINUE
