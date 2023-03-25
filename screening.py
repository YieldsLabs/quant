from dotenv import load_dotenv
import os
import itertools
import pandas as pd

from broker import Broker
from backtester import Backtester
from strategy.AwesomeOscillatorBBStrategy import AwesomeOscillatorBBStrategy
from strategy.BollingerEngulfing import BollingerEngulfing
from strategy.EngulfingSMA import EngulfingSMA
from strategy.FalseBreakoutStrategy import FalseBreakoutStrategy
from strategy.ExtremeEuphoriaBBStrategy import ExtremeEuphoriaBBStrategy
from strategy.KangarooTailStrategy import KangarooTailStrategy
from strategy.KeltnerExtremeEuphoriaStrategy import KeltnerExtremeEuphoriaStrategy
from strategy.PSARZeroLagEMAStrategy import PSARZeroLagEMAStrategy
from strategy.PiercingStochasticStrategy import PiercingStochasticStrategy
from strategy.SmoothVWMAScalpingContrarian import SmoothVWMAScalpingContrarian
from strategy.StructuredDurationStrategy import StructuredDurationStrategy
from strategy.SwingIndicatorStrategy import SwingIndicatorStrategy
from strategy.UTBotAlertsBBStrategy import UTBotAlertsBBStrategy
from strategy.BollingerEngulfing import BollingerEngulfing
from tradetype import TradeType

from risk_management.riskmanager import RiskManager
from risk_management.stop_loss import LowHighStopLossFinder, ATRStopLossFinder, TrailingStopLossFinder
from risk_management.take_profit import EmptyTakeProfitFinder, RiskRewardTakeProfitFinder

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

broker = Broker(API_KEY, API_SECRET)
symbols = ['LPTUSDT', 'XRPUSDT', 'ETHUSDT', 'SOLUSDT', 'UNFIUSDT']
timeframes = ['1m']
row_number = 2000
lookback_period = 30
risk_reward_ratio = 1.5
multiplier = 1.2

strategies = [
    EngulfingSMA(),
    ExtremeEuphoriaBBStrategy(),
    SwingIndicatorStrategy(),
    StructuredDurationStrategy(),
    KangarooTailStrategy(),
    AwesomeOscillatorBBStrategy(),
    SmoothVWMAScalpingContrarian(),
    BollingerEngulfing(),
]
stop_loss_finders = [
    TrailingStopLossFinder(lookback_period=lookback_period),
    ATRStopLossFinder(multiplier=multiplier)
]
take_profit_finders = [
    RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
    EmptyTakeProfitFinder()
]
combinations = list(itertools.product(symbols, timeframes, strategies, stop_loss_finders, take_profit_finders))
results_list = []

for symbol, timeframe, strategy, stop_loss_finder, take_profit_finder in combinations:
    ohlcv = broker.get_historical_data(symbol, timeframe, limit=row_number)
    stop_loss_finder.set_ohlcv(ohlcv)

    rm = RiskManager(stop_loss_finder, take_profit_finder)
    backtester = Backtester(strategy, rm, ohlcv)
    result = backtester.run(trade_type=TradeType.BOTH)
    result.update({
        'symbol': symbol,
        'timeframe': timeframe,
        'strategy': strategy,
        'stop_loss_finder': stop_loss_finder,
        'take_profit_finder': take_profit_finder,
        'win_rate': result['win_rate'] * 100
    })

    results_list.append(result)
    
    print(f"{symbol} orders for strategy: {strategy}, TimeFrame: {timeframe}, StopLossFinder: {stop_loss_finder}, TakeProfitFinder: {take_profit_finder}")
    print(backtester.get_orders().head())

results_df = pd.DataFrame(results_list)
sorded_results = results_df.sort_values(by="total_pnl", ascending=False)

print(sorded_results[['strategy', 'take_profit_finder', 'stop_loss_finder', 'total_pnl', 'win_rate', 'symbol']])