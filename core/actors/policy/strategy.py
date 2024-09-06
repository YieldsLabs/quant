from typing import Any

from .event import EventPolicy


class StrategyPolicy(EventPolicy):
    @classmethod
    def should_process(cls, actor, event) -> bool:
        symbol, timeframe = cls._get_event_key(event)
        return actor.symbol == symbol and actor.timeframe == timeframe

    @classmethod
    def _get_event_key(cls, event: Any):
        key = cls._extract_key(event)

        if not all(hasattr(key, attr) for attr in ("symbol", "timeframe")):
            raise AttributeError("Key does not have 'symbol' or 'timeframe' attributes")

        return key.symbol, key.timeframe

    @staticmethod
    def _extract_key(event: Any):
        if hasattr(event, "signal"):
            return event.signal
        elif hasattr(event, "position") and hasattr(event.position, "signal"):
            return event.position.signal

        return event
