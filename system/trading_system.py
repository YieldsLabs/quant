import asyncio
from enum import Enum, auto
from itertools import product
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.timeframe import Timeframe
from strategies.contrarian.contrarian_macrossover import ContrarianMACrossover
from strategy_management.strategy_manager import StrategyManager

from system.abstract_system import AbstractSystem
from system.trading_context import TradingContext
from trader.create_trader import create_trader


class TradingState(Enum):
    INIT = auto()
    BACKTESTING = auto()
    TRADING = auto()
    OPTIMIZATION = auto()
    STOPPED = auto()


class TradingSystem(AbstractSystem):
    def __init__(self, context: TradingContext, state: TradingState = TradingState.INIT):
        super().__init__()
        self.context = context
        self.state = state
        self.symbols = ['BTCUSDT', 'ETHUSDT']
        self.timeframes = [Timeframe.FIVE_MINUTES]
        self.strategies_classes = [
            ContrarianMACrossover
        ]

    async def start(self):
        while True:
            match self.state:
                case TradingState.INIT:
                    await self._initialization()
                    self.state = TradingState.BACKTESTING
                case TradingState.BACKTESTING:
                    await self._run_backtest()
                    self.state = TradingState.OPTIMIZATION
                case TradingState.OPTIMIZATION:
                    await self._run_optimization()
                    self.state = TradingState.TRADING
                case TradingState.TRADING:
                    await self._run_trading()
                    self.state = TradingState.STOPPED
                case TradingState.STOPPED:
                    await self._stop()
                    return

    async def _stop(self):
        await self.dispatcher.stop()

    async def _initialization(self):
        self.symbols = await self.context.datasource.symbols()

        leverage = self.context.leverage

        for symbol in self.symbols:
            self.context.broker.set_leverage(symbol, leverage)
            self.context.broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
            self.context.broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=leverage)

    async def _run_backtest(self):
        self.strategy_manager = StrategyManager([cls() for cls in self.strategies_classes])
        self.trader = create_trader(self.context.broker)
        await self.context.backtest.run(self.symbols, self.timeframes, self.context.lookback)
        await self.dispatcher.stop_workers()

    async def _run_optimization(self):
        await asyncio.sleep(100)

    async def _run_trading(self):
        self.trader = create_trader(self.context.broker, live_trading=False)

        timeframes_symbols = list(product(self.symbols, self.timeframes))

        await self.context.ws_handler.subscribe(timeframes_symbols)
        await self.dispatcher.stop_workers()
