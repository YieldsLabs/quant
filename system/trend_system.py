import asyncio
from enum import Enum, auto
from itertools import product
import logging
from random import shuffle

from core.commands.account import UpdateAccountSize
from core.commands.backtest import BacktestRun
from core.commands.broker import Subscribe, UpdateSettings
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.queries.broker import GetAccountBalance, GetSymbols
from core.queries.portfolio import GetTopStrategy
from infrastructure.estimator import Estimator

from .trading_context import TradingContext

logger = logging.getLogger(__name__)


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    TRADING = auto()
    STOPPED = auto()


class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext):
        super().__init__()
        self.context = context
        self.state = SystemState.BACKTESTING

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
                case SystemState.STOPPED:
                    return

    async def _run_backtest(self):
        logger.info('Run backtest')
        
        symbols = await self.query(GetSymbols())

        if len(self.context.symbols) > 0:
            symbols = [symbol for symbol in symbols if symbol.name in self.context.symbols]
        
        shuffle(symbols)
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])

        total_steps = len(symbols_and_timeframes) * len(self.context.strategies)
        estimator = Estimator(total_steps)

        async for actors in self._generate_backtest_actors(symbols_and_timeframes, self.context.strategies):
            account_size = await self.query(GetAccountBalance())
            await self.execute(UpdateAccountSize(account_size))
        
            await asyncio.gather(*[actor.start() for actor in actors])

            signal = actors[0]

            await self.execute(
                BacktestRun(self.context.datasource, signal.symbol, signal.timeframe, self.context.lookback, self.context.batch_size))

            logger.info(f"Estimated remaining time: {estimator.remaining_time():.2f} seconds")

            await asyncio.gather(*[actor.stop() for actor in actors])
            
    async def _run_optimization(self):
        logger.info('Run optimization')
        strategies = await self.query(GetTopStrategy(num=20))
       
        logger.info(strategies)

    async def _run_trading(self):
        logger.info('Run trading')
        
        strategies = await self.query(GetTopStrategy(num=1))
        
        logger.info(strategies)

        symbols = [strategy[1] for strategy in strategies]
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])
        
        await self.execute(Subscribe(symbols_and_timeframes))
    
        async for actors in self._generate_trading_actors(symbols_and_timeframes, strategies):
            account_size = await self.query(GetAccountBalance())
            await self.execute(UpdateAccountSize(account_size))
            
            signal = actors[0]

            await self.execute(
                UpdateSettings(signal.symbol, self.context.leverage, PositionMode.ONE_WAY, MarginMode.ISOLATED))
            
            await asyncio.gather(*[actor.start() for actor in actors])

    def _initialize_actors(self, symbol, timeframe, is_live):
        executor_actor = self.context.executor_factory.create_actor(symbol, timeframe, live=is_live)
        position_actor = self.context.position_factory.create_actor(symbol, timeframe)
        risk_actor = self.context.risk_factory.create_actor(symbol, timeframe)
        
        return executor_actor, position_actor, risk_actor
         
    async def _generate_backtest_actors(self, symbols_and_timeframes, strategies):
        for symbol, timeframe in symbols_and_timeframes:
            executor_actor, position_actor, risk_actor = self._initialize_actors(symbol, timeframe, False)

            for strategy_name, strategy_parameters in strategies:
                signal_actor = self.context.signal_factory.create_actor(
                    symbol, timeframe, self.context.strategy_path, strategy_name, strategy_parameters)

                yield signal_actor, position_actor, risk_actor, executor_actor

    async def _generate_trading_actors(self, symbols_and_timeframes, strategies):
        for symbol, timeframe in symbols_and_timeframes:
            executor_actor, position_actor, risk_actor = self._initialize_actors(symbol, timeframe, self.context.live_mode)
            
            for strategy, strategy_symbol in strategies:
                if symbol == strategy_symbol:
                    signal_actor = self.context.signal_factory.create_actor(
                        symbol, timeframe, self.context.strategy_path, strategy.name, strategy.hyperparameters)
                    
                    yield signal_actor, position_actor, risk_actor, executor_actor
