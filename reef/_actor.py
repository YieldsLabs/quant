import asyncio
import logging
import time
from dataclasses import dataclass

from coral import DataSourceFactory
from core.actors import BaseActor
from core.events.market import NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.order_type import OrderStatus, OrderType
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

logger = logging.getLogger(__name__)


@dataclass(order=True)
class PQOrder:
    timestamp: float
    order_id: str
    symbol: Symbol
    datasource: DataSourceType


class ReefActor(BaseActor):
    def __init__(
        self, datasource_factory: DataSourceFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self._order_queue = asyncio.PriorityQueue()
        self._datasource_factory = datasource_factory
        self._tasks = set()
        self.order_config = config_service.get("order")

    def on_start(self):
        worker_task = asyncio.create_task(self._process_orders())
        worker_task.add_done_callback(self._tasks.discard)
        self._tasks.add(worker_task)

        poll_task = asyncio.create_task(self._fetch_open_orders())
        poll_task.add_done_callback(self._tasks.discard)
        self._tasks.add(poll_task)

    def on_stop(self):
        for task in list(self._tasks):
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
        pq_order = PQOrder(time.time(), order.id, event.symbol, event.datasource)

        await self._order_queue.put((pq_order.timestamp, pq_order))

        logging.info(f"Order {order.id} {order.status} added to the queue.")

    async def _process_orders(self):
        expiration_time = self.order_config.get("expiration_time", 10)
        monitor_interval = self.order_config.get("monitor_interval", 10)

        try:
            while True:
                timestamp, pq_order = await self._order_queue.get()
                current_time = time.time()

                if current_time - timestamp > expiration_time:
                    await self._cancel_order(
                        pq_order.order_id, pq_order.symbol, pq_order.datasource
                    )
                else:
                    sleep_time = expiration_time - (current_time - timestamp)

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

    async def _fetch_open_orders(self):
        services = [
            DataSourceType.BYBIT,
        ]
        monitor_interval = self.order_config.get("monitor_interval", 10)

        for datasource in services:
            service = self._datasource_factory.create(datasource, ProtocolType.REST)
            orders = await asyncio.to_thread(service.fetch_all_open_orders)

            for order_id, symbol in orders:
                pq_order = PQOrder(time.time(), order_id, symbol, datasource)
                await self._order_queue.put((pq_order.timestamp, pq_order))

            await asyncio.sleep(monitor_interval)
