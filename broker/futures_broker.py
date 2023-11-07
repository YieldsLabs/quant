from core.commands.broker import ClosePosition, OpenPosition, UpdateSettings
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_broker import AbstractBroker
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.order import Order, OrderStatus
from core.queries.broker import (
    GetAccountBalance,
    GetOpenPosition,
    GetSymbol,
    GetSymbols,
)


class FuturesBroker(AbstractBroker):
    def __init__(self, exchange: AbstractExchange):
        super().__init__()
        self.exchange = exchange

    @command_handler(UpdateSettings)
    def update_symbol_settings(self, command: UpdateSettings):
        self.exchange.update_symbol_settings(
            command.symbol, command.position_mode, command.margin_mode, command.leverage
        )

    @command_handler(OpenPosition)
    def open_position(self, command: OpenPosition):
        position = command.position
        symbol = position.signal.symbol

        self.exchange.open_market_position(symbol, position.side, position.size)

    @command_handler(ClosePosition)
    def close_position(self, command: ClosePosition):
        symbol = command.position.signal.symbol

        self.exchange.close_position(symbol)

    @query_handler(GetOpenPosition)
    def get_open_position(self, query: GetOpenPosition):
        position = query.position
        exchange_position = self.exchange.fetch_position(position.signal.symbol)

        if not exchange_position:
            order = Order(status=OrderStatus.FAILED, price=0, size=0)

            return position.add_order(order)

        else:
            order = Order(
                status=OrderStatus.EXECUTED,
                size=exchange_position["position_size"],
                price=exchange_position["entry_price"],
            )

            return position.add_order(order).update_prices(order.price)

    @query_handler(GetSymbols)
    def get_symbols(self, _query: GetSymbols):
        return self.exchange.fetch_symbols()

    @query_handler(GetSymbol)
    def get_symbol(self, query: GetSymbol):
        symbols = self.exchange.fetch_symbols()
        return next((symbol for symbol in symbols if symbol.name == query.symbol), None)

    @query_handler(GetAccountBalance)
    def get_account_balance(self, query: GetAccountBalance):
        return self.exchange.fetch_account_balance(query.currency)
