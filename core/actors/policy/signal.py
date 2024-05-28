from core.actors import StrategyActor
from core.events.ohlcv import NewMarketDataReceived

from .event import EventPolicy


class SignalPolicy(EventPolicy):
    @classmethod
    def should_process(cls, actor: StrategyActor, event: NewMarketDataReceived) -> bool:
        return (
            event.symbol == actor.symbol
            and event.timeframe == actor.timeframe
            and event.closed
        )
