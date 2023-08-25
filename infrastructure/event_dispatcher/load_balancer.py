import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

class LoadBalancer:
    def __init__(self, priority_groups: int):
        self._group_event_counts = np.zeros(priority_groups)
        self._initialize_load_balancer(priority_groups)
        self._group_event_counts_threshold = 1e4

    def _initialize_load_balancer(self, priority_groups: int):
        self._kp = 0.5
        self._ki = 0.6
        self._kd = 0.1
        self._integral_errors = np.zeros(priority_groups)
        self._previous_errors = np.zeros(priority_groups)
        self._target_ratios = 1 / (np.arange(priority_groups) + 1)

    def register_event(self, priority_group: int):
        if 0 <= priority_group < len(self._group_event_counts):
            self._group_event_counts[priority_group] += 1
            
            if self._group_event_counts.max() > self._group_event_counts_threshold:
                self._group_event_counts *= 0.5
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

        # weights = np.abs(control_outputs)
        # weights /= weights.sum()

        weights = softmax(control_outputs)

        return np.random.choice(np.arange(len(control_outputs)), p=weights)
