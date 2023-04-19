from collections import defaultdict
from itertools import product
import random
from typing import Dict, List, Type
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.portfolio import BestStrategyEvent, PortfolioPerformance, PortfolioPerformanceEvent
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from labels.parse_label import parse_meta_label

class Backtest(AbstractEventManager):
    def __init__(self, datasource: Type[AbstractDatasource]):
        super().__init__()
        self.datasource = datasource
        self.strategy_performance: Dict[str, Dict[str, PortfolioPerformance]] = defaultdict(dict)

    @register_handler(PortfolioPerformanceEvent)
    def _on_portfolio(self, event: PortfolioPerformanceEvent):
        strategy_id = event.id
        performance = event.performance
        
        symbol = parse_meta_label(strategy_id)[0]
        
        self.strategy_performance[symbol][strategy_id] = performance

        best_strategy = self._simple_search_the_best_strategy(symbol)

        if best_strategy:
            self.dispatcher.dispatch(BestStrategyEvent(id=best_strategy[0], performance=best_strategy[1]))
    
    def run(self, symbols: List[str], timeframes: List[Timeframe], lookback: int = 3000):
        symbols_and_timeframes = list(product(symbols, timeframes))
        
        random.shuffle(symbols_and_timeframes)

        for symbol, timeframe in symbols_and_timeframes:
            historical_data = self.datasource.fetch(symbol, timeframe, lookback)

            self._process_historical_data(symbol, timeframe, historical_data)
    
    def _process_historical_data(self, symbol: str, timeframe: Timeframe, historical_data):
        for timestamp, open, high, low, close, volume in historical_data:
            ohlcv = OHLCV(timestamp, float(open), float(high), float(low), float(close), float(volume))
            
            self.dispatcher.dispatch(OHLCVEvent(symbol, timeframe, ohlcv))

    def _simple_search_the_best_strategy(self, symbol: str, metric: str = 'sharpe_ratio', min_total_trades: int = 20):
        if symbol not in self.strategy_performance:
            return None

        strategies = self.strategy_performance[symbol]

        if not strategies:
            return None

        metric_values = [getattr(strategies[name], metric, 0) for name in strategies if strategies[name].total_trades >= min_total_trades]
        
        if not metric_values:
            return None

        avg_metric = sum(metric_values) / len(metric_values)

        best_strategy = max(strategies.items(), key=lambda x: getattr(x[1], metric, 0))

        if getattr(strategies[best_strategy[0]], metric, 0) < avg_metric:
            return None

        return best_strategy
