from core.event_decorators import event_handler, query_handler
from core.events.position import PositionClosed, PositionOpened
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.queries.portfolio import GetDrawdown, GetEquity, GetOpenPositions, GetTopStrategy, GetTotalPnL


class Portfolio(AbstractEventManager):
    def __init__(self):
        super().__init__()

    @event_handler(PositionOpened)
    def handle_open_position(self, event: PositionOpened):
        pass
    
    @event_handler(PositionClosed)
    def handle_close_positon(self, event: PositionClosed):
        pass

    @query_handler(GetTopStrategy)
    def top_strategy(self, query: GetTopStrategy):
        pass

    @query_handler(GetOpenPositions)
    def open_positions(self, query: GetOpenPositions):
        pass

    @query_handler(GetEquity)
    def equity(self, query: GetEquity):
        pass
    
    @query_handler(GetDrawdown)
    def drawdown(self, query: GetDrawdown):
        pass

    @query_handler(GetTotalPnL)
    def total_pnl(self, query: GetTotalPnL):
        pass