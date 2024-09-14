import logging
import time

from core.commands.broker import (
    ClosePosition,
    OpenPosition,
    UpdateSettings,
)
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.exchange import ExchangeType
from core.models.order import Order, OrderStatus
from core.models.side import PositionSide
from core.queries.account import GetBalance
from core.queries.broker import GetSymbol, GetSymbols, HasPosition
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

        if not trade:
            return Order(status=OrderStatus.FAILED, price=0, size=0)

        return Order(
            status=OrderStatus.CLOSED,
            size=trade["amount"],
            price=trade["price"],
            fee=trade["fee"],
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

    @command_handler(UpdateSettings)
    def update_symbol_settings(self, command: UpdateSettings):
        self.exchange.update_symbol_settings(
            command.symbol, command.position_mode, command.margin_mode, command.leverage
        )

    @command_handler(OpenPosition)
    async def open_position(self, command: OpenPosition):
        position = command.position
        symbol = position.signal.symbol

        logger.info(f"Try to open position: {position}")

        if self.exchange.fetch_position(symbol, position.side):
            logging.info("Position already exists")
            return

        pending_order = position.entry_order()

        entry_price = pending_order.price
        size = pending_order.size

        num_orders = min(
            max(1, int(size / symbol.min_position_size)), self.config["max_order_slice"]
        )
        size = round(size / num_orders, symbol.position_precision)
        order_counter = 0
        num_order_breach = 0
        order_timestamps = {}
        exp_time = self.config["order_expiration_time"]

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

            spread = (
                price - entry_price
                if position.side == PositionSide.LONG
                else entry_price - price
            )

            spread_percentage = 100 * (spread / entry_price)

            logging.info(
                f"Trying to open order -> algo price: {price}, theo price: {entry_price}, spread: {spread_percentage}%"
            )

            if spread_percentage > 0.35:
                break

            curr_time = time.time()
            expired_orders = [
                order_id
                for order_id, timestamp in order_timestamps.items()
                if curr_time - timestamp > exp_time
            ]

            for order_id in expired_orders:
                self.exchange.cancel_order(order_id, symbol)
                order_timestamps.pop(order_id)

            for order_id in list(order_timestamps.keys()):
                if self.exchange.has_filled_order(order_id, symbol):
                    order_timestamps.pop(order_id)
                    order_counter += 1

            if order_counter >= num_orders:
                logging.info(f"All orders are filled: {order_counter}")
                break

            if not self.exchange.has_open_orders(symbol, position.side) and not len(
                order_timestamps.keys()
            ):
                order_id = self.exchange.create_limit_order(
                    symbol, position.side, size, price
                )
                if order_id:
                    order_timestamps[order_id] = time.time()

        for order_id in list(order_timestamps.keys()):
            self.exchange.cancel_order(order_id, symbol)

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
        size = round(exit_order.size / num_orders, symbol.position_precision)
        order_counter = 0
        order_timestamps = {}
        max_spread = float("-inf")
        exp_time = self.config["order_expiration_time"]

        async for bid, ask in self.algo_price.next_value(symbol, self.exchange):
            if not self.exchange.fetch_position(symbol, position_side):
                break

            price = bid if position.side == PositionSide.LONG else ask

            spread = (
                price - exit_order.price
                if position_side == PositionSide.LONG
                else exit_order.price - price
            )
            max_spread = max(max_spread, spread)

            logging.info(
                f"Trying to reduce order -> algo price: {price}, theo price: {exit_order.price}, spread: {spread}, max spread: {max_spread}"
            )

            curr_time = time.time()
            expired_orders = [
                order_id
                for order_id, timestamp in order_timestamps.items()
                if curr_time - timestamp > exp_time
            ]

            for order_id in expired_orders:
                self.exchange.cancel_order(order_id, symbol)
                order_timestamps.pop(order_id)

            for order_id in list(order_timestamps.keys()):
                if self.exchange.has_filled_order(order_id, symbol):
                    order_timestamps.pop(order_id)
                    order_counter += 1

            if order_counter >= num_orders:
                logging.info(f"All orders are filled: {order_counter}")
                break

            if not (
                self.exchange.has_open_orders(symbol, position_side, True)
                or len(order_timestamps.keys())
            ):
                order_id = self.exchange.create_reduce_order(
                    symbol, position_side, size, price
                )
                if order_id:
                    order_timestamps[order_id] = time.time()

        for order_id in list(order_timestamps.keys()):
            self.exchange.cancel_order(order_id, symbol)
