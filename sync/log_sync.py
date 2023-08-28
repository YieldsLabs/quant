import asyncio
from core.events.backtest import BacktestEnded
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.event_decorators import event_handler
from core.events.ohlcv import NewMarketDataReceived
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import  PositionClosed, PositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.signal import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived


class LogSync(AbstractEventManager):
    def __init__(self):
        super().__init__()
        self.lock = asyncio.Lock()
        self.counter = 0

    @event_handler(NewMarketDataReceived)
    async def _log_market(self, event: NewMarketDataReceived):
        print('----------------------------------------------------->')
        
        async with self.lock:
            self.counter += 1
            print(self.counter)
        
        print(event)

    @event_handler(GoLongSignalReceived)
    async def _log_go_long(self, event: GoLongSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @event_handler(GoShortSignalReceived)
    async def _log_go_short(self, event: GoShortSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @event_handler(PositionOpened)
    async def _log_position_opened(self, event: PositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @event_handler(PositionClosed)
    async def _log_closed_position(self, event: PositionClosed):
        print('----------------------------------------------------->')
        print(event)

    @event_handler(RiskThresholdBreached)
    async def _log_exit_risk(self, event: RiskThresholdBreached):
        print('----------------------------------------------------->')
        print(event)

    # @event_handler(ExitLongSignalReceived)
    # async def _log_exit_long(self, event: ExitLongSignalReceived):
    #     print('----------------------------------------------------->')
    #     print(event)

    # @event_handler(ExitShortSignalReceived)
    # async def _log_exit_short(self, event: ExitShortSignalReceived):
    #     print('----------------------------------------------------->')
    #     print(event)


    # @event_handler(PortfolioPerformanceUpdated)
    # async def _log_portfolio_performance(self, event: PortfolioPerformanceUpdated):
    #     print('----------------------------------------------------->')
    #     print(event)
