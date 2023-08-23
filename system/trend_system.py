import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.models.broker import MarginMode, PositionMode
from core.events.backtest import BacktestStarted
from core.interfaces.abstract_system import AbstractSystem

from .trading_context import TradingContext


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    TRADING = auto()
    STOPPED = auto()


class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext, state: SystemState = SystemState.BACKTESTING):
        super().__init__()
        self.context = context
        self.state = state
        self.strategy_actors = []

    async def start(self):
        while True:
            match self.state:
                case SystemState.BACKTESTING:
                    await self._run_backtest()
                    self.state = SystemState.OPTIMIZATION
                case SystemState.OPTIMIZATION:
                    await self._run_optimization()
                    self.state = SystemState.TRADING
                case SystemState.TRADING:
                    await self._run_trading()
                    self.state = SystemState.STOPPED
                case SystemState.STOPPED:
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

        async with self.context.executor_factory.create_executor(live=False):
            for actor in self.strategy_actors:
                await self._ensure_actor_state(actor)

                await self.dispatcher.dispatch(
                    BacktestStarted(self.context.datasource, actor.strategy, self.context.lookback))
                
                await self.dispatcher.wait()
                await actor.stop()

    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        top_strategies = await self.context.portfolio.get_top_strategies(3)

        if len(top_strategies) == 0:
            return

        uniq_symbols = list(set([strategy.symbol for strategy in top_strategies]))

        for symbol in uniq_symbols:
            self.context.broker.set_settings(symbol, self.context.leverage, position_mode=PositionMode.ONE_WAY, margin_mode=MarginMode.ISOLATED)

        async with self.context.executor_factory.create_executor(self.context.live_mode):
            actors = list({
                actor
                for strategy in top_strategies
                for actor in self.strategy_actors
                if actor.strategy == strategy
            })

            for actor in actors:
                await self._ensure_actor_state(actor)

            symbols_and_timeframes = [(actor.strategy.symbol, actor.strategy.timeframe) for actor in actors]
            
            await self.context.ws_handler.subscribe(symbols_and_timeframes)

    async def _ensure_actor_state(self, actor):
        if actor.running:
            actor.stop()

        await actor.start()
