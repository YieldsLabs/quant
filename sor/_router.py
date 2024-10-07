import logging
import time

from coral import DataSourceFactory
from core.commands.position import ClosePosition, OpenPosition
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.datasource_type import DataSourceType
from core.models.entity.order import Order
from core.models.order_type import OrderStatus
from core.models.protocol_type import ProtocolType
from core.models.side import PositionSide
from core.queries.account import GetBalance
from core.queries.position import GetClosePosition, GetOpenPosition, HasPosition

from ._twap import TWAP

logger = logging.getLogger(__name__)


class SmartRouter(AbstractEventManager):
    def __init__(self, datasource_factory: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        self.exchange = datasource_factory.create(DataSourceType.BYBIT, ProtocolType.REST)
        self.algo_price = TWAP(config_service)
        self.config = config_service.get("position")

    @query_handler(GetOpenPosition)
    def get_open_position(self, query: GetOpenPosition):
        position = query.position

        broker_position = self.exchange.fetch_position(
            position.signal.symbol, position.side
        )

        logging.info(f"Broker open position: {broker_position}")

        if not broker_position:
            return Order(status=OrderStatus.FAILED, price=0, size=0)
        else:
            return Order(
                status=OrderStatus.EXECUTED,
                size=broker_position["position_size"],
                price=broker_position["entry_price"],
                fee=broker_position["open_fee"],
            )

    @query_handler(GetClosePosition)
    def get_close_position(self, query: GetClosePosition):
        position = query.position
        symbol = position.signal.symbol

        trade = self.exchange.fetch_trade(
            symbol,
            position.side,
            position.last_modified,
            position.size,
            self.config["max_order_slice"],
        )

        logging.info(f"Broker close position: {trade}")

        if not trade:
            return Order(status=OrderStatus.FAILED, price=0, size=0)

        return Order(
            status=OrderStatus.CLOSED,
            size=trade["amount"],
            price=trade["price"],
            fee=trade["fee"],
        )

    @query_handler(GetBalance)
    def get_account_balance(self, query: GetBalance):
        return self.exchange.fetch_account_balance(query.currency)

    @query_handler(HasPosition)
    def has_position(self, query: HasPosition):
        position = query.position
        symbol = position.signal.symbol
        side = position.side

        existing_position = self.exchange.fetch_position(symbol, side)

        if existing_position:
            logging.info(f"Position check: {side} position for {symbol} exists.")
            return True

        logging.info(f"Position check: No existing {side} position found for {symbol}.")
        return False

    @command_handler(OpenPosition)
    async def open_position(self, command: OpenPosition):
        position = command.position
        symbol = position.signal.symbol
        position_side = position.side

        logger.info(f"Try to open position: {position}")

        if self.exchange.fetch_position(symbol, position_side):
            logging.info("Position already exists")
            return

        pending_order = position.entry_order()

        entry_price = pending_order.price
        size = pending_order.size

        num_orders = min(
            max(1, int(size / symbol.min_position_size)), self.config["max_order_slice"]
        )
        orders_size = round(size / num_orders, symbol.position_precision)

        num_order_breach = 0

        async for bid, ask in self.algo_price.next_value(symbol, self.exchange):
            price = ask if position.side == PositionSide.LONG else bid
            stop_loss = position.stop_loss

            current_distance_to_stop_loss = abs(stop_loss - price)
            distance_to_stop_loss = abs(entry_price - stop_loss)

            threshold_breach = (
                self.config["stop_loss_threshold"] * distance_to_stop_loss
                > current_distance_to_stop_loss
            )

            if threshold_breach:
                logging.info(
                    f"Order risk breached: ENTR: {entry_price}, STPLS: {stop_loss}, THEO_DSTNC: {distance_to_stop_loss}, ALG_DSTNC: {current_distance_to_stop_loss}"
                )

                num_order_breach += 1

                if num_order_breach >= self.config["max_order_breach"]:
                    break

            existing_position = self.exchange.fetch_position(symbol, position_side)

            if existing_position and existing_position.position_size >= size:
                break
            else:
                self.exchange.create_limit_order(symbol, position_side, orders_size, price)

    @command_handler(ClosePosition)
    async def close_position(self, command: ClosePosition):
        position = command.position

        symbol = position.signal.symbol
        position_side = position.side

        if not self.exchange.fetch_position(symbol, position_side):
            logging.info("Position is not existed")
            return

        exit_order = position.exit_order()

        num_orders = min(
            max(1, int(exit_order.size / symbol.min_position_size)),
            self.config["max_order_slice"],
        )
        orders_size = round(exit_order.size / num_orders, symbol.position_precision)

        async for bid, ask in self.algo_price.next_value(symbol, self.exchange):
            price = bid if position.side == PositionSide.LONG else ask

            logging.info(
                f"Trying to reduce order -> algo price: {price}, theo price: {exit_order.price}, spread: {spread}, max spread: {max_spread}"
            )

            if not self.exchange.fetch_position(symbol, position_side):
                break

            self.exchange.create_reduce_order(
                symbol, position_side, orders_size, price
            )                
