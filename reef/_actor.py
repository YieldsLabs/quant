import asyncio
import logging
import time

import numpy as np

from coral import DataSourceFactory
from core.actors import BaseActor
from core.events.market import NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.order_type import OrderStatus, OrderType
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

from ._order import PQOrder

logger = logging.getLogger(__name__)


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
        self._stop_event.clear()

        worker_task = asyncio.create_task(self._process_orders())
        self._tasks.add(worker_task)
        worker_task.add_done_callback(lambda t: self._tasks.discard(t))

        poll_task = asyncio.create_task(self._fetch_open_orders())
        self._tasks.add(poll_task)
        poll_task.add_done_callback(lambda t: self._tasks.discard(t))

    def on_stop(self):
        self._stop_event.set()

        tasks_to_cancel = [task for task in self._tasks if not task.done()]

        for task in tasks_to_cancel:
            task.cancel()

        self._tasks.clear()

    def pre_receive(self, event: NewMarketOrderReceived):
        return (
            isinstance(event, NewMarketOrderReceived)
            and event.order.type != OrderType.PAPER
            and event.order.status == OrderStatus.PENDING
        )

    async def on_receive(self, event: NewMarketOrderReceived):
        await self._put_order(PQOrder(event.order.id, event.symbol, event.datasource))

    async def _process_orders(self):
        monitor_interval = self.order_config.get("monitor_interval", 10)

        try:
            while not self._stop_event.is_set():
                pq_order = await self._order_queue.get()

                if pq_order.is_expired:
                    await self._cancel_order(
                        pq_order.order_id, pq_order.symbol, pq_order.datasource
                    )
                else:
                    sleep_time = pq_order.ttl - (time.time() - pq_order.timestamp)

                    if sleep_time > 0:
                        await asyncio.sleep(sleep_time)

                    await self._cancel_order(
                        pq_order.order_id, pq_order.symbol, pq_order.datasource
                    )

                self._order_queue.task_done()

                await asyncio.sleep(
                    np.mean(np.random.exponential(monitor_interval, size=100))
                )
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

        datasource_tasks = [
            asyncio.create_task(self._fetch_orders(datasource))
            for datasource in services
        ]

        results = await asyncio.gather(*datasource_tasks, return_exceptions=True)

        open_orders = []

        for datasource, result in zip(services, results):
            if isinstance(result, Exception):
                logging.error(f"Error fetching orders for {datasource}: {str(result)}")
                continue

            open_orders.extend(
                [PQOrder(order_id, symbol, datasource) for order_id, symbol in result]
            )

        for open_order in open_orders:
            await self._put_order(open_order)

        await asyncio.sleep(np.random.exponential(monitor_interval))

    async def _put_order(self, pq_order: PQOrder):
        if not any(
            existing_order.order_id == pq_order.order_id
            for existing_order in self._order_queue._queue
        ):
            await self._order_queue.put(pq_order)
            logging.info(f"Order {pq_order.order_id} added to the queue.")
        else:
            logging.info(
                f"Order {pq_order.order_id} already exists in the queue, skipping."
            )
