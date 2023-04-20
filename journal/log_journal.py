from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.order import FillOrder
from core.events.portfolio import BestStrategyEvent, CheckExitConditions, PortfolioPerformanceEvent
from core.events.position import ClosePosition, OpenLongPosition, OpenShortPosition
from core.events.strategy import GoLong, GoShort


class LogJournal(AbstractEventManager):
    def __init__(self):
        super().__init__()
        self.counter = 0

    @register_handler(OHLCVEvent)
    def _on_market(self, event: OHLCVEvent):
        print('----------------------------------------------------->')
        print('OHLCV event')
        print(event)

    @register_handler(PortfolioPerformanceEvent)
    def _portfolio_performance(self, event: PortfolioPerformanceEvent):
        print('----------------------------------------------------->')
        print('Portfolio performance')
        print(event)

    @register_handler(FillOrder)
    def _fill_order(self, event: FillOrder):
        print('----------------------------------------------------->')
        print('Fill Order')
        print(event)

    @register_handler(CheckExitConditions)
    def _check_exit(self, event: CheckExitConditions):
        print('----------------------------------------------------->')
        print('Check Exit Conditions')
        print(event)

    @register_handler(BestStrategyEvent)
    def _on_best_strategy(self, event: BestStrategyEvent):
        print('----------------------------------------------------->')
        print('Best Strategy Event')
        print(event)

    @register_handler(GoLong)
    def _go_long(self, event: GoLong):
        print('----------------------------------------------------->')
        print('Go Long')
        print(event)

    @register_handler(GoShort)
    def _go_short(self, event: GoShort):
        print('----------------------------------------------------->')
        print('Go Short')
        print(event)

    @register_handler(OpenLongPosition)
    def _open_long_position(self, event: OpenLongPosition):
        print('----------------------------------------------------->')
        print('Open Long Position')
        print(event)

    @register_handler(OpenShortPosition)
    def _open_short_position(self, event: OpenShortPosition):
        print('----------------------------------------------------->')
        print('Open Short Position')
        print(event)

    @register_handler(ClosePosition)
    def _close_position(self, event: ClosePosition):
        print('----------------------------------------------------->')
        print('Close Position')
        print(event)
