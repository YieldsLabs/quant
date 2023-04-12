import inspect
from itertools import product
import numpy as np


strategy_hyperparameters = {
    'overbought': [10, 30, 5],
    'oversold': [70, 90, 5],
    'sma_period': [20, 100, 10],
    'slow_sma_period': [50, 200, 2],
    'stdev_multi': [0.5, 2, 0.5],
    'tolerance': [0.002, 0.01, 0.002],
    'lookback': [50, 150, 50]
}

stoploss_hyperparameters = {
    'atr_multi': [0.7, 1.6, 0.1],
}

takeprofit_hyperparameters = {
    'risk_reward_ratio': [1, 5.5, 0.5],
}


def create_instances_with_hyperparameters(class_map, hyperparameters, pre_args=None):
    instances_dict = {}

    if pre_args is None:
        pre_args = tuple()

    for cls in class_map.values():
        signature = inspect.signature(cls.__init__)
        parameters = signature.parameters

        applicable_hyperparams = {
            param_name: np.arange(*hyperparameters[param_name])
            for param_name in parameters
            if param_name in hyperparameters
        }

        if not applicable_hyperparams:
            instance = cls(*pre_args)
            instances_dict[str(instance)] = instance
        else:
            param_combinations = product(*applicable_hyperparams.values())
            for combination in param_combinations:
                instance = cls(*pre_args, **dict(zip(applicable_hyperparams.keys(), combination)))
                instances_dict[str(instance)] = instance

    return list(instances_dict.values())