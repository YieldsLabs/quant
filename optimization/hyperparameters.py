strategy_hyperparameters = {
    'overbought': [10, 30, 10],
    'oversold': [70, 90, 10],
    'sma_period': [20, 100, 10],
    'slow_sma_period': [50, 200, 50],
    'stdev_multi': [0.5, 2, 0.5],
    'tolerance': [0.002, 0.01, 0.002],
    'lookback': [50, 150, 50],
    'ao_short_period': [5, 15, 5],
    'ao_long_period': [20, 50, 15]
}

stoploss_hyperparameters = {
    'atr_multi': [0.7, 2.1, 0.1],
}

takeprofit_hyperparameters = {
    'risk_reward_ratio': [1, 6, 0.5],
}
