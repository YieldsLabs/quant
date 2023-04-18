from abc import ABC, abstractmethod


class AbstractScreening(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
