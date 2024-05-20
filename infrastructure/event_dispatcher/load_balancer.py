import numpy as np


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


class LoadBalancer:
    def __init__(
        self,
        priority_groups: int,
        initial_kp: float = 0.3,
        initial_ki: float = 0.6,
        initial_kd: float = 0.1,
        learning_rate: float = 0.001,
        decay_rate: float = 0.99,
    ):
        self._group_event_counts = np.zeros(priority_groups)
        self._initialize_load_balancer(
            priority_groups, initial_kp, initial_ki, initial_kd
        )
        self._group_event_counts_threshold = 1e4
        self._learning_rate = learning_rate
        self._decay_rate = decay_rate

    def _initialize_load_balancer(
        self,
        priority_groups: int,
        initial_kp: float,
        initial_ki: float,
        initial_kd: float,
    ):
        self._kp = np.ones(priority_groups) * initial_kp
        self._ki = np.ones(priority_groups) * initial_ki
        self._kd = np.ones(priority_groups) * initial_kd

        self._integral_errors = np.zeros(priority_groups)
        self._previous_errors = np.zeros(priority_groups)
        self._target_ratios = 1 / (np.arange(priority_groups) + 1)

    def register_event(self, priority_group: int):
        if not 0 <= priority_group < len(self._group_event_counts):
            raise ValueError(f"Invalid priority group: {priority_group}")

        self._group_event_counts[priority_group] += 1

        if self._group_event_counts.max() > self._group_event_counts_threshold:
            self._group_event_counts *= 0.5

        self._group_event_counts_threshold = max(
            self._group_event_counts_threshold * 1.1, 1e4
        )

    def determine_priority_group(self, priority: int) -> int:
        total_group = self._group_event_counts.sum()

        if total_group == 0:
            return np.clip(priority - 1, 0, len(self._group_event_counts) - 1)

        processed_ratios = self._group_event_counts / total_group
        errors = self._target_ratios - processed_ratios
        self._update_pid(errors)

        control_outputs = (
            self._kp * errors
            + self._ki * self._integral_errors
            + self._kd * (errors - self._previous_errors)
        )

        self._previous_errors = errors.copy()

        weights = softmax(control_outputs)
        self._learning_rate *= self._decay_rate

        return np.random.choice(np.arange(len(control_outputs)), p=weights)

    def _update_pid(self, errors: np.ndarray):
        for i, error in enumerate(errors):
            self._integral_errors[i] += error
            self._kp[i] = np.clip(self._kp[i] + self._learning_rate * error, 0, 1)
            self._ki[i] = np.clip(
                self._ki[i] + self._learning_rate * self._integral_errors[i], 0, 1
            )
            self._kd[i] = np.clip(
                self._kd[i] + self._learning_rate * (error - self._previous_errors[i]),
                0,
                1,
            )
