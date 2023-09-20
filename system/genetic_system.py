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
from core.models.individual import Individual
from core.interfaces.abstract_system import AbstractSystem
from core.queries.broker import GetAccountBalance, GetSymbols
from core.queries.portfolio import GetFitness, GetTopStrategy
from infrastructure.estimator import Estimator
from core.models.strategy import Strategy

from .squad import Squad
from .trading_context import TradingContext

logger = logging.getLogger(__name__)


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    EVALUATION = auto()
    TRADING = auto()
    STOPPED = auto()

class Event(Enum):
    RUN_BACKTEST = auto()
    BACKTEST_COMPLETE = auto()
    EVALUATION_COMPLETE = auto()
    OPTIMIZATION_COMPLETE = auto()
    TRADING_STOPPED = auto()
    SYSTEM_STOP = auto()


class GeneticSystem(AbstractSystem):
    def __init__(self, context: TradingContext):
        super().__init__()
        self.context = context
        self.state = SystemState.BACKTESTING
        self.event_queue = asyncio.Queue()
        self.population: list[Individual] = []
        self.generation = 0

    async def start(self):
        await self._generate_population()
        await self._run_backtest()
        
        while True:
            event = await self.event_queue.get()
            match self.state:
                case SystemState.BACKTESTING:
                    if event == Event.BACKTEST_COMPLETE:
                        self.state = SystemState.EVALUATION
                        await self._run_evaluation()
                case SystemState.EVALUATION:
                    if event == Event.EVALUATION_COMPLETE:
                        self.state = SystemState.OPTIMIZATION
                        await self._run_optimization()
                    if event == Event.RUN_BACKTEST:
                        self.state = SystemState.BACKTESTING
                        await self._run_backtest()
                case SystemState.OPTIMIZATION:
                    if event == Event.EVALUATION_COMPLETE:
                        self.state = SystemState.TRADING
                        await self._run_trading()
                    if event == Event.SYSTEM_STOP:
                        return

    def stop(self):
        self.event_queue.put_nowait(Event.SYSTEM_STOP)

    async def _run_backtest(self):
        logger.info(f"Run backtest: {len(self.population)}")

        total_steps = len(self.population) // self.context.backtest_parallel
       
        estimator = Estimator(total_steps)

        batch = []
        
        async for squad in self._generate_actors(self.population):
            batch.append(squad)
            
            if len(batch) == self.context.backtest_parallel:
                await self._process_batch(batch)
                
                logger.info(f"Estimated remaining time: {estimator.remaining_time():.2f} seconds")
                
                batch = []

        if batch:
            await self._process_batch(batch)

        await self.event_queue.put(Event.BACKTEST_COMPLETE)

    async def _process_batch(self, batch):
        tasks = [self._process_squad(squad) for squad in batch]
        await asyncio.gather(*tasks)

    async def _process_squad(self, squad: Squad):
        await squad.start()
        
        await self._refresh_account()
        
        await self.execute(
            BacktestRun(self.context.datasource, squad.symbol, squad.timeframe, self.context.lookback, self.context.batch_size))

        await squad.stop()

    async def _run_evaluation(self):
        logger.info('Run Evaluation')

        if self.generation >= self.context.max_generations:
            await self.event_queue.put(Event.EVALUATION_COMPLETE)
            return

        for individual in self.population:
            fitness_value = await self.query(GetFitness(individual.symbol, individual.timeframe, individual.strategy))
            individual.update_fitness(fitness_value)

        parents = []
        selected_parents_indices = set()

        while len(parents) < len(self.population) // 2:
            contenders = np.random.choice(self.population, size=5, replace=False)
            winner = max(contenders, key=lambda individual: individual.fitness)
            
            winner_index = self.population.index(winner)

            if winner_index not in selected_parents_indices:
                parents.append(winner)
                selected_parents_indices.add(winner_index)

        while len(parents) % 2 != 0:
            contenders = np.random.choice(self.population, size=5, replace=False)
            winner = max(contenders, key=lambda individual: individual.fitness)
            winner_index = self.population.index(winner)
            
            if winner_index not in selected_parents_indices:
                parents.append(winner)
                selected_parents_indices.add(winner_index)

        children = []
        
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = self._crossover(parent1, parent2)
    
            children.extend([child1, child2])

        self.population.sort(key=lambda individual: individual.fitness)
        self.population[:len(children)] = children

        self.generation += 1

        await self.event_queue.put(Event.RUN_BACKTEST)
   
    async def _run_optimization(self):
        logger.info('Run optimization')
        
        strategies = await self.query(GetTopStrategy(num=5))

        logger.info(strategies)

        await self.event_queue.put(Event.OPTIMIZATION_COMPLETE)

    async def _run_trading(self):
        logger.info('Run trading')
        
        strategies = await self.query(GetTopStrategy(num=1))
        
        logger.info(strategies)

        symbols = [strategy[1] for strategy in strategies]
        symbols_and_timeframes = sorted(list(product(symbols, self.context.timeframes)), key=lambda x: x[1])
        
        await self.execute(Subscribe(symbols_and_timeframes))

        trading_data = list(product(symbols_and_timeframes, [strategy[0] for strategy in strategies]))
    
        async for squad in self._generate_actors(trading_data, self.context.live_mode):
            await self.execute(
                UpdateSettings(squad.symbol, self.context.leverage, PositionMode.ONE_WAY, MarginMode.ISOLATED))
            
            await squad.start()
            
            await self._refresh_account()
         
    async def _generate_actors(self, population, is_live=False):
        for individual in population:
            yield self.context.squad_factory.create_squad(individual.symbol, individual.timeframe, individual.strategy, is_live)

    async def _generate_population(self):
        strategies = self.context.strategy_generator.generate(self.context.sample_size)
       
        logger.info(f"Total strategies: {len(strategies)}")

        all_symbols = await self.query(GetSymbols())
        filtered_symbols = [symbol for symbol in all_symbols if symbol.name not in self.context.blacklist]

        num_symbols_to_sample = min(self.context.sample_size, len(filtered_symbols))
        num_timeframes_to_sample = min(self.context.sample_size, len(self.context.timeframes))

        sampled_symbols = np.random.choice(filtered_symbols, size=num_symbols_to_sample, replace=False)
        sampled_timeframes = np.random.choice(self.context.timeframes, size=num_timeframes_to_sample, replace=False)

        logger.info(f"Total sampled symbols: {len(sampled_symbols)}")
        logger.info(f"Total sampled timeframes: {len(sampled_timeframes)}")

        symbols_and_timeframes = list(product(sampled_symbols, sampled_timeframes))
        backtest_data = list(product(symbols_and_timeframes, strategies))

        shuffle(backtest_data)
        
        for (symbol, timeframe), strategy in backtest_data:
            self.population.append(Individual(symbol, timeframe, strategy))
    
    async def _refresh_account(self):
        account_size = await self.query(GetAccountBalance())
        await self.execute(UpdateAccountSize(account_size))

    def _crossover(self, parent1, parent2):
        attributes = ['signal', 'symbol', 'timeframe']
        chosen_attr = np.random.choice(attributes)

        if parent1.strategy.name == parent2.strategy.name:
            if chosen_attr == 'signal':
                child1_strategy = Strategy(parent1.strategy.name, parent2.strategy.signal, parent1.strategy.filter, parent1.strategy.stop_loss)
                child2_strategy = Strategy(parent2.strategy.name, parent1.strategy.signal, parent2.strategy.filter, parent2.strategy.stop_loss)
                return Individual(parent1.symbol, parent1.timeframe, child1_strategy), Individual(parent2.symbol, parent2.timeframe, child2_strategy)
        
        if chosen_attr == 'symbol':
            return Individual(parent2.symbol, parent1.timeframe, parent1.strategy), Individual(parent1.symbol, parent2.timeframe, parent2.strategy)
        
        elif chosen_attr == 'timeframe':
            return Individual(parent1.symbol, parent2.timeframe, parent1.strategy), Individual(parent2.symbol, parent1.timeframe, parent2.strategy)
        
        return parent1, parent2