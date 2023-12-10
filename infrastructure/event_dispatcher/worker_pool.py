import asyncio

from core.events.base import Event

from .event_handler import EventHandler
from .event_worker import EventWorker
from .load_balancer import LoadBalancer


class WorkerPool:
    def __init__(self, num_workers: int, num_priority_groups: int, event_handler: EventHandler, cancel_event: asyncio.Event):
        self.events_in_queue = set()
        self.workers = [EventWorker(event_handler, cancel_event, self.events_in_queue) for _ in range(num_workers)]
        self.load_balancer = LoadBalancer(num_priority_groups)
        self.priority_to_worker_map = {i: i % num_workers for i in range(num_priority_groups)}

    async def dispatch_to_worker(self, event: Event, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(event.meta.priority)
        worker_index = self.priority_to_worker_map[priority_group]
        
        await self.workers[worker_index].dispatch(event, *args, **kwargs)
        self.load_balancer.register_event(priority_group)

    async def wait(self) -> None:
        await asyncio.gather(*(worker.wait() for worker in self.workers))