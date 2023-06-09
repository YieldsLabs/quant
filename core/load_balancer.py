import random
import numpy as np


class LoadBalancer:
    def __init__(self, priority_groups: int):
        self._group_event_counts = np.zeros(priority_groups)
        self._initialize_load_balancer(priority_groups)

    def _initialize_load_balancer(self, priority_groups: int):
        self._kp = 1.0
        self._ki = 0.6
        self._kd = 0.3
        self._integral_errors = np.zeros(priority_groups)
        self._previous_errors = np.zeros(priority_groups)
        self._target_ratios = 1 / (np.arange(priority_groups) + 1)

    def determine_priority_group(self, priority: int) -> int:
        total_events = self._group_event_counts.sum()

        if total_events == 0:
            return min(max(priority - 1, 0), len(self._group_event_counts) - 1)

        processed_ratios = self._group_event_counts / total_events
        errors = self._target_ratios - processed_ratios
        self._integral_errors += errors
        derivative_errors = errors - self._previous_errors
        self._previous_errors = errors

        control_outputs = (self._kp * errors + self._ki * self._integral_errors + self._kd * derivative_errors)
        control_output_sum = control_outputs.sum()
        weights = control_outputs / control_output_sum

        return random.choices(range(len(control_outputs)), weights=weights)[0]
