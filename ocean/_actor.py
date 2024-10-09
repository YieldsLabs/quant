from typing import Union

import numpy as np

from coral import DataSourceFactory
from core.actors import BaseActor
from core.commands.broker import UpdateSymbolSettings
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.protocol_type import ProtocolType
from core.queries.broker import GetSimilarSymbols, GetSymbols

from ._gsim import SIM

OceanEvent = Union[GetSymbols, GetSimilarSymbols, UpdateSymbolSettings]


class OceanActor(BaseActor, EventHandlerMixin):
    def __init__(self, datasource: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.datasource = datasource
        self.config = config_service.get("ocean")
        self.gsim = SIM(
            max_level=8, max_neighbors=40, ef_construction=500, ef_search=50
        )
        self._init_embeddings()

    async def on_receive(self, event: OceanEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(GetSymbols, self._get_symbols)
        self.register_handler(GetSimilarSymbols, self._get_similar_symbols)
        self.register_handler(UpdateSymbolSettings, self._update_symbol_settings)

    def _get_symbols(self, event: GetSymbols):
        exchange = self.datasource.create(event.datasource, ProtocolType.REST)
        symbols = exchange.fetch_future_symbols()

        if not event.cap:
            return symbols

        similar_symbols = self.gsim.find_similar_by_cap(
            event.cap, top_k=self.config.get("top_k")
        )

        if not similar_symbols:
            return symbols

        return [symbol for symbol in symbols if symbol.name in similar_symbols]

    def _get_similar_symbols(self, event: GetSimilarSymbols):
        exchange = self.datasource.create(event.datasource, ProtocolType.REST)
        symbols = exchange.fetch_future_symbols()

        similar_symbols = self.gsim.find_similar_symbols(
            event.symbol.name, top_k=self.config.get("top_k")
        )

        if not similar_symbols:
            return []

        return [symbol for symbol in symbols if symbol.name in similar_symbols]

    def _update_symbol_settings(self, event: UpdateSymbolSettings):
        exchange = self.datasource.create(event.datasource, ProtocolType.REST)
        exchange.update_symbol_settings(
            event.symbol, event.position_mode, event.margin_mode, event.leverage
        )

    def _init_embeddings(self):
        embs = np.load(self.config.get("emb_file"), allow_pickle=True)

        for symbol, emb in embs:
            self.gsim.insert(emb, symbol)

        self.gsim.perform_clustering()
