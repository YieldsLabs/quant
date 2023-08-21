import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.models.broker import MarginMode, PositionMode
from core.events.backtest import BacktestStarted
from trader.create_trader import create_trader
from core.interfaces.abstract_system import AbstractSystem

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
        self.strategy_actors = []

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
        await self.context.portfolio.initialize_account()

        symbols = await self.context.datasource.symbols()
        symbols_and_timeframes = list(product(symbols, self.context.timeframes))

        shuffle(symbols_and_timeframes)

        self.strategy_actors = [
            self.context.strategy_factory.create_actor(symbol, timeframe, f'./strategy/{strategy[0]}.wasm', strategy[1], strategy[2])
            for symbol, timeframe in symbols_and_timeframes
            for strategy in self.context.strategies
        ]

        with create_trader(self.context.broker):
            for actor in self.strategy_actors:
                await self.dispatcher.dispatch(
                    BacktestStarted(self.context.datasource, actor, self.context.lookback))
                await self.dispatcher.wait()

    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        top_strategies = await self.context.portfolio.get_top_strategies(3)

        symbols_and_timeframes = [(strategy[0], strategy[1]) for strategy in top_strategies]
        strategies = [strategy[2] for strategy in top_strategies]

        for symbol, _ in symbols_and_timeframes:
            self.context.broker.set_settings(symbol, self.context.leverage, position_mode=PositionMode.ONE_WAY, margin_mode=MarginMode.ISOLATED)

        with create_trader(self.context.broker, live_trading=self.context.live_mode):
            actors = [
                actor
                for symbol, timeframe in symbols_and_timeframes
                for strategy in strategies
                for actor in self.strategy_actors
                if actor.strategy == strategy[0] and actor.timeframe == timeframe and actor.symbol == symbol
            ]

            for actor in actors:
                if actor.running:
                    actor.stop()

                actor.start()

            await self.context.ws_handler.subscribe(symbols_and_timeframes)
