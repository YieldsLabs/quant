from core.commands.broker import ClosePosition, OpenPosition, UpdateSettings
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.exchange import ExchangeType
from core.queries.account import GetBalance
from core.queries.broker import GetSymbol, GetSymbols
from core.queries.position import GetOpenPosition


class SmartRouter(AbstractEventManager):
    def __init__(self, exchange_factory: AbstractExchangeFactory):
        super().__init__()
        self.exchange_factory = exchange_factory
        self.exchange = self.exchange_factory.create(ExchangeType.BYBIT)

    @query_handler(GetOpenPosition)
    def get_open_position(self, query: GetOpenPosition):
        position = query.position

        return self.exchange.fetch_position(position.signal.symbol)

    @query_handler(GetSymbols)
    def get_symbols(self, _query: GetSymbols):
        return self.exchange.fetch_symbols()

    @query_handler(GetSymbol)
    def get_symbol(self, query: GetSymbol):
        symbols = self.exchange.fetch_symbols()

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
    def open_position(self, command: OpenPosition):
        position = command.position

        symbol = position.signal.symbol
        side = position.side
        size = position.size

        self.exchange.open_market_position(symbol, side, size)

    @command_handler(ClosePosition)
    def close_position(self, command: ClosePosition):
        symbol = command.position.signal.symbol

        self.exchange.close_position(symbol)
