import asyncio
from enum import Enum, auto
from itertools import product
import logging
from random import shuffle
import numpy as np

from core.commands.account import UpdateAccountSize
from core.commands.backtest import BacktestRun
from core.commands.broker import Subscribe, UpdateSettings
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy
from core.queries.broker import GetAccountBalance, GetSymbols
from core.queries.portfolio import GetTopStrategy
from infrastructure.estimator import Estimator
from strategy.indicator.cross_ma import CrossMovingAverageIndicator
from strategy.stop_loss.atr import ATRStopLoss

from .trading_context import TradingContext

logger = logging.getLogger(__name__)


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    TRADING = auto()
    STOPPED = auto()


class Event(Enum):
    BACKTEST_COMPLETE = auto()
    OPTIMIZE_COMPLETE = auto()
    TRADING_STOPPED = auto()
    SYSTEM_STOP = auto()


class StrategyGenerator:
    def generate(self, n_samples):
        strategies = self._diversified_strategies() + self._random_strategies(n_samples)
        shuffle(strategies)
        
        return strategies

    def _diversified_strategies(self):
        atr_multi_values = [0.87, 1.05, 2.6]
        moving_average_periods = [(50, 100), (30, 70), (21, 34)]
        ma_types = [
            MovingAverageType.ALMA,
            MovingAverageType.DEMA,
            MovingAverageType.FRAMA,
            MovingAverageType.SINWMA,
            MovingAverageType.TMA
        ]

        return [
            Strategy(
                'crossma', 
                (CrossMovingAverageIndicator(ma_type, StaticParameter(short_period), StaticParameter(long_period)),),
                ATRStopLoss(multi=StaticParameter(atr_multi_value))
            )
            for ma_type in ma_types
            for short_period, long_period in moving_average_periods
            for atr_multi_value in atr_multi_values
        ]
    
    def _random_strategies(self, num):
        strategies_set = set()

        while len(strategies_set) < num:
            moving_avg_type = np.random.choice(list(MovingAverageType))
            
            short_period = RandomParameter(5.0, 50.0, 5.0)
            long_period = RandomParameter(50.0, 200.0, 10.0)

            short_period, long_period = sorted([short_period, long_period])

            atr_multi = RandomParameter(0.85, 2, 0.05)

            strategy = Strategy(
                'crossma',
                (CrossMovingAverageIndicator(moving_avg_type, short_period, long_period),),
                ATRStopLoss(multi=atr_multi)
            )
            
            strategies_set.add(strategy)

        return list(strategies_set)


class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext, n_samples: int = 50):
        super().__init__()
        self.context = context
        self.state = SystemState.BACKTESTING
        self.event_queue = asyncio.Queue()
        self.strategy_generator = StrategyGenerator()
        self.n_samples = n_samples

    async def start(self):
       await self._run_backtest()
       
       while True:
            event = await self.event_queue.get()
            
            match self.state:
                case SystemState.BACKTESTING:
                    if event == Event.BACKTEST_COMPLETE:
                        self.state = SystemState.OPTIMIZATION
                        await self._run_optimization()
                case SystemState.OPTIMIZATION:
                    if event == Event.OPTIMIZE_COMPLETE:
                        self.state = SystemState.TRADING
                        await self._run_trading()
                    if event == Event.SYSTEM_STOP:
                        return

    def stop(self):
        self.event_queue.put_nowait(Event.SYSTEM_STOP)

    async def _run_backtest(self):
        logger.info('Run backtest')
        
        strategies = self.strategy_generator.generate(self.n_samples)

        logger.info(f"Total strategies: {len(strategies)}")

        symbols = await self.query(GetSymbols())

        if len(self.context.blacklist) > 0:
            symbols = [symbol for symbol in symbols if symbol.name not in set(self.context.blacklist)]
        
        sampled_symbols = np.random.choice(symbols, size=min(self.n_samples, len(symbols)), replace=False)

        logger.info(f"Total symbols: {len(sampled_symbols)}")

        sampled_timeframes = np.random.choice(self.context.timeframes, size=min(self.n_samples, len(self.context.timeframes)), replace=False)
        symbols_and_timeframes = list(product(sampled_symbols, sampled_timeframes))

        backtest_data = list(product(symbols_and_timeframes, strategies))
        shuffle(backtest_data)

        total_steps = len(backtest_data)
       
        estimator = Estimator(total_steps)

        async for squad in self._generate_actors(backtest_data):
            await squad.start()
            
            account_size = await self.query(GetAccountBalance())
            await self.execute(UpdateAccountSize(account_size))

            await self.execute(
                BacktestRun(self.context.datasource, squad.symbol, squad.timeframe, self.context.lookback, self.context.batch_size))

            logger.info(f"Estimated remaining time: {estimator.remaining_time():.2f} seconds")

            await squad.stop()

        await self.event_queue.put(Event.BACKTEST_COMPLETE)
            
    async def _run_optimization(self):
        logger.info('Run optimization')
        
        strategies = await self.query(GetTopStrategy(num=20))
       
        logger.info(strategies)

        await self.event_queue.put(Event.OPTIMIZE_COMPLETE)

    async def _run_trading(self):
        logger.info('Run trading')
        
        strategies = await self.query(GetTopStrategy(num=3))
        
        logger.info(strategies)

        symbols = [strategy[1] for strategy in strategies]
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])
        
        await self.execute(Subscribe(symbols_and_timeframes))

        trading_data = list(product(symbols_and_timeframes, [strategy[0] for strategy in strategies]))
    
        async for squad in self._generate_actors(trading_data, True):
            await self.execute(
                UpdateSettings(squad.symbol, self.context.leverage, PositionMode.ONE_WAY, MarginMode.ISOLATED))
            
            await squad.start()
            
            account_size = await self.query(GetAccountBalance())
            await self.execute(UpdateAccountSize(account_size))
         
    async def _generate_actors(self, data, is_live=False):
        for (symbol, timeframe), strategy in data:
            yield self.context.squad_factory.create_squad(symbol, timeframe, strategy, is_live)