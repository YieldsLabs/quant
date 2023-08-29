from core.event_decorators import event_handler, query_handler
from core.events.position import PositionClosed
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.queries.portfolio import GetTopStrategy, GetTotalPnL
from portfolio.portfolio_storage import PortfolioStorage


class Portfolio(AbstractEventManager):
    def __init__(self, risk_per_trade: int):
        super().__init__()
        self.state = PortfolioStorage()
        self.risk_per_trade = risk_per_trade

    @event_handler(PositionClosed)
    async def handle_close_positon(self, event: PositionClosed):
        await self.state.update(event.position)

    @query_handler(GetTopStrategy)
    async def top_strategy(self, query: GetTopStrategy):
         return await self.state.get_top_strategy(query.strategy)

    @query_handler(GetTotalPnL)
    async def total_pnl(self, query: GetTotalPnL):
        return await self.state.get_pnl(query.strategy)