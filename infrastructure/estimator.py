import asyncio


class Estimator:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.start_time = asyncio.get_event_loop().time()
        self.steps_processed = 0
    
    def remaining_time(self):
        self.steps_processed += 1
        elapsed_time = asyncio.get_event_loop().time() - self.start_time
        average_time_per_step = elapsed_time / self.steps_processed
        remaining_steps = self.total_steps - self.steps_processed
        return average_time_per_step * remaining_steps

