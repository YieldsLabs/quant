import asyncio
import logging
import re
from typing import Union

from core.actors import BaseActor
from core.interfaces.abstract_llm_service import AbstractLLMService
from core.mixins import EventHandlerMixin
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.side import SignalSide
from core.models.signal_risk import SignalRisk
from core.queries.copilot import EvaluateSession, EvaluateSignal

from ._prompt import signal_risk_pattern, signal_risk_prompt, system_prompt

CopilotEvent = Union[EvaluateSignal, EvaluateSession]

logger = logging.getLogger(__name__)
LOOKBACK = 2


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

    async def _evaluate_signal(self, msg: EvaluateSignal) -> SignalRisk:
        signal = msg.signal

        curr_bar = signal.ohlcv
        prev_bar = msg.prev_bar
        side = "LONG" if signal.side == SignalSide.BUY else "SHORT"
        trend = msg.ta.trend
        osc = msg.ta.oscillator
        volatility = msg.ta.volatility

        prompt = signal_risk_prompt.format(
            curr_bar=curr_bar,
            prev_bar=prev_bar,
            side=side,
            timeframe=signal.timeframe,
            macd_histogram=trend.macd[-LOOKBACK:],
            rsi=osc.srsi[-LOOKBACK:],
            k=osc.k[-LOOKBACK:],
            bbp=volatility.bbp[-LOOKBACK:],
        )

        logger.info(f"Signal Prompt: {prompt}")

        answer = await self.llm.call(system_prompt, prompt)

        logger.info(f"LLM Answer: {answer}")

        match = re.search(signal_risk_pattern, answer)

        if not match:
            risk = SignalRisk(
                type=SignalRiskType.NONE,
            )
        else:
            risk = SignalRisk(
                type=SignalRiskType.from_string(match.group(1)),
                tp=float(match.group(2)),
                sl=float(match.group(3)),
            )

        logger.info(f"Signal Risk: {risk}")

        return risk

    async def _evaluate_session(self, msg: EvaluateSession) -> SessionRiskType:
        await asyncio.sleep(0.1337)
        return SessionRiskType.CONTINUE
