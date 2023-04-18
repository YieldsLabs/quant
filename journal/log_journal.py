from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.order import FillOrder
from core.events.portfolio import PortfolioPerformanceEvent


class LogJournal(AbstractEventManager):
    def __init__(self):
        super().__init__()

    @register_handler(PortfolioPerformanceEvent)
    def _portfolio_performance(self, event: PortfolioPerformanceEvent):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(FillOrder)
    def _fill_order(self, event: FillOrder):
        print('----------------------------------------------------->')
        print(event)
