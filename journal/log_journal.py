from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.order import FillOrder
from core.events.portfolio import BestStrategyEvent, PortfolioPerformanceEvent
from core.events.position import OpenLongPosition, OpenShortPosition
from core.events.strategy import GoLong, GoShort


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

    @register_handler(BestStrategyEvent)
    def _fill_order(self, event: BestStrategyEvent):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(GoLong)
    def _go_long(self, event: GoLong):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(GoShort)
    def _go_short(self, event: GoShort):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(OpenLongPosition)
    def _open_long(self, event: OpenLongPosition):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(OpenShortPosition)
    def _open_short(self, event: OpenShortPosition):
        print('----------------------------------------------------->')
        print(event)
