import time
import logging


class ThroughputMonitor:
    def __init__(self, events_to_log: int = 100):
        self.events_to_log = events_to_log
        self.start_time = time.monotonic()
        self.num_events = 0

    def event_processed(self):
        self.num_events += 1
        if self.num_events % self.events_to_log == 0:
            self._log_throughput()

    def _log_throughput(self):
        elapsed_time = time.monotonic() - self.start_time
        throughput = self.num_events / elapsed_time

        print(f"Throughput = {throughput:.2f} events/sec")

        self.num_events = 0
        self.start_time = time.monotonic()
