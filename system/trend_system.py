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

class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext):
        super().__init__()
        self.context = context
        self.state = SystemState.BACKTESTING
        self.event_queue = asyncio.Queue()

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

    def _diversified_strategies(self):
        atr_multi_values = [0.87, 0.94, 1.05]
        moving_average_periods = [(50, 100), (30, 70), (20, 60)]
        ma_types = [MovingAverageType.SMA, MovingAverageType.EMA, MovingAverageType.WMA, MovingAverageType.DEMA]

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
    
    def _random_strategies(self, num=21):
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

    async def _run_backtest(self):
        logger.info('Run backtest')
        
        strategies = self._random_strategies() + self._diversified_strategies()
        shuffle(strategies)

        logger.info(f"Total strategies: {len(strategies)}")

        symbols = await self.query(GetSymbols())

        if len(self.context.blacklist) > 0:
            symbols = [symbol for symbol in symbols if symbol.name not in set(self.context.blacklist)]
        
        shuffle(symbols)
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])

        logger.info(f"Total symbols: {len(symbols)}")

        total_steps = len(symbols_and_timeframes) * len(strategies)
       
        estimator = Estimator(total_steps)

        async for squad in self._generate_backtest_actors(symbols_and_timeframes, strategies):
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
        
        strategies = await self.query(GetTopStrategy(num=1))
        
        logger.info(strategies)

        symbols = [strategy[1] for strategy in strategies]
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])
        
        await self.execute(Subscribe(symbols_and_timeframes))
    
        async for squad in self._generate_trading_actors(symbols_and_timeframes, strategies):
            await self.execute(
                UpdateSettings(squad.symbol, self.context.leverage, PositionMode.ONE_WAY, MarginMode.ISOLATED))
            
            await squad.start()
            
            account_size = await self.query(GetAccountBalance())
            await self.execute(UpdateAccountSize(account_size))

         
    async def _generate_backtest_actors(self, symbols_and_timeframes, strategies):
        for symbol, timeframe in symbols_and_timeframes:
            for strategy in strategies:
                yield self.context.squad_factory.create_squad(symbol, timeframe, strategy, False)

    async def _generate_trading_actors(self, symbols_and_timeframes, strategies):
        for symbol, timeframe in symbols_and_timeframes:
            for strategy, strategy_symbol in strategies:
                if symbol == strategy_symbol:
                    yield self.context.squad_factory.create_squad(symbol, timeframe, strategy, True)
