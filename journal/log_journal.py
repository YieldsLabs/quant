import asyncio
import time
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.portfolio import PortfolioPerformanceEvent
from core.events.position import PositionClosed, OrderFilled, PositionReadyToClose, LongPositionOpened, ShortPositionOpened
from core.events.risk import EvaluateRisk
from core.events.strategy import GoLong, GoShort


class LogJournal(AbstractEventManager):
    def __init__(self):
        super().__init__()
        self.num_events = 0
        self.start_time = time.monotonic()
        self.lock = asyncio.Lock()

    @register_handler(OHLCVEvent)
    async def _on_market(self, event: OHLCVEvent):
        async with self.lock:
            self.num_events += 1
        elapsed_time = time.monotonic() - self.start_time
        print('----------------------------------------------------->')
        print(event)
        print(f"Processed {self.num_events} events in {elapsed_time:.2f} seconds, throughput = {self.num_events/elapsed_time:.2f} events/s.")

    @register_handler(GoLong)
    async def _on_go_long(self, event: GoLong):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(GoShort)
    async def _on_go_short(self, event: GoShort):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(OrderFilled)
    async def _on_fill_order(self, event: OrderFilled):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(LongPositionOpened)
    async def _on_open_long_position(self, event: LongPositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ShortPositionOpened)
    async def _on_open_short_position(self, event: ShortPositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(EvaluateRisk)
    async def _on_check_exit(self, event: EvaluateRisk):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(PositionReadyToClose)
    async def _on_close_position(self, event: PositionReadyToClose):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(PositionClosed)
    async def _on_closed_position(self, event: PositionClosed):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(PortfolioPerformanceEvent)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceEvent):
        print('----------------------------------------------------->')
        print(event)
