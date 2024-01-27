import logging
import time

from core.commands.broker import ClosePosition, OpenPosition, UpdateSettings
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.exchange import ExchangeType
from core.models.order import Order, OrderStatus
from core.queries.account import GetBalance
from core.queries.broker import GetSymbol, GetSymbols
from core.queries.position import GetClosePosition, GetOpenPosition

from ._twap import TWAP

logger = logging.getLogger(__name__)


class SmartRouter(AbstractEventManager):
    def __init__(
        self, exchange_factory: AbstractExchangeFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self.exchange_factory = exchange_factory
        self.exchange = self.exchange_factory.create(ExchangeType.BYBIT)
        self.algo_price = TWAP(config_service)
        self.config = config_service.get("position")

    @query_handler(GetOpenPosition)
    def get_open_position(self, query: GetOpenPosition):
        position = query.position

        broker_position = self.exchange.fetch_position(
            position.signal.symbol, position.side
        )

        logging.info(f"Broker position: {broker_position}")

        if not broker_position:
            return Order(status=OrderStatus.FAILED, price=0, size=0)
        else:
            return Order(
                status=OrderStatus.EXECUTED,
                size=broker_position["position_size"],
                price=broker_position["entry_price"],
            )

    @query_handler(GetClosePosition)
    def get_close_position(self, query: GetClosePosition):
        position = query.position

        symbol = position.signal.symbol

        trade = self.exchange.fetch_trade(symbol)

        logging.info(f"Trade: {trade}")

        if not trade:
            return Order(status=OrderStatus.FAILED, price=0, size=0)

        return Order(
            status=OrderStatus.CLOSED, size=trade["amount"], price=trade["price"]
        )

    @query_handler(GetSymbols)
    def get_symbols(self, _query: GetSymbols):
        return self.exchange.fetch_future_symbols()

    @query_handler(GetSymbol)
    def get_symbol(self, query: GetSymbol):
        symbols = self.exchange.fetch_future_symbols()

        return next((symbol for symbol in symbols if symbol.name == query.symbol), None)

    @query_handler(GetBalance)
    def get_account_balance(self, query: GetBalance):
        return self.exchange.fetch_account_balance(query.currency)

    @command_handler(UpdateSettings)
    def update_symbol_settings(self, command: UpdateSettings):
        self.exchange.update_symbol_settings(
            command.symbol, command.position_mode, command.margin_mode, command.leverage
        )

    @command_handler(OpenPosition)
    async def open_position(self, command: OpenPosition):
        position = command.position

        logger.info(f"Try to open position: {position}")

        symbol = position.signal.symbol
        position_size = position.size
        stop_loss = position.stop_loss_price
        entry_price = position.entry_price

        distance_to_stop_loss = abs(entry_price - stop_loss)

        min_size = symbol.min_position_size
        num_orders = min(
            max(1, int(position_size / min_size)), self.config["max_order_slice"]
        )
        size = round(position_size / num_orders, symbol.position_precision)
        order_counter = 0
        num_order_breach = 0
        order_timestamps = {}

        for price in self.algo_price.calculate(symbol, self.exchange):
            logging.info(f"Trying to open order: {price}")

            current_distance_to_stop_loss = abs(stop_loss - price)

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

            for order_id in list(order_timestamps.keys()):
                if self.exchange.has_order(order_id, symbol):
                    order_timestamps.pop(order_id)
                    order_counter += 1

            curr_time = time.time()
            expired_orders = [
                order_id
                for order_id, timestamp in order_timestamps.items()
                if curr_time - timestamp > self.config["order_expiration_time"]
            ]

            for order_id in expired_orders:
                self.exchange.cancel_order(order_id, symbol)
                order_timestamps.pop(order_id)

            if order_counter >= num_orders:
                logging.info(f"All orders are filled: {order_counter}")
                break

            if len(order_timestamps.keys()) < 1:
                order_id = self.exchange.create_limit_order(
                    symbol, position.side, size, price
                )
                order_timestamps[order_id] = time.time()

        for order_id in list(order_timestamps.keys()):
            self.exchange.cancel_order(order_id, symbol)

    @command_handler(ClosePosition)
    def close_position(self, command: ClosePosition):
        position = command.position
        symbol = position.signal.symbol
        position_size = position.size

        min_size = symbol.min_position_size
        num_orders = min(
            max(1, int(position_size / min_size)), self.config["max_order_slice"]
        )
        size = round(position_size / num_orders, symbol.position_precision)
        order_counter = 0
        order_timestamps = {}

        for price in self.algo_price.calculate(symbol, self.exchange):
            logging.info(f"Trying to reduce order: {price}")

            for order_id in list(order_timestamps.keys()):
                if self.exchange.has_order(order_id, symbol):
                    order_timestamps.pop(order_id)
                    order_counter += 1

            curr_time = time.time()
            expired_orders = [
                order_id
                for order_id, timestamp in order_timestamps.items()
                if curr_time - timestamp > self.config["order_expiration_time"]
            ]

            for order_id in expired_orders:
                self.exchange.cancel_order(order_id, symbol)
                order_timestamps.pop(order_id)

            if order_counter >= num_orders:
                logging.info(f"All orders are filled: {order_counter}")
                break

            if len(order_timestamps.keys()) < 2:
                order_id = self.exchange.create_reduce_order(
                    symbol, position.side, size, price
                )
                order_timestamps[order_id] = time.time()

        for order_id in list(order_timestamps.keys()):
            self.exchange.cancel_order(order_id, symbol)

        self.exchange.close_full_position(symbol, position.side)
