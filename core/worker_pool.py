import asyncio

from .events.base_event import EventEnded
from .event_worker import EventWorker
from .load_balancer import LoadBalancer
from .event_handler import EventHandler


class WorkerPool:
    def __init__(self, num_workers: int, num_priority_group: int, event_handler: EventHandler, cancel_event: asyncio.Event):
        self.workers = [EventWorker(event_handler, cancel_event) for _ in range(num_workers)]
        self.load_balancer = LoadBalancer(num_priority_group)

    async def dispatch_to_worker(self, priority: int, event: EventEnded, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(priority)
        await self.workers[priority_group].dispatch(event, *args, **kwargs)
