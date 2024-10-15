import asyncio
import logging
import time
from dataclasses import dataclass, field

import numpy as np

from coral import DataSourceFactory
from core.actors import BaseActor
from core.events.market import NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.order_type import OrderStatus, OrderType
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

logger = logging.getLogger(__name__)


@dataclass(order=True, frozen=True)
class PQOrder:
    order_id: str = field(compare=False)
    symbol: Symbol = field(compare=False)
    datasource: DataSourceType = field(compare=False)
    timestamp: float = field(default_factory=lambda: time.time(), compare=True)
    ttl: float = field(
        default_factory=lambda: np.mean(np.random.exponential(3, size=1000)),
        compare=False,
    )


class ReefActor(BaseActor):
    def __init__(
        self, datasource_factory: DataSourceFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self._order_queue = asyncio.PriorityQueue()
        self._datasource_factory = datasource_factory
        self._tasks = set()
        self.order_config = config_service.get("order")
        self._stop_event = asyncio.Event()

    def on_start(self):
        worker_task = asyncio.create_task(self._process_orders())
        worker_task.add_done_callback(self._tasks.discard)
        self._tasks.add(worker_task)

        poll_task = asyncio.create_task(self._fetch_open_orders())
        poll_task.add_done_callback(self._tasks.discard)
        self._tasks.add(poll_task)

    def on_stop(self):
        self._stop_event.set()

        for task in list(self._tasks):
            if not task.done():
                task.cancel()

        self._tasks.clear()

    def pre_receive(self, event: NewMarketOrderReceived):
        return (
            isinstance(event, NewMarketOrderReceived)
            and event.order.type != OrderType.PAPER
            and event.order.status == OrderStatus.PENDING
        )

    async def on_receive(self, event: NewMarketOrderReceived):
        order = event.order
        pq_order = PQOrder(order.id, event.symbol, event.datasource)

        await self._order_queue.put(pq_order)

        logging.info(f"Order {order.id} {order.status} added to the queue.")

    async def _process_orders(self):
        monitor_interval = self.order_config.get("monitor_interval", 10)

        try:
            while not self._stop_event.is_set():
                pq_order = await self._order_queue.get()
                current_time = time.time()

                if current_time - pq_order.timestamp > pq_order.ttl:
                    await self._cancel_order(
                        pq_order.order_id, pq_order.symbol, pq_order.datasource
                    )
                else:
                    sleep_time = pq_order.ttl - (current_time - pq_order.timestamp)

                    if sleep_time > 0:
                        await asyncio.sleep(sleep_time)

                    await self._cancel_order(
                        pq_order.order_id, pq_order.symbol, pq_order.datasource
                    )

                self._order_queue.task_done()

                await asyncio.sleep(monitor_interval)
        except asyncio.CancelledError:
            logging.info("Order processing task was cancelled.")
        except Exception as e:
            logging.error(f"Error in processing or monitoring orders: {str(e)}")

    async def _cancel_order(
        self, order_id: str, symbol: Symbol, datasource: DataSourceType
    ):
        service = self._datasource_factory.create(datasource, ProtocolType.REST)

        await asyncio.to_thread(service.cancel_order, order_id, symbol)

        logging.info(f"Order {order_id} for symbol {symbol.name} canceled.")

    async def _fetch_orders(self, datasource):
        service = self._datasource_factory.create(datasource, ProtocolType.REST)

        return await asyncio.to_thread(service.fetch_all_open_orders)

    async def _fetch_open_orders(self):
        services = [
            DataSourceType.BYBIT,
        ]
        monitor_interval = self.order_config.get("monitor_interval", 10)

        open_orders = []

        tasks = [
            asyncio.create_task(self._fetch_orders(datasource))
            for datasource in services
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for datasource, result in zip(services, results):
            open_orders.extend(
                [PQOrder(order_id, symbol, datasource) for order_id, symbol in result]
            )

        for open_order in open_orders:
            if not any(
                existing_order.order_id == open_order.order_id
                for existing_order in self._order_queue._queue
            ):
                await self._order_queue.put(open_order)

        await asyncio.sleep(monitor_interval)
