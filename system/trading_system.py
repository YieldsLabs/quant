from enum import Enum
from itertools import product

from system.abstract_system import AbstractSystem
from system.trading_context import TradingContext
from trader.create_trader import create_trader


class TradingState(Enum):
    BACKTESTING = 1
    TRADING = 2
    STOPPED = 3

class TradingSystem(AbstractSystem):
    def __init__(self, context: TradingContext):
        super().__init__()
        self.context = context
        self.state = TradingState.BACKTESTING

    async def start(self):
        while True:
            match self.state:
                case TradingState.BACKTESTING:
                    await self._run_backtest()
                    self.state = TradingState.TRADING
                case TradingState.TRADING:
                    await self._run_trading()
                    self.state = TradingState.STOPPED
                case TradingState.STOPPED:
                    await self._stop()
                    return

    async def _stop(self):
        await self.dispatcher.stop()

    async def _run_backtest(self):
        self.trader = create_trader(self.context.broker, live_trading=False)

        await self.context.backtest.run(self.context.symbols, self.context.timeframes, self.context.lookback)

    async def _run_trading(self):
        self.trader = create_trader(self.context.broker, live_trading=False)

        timeframes_symbols = list(product(self.context.symbols, self.context.timeframes))

        await self.context.subscribe(timeframes_symbols)