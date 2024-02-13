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
        result = average_time_per_step * remaining_steps
        remaining_time_seconds = max(0, int(result))

        days = remaining_time_seconds // (24 * 3600)
        remaining_time_seconds %= 24 * 3600
        hours = remaining_time_seconds // 3600
        remaining_time_seconds %= 3600
        minutes = remaining_time_seconds // 60
        remaining_time_seconds %= 60
        seconds = remaining_time_seconds

        return f"{int(days)}:{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
