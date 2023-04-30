from abc import abstractmethod


class AbstractSystem:
    @abstractmethod
    def start(self):
        pass