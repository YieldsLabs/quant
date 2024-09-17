import numpy as np


class PID:
    def __init__(
        self,
        num_groups: int,
        kp: float = 0.3,
        ki: float = 0.6,
        kd: float = 0.1,
        learning_rate: float = 0.001,
        decay_rate: float = 0.99,
    ):
        self.kp = np.ones(num_groups) * kp
        self.ki = np.ones(num_groups) * ki
        self.kd = np.ones(num_groups) * kd

        self.integral_errors = np.zeros(num_groups)
        self.previous_errors = np.zeros(num_groups)

        self.learning_rate = learning_rate
        self.decay_rate = decay_rate

    def update(self, errors: np.ndarray):
        control_outputs = np.zeros_like(errors)

        for i, error in enumerate(errors):
            self.integral_errors[i] += error
            derivative = error - self.previous_errors[i]

            self.kp[i] = np.clip(self.kp[i] + self.learning_rate * error, 0, 1)
            self.ki[i] = np.clip(
                self.ki[i] + self.learning_rate * self.integral_errors[i], 0, 1
            )
            self.kd[i] = np.clip(self.kd[i] + self.learning_rate * derivative, 0, 1)

            control_outputs[i] = (
                self.kp[i] * error
                + self.ki[i] * self.integral_errors[i]
                + self.kd[i] * derivative
            )

            self.previous_errors[i] = error

        self.learning_rate *= self.decay_rate

        return control_outputs
