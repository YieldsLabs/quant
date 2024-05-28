from typing import Any

from .event import EventPolicy


class StrategyPolicy(EventPolicy):
    @classmethod
    def should_process(cls, actor, event) -> bool:
        symbol, timeframe = cls._get_event_key(event)
        return actor.symbol == symbol and actor.timeframe == timeframe

    @classmethod
    def _get_event_key(event: Any):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal
            if hasattr(event, "position")
            else event
        )
        return (signal.symbol, signal.timeframe)
