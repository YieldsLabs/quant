import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.commands.account import AccountUpdate

from core.commands.backtest import BacktestRun
from core.commands.position import PositionCloseAll
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.queries.broker import GetSymbols
from core.queries.position import PositionAll

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
        self.signals = []

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
        async for signal, executor in self._generate_actors():
            await asyncio.gather(signal.start(), executor.start())

            await self.dispatcher.execute(
                BacktestRun(
                    self.context.datasource,
                    signal.symbol,
                    signal.timeframe,
                    self.context.lookback,
                    self.context.batch_size
                ))

            await asyncio.gather(signal.stop(), executor.stop())

            self.signals.append(signal)

    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        print('Run trading')
        # top_strategies = await self.context.portfolio.get_top_strategies(3)

        # print(top_strategies)

        # if len(top_strategies) == 0:
        #     return

        # uniq_symbols = list(set([strategy.symbol for strategy in top_strategies]))

        # for symbol in uniq_symbols:
        #     self.context.broker.set_settings(symbol, self.context.leverage, position_mode=PositionMode.ONE_WAY, margin_mode=MarginMode.ISOLATED)

        # async with self.context.executor_factory.create_executor(self.context.live_mode):
        #     actors = list({
        #         actor
        #         for strategy in top_strategies
        #         for actor in self.strategy_actors
        #         if actor.strategy == strategy
        #     })

        #     symbols_and_timeframes = [(actor.strategy.symbol, actor.strategy.timeframe) for actor in actors]
            
        #     await self.context.ws_handler.subscribe(symbols_and_timeframes)


    async def _generate_actors(self):
        symbols = await self.dispatcher.query(GetSymbols())
        symbols_and_timeframes = list(product(symbols, self.context.timeframes))
        shuffle(symbols_and_timeframes)
    
        for symbol, timeframe in symbols_and_timeframes:
            for strategy in self.context.strategies:
                strategy_path = f'./wasm/{strategy[0]}.wasm'
                strategy_name = strategy[1]
                strategy_parameters = strategy[2]
                
                signal_actor = self.context.signal_factory.create_actor(symbol, timeframe, strategy_path, strategy_name, strategy_parameters)
                executor_actor = self.context.executor_factory.create_actor(symbol, timeframe, live=False)

                yield signal_actor, executor_actor

