import asyncio
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.portfolio import BestStrategyEvent, PortfolioPerformanceEvent
from core.events.position import CheckExitConditions, FillOrder, ReadyToClosePosition, OpenLongPosition, OpenShortPosition
from core.events.strategy import GoLong, GoShort


class LogJournal(AbstractEventManager):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.lock = asyncio.Lock()

    @register_handler(OHLCVEvent)
    async def _on_market(self, event: OHLCVEvent):
        async with self.lock:
            self.counter += 1
        print('----------------------------------------------------->')
        print(event)
        print(self.counter)

    @register_handler(PortfolioPerformanceEvent)
    def _portfolio_performance(self, event: PortfolioPerformanceEvent):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(FillOrder)
    def _fill_order(self, event: FillOrder):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(CheckExitConditions)
    def _check_exit(self, event: CheckExitConditions):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(BestStrategyEvent)
    def _on_best_strategy(self, event: BestStrategyEvent):
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
    def _open_long_position(self, event: OpenLongPosition):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(OpenShortPosition)
    def _open_short_position(self, event: OpenShortPosition):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ReadyToClosePosition)
    def _close_position(self, event: ReadyToClosePosition):
        print('----------------------------------------------------->')
        print(event)
