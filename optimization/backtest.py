from collections import defaultdict
from itertools import product
import random
from typing import Dict, List, Optional, Type
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.portfolio import PortfolioPerformance, PortfolioPerformanceEvent
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource

class Backtest(AbstractEventManager):
    def __init__(self, datasource: Type[AbstractDatasource]):
        super().__init__()
        self.datasource = datasource
        self.strategy_performance: Dict[str, Dict[str, PortfolioPerformance]] = defaultdict(dict)

    @register_handler(PortfolioPerformanceEvent)
    def _on_portfolio(self, event: PortfolioPerformanceEvent):
        strategy_id = event.id
        performance = event.performance
        
        _symbol = strategy_id.split("_")[0]
        
        self.strategy_performance[_symbol][strategy_id] = performance

        best_strategy = self._get_best_strategy(_symbol)
        
        print('---------------------------------------------------->')
        print(best_strategy)

    def _get_best_strategy(self, symbol: str, metric: str = 'sharpe_ratio', min_total_trades: int = 10) -> Optional[str]:
        if symbol not in self.strategy_performance:
            return None

        strategies = self.strategy_performance[symbol]

        if not strategies:
            return None

        # filtered_strategies = {k: v for k, v in strategies.items() if v.total_trades >= min_total_trades}

        # if not filtered_strategies:
        #     return None

        return max(strategies.items(), key=lambda x: getattr(x[1], metric, 0))


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
