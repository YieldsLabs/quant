import asyncio

from .events.base_event import Event
from .event_worker import EventWorker
from .load_balancer import LoadBalancer
from .event_handler import EventHandler


class WorkerPool:
    def __init__(self, num_workers: int, num_priority_group: int, event_handler: EventHandler, cancel_event: asyncio.Event):
        self.workers = [EventWorker(event_handler, cancel_event) for _ in range(num_workers)]
        self.load_balancer = LoadBalancer(num_priority_group)

    async def dispatch_to_worker(self, event: Event, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(event.meta.priority)
        await self.workers[priority_group].dispatch(event, *args, **kwargs)

    async def wait(self) -> None:
        for worker in self.workers:
            await worker.wait()
