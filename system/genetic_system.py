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
from core.events.backtest import BacktestStarted

from .squad import Squad
from .trading_context import TradingContext

logger = logging.getLogger(__name__)


class SystemState(Enum):
    GENERATE_POPULATION = auto()
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    EVOLUTION = auto()
    TRADING = auto()
    STOPPED = auto()

class Event(Enum):
    GENERATE_COMPLETE = auto()
    RUN_BACKTEST = auto()
    REGENERATE_POPULATION = auto()
    BACKTEST_COMPLETE = auto()
    EVOLUTION_COMPLETE = auto()
    OPTIMIZATION_COMPLETE = auto()
    TRADING_STOPPED = auto()
    SYSTEM_STOP = auto()

class GeneticAttributes(Enum):
    SYMBOL = auto()
    TIMEFRAME = auto()
    STRATEGY = auto()

class GeneticSystem(AbstractSystem):
    def __init__(self, context: TradingContext, elite_count: int, mutation_rate: float):
        super().__init__()
        self.context = context
        self.state = SystemState.GENERATE_POPULATION
        self.event_queue = asyncio.Queue()
        self.population: list[Individual] = []
        self.elite_count = elite_count
        self.mutation_rate = mutation_rate
        self.generation = 0

    async def start(self):
        await self._generate_population()
        
        while True:
            event = await self.event_queue.get()
            match self.state:
                case SystemState.GENERATE_POPULATION:
                    if event == Event.GENERATE_COMPLETE:
                        self.state = SystemState.BACKTESTING
                        await self._run_backtest()
                case SystemState.BACKTESTING:
                    if event == Event.BACKTEST_COMPLETE:
                        self.state = SystemState.EVOLUTION
                        await self._run_evolution()
                case SystemState.EVOLUTION:
                    if event == Event.EVOLUTION_COMPLETE:
                        self.state = SystemState.OPTIMIZATION
                        await self._run_optimization()
                    if event == Event.RUN_BACKTEST:
                        self.state = SystemState.BACKTESTING
                        await self._run_backtest()
                case SystemState.OPTIMIZATION:
                    if event == Event.OPTIMIZATION_COMPLETE:
                        self.state = SystemState.TRADING
                        await self._run_trading()
                    if event == Event.REGENERATE_POPULATION:
                        self.state = SystemState.GENERATE_POPULATION
                        await self._generate_population()
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
        
        await self.dispatch(BacktestStarted(squad.symbol, squad.timeframe, squad.strategy))
    
        await self.execute(
            BacktestRun(self.context.datasource, squad.symbol, squad.timeframe, self.context.lookback, self.context.batch_size))

        await squad.stop()

    async def _run_evolution(self):
        logger.info(f"Run Evolution: {self.generation}")

        if self.generation >= self.context.max_generations:
            await self.event_queue.put(Event.EVOLUTION_COMPLETE)
            return

        for individual in self.population:
            fitness_value = await self.query(GetFitness(individual.symbol, individual.timeframe, individual.strategy))
            individual.update_fitness(fitness_value)

        elite = sorted(self.population, key=lambda individual: individual.fitness, reverse=True)[:self.elite_count]

        logger.info('Parents selection')
        candidates = list(self.population)
        parents = []

        while len(parents) < (len(self.population) - self.elite_count):
            contenders = np.random.choice(candidates, size=5, replace=True)
            winner = max(contenders, key=lambda individual: individual.fitness)
            parents.append(winner)
            candidates.remove(winner)

        if len(parents) % 2 != 0:
            parents.pop()

        logger.info('Mutation')
        for idx, parent in enumerate(parents):
            if np.random.rand() < self.mutation_rate:
                parents[idx] = await self._mutate(parent)

        children = []
        for i in range(0, len(parents), 2):
            child1, child2 = self._crossover(parents[i], parents[i + 1])
            children.extend([child1, child2])

        logger.info('New population')
        self.population[:len(children)] = children
        self.population[:self.elite_count] = elite

        self.generation += 1
        await self.event_queue.put(Event.RUN_BACKTEST)
   
    async def _run_optimization(self):
        logger.info('Run optimization')
        
        strategies = await self.query(GetTopStrategy(num=5))

        logger.info(strategies)

        if not len(strategies):
            await self.event_queue.put(Event.REGENERATE_POPULATION)
            return

        await self.event_queue.put(Event.OPTIMIZATION_COMPLETE)

    async def _run_trading(self):
        logger.info('Run trading')
        
        strategies = await self.query(GetTopStrategy(num=1))
        
        logger.info(strategies)

        symbols_and_timeframes = [(strategy[0], strategy[1]) for strategy in strategies]

        await self.execute(Subscribe(symbols_and_timeframes))

        population = []
        
        for symbol, timeframe, strategy in strategies:
            population.append(Individual(symbol, timeframe, strategy))

        async for squad in self._generate_actors(population, self.context.live_mode):
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

        await self.event_queue.put(Event.GENERATE_COMPLETE)

    async def _refresh_account(self):
        account_size = await self.query(GetAccountBalance())
        await self.execute(UpdateAccountSize(account_size))

    def _crossover(self, parent1, parent2):
        chosen_attr = np.random.choice(list(GeneticAttributes))

        if parent1.strategy.name == parent2.strategy.name:
            if chosen_attr == GeneticAttributes.STRATEGY:
                child1_strategy = Strategy(parent1.strategy.name, parent2.strategy.signal, parent1.strategy.filter, parent1.strategy.stop_loss)
                child2_strategy = Strategy(parent2.strategy.name, parent1.strategy.signal, parent2.strategy.filter, parent2.strategy.stop_loss)
                return Individual(parent1.symbol, parent1.timeframe, child1_strategy), Individual(parent2.symbol, parent2.timeframe, child2_strategy)
        
        if chosen_attr == GeneticAttributes.SYMBOL:
            return Individual(parent2.symbol, parent1.timeframe, parent1.strategy), Individual(parent1.symbol, parent2.timeframe, parent2.strategy)
        
        elif chosen_attr == GeneticAttributes.TIMEFRAME:
            return Individual(parent1.symbol, parent2.timeframe, parent1.strategy), Individual(parent2.symbol, parent1.timeframe, parent2.strategy)
        
        return parent1, parent2
    
    async def _mutate(self, individual):
        mutation_choice = np.random.choice(list(GeneticAttributes))

        if mutation_choice == GeneticAttributes.STRATEGY:
            strategies = self.context.strategy_generator.generate(5)
            individual.strategy = strategies[0]
        
        elif mutation_choice == GeneticAttributes.SYMBOL:
            all_symbols = await self.query(GetSymbols())
            filtered_symbols = [symbol for symbol in all_symbols if symbol.name not in self.context.blacklist]
            individual.symbol = np.random.choice(filtered_symbols)
        
        elif mutation_choice == GeneticAttributes.TIMEFRAME:
            individual.timeframe = np.random.choice(self.context.timeframes)

        return individual