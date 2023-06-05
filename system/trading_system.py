import asyncio
from enum import Enum, auto
from itertools import product

from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.timeframe import Timeframe
from strategy.contrarian.contrarian_168pattern import Contrarian168Pattern
from strategy.contrarian.contrarian_deepthreemove import ContrarianDeepThreeMove
from strategy.contrarian.contrarian_lighttouch import ContrarianLightTouch
from strategy.contrarian.contrarian_macrossover import ContrarianMACrossover
from strategy.contrarian.contrarian_neutralitypullback import ContrarianNeutralityPullBack
from strategy.contrarian.contrarian_patterns import ContrarianPatterns
from strategy.contrarian.contrarian_reversal import ContrarianReversal
from strategy_management.strategy_manager import StrategyManager
from trader.create_trader import create_trader

from .abstract_system import AbstractSystem
from .trading_context import TradingContext


class TradingState(Enum):
    INIT = auto()
    BACKTESTING = auto()
    TRADING = auto()
    OPTIMIZATION = auto()
    STOPPED = auto()


class TradingSystem(AbstractSystem):
    def __init__(self, context: TradingContext, state: TradingState = TradingState.BACKTESTING):
        super().__init__()
        self.context = context
        self.state = state
        self.symbols = []
        self.timeframes = [
            Timeframe.ONE_MINUTE,
            Timeframe.FIVE_MINUTES,
            Timeframe.FIFTEEN_MINUTES
        ]
        self.strategies_classes = [
            ContrarianMACrossover,
            ContrarianReversal,
            ContrarianLightTouch,
            Contrarian168Pattern,
            ContrarianNeutralityPullBack,
            ContrarianDeepThreeMove,
            ContrarianPatterns
        ]

    async def start(self):
        while True:
            match self.state:
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
                    return

    async def _run_backtest(self):
        symbols = await self.context.datasource.symbols()

        with create_trader(self.context.broker):
            for strategy in self.strategies_classes:
                with StrategyManager([strategy()]):
                    await self.context.backtest.run(symbols, self.timeframes, self.context.lookback)
                    await self.dispatcher.wait()

    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        top_strategies = await self.context.optimization.get_top_strategies()

        symbols = [strategy[0] for strategy in top_strategies]
        timeframes = [strategy[1] for strategy in top_strategies]
        strategies = [strategy[2] for strategy in top_strategies]

        for symbol in symbols:
            self.context.broker.set_settings(symbol, self.context.leverage, position_mode=PositionMode.ONE_WAY, margin_mode=MarginMode.ISOLATED)

        with create_trader(self.context.broker, live_trading=self.context.live_mode):
            strategy_instances = [strategy_cls(*strategy[1]) for strategy in strategies for strategy_cls in self.strategies_classes if strategy_cls.NAME == strategy[0]]

            with StrategyManager(strategy_instances):
                timeframes_symbols = list(product(symbols, timeframes))
                await self.context.ws_handler.subscribe(timeframes_symbols)
