from typing import Union
from core.tasks.feed import StartHistoricalFeed, StartRealtimeFeed

from .event import EventPolicy

FeedEvent = Union[StartHistoricalFeed, StartRealtimeFeed]

class FeedPolicy(EventPolicy):
    @classmethod
    def should_process(cls, actor, event: FeedEvent) -> bool:
        return (
            event.symbol == actor.symbol
            and event.timeframe == actor.timeframe
            and event.datasource == actor.datasource
        )
