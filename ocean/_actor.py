from typing import Union

from core.actors import BaseActor
from core.commands.broker import UpdateSymbolSettings
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.mixins import EventHandlerMixin
from core.queries.broker import GetSymbol, GetSymbols

OceanEvent = Union[GetSymbols, GetSymbol, UpdateSymbolSettings]


class OceanActor(BaseActor, EventHandlerMixin):
    def __init__(self, exchange_factory: AbstractExchangeFactory):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.exchange_factory = exchange_factory

    async def on_receive(self, event: OceanEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(GetSymbols, self._get_symbols)
        self.register_handler(GetSymbol, self._get_symbol)
        self.register_handler(UpdateSymbolSettings, self._update_symbol_settings)

    def _get_symbols(self, event: GetSymbols):
        exchange = self.exchange_factory.create(event.exchange)
        symbols = exchange.fetch_future_symbols()

        return symbols

    def _get_symbol(self, event: GetSymbol):
        exchange = self.exchange_factory.create(event.exchange)
        symbols = exchange.fetch_future_symbols()

        return next((symbol for symbol in symbols if symbol == event.symbol), None)

    def _update_symbol_settings(self, event: UpdateSymbolSettings):
        exchange = self.exchange_factory.create(event.exchange)

        exchange.update_symbol_settings(
            event.symbol, event.position_mode, event.margin_mode, event.leverage
        )
