import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.commands.backtest import BacktestRun
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.queries.broker import GetAccountBalance, GetSymbols

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
        async for actors in self._generate_actors():
            await asyncio.gather(*[actor.start() for actor in actors])

            signal = actors[0]

            await self.dispatcher.execute(
                BacktestRun(self.context.datasource, signal.symbol, signal.timeframe, self.context.lookback, self.context.batch_size))

            await asyncio.gather(*[actor.stop() for actor in actors])

            self.signals.append(signal)
            
    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        print('Run trading')

    async def _generate_actors(self):
        symbols  = await self.dispatcher.query(GetSymbols())
        account_size = await self.dispatcher.query(GetAccountBalance())
        
        symbols_and_timeframes = list(product(symbols, self.context.timeframes))
        shuffle(symbols_and_timeframes)
    
        for symbol, timeframe in symbols_and_timeframes:
            executor_actor = self.context.executor_factory.create_actor(symbol, timeframe, live=False)
            position_actor = self.context.position_factory.create_actor(symbol, timeframe, account_size)
            risk_actor = self.context.risk_factory.create_actor(symbol, timeframe)

            for path, strategy_name, strategy_parameters in self.context.strategies:
                strategy_path = f'./wasm/{path}.wasm'
                
                signal_actor = self.context.signal_factory.create_actor(symbol, timeframe, strategy_path, strategy_name, strategy_parameters)

                yield signal_actor, position_actor, risk_actor, executor_actor

