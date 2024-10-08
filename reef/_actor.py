import asyncio
import logging
import time
from typing import Dict, Tuple

from coral import DataSourceFactory
from core.actors import BaseActor
from core.events.market import NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.entity.order import Order
from core.models.order_type import OrderStatus, OrderType
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

logger = logging.getLogger(__name__)


class ReefActor(BaseActor):
    def __init__(
        self, datasource_factory: DataSourceFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self._lock = asyncio.Lock()
        self._orders: Dict[str, Tuple[float, Symbol, DataSourceType]] = {}
        self._datasource_factory = datasource_factory
        self._tasks = set()
        order_config = config_service.get("order")
        self.expiration_time = order_config.get("expiration_time", 10)
        self.monitor_interval = order_config.get("monitor_interval", 10)

    def on_start(self):
        task = asyncio.create_task(self._monitor_orders())
        task.add_done_callback(self._tasks.discard)
        self._tasks.add(task)

    def on_stop(self):
        for task in list(self._tasks):
            task.cancel()

        self._tasks.clear()

    def pre_receive(self, event: NewMarketOrderReceived):
        return (
            isinstance(event, NewMarketOrderReceived)
            and event.order.type != OrderType.PAPER
        )

    async def on_receive(self, event: NewMarketOrderReceived):
        match event.order.status:
            case OrderStatus.EXECUTED:
                await self._clear_order(event.order)
            case OrderStatus.PENDING:
                await self._append_order(event.order, event.symbol, event.datasource)

    async def _clear_order(self, order: Order):
        async with self._lock:
            if order.id in self._orders:
                self._orders.pop(order.id)

                logging.info(f"Order {order.id} cleared.")

    async def _append_order(
        self, order: Order, symbol: Symbol, datasource: DataSourceType
    ):
        async with self._lock:
            self._orders[order.id] = (time.time(), symbol, datasource)

            logging.info(f"Order {order.id} appended for symbol {symbol.name}.")

    async def _monitor_orders(self):
        fetch_interval = 5
        counter = 0

        try:
            while True:
                await asyncio.sleep(self.monitor_interval)
                await self._cancel_expired_orders()

                if counter % fetch_interval == 0:
                    await self._fetch_open_orders()
                    counter = 0

                counter += 1
        except asyncio.CancelledError:
            logging.info("Monitoring task canceled.")
        except Exception as e:
            logging.error(f"Error in monitoring orders: {str(e)}")

    async def _cancel_expired_orders(self):
        curr_time = time.time()
        expired_orders = []

        async with self._lock:
            expired_orders = [
                (order_id, symbol, datasource)
                for order_id, (timestamp, symbol, datasource) in self._orders.items()
                if curr_time - timestamp > self.expiration_time
            ]

        if expired_orders:
            logging.info(f"Found {len(expired_orders)} expired orders. Canceling...")

        for order_id, symbol, datasource in expired_orders:
            service = self._datasource_factory.create(datasource, ProtocolType.REST)
            service.cancel_order(order_id, symbol)

            async with self._lock:
                self._orders.pop(order_id, None)
            logging.info(f"Order {order_id} for symbol {symbol.name} canceled.")

    async def _fetch_open_orders(self):
        orders = []
        services = [
            self._datasource_factory.create(DataSourceType.BYBIT, ProtocolType.REST),
        ]

        for service in services:
            orders += service.fetch_all_open_orders()

        curr_time = time.time()

        async with self._lock:
            for order_id, order_symbol in orders:
                if order_id in self._orders:
                    timestamp, symbol, datasource = self._orders.get(order_id)

                    if curr_time - timestamp > self.expiration_time:
                        service = self._datasource_factory.create(
                            datasource, ProtocolType.REST
                        )
                        service.cancel_order(order_id, symbol)
                        self._orders.pop(order_id, None)

                        logging.info(
                            f"Order {order_id} for symbol {symbol.name} canceled."
                        )
                else:
                    logging.warning(
                        f"Untracked order {order_id} found, attempting cancellation."
                    )
                    for service in services:
                        service.cancel_order(order_id, order_symbol)
