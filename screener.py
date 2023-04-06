from analytics.performance import PerformanceStats
from broker.futures_bybit_broker import FuturesBybitBroker
from optimization.strategy_screening import StrategyScreening
from ohlcv.bybit_datasource import BybitDataSource
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from shared.timeframes import Timeframes
from strategy.bollinger_engulfing_strategy import BollingerEngulfing

from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder


API_KEY = "72BhMPoxIHux9w2O6X"
API_SECRET = "Hk9gmfO1YF2JaatRI2jjxwUfEPuq0eapfoMX"

broker = FuturesBybitBroker(API_KEY, API_SECRET)

symbols = [
    'ADAUSDT',
    'NEARUSDT',
    'XRPUSDT',
    'SOLUSDT'
]

timeframes = [
    Timeframes.ONE_MINUTE,
    Timeframes.THREE_MINUTES,
    Timeframes.FIVE_MINUTES
]

lookback = 1000
lookback_period = 50
sma_period = 50
slow_sma_period = 100
initial_account_size = 1000
num_last_trades = 15
stdev_multi = 2

atr_multi = [
    0.85,
    # 1,
    # 1.5,
    2
]

risk_reward = [
    1.5,
    2,
    # 3,
    4,
    # 5
]

datasource = BybitDataSource(broker, lookback)
ohlcv_context = OhlcvContext(datasource)

strategies = [
    # EngulfingSMA(slow_sma_period=slow_sma_period),
    BollingerEngulfing(sma_period=sma_period, multiplier=stdev_multi),
    # ExtremeEuphoriaBBStrategy(sma_period=sma_period, multiplier=stdev_multi),
    # KangarooTailStrategy(sma_period=slow_sma_period),
    # AwesomeOscillatorBBStrategy(sma_period=sma_period),
    # FairValueGapStrategy(slow_sma_period=slow_sma_period)
]

atrs = [ATRStopLossFinder(ohlcv_context, multiplier=atr_multi) for atr_multi in atr_multi]

stop_loss_finders = [] \
    + atrs \
    + [LowHighStopLossFinder(ohlcv_context, stop_loss_finder=atr, lookback_period=lookback_period) for atr in atrs]

take_profit_finders = [] \
    + [RiskRewardTakeProfitFinder(risk_reward_ratio=rrr) for rrr in risk_reward]

analytics = PerformanceStats(initial_account_size=initial_account_size)

screener = StrategyScreening(
    ohlcv=ohlcv_context,
    broker=broker,
    analytics=analytics,
    symbols=symbols,
    timeframes=timeframes,
    strategies=strategies,
    stop_loss_finders=stop_loss_finders,
    take_profit_finders=take_profit_finders
)

results_df = screener.run()

# print(results_df.head(10))
