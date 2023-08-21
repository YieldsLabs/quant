import numpy as np


class LoadBalancer:
    def __init__(self, priority_groups: int):
        self._group_event_counts = np.zeros(priority_groups)
        self._initialize_load_balancer(priority_groups)

    def _initialize_load_balancer(self, priority_groups: int):
        self._kp = 1.5
        self._ki = 0.8
        self._kd = 0.5
        self._integral_errors = np.zeros(priority_groups)
        self._previous_errors = np.zeros(priority_groups)
        self._target_ratios = 1 / (np.arange(priority_groups) + 1)

    def register_event(self, priority_group: int):
        if 0 <= priority_group < len(self._group_event_counts):
            self._group_event_counts[priority_group] += 1
        else:
            raise ValueError("Invalid priority group!")

    def determine_priority_group(self, priority: int) -> int:
        total_group = self._group_event_counts.sum()

        if total_group == 0:
            return np.clip(priority - 1, 0, len(self._group_event_counts) - 1)

        processed_ratios = self._group_event_counts / total_group

        errors = self._target_ratios - processed_ratios

        self._integral_errors += errors

        derivative_errors = errors - self._previous_errors

        self._previous_errors = errors.copy()

        control_outputs = (self._kp * errors
                           + self._ki * self._integral_errors
                           + self._kd * derivative_errors)

        weights = np.abs(control_outputs)
        weights /= weights.sum()

        return np.random.choice(np.arange(len(control_outputs)), p=weights)
